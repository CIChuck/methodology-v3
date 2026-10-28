#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Replay isolated v2/T3 upgrades and a synthetic task-level build exercise.

All inputs come from this repository's history and frozen archive. No original
repository, credentials, remote Git host, actual human approval, or formal
independent review is used. Every destination is in a temporary directory.
"""
from __future__ import annotations

import hashlib
import io
import json
import os
import platform
import subprocess
import sys
import tarfile
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "docs/resources/evolution/v3-migration"
RECORD = "docs/methodology/schema/installation.json"
BASE = "54f0de27f2b59fdcc54e4f57bb9f73dc92843f4a"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def state(root: Path) -> dict[str, str]:
    result = {}
    for p in sorted(root.rglob("*")):
        if ".git" in p.relative_to(root).parts:
            continue
        name = p.relative_to(root).as_posix()
        if p.is_symlink():
            result[name] = "link:" + os.readlink(p)
        elif p.is_file():
            result[name] = hashlib.sha256(p.read_bytes()).hexdigest()
    return result


def main() -> int:
    report = {
        "kind": "local deterministic migration experiments",
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "source_revision": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "platform": platform.platform(), "python": platform.python_version(),
        "commands": [], "scenarios": {},
        "limitations": ["No hosted CI or Linux run", "No fresh-context independent review or human acceptance", "Development exercise is task-level synthetic baseline/tooling authority, not a real product gate traversal"],
    }

    def run(cwd: Path, *args: str, expected: int = 0) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(args, cwd=cwd, capture_output=True, text=True, check=False)
        report["commands"].append({"cwd": str(cwd), "argv": list(args), "expected": expected, "actual": result.returncode, "output_tail": (result.stdout + result.stderr)[-2000:]})
        if result.returncode != expected:
            raise RuntimeError(f"command returned {result.returncode}, expected {expected}: {args}\n{result.stdout}\n{result.stderr}")
        return result

    def install(target: Path, source: Path = ROOT, *options: str, expected: int = 0) -> subprocess.CompletedProcess[str]:
        return run(source, str(source / "scripts/install-methodology.sh"), *options, str(target), expected=expected)

    def board(target: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return run(target, sys.executable, "scripts/devboard.py", *args)

    with tempfile.TemporaryDirectory(prefix="gendev-v3-experiments-") as directory:
        tmp = Path(directory)
        fresh = tmp / "fresh"
        fresh.mkdir()
        install(fresh)
        run(fresh, "./scripts/init-project.sh", "Synthetic C1 Toolkit Fixture")
        new_owned = json.loads((fresh / RECORD).read_text())["files"]
        report["scenarios"]["fresh"] = {"result": "PASS", "owned_files": len(new_owned), "skills": len(list((fresh / ".agents/skills").glob("*/SKILL.md")))}

        v2 = tmp / "v2-source"
        v2.mkdir()
        raw = subprocess.check_output(["git", "archive", BASE], cwd=ROOT)
        with tarfile.open(fileobj=io.BytesIO(raw)) as archive:
            archive.extractall(v2, filter="data")
        old = tmp / "v2-product"
        old.mkdir()
        install(old, v2)
        run(old, "./scripts/init-project.sh", "Synthetic V2 Upgrade Fixture")
        authority = state(old / "docs/project")
        install(old, ROOT, "--force")
        require(state(old / "docs/project") == authority, 'Fixture invariant failed: state(old / "docs/project") == authority')
        run(old, "./scripts/gendev-doctor.sh")
        board(old, "validate")
        report["scenarios"]["v2_to_v3"] = {"result": "PASS", "authority_unchanged": True, "prior_installations_retained": len(json.loads((old / RECORD).read_text())["installation_history"])}

        t3 = tmp / "t3-copy"
        t3.mkdir()
        input_archive = EVIDENCE / "inputs/T3_Code_Sample.tar.gz"
        manifest = json.loads((EVIDENCE / "input-manifest.json").read_text())
        require(hashlib.sha256(input_archive.read_bytes()).hexdigest() == manifest["sources"]["T3_Code_Sample"]["archive_sha256"], 'Fixture invariant failed: hashlib.sha256(input_archive.read_bytes()).hexdigest() == manifest["sources"]["T3_Code_Sample"]["archive_sha256"]')
        with tarfile.open(input_archive) as archive:
            archive.extractall(t3, filter="data")
        before = state(t3)
        conflict = install(t3, ROOT, "--force", expected=1)
        require(state(t3) == before, 'Fixture invariant failed: state(t3) == before')
        project = state(t3 / "docs/project")
        policies = state(t3 / "docs/policies")
        original_record = json.loads((t3 / RECORD).read_text())
        record = json.loads((t3 / RECORD).read_text())
        adopted = []
        # Explicit fixture reconciliation: these previously local toolkit files
        # are now maintained by v3. Pin their actual old bytes before upgrading.
        for name in sorted(new_owned):
            p = t3 / name
            if name not in record["files"] and p.is_file() and not p.is_symlink():
                record["files"][name] = hashlib.sha256(p.read_bytes()).hexdigest()
                adopted.append(name)
        record["fixture_reconciliation"] = {"scope": "synthetic copied-input experiment only", "decision": "adopt shared toolkit paths into incoming baseline ownership", "paths": adopted}
        (t3 / RECORD).write_text(json.dumps(record, indent=2) + "\n")
        install(t3, ROOT, "--force")
        upgraded = json.loads((t3 / RECORD).read_text())
        require(upgraded["local_amendments"] == original_record["local_amendments"], 'Fixture invariant failed: upgraded["local_amendments"] == original_record["local_amendments"]')
        require(state(t3 / "docs/project") == project, 'Fixture invariant failed: state(t3 / "docs/project") == project')
        require(state(t3 / "docs/policies") == policies, 'Fixture invariant failed: state(t3 / "docs/policies") == policies')
        run(t3, "./scripts/gendev-doctor.sh")
        run(t3, "./scripts/check-methodology.sh")
        board_before = (t3 / "docs/planning/board.yaml").read_bytes()
        board(t3, "render")
        require((t3 / "docs/planning/board.yaml").read_bytes() == board_before, "Dashboard refresh changed task state")
        board(t3, "validate")
        report["scenarios"]["t3_copy_to_v3"] = {"result": "PASS", "initial_conflict_zero_writes": True, "initial_conflict": conflict.stderr.strip(), "explicit_fixture_ownership_adoptions": adopted, "local_amendments_retained": len(upgraded["local_amendments"]), "project_authority_unchanged": True, "project_policies_unchanged": True}

        # This is a synthetic baseline-tooling task; the product scaffold's G1
        # remains pending. No product generation or acceptance is implied.
        authority_before = state(fresh / "docs/project")
        packet = fresh / "docs/planning/queued/fixture-tool"
        packet.mkdir()
        (packet / "README.md").write_text("# Synthetic baseline-tooling construction directive\n\nScope: tools/tag_fixture.py and its test only.\nRequirements: accept a list of strings; strip surrounding whitespace; remove empty entries; deduplicate and sort case-sensitively.\nNon-goals: product behavior, network, persistence, dependencies and gate changes.\nVerification: tests/test_tag_fixture.py with positive, empty and mixed-case cases.\nAuthority: synthetic task direction for this isolated regression exercise.\nHuman labels below are fixture data, not actual approvals.\n")
        data = yaml.safe_load((fresh / "docs/planning/board.yaml").read_text())
        data["tasks"] = [{"id": "fixture-tool", "title": "Synthetic baseline helper exercise", "priority": 1, "work_state": "queued", "condition": "normal", "implementation_authority": "not_granted", "packet": "docs/planning/queued/fixture-tool/", "next_gate": "Synthetic scope approval", "delivery_state": "not_started", "branch": None, "depends_on": [], "validation": []}]
        (fresh / "docs/planning/board.yaml").write_text(yaml.safe_dump(data, sort_keys=False))
        board(fresh, "render")
        board(fresh, "transition", "fixture-tool", "approved", "--actor", "Synthetic Fixture Maintainer", "--actor-role", "maintainer", "--note", "Synthetic fixture task direction; not a real human approval", "--next-gate", "Start isolated helper task")
        packet.rename(fresh / "docs/planning/active/fixture-tool")
        board(fresh, "transition", "fixture-tool", "started", "--packet", "docs/planning/active/fixture-tool/", "--branch", "fixture/tool", "--actor", "Fixture Builder", "--actor-role", "agent", "--note", "Synthetic isolated task start", "--next-gate", "Run bounded helper verification; independent review pending")
        (fresh / "tools").mkdir()
        (fresh / "tools/tag_fixture.py").write_text('def normalized_tags(values: list[str]) -> list[str]:\n    """Return unique nonempty stripped strings in case-sensitive order."""\n    return sorted({value.strip() for value in values if value.strip()})\n')
        (fresh / "tests/test_tag_fixture.py").write_text('import unittest\nfrom tools.tag_fixture import normalized_tags\n\nclass TagFixtureTests(unittest.TestCase):\n    def test_deduplicates_and_strips(self):\n        self.assertEqual(normalized_tags([" z ", "a", "z", "", "  "]), ["a", "z"])\n    def test_empty(self):\n        self.assertEqual(normalized_tags([]), [])\n    def test_case_sensitive(self):\n        self.assertEqual(normalized_tags(["a", "A"]), ["A", "a"])\n')
        run(fresh, sys.executable, "-B", "-m", "unittest", "discover", "-s", "tests", "-p", "test_tag_fixture.py", "-v")
        board(fresh, "validate")
        require("IN_PROGRESS fixture-tool" in board(fresh, "next").stdout, 'Fixture invariant failed: "IN_PROGRESS fixture-tool" in board(fresh, "next").stdout')
        require(state(fresh / "docs/project") == authority_before, 'Fixture invariant failed: state(fresh / "docs/project") == authority_before')
        report["scenarios"]["development_exercise"] = {"result": "PASS", "kind": "synthetic baseline helper, not product implementation", "executed_tests": 3, "task_state": "started", "product_authority_unchanged": True, "independent_review": "pending", "human_acceptance": "pending"}

    output = Path(sys.argv[1]) if len(sys.argv) > 1 else EVIDENCE / "experiments.json"
    output.write_text(json.dumps(report, indent=2) + "\n")
    print(f"PASS: {len(report['scenarios'])} isolated scenarios; evidence: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
