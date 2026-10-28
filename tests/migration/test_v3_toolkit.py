from __future__ import annotations

import hashlib
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

REPOSITORY = Path(__file__).resolve().parents[2]
RECORD = "docs/methodology/schema/installation.json"
MANAGED = "docs/methodology/templates/architecture-template.md"
IMPORTED_SKILLS = {"babysit-pr", "council", "file-pr", "full-send", "full-stop",
                   "leaving-pr-comments", "modernize", "sol-loop", "takeover"}


def inventory(root: Path) -> dict[str, tuple[str, object, int]]:
    result: dict[str, tuple[str, object, int]] = {}
    for p in sorted(root.rglob("*")):
        name = p.relative_to(root).as_posix()
        if p.is_symlink():
            result[name] = ("link", os.readlink(p), 0)
        elif p.is_dir():
            result[name] = ("directory", None, stat.S_IMODE(p.stat().st_mode))
        else:
            result[name] = ("file", p.read_bytes(), stat.S_IMODE(p.stat().st_mode))
    return result


class ToolkitMigrationTests(unittest.TestCase):
    def setUp(self) -> None:
        tmp = tempfile.TemporaryDirectory(prefix="gendev-v3-test-")
        self.addCleanup(tmp.cleanup)
        self.base = Path(tmp.name)
        self.target = self.base / "product with spaces"
        self.target.mkdir()

    def install(self, *args: str, source: Path = REPOSITORY, env: dict[str, str] | None = None, expected: int = 0) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            [str(source / "scripts/install-methodology.sh"), *args, str(self.target)],
            capture_output=True, text=True, check=False,
            env={**os.environ, **(env or {})},
        )
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result

    def command(self, *args: str, expected: int = 0, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(args, cwd=self.target, capture_output=True, text=True, check=False, env={**os.environ, **(env or {})})
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result

    def record(self) -> dict:
        return json.loads((self.target / RECORD).read_text())

    def source_copy(self) -> Path:
        copied = self.base / "incoming"
        shutil.copytree(REPOSITORY, copied, symlinks=True, ignore=shutil.ignore_patterns(".git", ".venv", ".tmp", "__pycache__"))
        return copied

    def test_fresh_install_is_portable_and_has_no_migration_task_or_product_metadata(self) -> None:
        (self.target / "pyproject.toml").write_text("# Existing product environment\n")
        self.install()
        self.assertEqual((self.target / "pyproject.toml").read_text(), "# Existing product environment\n")
        self.assertFalse((self.target / "uv.lock").exists())
        self.assertFalse((self.target / "docs/project").exists())
        self.assertFalse((self.target / "docs/planning/active/v3-baseline-migration").exists())
        template = (self.target / "docs/planning/task-template.md").read_text()
        self.assertNotIn("t3-code-sample", template)
        self.assertIn("Project: [project-slug]", template)
        self.assertIn("Project: different-project", template.replace("[project-slug]", "different-project"))
        self.assertEqual(yaml.safe_load((self.target / "docs/planning/board.yaml").read_text())["tasks"], [])
        self.command(sys.executable, "scripts/devboard.py", "validate")
        self.assertEqual(self.command(sys.executable, "scripts/devboard.py", "next").stdout.strip(), "NO_OPEN_TASK")
        skills = list((self.target / ".agents/skills").glob("*/SKILL.md"))
        self.assertEqual(len(skills), 24)
        self.assertTrue(IMPORTED_SKILLS <= {skill.parent.name for skill in skills})
        for skill in skills:
            self.assertTrue(skill.is_file(), skill)
            metadata = yaml.safe_load(skill.read_text().split("---", 2)[1])
            self.assertEqual(metadata["name"], skill.parent.name)
            self.assertTrue(metadata["description"])
        helper = ".agents/skills/babysit-pr/scripts/pr-wait"
        self.assertIn("Watch a GitHub PR", self.command(sys.executable, helper, "--help").stdout)
        for name in ("full-send", "full-stop", "leaving-pr-comments", "modernize"):
            self.assertTrue((self.target / ".agents/skills" / name / "agents/openai.yaml").is_file())
        record = self.record()
        self.assertEqual(record["distribution_candidate"]["status"], "unreleased")
        self.assertNotIn("docs/planning/board.yaml", record["files"])
        self.assertNotIn("docs/policies/repository-engineering-policy.md", record["files"])
        self.assertIn("Distribution candidate: methodology-v3 (unreleased)", self.command("./scripts/gendev-doctor.sh").stdout)

    def test_clean_upgrade_preserves_board_authority_policies_custom_skills_and_history(self) -> None:
        self.install()
        self.command("./scripts/init-project.sh", "Fixture Product")
        custom = self.target / "docs/methodology/dev-skills/custom/SKILL.md"
        custom.parent.mkdir()
        custom.write_text("---\nname: custom\ndescription: Fixture local skill\n---\n")
        entry = self.target / ".agents/skills/custom/SKILL.md"
        entry.parent.mkdir()
        entry.symlink_to("../../../docs/methodology/dev-skills/custom/SKILL.md")
        policy = self.target / "docs/policies/repository-engineering-policy.md"
        policy.write_text(policy.read_text() + "\nLocal policy addition.\n")
        board = self.target / "docs/planning/board.yaml"
        # Exercise persistence of local board data without inventing a task approval.
        board.write_text(board.read_text().replace('"2026-10-27"', '"2026-10-26"'))
        before = {name: inventory(self.target / name) for name in ["docs/project", "docs/policies", ".agents", "docs/planning"]}
        old = self.record()
        self.install("--force")
        self.assertEqual(before, {name: inventory(self.target / name) for name in before})
        self.assertTrue(entry.is_file())
        new = self.record()
        self.assertEqual(new["installation_history"][-1]["source_commit"], old["source_commit"])
        self.assertNotIn(custom.relative_to(self.target).as_posix(), new["files"])
        self.command("./scripts/gendev-doctor.sh")

    def test_edited_baseline_refuses_upgrade_without_writing(self) -> None:
        self.install()
        p = self.target / MANAGED
        p.write_text(p.read_text() + "\nLocal amendment not reconciled.\n")
        before = inventory(self.target)
        result = self.install("--force", expected=1)
        self.assertIn(MANAGED, result.stderr)
        self.assertEqual(inventory(self.target), before)

    def test_clean_owned_file_can_receive_an_actual_upstream_update(self) -> None:
        self.install()
        source = self.source_copy()
        changed = source / MANAGED
        changed.write_text(changed.read_text() + "\nIncoming fixture revision.\n")
        self.install("--force", source=source)
        self.assertEqual((self.target / MANAGED).read_bytes(), changed.read_bytes())
        self.command("./scripts/gendev-doctor.sh")

    def test_approved_local_amendment_conflict_is_not_hidden_by_effective_hash(self) -> None:
        self.install()
        p = self.target / MANAGED
        p.write_text(p.read_text() + "\nApproved local fixture amendment.\n")
        record = self.record()
        record["files"][MANAGED] = hashlib.sha256(p.read_bytes()).hexdigest()
        record["local_amendments"] = [{"id": "fixture", "files": {MANAGED: {"effective_sha256": record["files"][MANAGED]}}}]
        (self.target / RECORD).write_text(json.dumps(record))
        before = inventory(self.target)
        self.assertIn("local amendment needs reconciliation", self.install("--force", expected=1).stderr)
        self.assertEqual(inventory(self.target), before)

    def test_absorbed_local_amendment_record_survives(self) -> None:
        self.install()
        record = self.record()
        amendments = [{"id": "fixture-absorbed", "files": {MANAGED: {"effective_sha256": record["files"][MANAGED]}}}]
        record["local_amendments"] = amendments
        (self.target / RECORD).write_text(json.dumps(record))
        self.install("--force")
        self.assertEqual(self.record()["local_amendments"], amendments)
        self.assertEqual(self.record()["installation_history"][-1]["local_amendments"], amendments)

    def test_new_baseline_file_cannot_clobber_an_unowned_local_addition(self) -> None:
        self.install()
        name = "docs/methodology/dev-skills/custom-collision.md"
        (self.target / name).write_text("Local content\n")
        source = self.source_copy()
        (source / name).write_text("Incoming content\n")
        before = inventory(self.target)
        self.assertIn(name, self.install("--force", source=source, expected=1).stderr)
        self.assertEqual(inventory(self.target), before)

    def test_symlink_parent_is_rejected_without_touching_external_files(self) -> None:
        outside = self.base / "outside"
        outside.mkdir()
        (outside / "sentinel").write_text("untouched")
        (self.target / "docs").symlink_to(outside, target_is_directory=True)
        before = inventory(outside)
        self.install("--force", expected=1)
        self.assertEqual(inventory(outside), before)
        self.assertTrue((self.target / "docs").is_symlink())

    def test_symlink_in_place_of_owned_file_is_rejected(self) -> None:
        self.install()
        owned = self.target / MANAGED
        outside = self.base / "outside.md"
        outside.write_bytes(owned.read_bytes())
        owned.unlink()
        owned.symlink_to(outside)
        before = inventory(self.target)
        self.install("--force", expected=1)
        self.assertEqual(inventory(self.target), before)

    def test_removed_owned_file_requires_reconciliation(self) -> None:
        self.install()
        (self.target / MANAGED).unlink()
        before = inventory(self.target)
        self.install("--force", expected=1)
        self.assertEqual(inventory(self.target), before)

    def test_malformed_ownership_record_refuses_without_writes(self) -> None:
        self.install()
        (self.target / RECORD).write_text('{"files": []}')
        before = inventory(self.target)
        self.install("--force", expected=1)
        self.assertEqual(inventory(self.target), before)

    def test_duplicate_ownership_fields_refuse_without_writes(self) -> None:
        self.install()
        (self.target / RECORD).write_text('{"files": {}, "files": {}}')
        before = inventory(self.target)
        self.assertIn("duplicate JSON field", self.install("--force", expected=1).stderr)
        self.assertEqual(inventory(self.target), before)

    def test_permission_only_restriction_and_executable_changes_refuse_without_writes(self) -> None:
        self.install()
        p = self.target / "scripts/check-methodology.sh"
        original_mode = stat.S_IMODE(p.stat().st_mode)
        for mode in [0o700, 0o644]:
            p.chmod(mode)
            before = inventory(self.target)
            self.assertIn("permissions", self.install("--force", expected=1).stderr)
            self.assertEqual(inventory(self.target), before)
            p.chmod(original_mode)

    def test_doctor_detects_permission_only_change(self) -> None:
        self.install()
        (self.target / "scripts/check-methodology.sh").chmod(0o700)
        result = self.command("./scripts/gendev-doctor.sh", expected=5)
        self.assertIn("modified permissions", result.stdout)

    def test_legacy_permission_record_refuses_ambiguous_replacement(self) -> None:
        self.install()
        record = self.record()
        record.pop("file_modes")
        (self.target / RECORD).write_text(json.dumps(record))
        (self.target / "scripts/check-methodology.sh").chmod(0o700)
        before = inventory(self.target)
        self.assertIn("legacy permissions", self.install("--force", expected=1).stderr)
        self.assertEqual(inventory(self.target), before)

    def test_legacy_matching_modes_are_adopted_without_fabricating_history(self) -> None:
        self.install()
        record = self.record()
        record.pop("file_modes")
        (self.target / RECORD).write_text(json.dumps(record))
        self.install("--force")
        upgraded = self.record()
        self.assertEqual(upgraded["file_modes"]["scripts/check-methodology.sh"], 0o755)
        self.assertIn("scripts/check-methodology.sh", upgraded["legacy_mode_adoptions"])
        self.assertNotIn("file_modes", upgraded["installation_history"][-1])
        self.command("./scripts/gendev-doctor.sh")

    def test_clean_recorded_mode_can_receive_an_upstream_update(self) -> None:
        self.install()
        source = self.source_copy()
        (source / "docs/methodology/constitution/gendev.md").chmod(0o600)
        self.install("--force", source=source)
        name = "docs/methodology/constitution/gendev.md"
        self.assertEqual(stat.S_IMODE((self.target / name).stat().st_mode), 0o600)
        self.assertEqual(self.record()["file_modes"][name], 0o600)
        self.command("./scripts/gendev-doctor.sh")

    def test_invalid_permission_metadata_refuses_before_writes(self) -> None:
        self.install()
        record = self.record()
        record["file_modes"]["scripts/check-methodology.sh"] = "0755"
        (self.target / RECORD).write_text(json.dumps(record))
        before = inventory(self.target)
        self.install("--force", expected=1)
        self.assertEqual(inventory(self.target), before)
        self.assertIn("invalid recorded permissions", self.command("./scripts/gendev-doctor.sh", expected=5).stdout)

    def test_rollback_restores_fresh_target_after_first_and_last_writes(self) -> None:
        (self.target / "AGENTS.md").write_text("# Existing project instructions\n")
        (self.target / ".gitignore").write_text("local-runtime/\n")
        before = inventory(self.target)
        for env in [{"GENDEV_INSTALL_FAIL_AFTER": "1"}, {"GENDEV_INSTALL_FAIL_AT": RECORD}]:
            self.install("--integrate-agents", env=env, expected=1)
            self.assertEqual(inventory(self.target), before)

    def test_rollback_restores_prior_record_and_local_state_during_upgrade(self) -> None:
        (self.target / "AGENTS.md").write_text("# Existing project instructions\n")
        self.install("--integrate-agents")
        before = inventory(self.target)
        self.install("--force", "--integrate-agents", env={"GENDEV_INSTALL_FAIL_AT": RECORD}, expected=1)
        self.assertEqual(inventory(self.target), before)

    def test_dry_run_and_preflight_agent_collision_make_no_writes(self) -> None:
        (self.target / "AGENTS.md").write_text("# Existing project instructions\n")
        before = inventory(self.target)
        self.install("--dry-run", "--integrate-agents")
        self.assertEqual(inventory(self.target), before)
        (self.target / "AGENTS.gendev.md").write_text("# Existing independent instructions\n")
        before = inventory(self.target)
        self.install("--integrate-agents", expected=1)
        self.assertEqual(inventory(self.target), before)

    def test_initial_and_later_directives_render_canonical_anti_drift_contract(self) -> None:
        self.install()
        self.command("./scripts/init-project.sh", "Fixture / A&B")
        self.command("./scripts/init-phase.sh", "2", "Fixture / A&B")
        template = (REPOSITORY / "docs/methodology/templates/phase-construction-directive-template.md").read_text()
        anti_drift = template.split("## 14. Anti-Drift", 1)[1].split("\n## 15.", 1)[0]
        for phase in ["1", "2"]:
            directive = (self.target / f"docs/project/build-plan/phases/phase-{phase}-construction-directive.md").read_text()
            self.assertIn(anti_drift, directive)
            self.assertIn(f"Position: G5.{phase}.3", directive)
            self.assertIn(f"phase-{phase}-tactical-implementation-plan.md", directive)
            self.assertIn("Fixture / A&B", directive)
            self.assertNotIn("[id]", directive)
            self.assertNotIn("[phase-build-plan]", directive)
            self.assertIn("private helpers", directive)

    def test_manifest_names_round_trip_quotes_backslashes_unicode_and_tokens(self) -> None:
        self.install()
        names = [
            'Widget "QA"',
            r"Widget \\ QA",
            r"Widget \n QA",
            'Widget "QA" O\'Brien \\ [id] / A&B',
            "Projet Café 💡 [Project Name] [phase-build-plan]",
        ]
        for number, name in enumerate(names):
            with self.subTest(name=name):
                args = ("./scripts/init-project.sh", name) if number == 0 else ("./scripts/init-project.sh", "--force", name)
                self.command(*args)
                manifest = yaml.safe_load((self.target / "docs/project/project.yaml").read_text())
                self.assertEqual(manifest["project"]["name"], name)
                directive = self.target / "docs/project/build-plan/phases/phase-1-construction-directive.md"
                self.assertIn(name, directive.read_text())
        self.command("./scripts/init-phase.sh", "2", names[-1])
        self.assertIn(names[-1], (self.target / "docs/project/build-plan/phases/phase-2-construction-directive.md").read_text())

    def test_invalid_names_fail_before_creation_or_forced_replacement(self) -> None:
        self.install()
        invalid = ["", "Widget\nQA", "Widget\tQA", "Widget\x7fQA", "Widget\x80QA", "Widget\u0085QA", "Widget\u2028QA", "Widget\u2029QA", "   "]
        for name in invalid:
            with self.subTest(name=name):
                self.assertIn("single-line", self.command("./scripts/init-project.sh", name, expected=2).stderr)
                self.assertFalse((self.target / "docs/project").exists())
        self.command("./scripts/init-project.sh", "Existing valid fixture")
        before = inventory(self.target / "docs/project")
        self.command("./scripts/init-project.sh", "--force", invalid[0], expected=2)
        self.assertEqual(inventory(self.target / "docs/project"), before)
        for name in invalid:
            with self.subTest(phase_name=name):
                self.command("./scripts/init-phase.sh", "2", name, expected=2)
                self.assertEqual(inventory(self.target / "docs/project"), before)

    def exercise_documented_dry_run(self, source: Path, *, omit: str | None = None,
                                    external_links: bool = False) -> None:
        # Extra files and project adaptations must never leak into fresh setup.
        marker = "LIVE-SECRET-AND-TASK-HISTORY"
        (source / ".env").write_text(marker)
        (source / "docs/methodology/unowned-secret.env").write_text(marker)
        (source / "docs/policies/local-secret.env").write_text(marker)
        (source / "docs/policies/legacy-policy-debt.md").write_text(marker)
        (source / "AGENTS.md").write_text(marker)
        (source / "docs/planning/board.yaml").write_text(marker)
        if omit is not None:
            path = source / omit
            shutil.rmtree(path) if path.is_dir() else path.unlink()
        if external_links:
            private = self.base / "external-private-skill.md"
            private.write_text(marker)
            links = [".agents/skills/private/SKILL.md", "docs/methodology/private-secret.md",
                     "docs/project-template/planning/private-secret.md",
                     "docs/project-template/dry-run-policies/private-secret.md"]
            for name in links:
                path = source / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.symlink_to(private)
            # A directory link must also be excluded without walking its files.
            (source / "docs/methodology/private-directory").symlink_to(self.base, target_is_directory=True)
        before = inventory(source)
        guide = (REPOSITORY / "docs/methodology/guides/orchestration-validation.md").read_text()
        commands = guide.split("```bash\n", 1)[1].split("```", 1)[0]
        result = subprocess.run(["bash", "-e", "-c", commands + '\nprintf "FIXTURE=%s\\n" "$PWD"\n'],
                                cwd=source, capture_output=True, text=True,
                                env={**os.environ, "TMPDIR": str(self.base)})
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Initialized docs/project for Example Product", result.stdout)
        self.assertEqual(inventory(source), before)
        fixture = Path(next(line.removeprefix("FIXTURE=") for line in result.stdout.splitlines() if line.startswith("FIXTURE=")))
        self.assertNotEqual(fixture, source)
        def run(*args: str, expected: int = 0) -> subprocess.CompletedProcess[str]:
            result = subprocess.run(args, cwd=fixture, capture_output=True, text=True)
            self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
            return result
        self.assertIn("Integrity: verified", run("./scripts/gendev-doctor.sh").stdout)
        run(sys.executable, "scripts/devboard.py", "validate")
        self.assertEqual(run(sys.executable, "scripts/devboard.py", "next").stdout.strip(), "NO_OPEN_TASK")
        checker = run("./scripts/check-methodology.sh", expected=1)
        errors = [line for line in checker.stdout.splitlines() if line.startswith("ERROR:")]
        self.assertEqual(len(errors), 1, checker.stdout + checker.stderr)
        self.assertIn("GENDEV-MANIFEST-ENFORCEMENT-002", errors[0])
        self.assertIn("required_attester", errors[0])
        record = json.loads((fixture / RECORD).read_text())
        self.assertTrue(record["fixture"])
        self.assertEqual(record["installation_history"], [])
        self.assertEqual(record["local_amendments"], [])
        self.assertFalse((fixture / ".git").exists())
        self.assertFalse((fixture / ".env").exists())
        self.assertFalse((fixture / "docs/methodology/unowned-secret.env").exists())
        self.assertFalse((fixture / "docs/policies/local-secret.env").exists())
        self.assertFalse((fixture / "docs/planning/active/v3-baseline-migration").exists())
        self.assertEqual(yaml.safe_load((fixture / "docs/planning/board.yaml").read_text())["tasks"], [])
        for policy in (REPOSITORY / "docs/project-template/dry-run-policies").glob("*.md"):
            self.assertEqual((fixture / "docs/policies" / policy.name).read_bytes(), policy.read_bytes())
        skills = list((fixture / ".agents/skills").glob("*/SKILL.md"))
        self.assertEqual(len(skills), 24)
        self.assertTrue(IMPORTED_SKILLS <= {skill.parent.name for skill in skills})
        self.assertTrue(all(skill.is_file() and (skill.is_symlink() or skill.parent.is_symlink()) for skill in skills))
        self.assertIn("Watch a GitHub PR", run(sys.executable, ".agents/skills/babysit-pr/scripts/pr-wait", "--help").stdout)
        self.assertTrue((fixture / ".agents/skills/full-send/agents/openai.yaml").is_file())
        for path in fixture.rglob("*"):
            if path.is_file():
                self.assertNotIn(marker.encode(), path.read_bytes(), str(path))
        manifest = yaml.safe_load((fixture / "docs/project/project.yaml").read_text())
        self.assertEqual(manifest["approvals"]["current_gate"]["gate"], "G1")
        self.assertEqual(manifest["approvals"]["current_gate"]["status"], "pending")
        # Explicit synthetic fixture identity only; naming supplies no approval.
        manifest_path = fixture / "docs/project/project.yaml"
        manifest_path.write_text(manifest_path.read_text().replace("required_attester: TBD", "required_attester: Synthetic Fixture Attester"))
        run("./scripts/check-methodology.sh")

    def test_documented_fresh_dry_run_works_from_initialized_product(self) -> None:
        self.install()
        self.command("./scripts/init-project.sh", "Existing Fixture")
        self.exercise_documented_dry_run(self.target)

    def test_dry_run_excludes_external_project_and_unowned_baseline_tree_links(self) -> None:
        self.install()
        self.command("./scripts/init-project.sh", "Existing Fixture")
        self.exercise_documented_dry_run(self.target, external_links=True)

    def test_dry_run_does_not_require_live_project_owned_surfaces(self) -> None:
        for number, surface in enumerate(("AGENTS.md", ".agents/skills", "docs/policies")):
            with self.subTest(surface=surface):
                self.target = self.base / f"initialized-product-{number}"
                self.target.mkdir()
                self.install()
                self.command("./scripts/init-project.sh", "Existing Fixture")
                self.exercise_documented_dry_run(self.target, omit=surface)

    def test_documented_fresh_dry_run_works_from_methodology_checkout(self) -> None:
        source = self.source_copy()
        for args in (("git", "init"), ("git", "add", "."),
                     ("git", "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                      "commit", "-qm", "Synthetic source fixture")):
            subprocess.run(args, cwd=source, check=True, capture_output=True)
        self.exercise_documented_dry_run(source)

    def test_dry_run_seed_snapshots_match_reusable_source_policies(self) -> None:
        seeds = REPOSITORY / "docs/project-template/dry-run-policies"
        policies = REPOSITORY / "docs/policies"
        self.assertEqual({p.name for p in seeds.glob("*.md")}, {p.name for p in policies.glob("*.md")})
        for path in seeds.glob("*.md"):
            self.assertEqual(path.read_bytes(), (policies / path.name).read_bytes())

    def test_dry_run_refuses_incomplete_installed_baseline_before_output(self) -> None:
        self.install()
        (self.target / "requirements-devboard.txt").unlink()
        before = inventory(self.target)
        result = self.command(sys.executable, "scripts/create-dry-run.py", expected=1)
        self.assertIn("source doctor failed", result.stderr)
        self.assertEqual(result.stdout, "")
        self.assertEqual(inventory(self.target), before)

    def test_dry_run_refuses_changed_or_symlinked_owned_baseline(self) -> None:
        self.install()
        path = self.target / MANAGED
        original = path.read_bytes()
        for kind in ("changed", "symlink"):
            with self.subTest(kind=kind):
                path.unlink()
                if kind == "changed":
                    path.write_bytes(original + b"\nLocal change.\n")
                else:
                    external = self.base / "external-owned-template.md"
                    external.write_bytes(original)
                    path.symlink_to(external)
                before = inventory(self.target)
                result = self.command(sys.executable, "scripts/create-dry-run.py", expected=1)
                self.assertIn("source doctor failed", result.stderr)
                self.assertEqual(result.stdout, "")
                self.assertEqual(inventory(self.target), before)

    def test_normal_installer_still_rejects_external_source_discovery_links(self) -> None:
        source = self.source_copy()
        external = self.base / "external-private.md"
        external.write_text("Synthetic private skill\n")
        link = source / ".agents/skills/private/SKILL.md"
        link.parent.mkdir()
        link.symlink_to(external)
        before = inventory(self.target)
        result = self.install(source=source, expected=1)
        self.assertIn("external source symlink", result.stderr)
        self.assertEqual(inventory(self.target), before)

    def test_dry_run_refuses_symlinked_parent_of_selected_owned_files(self) -> None:
        self.install()
        templates = self.target / "docs/methodology/templates"
        external = self.base / "external-template-directory"
        shutil.move(templates, external)
        templates.symlink_to(external, target_is_directory=True)
        # Identical regular child files still hash correctly; source selection
        # must independently reject their unsafe parent before copying them.
        self.command("./scripts/gendev-doctor.sh")
        before = inventory(self.target)
        result = self.command(sys.executable, "scripts/create-dry-run.py", expected=1)
        self.assertIn("unsafe target parent: docs/methodology/templates", result.stderr)
        self.assertEqual(result.stdout, "")
        self.assertEqual(inventory(self.target), before)

    def test_dry_run_refuses_internal_tmpdir_without_source_mutation(self) -> None:
        self.install()
        before = inventory(self.target)
        result = self.command(sys.executable, "scripts/create-dry-run.py", expected=1,
                              env={"TMPDIR": str(self.target)})
        self.assertIn("TMPDIR must be outside", result.stderr)
        self.assertEqual(result.stdout, "")
        self.assertEqual(inventory(self.target), before)


if __name__ == "__main__":
    unittest.main()
