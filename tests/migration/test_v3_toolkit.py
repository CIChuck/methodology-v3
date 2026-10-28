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
        self.assertEqual(yaml.safe_load((self.target / "docs/planning/board.yaml").read_text())["tasks"], [])
        self.command(sys.executable, "scripts/devboard.py", "validate")
        self.assertEqual(self.command(sys.executable, "scripts/devboard.py", "next").stdout.strip(), "NO_OPEN_TASK")
        skills = list((self.target / ".agents/skills").glob("*/SKILL.md"))
        self.assertEqual(len(skills), 15)
        for skill in skills:
            self.assertTrue(skill.is_file(), skill)
            metadata = yaml.safe_load(skill.read_text().split("---", 2)[1])
            self.assertEqual(metadata["name"], skill.parent.name)
            self.assertTrue(metadata["description"])
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

    def test_documented_fresh_dry_run_works_from_initialized_product(self) -> None:
        self.install()
        self.command("./scripts/init-project.sh", "Existing Fixture")
        authority = inventory(self.target / "docs/project")
        guide = (REPOSITORY / "docs/methodology/guides/orchestration-validation.md").read_text()
        commands = guide.split("```bash\n", 1)[1].split("```", 1)[0]
        result = self.command("bash", "-e", "-c", commands, env={"TMPDIR": str(self.base)})
        self.assertIn("Initialized docs/project for Example Product", result.stdout)
        self.assertEqual(inventory(self.target / "docs/project"), authority)


if __name__ == "__main__":
    unittest.main()
