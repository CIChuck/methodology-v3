#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Plan conflict-aware baseline installation, then apply it transactionally.

The manifest distinguishes baseline-owned files from project-owned seed files.
Only baseline source files enter integrity ownership. Local extras are retained.
Conflicts are detected before any target mutation; --force is not data-loss
permission. No target hooks, credentials, package installers or Git writes run.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import signal
import stat
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any

RECORD = "docs/methodology/schema/installation.json"


class Conflict(ValueError):
    """A target needs explicit reconciliation before an upgrade can proceed."""


def json_record(path: Path) -> dict[str, Any]:
    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise Conflict(f"duplicate JSON field in {path.name}: {key}")
            result[key] = value
        return result

    result = json.loads(path.read_text(), object_pairs_hook=unique)
    if not isinstance(result, dict):
        raise Conflict(f"expected a JSON object: {path.name}")
    return result


def relative(value: str) -> str:
    if not isinstance(value, str) or not value or "\\" in value:
        raise Conflict("invalid manifest/record path")
    parts = value.split("/")
    if PurePosixPath(value).is_absolute() or any(p in ("", ".", "..") for p in parts):
        raise Conflict(f"noncanonical manifest/record path: {value}")
    if any(ord(c) < 32 for c in value):
        raise Conflict("control character in manifest/record path")
    return value


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def fingerprint(path: Path) -> tuple[str, bytes, int] | None:
    if path.is_symlink():
        return ("link", os.fsencode(os.readlink(path)), 0)
    if path.exists():
        if not path.is_file():
            raise Conflict(f"expected a regular file: {path}")
        return ("file", path.read_bytes(), stat.S_IMODE(path.stat().st_mode))
    return None


def check_parents(root: Path, name: str) -> None:
    path = root
    for part in PurePosixPath(name).parts[:-1]:
        path /= part
        if path.is_symlink() or (path.exists() and not path.is_dir()):
            raise Conflict(f"unsafe target parent: {path.relative_to(root)}")


@dataclass(frozen=True)
class Entry:
    path: str
    data: bytes
    mode: int
    link: bool
    owned: bool


def source_entries(source: Path, resources: bool, branch: str) -> list[Entry]:
    entries: list[Entry] = []
    seen: set[str] = set()
    for line in (source / "scripts/lib/distribution-manifest.txt").read_text().splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        kind, src, dst, mode, group = line.split("|")
        relative(src)
        relative(dst)
        if group == "optional_resources" and not resources:
            continue
        if kind not in {"tree", "file"} or group not in {
            "required", "workflow", "agents", "optional_resources", "project"
        }:
            raise Conflict(f"invalid distribution entry: {src}")
        base = source / src
        if not base.exists():
            raise Conflict(f"Distribution source missing: {src}")
        paths = sorted(base.rglob("*")) if kind == "tree" else [base]
        for path in paths:
            if "__pycache__" in path.parts or path.name == ".DS_Store" or path.suffix == ".pyc":
                continue
            if path.is_dir() and not path.is_symlink():
                continue
            name = (PurePosixPath(dst) / path.relative_to(base).as_posix()).as_posix() if kind == "tree" else dst
            relative(name)
            if name == RECORD:
                continue
            if name in seen:
                raise Conflict(f"duplicate distribution destination: {name}")
            seen.add(name)
            link = path.is_symlink()
            if link:
                # Source discovery links must remain internal in a fresh target.
                value = os.readlink(path)
                target_path = (source / src / path.relative_to(base)).resolve()
                if Path(value).is_absolute() or not target_path.is_relative_to(source.resolve()):
                    raise Conflict(f"external source symlink: {name}")
                data = os.fsencode(value)
            else:
                data = path.read_bytes()
            if name == ".github/workflows/methodology.yml":
                data = data.replace(b"      - master\n", f"      - {branch}\n".encode())
            owned = group not in {"project", "agents"}
            if link and owned:
                raise Conflict(f"baseline-owned symlink is unsupported: {name}")
            entries.append(Entry(name, data, 0o755 if mode == "executable" else stat.S_IMODE(path.stat().st_mode), link, owned))
    return entries


def git_value(source: Path, *args: str, fallback: str = "unknown") -> str:
    result = subprocess.run(["git", "-C", str(source), *args], capture_output=True, text=True, check=False)
    return result.stdout.strip() if result.returncode == 0 else fallback


