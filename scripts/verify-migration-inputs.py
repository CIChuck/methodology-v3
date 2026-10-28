#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Read-only comparison of the preserved source projects with the migration inventory."""
from __future__ import annotations

import hashlib
import json
import os
import stat
import subprocess
import sys
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    manifest = Path(sys.argv[1]) if len(sys.argv) > 1 else root / "docs/resources/evolution/v3-migration/input-manifest.json"
    record = json.loads(manifest.read_text())
    errors: list[str] = []
    env = {**os.environ, "GIT_OPTIONAL_LOCKS": "0"}
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
            if current != source[field]:
                errors.append(f"{label}: Git {field} changed")
        print(f"Checked {label}: {len(source['files'])} files/links and Git state")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("PASS: both original projects match the frozen input manifest")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
