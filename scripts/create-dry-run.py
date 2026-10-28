#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Build a fresh, isolated exercise from declared baseline assets, never live state.

An installed source must pass its integrity check. Its ownership record limits
selection; a methodology checkout uses tracked files. Project-owned adaptations
are replaced with canonical exercise seeds. This is a new fixture installation,
not a copy of the source's installation history or approval authority.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
from distribution import RECORD, Conflict, Entry, apply, digest, json_record, source_entries


def build(source: Path) -> Path:
    check = subprocess.run([str(source / "scripts/gendev-doctor.sh")],
                           capture_output=True, text=True, check=False)
    if check.returncode:
        raise Conflict("source doctor failed; repair the source before making an exercise:\n"
                       + check.stdout + check.stderr)
    installed = source / RECORD
    if installed.exists():
        origin = json_record(installed)
        allowed = set(origin["files"])
        provenance = {key: origin.get(key, "unknown") for key in
                      ("methodology_version", "source_commit", "source_tag")}
    else:
        tracked = subprocess.run(["git", "-C", str(source), "ls-files", "-z"],
                                 capture_output=True, check=False)
        if tracked.returncode or not (source / ".git").exists():
            raise Conflict("source needs an installation record or a tracked methodology checkout")
        allowed = set(os.fsdecode(tracked.stdout).split("\0"))
        revision = subprocess.check_output(["git", "-C", str(source), "rev-parse", "HEAD"], text=True).strip()
        provenance = {"source_commit": revision, "source_tag": "none",
                      "methodology_version": json_record(source / "docs/methodology/schema/lifecycle.json")["versions"]["candidate"]}

    for line in (source / "scripts/lib/distribution-manifest.txt").read_text().splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        kind, _, destination, _, group = line.split("|")
        if kind == "file" and group in {"required", "workflow"} and destination not in allowed:
            raise Conflict(f"required baseline file lacks ownership/tracking: {destination}")
    entries = [entry for entry in source_entries(source, False, "master")
               if entry.owned and entry.path in allowed]
    # Never copy live AGENTS, adapted policies, skill additions, board/task history,
    # product README, provenance history, Git, environment files or runtime state.
    entries.append(Entry("AGENTS.md", (source / "docs/methodology/agents/sample-agents.md").read_bytes()
                         + b"\nApply docs/policies/*.md. Skills are discoverable under .agents/skills/.\n"
                         + b"Run scripts/gendev-doctor.sh and scripts/project-state.sh before work; "
                         + b"validate the board and inspect next before task selection.\n", 0o644, False, False))
    entries.append(Entry("README.md", b"# Isolated GenDev orchestration exercise\n\n"
                         b"Disposable synthetic project; no inherited approvals or live product state.\n", 0o644, False, False))
    for base, destination in (("docs/project-template/planning", "docs/planning"),
                              ("docs/project-template/dry-run-policies", "docs/policies")):
        if not (source / base).is_dir():
            raise Conflict(f"missing canonical exercise seeds: {base}")
        for path in sorted((source / base).rglob("*")):
            if path.is_file():
                name = path.relative_to(source).as_posix()
                if path.is_symlink() or name not in allowed:
                    raise Conflict(f"exercise seed is not a baseline-owned regular file: {name}")
                entries.append(Entry(f"{destination}/{path.relative_to(source / base).as_posix()}",
                                     path.read_bytes(), 0o644, False, False))
    for entry in list(entries):
        if entry.path.startswith("docs/methodology/dev-skills/") and entry.data.startswith(b"---\nname: "):
            name = entry.data.split(b"\n", 2)[1].removeprefix(b"name: ").decode()
            if not name or any(c not in "abcdefghijklmnopqrstuvwxyz0123456789-" for c in name):
                raise Conflict(f"invalid skill name in {entry.path}")
            relative = "../../../" + entry.path
            entries.append(Entry(f".agents/skills/{name}/SKILL.md", os.fsencode(relative), 0o644, True, False))
    entries.append(Entry("docs/archive/completed/.gitkeep", b"", 0o644, False, False))
    names = [entry.path for entry in entries]
    if len(names) != len(set(names)):
        raise Conflict("duplicate exercise destination")
    record = {"record": "gendev-installation", "schema": 1, **provenance,
              "source_remote": "isolated-local-exercise", "source_worktree_dirty": True,
              "installed_on": datetime.now(timezone.utc).isoformat(),
              "fixture": True, "fixture_source": str(source),
              "files": {e.path: digest(e.data) for e in entries if e.owned},
              "file_modes": {e.path: e.mode for e in entries if e.owned},
              "installation_history": [], "local_amendments": []}
    candidate = source / "docs/methodology/schema/candidate.json"
    if candidate.exists():
        record["distribution_candidate"] = json_record(candidate)
    entries.append(Entry(RECORD, (json.dumps(record, indent=2) + "\n").encode(), 0o644, False, False))
    if Path(tempfile.gettempdir()).resolve().is_relative_to(source.resolve()):
        raise Conflict("TMPDIR must be outside the source repository")
    target = Path(tempfile.mkdtemp(prefix="methodology-dry-run."))
    try:
        apply(target, entries)
        return target
    except BaseException:
        shutil.rmtree(target)
        raise


if __name__ == "__main__":
    if len(sys.argv) != 1:
        raise SystemExit("Usage: python3 scripts/create-dry-run.py")
    try:
        print(build(Path(__file__).resolve().parent.parent))
    except (Conflict, OSError, ValueError, subprocess.SubprocessError) as error:
        print(f"Cannot create dry run: {error}", file=sys.stderr)
        raise SystemExit(1)