def plan(source: Path, target: Path, force: bool, resources: bool, integrate: bool, branch: str) -> tuple[list[Entry], list[str]]:
    entries = source_entries(source, resources, branch)
    check_parents(target, RECORD)
    record_path = target / RECORD
    if record_path.is_symlink():
        raise Conflict(f"symlink installation record: {RECORD}")
    old = json_record(record_path) if record_path.exists() else {}
    if not isinstance(old, dict) or not isinstance(old.get("files", {}), dict):
        raise Conflict("malformed installation ownership record")
    owned: dict[str, str] = old.get("files", {})
    modes = old.get("file_modes", {})
    if not isinstance(modes, dict) or set(modes) - set(owned):
        raise Conflict("malformed permission ownership record")
    for name, mode in modes.items():
        if type(mode) is not int or not 0 <= mode <= 0o7777:
            raise Conflict(f"invalid permission ownership mode: {name}")
    incoming = {e.path: e for e in entries if e.owned}
    new_modes: dict[str, int] = dict(modes)
    legacy_mode_adoptions: list[str] = []
    # Verify all previously owned files, including retired files retained in place.
    for name, expected in owned.items():
        relative(name)
        if not isinstance(expected, str) or not re.fullmatch(r"[0-9a-f]{64}", expected):
            raise Conflict(f"invalid ownership digest: {name}")
        check_parents(target, name)
        state = fingerprint(target / name)
        if state is None or state[0] != "file" or digest(state[1]) != expected:
            raise Conflict(f"locally modified, removed or symlink baseline file: {name}; reconcile before upgrading")
        if name in modes:
            if state[2] != modes[name]:
                raise Conflict(f"locally modified permissions: {name}; reconcile before upgrading")
        else:
            # Legacy records prove bytes only. Do not silently replace an
            # ambiguous local restriction. Retired files are not overwritten.
            if name in incoming and state[2] != incoming[name].mode:
                raise Conflict(f"legacy permissions need reconciliation: {name}")
            new_modes[name] = state[2]
            legacy_mode_adoptions.append(name)
    amendments = old.get("local_amendments", [])
    if not isinstance(amendments, list):
        raise Conflict("malformed local amendment history")
    for amendment in amendments:
        if not isinstance(amendment, dict) or not isinstance(amendment.get("files"), dict):
            raise Conflict("malformed local amendment file map")
        for name in amendment["files"]:
            relative(name)
            if name in incoming:
                check_parents(target, name)
                state = fingerprint(target / name)
                if state is None or state[0] != "file" or state[1] != incoming[name].data:
                    raise Conflict(f"local amendment needs reconciliation: {name}")

    writes: list[Entry] = []
    report: list[str] = []
    new_owned = dict(owned)
    for entry in entries:
        check_parents(target, entry.path)
        state = fingerprint(target / entry.path)
        if entry.owned:
            if state is not None:
                if not force:
                    raise Conflict(f"{entry.path} exists; use --force after reconciliation")
                if state[0] != "file" or (entry.path not in owned and (state[1] != entry.data or state[2] != entry.mode)):
                    raise Conflict(f"unowned collision needs reconciliation: {entry.path}")
            new_owned[entry.path] = digest(entry.data)
            new_modes[entry.path] = entry.mode
        elif state is not None:
            report.append(f"preserved: {entry.path} (project-owned)")
            continue
        writes.append(entry)
        report.append(f"{'upgraded' if state else 'installed'}: {entry.path}")

    if integrate and (target / "AGENTS.md").exists():
        check_parents(target, "AGENTS.md")
        state = fingerprint(target / "AGENTS.md")
        if state is None or state[0] != "file":
            raise Conflict("AGENTS.md integration requires a regular file")
        include = Entry("AGENTS.gendev.md", (source / "AGENTS.md").read_bytes(), 0o644, False, True)
        check_parents(target, include.path)
        existing = fingerprint(target / include.path)
        if existing and (existing[0] != "file" or (include.path not in owned and (existing[1] != include.data or existing[2] != include.mode))):
            raise Conflict("AGENTS.gendev.md needs reconciliation")
        writes.append(include)
        new_owned[include.path] = digest(include.data)
        new_modes[include.path] = include.mode
        if b"# BEGIN MANAGED GENDEV INSTRUCTIONS" not in state[1]:
            writes.append(Entry("AGENTS.md", state[1] + b"\n# BEGIN MANAGED GENDEV INSTRUCTIONS\nGenDev methodology instructions are available in AGENTS.gendev.md. Preserve local instructions above unless explicitly amended.\n# END MANAGED GENDEV INSTRUCTIONS\n", state[2], False, False))

    ignore = fingerprint(target / ".gitignore")
    if ignore and ignore[0] != "file":
        raise Conflict(".gitignore must be a regular file")
    ignore_data = ignore[1] if ignore else b""
    if b".tmp/" not in ignore_data.splitlines():
        writes.append(Entry(".gitignore", ignore_data + (b"\n" if ignore_data and not ignore_data.endswith(b"\n") else b"") + b".tmp/\n", ignore[2] if ignore else 0o644, False, False))

    history = old.get("installation_history", [])
    if not isinstance(history, list):
        raise Conflict("malformed installation history")
    registry = json_record(source / "docs/methodology/schema/lifecycle.json")
    record = dict(old)
    record.update({
        "record": "gendev-installation", "schema": 1,
        "methodology_version": registry["versions"]["candidate"],
        "source_remote": git_value(source, "remote", "get-url", "origin", fallback=str(source)),
        "source_tag": git_value(source, "describe", "--tags", "--exact-match", fallback="none"),
        "source_commit": git_value(source, "rev-parse", "HEAD"),
        "source_worktree_dirty": bool(git_value(source, "status", "--porcelain", fallback="")),
        "installed_on": datetime.now(timezone.utc).isoformat(),
        "installer_options": f"force={int(force)} resources={int(resources)} agents={int(integrate)} branch={branch}",
        "files": dict(sorted(new_owned.items())),
        "file_modes": dict(sorted(new_modes.items())),
        "legacy_mode_adoptions": legacy_mode_adoptions,
        "installation_history": history + ([{k: v for k, v in old.items() if k != "installation_history"}] if old else []),
    })
    candidate = source / "docs/methodology/schema/candidate.json"
    if candidate.exists():
        record["distribution_candidate"] = json_record(candidate)
    writes.append(Entry(RECORD, (json.dumps(record, indent=2) + "\n").encode(), 0o644, False, False))
    return writes, report


