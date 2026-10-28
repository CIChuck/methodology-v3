#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Read-only comparison of the preserved source projects with the migration inventory."""
from __future__ import annotations

import hashlib
import json
import os
import re
import stat
import subprocess
import sys
from pathlib import Path


T3_CHECKPOINT = re.compile(r"^refs/t3/orchestration-v2/checkpoints/([A-Za-z0-9_-]+)/ordinal/([0-9]+)$")


def compare_refs(base: Path, expected: str, current: str, *, allow_identical_t3_checkpoints: bool = False) -> tuple[list[str], list[dict[str, str]]]:
    """Protect every frozen ref; classify only the explicitly approved additions."""
    before = dict(line.split() for line in expected.splitlines())
    after = dict(line.split() for line in current.splitlines())
    errors: list[str] = []
    allowed: list[dict[str, str]] = []
    env = {**os.environ, "GIT_OPTIONAL_LOCKS": "0"}

    def git(*args: str) -> str:
        return subprocess.check_output(["git", *args], cwd=base, env=env, text=True, stderr=subprocess.DEVNULL).strip()

    for name, oid in before.items():
        if after.get(name) != oid:
            errors.append(f"frozen ref changed or removed: {name}")
    for name in sorted(set(after) - set(before)):
        match = T3_CHECKPOINT.fullmatch(name)
        anchors = []
        if allow_identical_t3_checkpoints and match:
            for old_name, old_oid in before.items():
                old_match = T3_CHECKPOINT.fullmatch(old_name)
                if old_match and old_match[1] == match[1]:
                    anchors.append((int(old_match[2]), old_name, old_oid))
        if not anchors:
            errors.append(f"unapproved added ref: {name}")
            continue
        ordinal, anchor_name, anchor_oid = max(anchors)
        try:
            oid = after[name]
            metadata = git("show", "--no-patch", "--format=%an%x00%ae%x00%s", oid).split("\0")
            tree = git("rev-parse", oid + "^{tree}")
            anchor_tree = git("rev-parse", anchor_oid + "^{tree}")
            if (
                int(match[2]) <= ordinal
                or git("cat-file", "-t", oid) != "commit"
                or metadata != ["T3 Code", "t3code@users.noreply.github.com", "t3 checkpoint ref=" + name]
                or tree != anchor_tree
            ):
                errors.append(f"added checkpoint does not satisfy approved exception: {name}")
                continue
            allowed.append({"ref": name, "oid": oid, "tree": tree, "frozen_anchor": anchor_name})
        except (subprocess.CalledProcessError, ValueError):
            errors.append(f"cannot verify added checkpoint: {name}")
    return errors, allowed


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    manifest = Path(sys.argv[1]) if len(sys.argv) > 1 else root / "docs/resources/evolution/v3-migration/input-manifest.json"
    record = json.loads(manifest.read_text())
    errors: list[str] = []
    env = {**os.environ, "GIT_OPTIONAL_LOCKS": "0"}
    approval_path = root / "docs/resources/evolution/v3-migration/review/round-1/checkpoint-exception-approval.json"
    approval = json.loads(approval_path.read_text()) if approval_path.exists() else {}
    approved_exception = (
        approval.get("approved_by") == "Chuck Russell"
        and approval.get("instruction") == "Approve the narrow checkpoint exception"
        and approval.get("original_inventory_changed") is False
    )
    for label, source in record["sources"].items():
        base = Path(source["path"])
        if not base.is_dir():
            errors.append(f"{label}: original source unavailable")
            continue
        names = set(subprocess.check_output(["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"], cwd=base, env=env).decode().split("\0")) - {""}
        if names != set(source["files"]):
            errors.append(f"{label}: source file inventory changed")
        for name, expected in source["files"].items():
            p = base / name
            if expected["kind"] == "symlink":
                if not p.is_symlink() or os.readlink(p) != expected["target"]:
                    errors.append(f"{label}: changed symlink {name}")
            elif not p.is_file() or p.is_symlink():
                errors.append(f"{label}: missing or changed file {name}")
            elif hashlib.sha256(p.read_bytes()).hexdigest() != expected["sha256"] or stat.S_IMODE(p.stat().st_mode) != expected["mode"]:
                errors.append(f"{label}: changed bytes or mode {name}")
        for args, field in [( ["status", "--porcelain=v1", "--untracked-files=all"], "status"), (["for-each-ref", "--format=%(refname) %(objectname)"], "refs")]:
            current = subprocess.check_output(["git", *args], cwd=base, env=env, text=True)
            if field == "refs":
                ref_errors, observations = compare_refs(base, source[field], current, allow_identical_t3_checkpoints=approved_exception)
                errors.extend(f"{label}: {error}" for error in ref_errors)
                for observation in observations:
                    print(f"APPROVED EXCEPTION: {label}: additive identical-tree T3 checkpoint {observation['ref']} ({observation['oid']}); anchor {observation['frozen_anchor']}")
            elif current != source[field]:
                errors.append(f"{label}: Git {field} changed")
        print(f"Checked {label}: {len(source['files'])} files/links and Git state")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("PASS: original project contents/state and frozen refs preserved; only explicitly approved identical-tree T3 checkpoint additions permitted")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