def apply(target: Path, entries: list[Entry]) -> None:
    originals = {e.path: fingerprint(target / e.path) for e in entries}
    applied: list[str] = []
    directories: list[Path] = []
    fail_after = int(os.environ.get("GENDEV_INSTALL_FAIL_AFTER", "0"))

    def write(path: Path, data: bytes, mode: int, link: bool) -> None:
        fd, name = tempfile.mkstemp(prefix=".gendev-write-", dir=path.parent)
        staging = Path(name)
        try:
            with os.fdopen(fd, "wb") as stream:
                stream.write(data)
            if link:
                staging.unlink()
                staging.symlink_to(os.fsdecode(data))
            else:
                staging.chmod(mode)
            os.replace(staging, path)
        finally:
            staging.unlink(missing_ok=True)

    try:
        for number, entry in enumerate(entries, 1):
            path = target / entry.path
            check_parents(target, entry.path)
            if fingerprint(path) != originals[entry.path]:
                raise Conflict(f"target changed during installation: {entry.path}")
            missing: list[Path] = []
            parent = path.parent
            while not parent.exists():
                missing.append(parent)
                parent = parent.parent
            for parent in reversed(missing):
                parent.mkdir()
                directories.append(parent)
            # Record before replacing, so a failing write can still restore it.
            applied.append(entry.path)
            write(path, entry.data, entry.mode, entry.link)
            if (fail_after and number >= fail_after) or os.environ.get("GENDEV_INSTALL_FAIL_AT") == entry.path:
                raise Conflict(f"Simulated install failure after {number} writes")
    except BaseException:
        for name in reversed(applied):
            path = target / name
            original = originals[name]
            if original is None:
                path.unlink(missing_ok=True)
            else:
                write(path, original[1], original[2], original[0] == "link")
        for directory in reversed(directories):
            directory.rmdir()
        raise


def main() -> int:
    if len(sys.argv) != 8:
        print("Usage: distribution.py SOURCE TARGET FORCE RESOURCES DRY_RUN INTEGRATE BRANCH", file=sys.stderr)
        return 2
    source_s, target_s, force_s, resources_s, dry_s, integrate_s, branch = sys.argv[1:]
    source, target = Path(source_s).resolve(), Path(target_s).resolve()
    if source.is_relative_to(target) or target.is_relative_to(source):
        print("blocked: source and target directories must not overlap", file=sys.stderr)
        return 1
    if not branch:
        branch = git_value(target, "symbolic-ref", "--quiet", "--short", "HEAD", fallback="main")
    valid_branch = subprocess.run(["git", "check-ref-format", "--branch", branch], capture_output=True, check=False)
    if valid_branch.returncode:
        print("blocked: invalid protected branch", file=sys.stderr)
        return 1

    def interrupted(signum: int, _frame: object) -> None:
        raise Conflict(f"installation interrupted by signal {signum}")

    for signum in (signal.SIGTERM, signal.SIGHUP):
        signal.signal(signum, interrupted)
    try:
        entries, report = plan(source, target, force_s == "1", resources_s == "1", integrate_s == "1", branch)
        if dry_s == "1":
            print("Distribution report: dry-run; no writes")
        else:
            apply(target, entries)
            print("Distribution report:")
        for line in report:
            print("  " + line)
        return 0
    except (Conflict, OSError, ValueError, KeyError, TypeError, KeyboardInterrupt) as exc:
        print(f"blocked: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
