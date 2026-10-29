import ast
import hashlib
import json
import os
import re
import stat
import subprocess
from pathlib import Path
import yaml

REPO = Path("/Users/chuckrussell/Dev/gendev/methodology-v3")
SOURCE_ROOT = Path("/Users/chuckrussell/Dev/gendev/tstack/skills")
CANDIDATE = "464cdec246996ebf5bc769174b22a4c62f82305e"
DELTA_BASE = "8abacf4b4b4a6d005cba3bdb92a68c9ce5d81376"
RUNTIME_REF = "aa25aa89762974012c0243e6134e9785f5db970d"

os.chdir(REPO)

def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def sha256_path(p: Path) -> str:
    return sha256_bytes(p.read_bytes())

def mode_int(p: Path) -> int:
    return stat.S_IMODE(p.lstat().st_mode)

results = {}

# Check 5a: 14 source/import digests and modes + 5 support helper/UI files identical to source & runtime ref
src_inv = json.loads((REPO / "docs/resources/evolution/skill-library-import/source-inventory.json").read_text())
imp_man = json.loads((REPO / "docs/resources/evolution/skill-library-import/import-manifest.json").read_text())

assert len(src_inv["files"]) == 14, f"Expected 14 source files, got {len(src_inv['files'])}"
assert len(imp_man) == 14, f"Expected 14 import manifest entries, got {len(imp_man)}"

src_git_head = subprocess.check_output(["git", "-C", str(SOURCE_ROOT), "rev-parse", "HEAD"], text=True).strip()
src_git_status = subprocess.check_output(["git", "-C", str(SOURCE_ROOT), "status", "--porcelain"], text=True).strip()

support_files = []
manifest_checks = []
for entry in imp_man:
    rel_src = entry["source"]
    src_path = SOURCE_ROOT / rel_src
    dst_path = REPO / entry["destination"]
    inv_meta = src_inv["files"][rel_src]

    actual_src_sha = sha256_path(src_path)
    actual_src_mode = mode_int(src_path)
    actual_dst_sha = sha256_path(dst_path)
    actual_dst_mode = mode_int(dst_path)

    src_ok = (actual_src_sha == entry["source_sha256"] == inv_meta["sha256"]) and (actual_src_mode == inv_meta["mode"])
    dst_ok = (actual_dst_sha == entry["destination_sha256"]) and (actual_dst_mode == inv_meta["mode"])
    changed_ok = (entry["changed"] == (actual_src_sha != actual_dst_sha))

    manifest_checks.append({
        "source": rel_src,
        "destination": entry["destination"],
        "src_ok": src_ok,
        "dst_ok": dst_ok,
        "changed": entry["changed"],
        "changed_ok": changed_ok,
        "mode": oct(actual_dst_mode),
    })

    if not entry["changed"]:
        # Support helper/UI file: check identical to source and runtime ref aa25aa8
        ref_bytes = subprocess.check_output(["git", "show", f"{RUNTIME_REF}:{entry['destination']}"])
        ref_mode_line = subprocess.check_output(["git", "ls-tree", RUNTIME_REF, entry["destination"]], text=True).strip().split()[0]
        ref_mode = int(ref_mode_line, 8) & 0o777
        support_files.append({
            "path": entry["destination"],
            "sha256": actual_dst_sha,
            "matches_source_bytes": actual_dst_sha == actual_src_sha,
            "matches_source_mode": actual_dst_mode == actual_src_mode,
            "matches_runtime_ref_bytes": sha256_bytes(ref_bytes) == actual_dst_sha,
            "matches_runtime_ref_mode": ref_mode == actual_dst_mode,
        })

assert len(support_files) == 5, f"Expected 5 unchanged support files, got {len(support_files)}"
assert all(m["src_ok"] and m["dst_ok"] and m["changed_ok"] for m in manifest_checks)
assert all(
    s["matches_source_bytes"] and s["matches_source_mode"] and s["matches_runtime_ref_bytes"] and s["matches_runtime_ref_mode"]
    for s in support_files
)

# Check 5b: 24 skill entrypoint metadata/name/description & relative resources, 9 bundle discovery links, 4 UI YAML files
agents_skills = sorted((REPO / ".agents/skills").iterdir())
assert len(agents_skills) == 24, f"Expected 24 .agents/skills entries, got {len(agents_skills)}"

bundle_links = []
skill_entrypoints = []
md_link_re = re.compile(r"\[[^\]]+\]\(([^)]+)\)")

for skill_dir in agents_skills:
    if skill_dir.is_symlink():
        target = os.readlink(skill_dir)
        resolved = skill_dir.resolve()
        bundle_links.append({
            "name": skill_dir.name,
            "symlink": target,
            "resolved": str(resolved.relative_to(REPO)),
            "exists": resolved.is_dir() and (resolved / "SKILL.md").is_file(),
        })
    skill_md = skill_dir / "SKILL.md"
    assert skill_md.is_file(), f"Missing {skill_md}"
    text = skill_md.read_text(encoding="utf-8")
    assert text.startswith("---\n"), f"Missing frontmatter in {skill_md}"
    fm_end = text.index("\n---\n", 4)
    fm = yaml.safe_load(text[4:fm_end])
    assert isinstance(fm, dict) and fm.get("name") == skill_dir.name and isinstance(fm.get("description"), str) and fm["description"].strip(), f"Bad frontmatter in {skill_md}: {fm}"

    # Check relative links inside SKILL.md (resolved from canonical file parent AND discovery skill_dir)
    canon_md = skill_md.resolve()
    rel_links = []
    for m in md_link_re.finditer(text[fm_end + 5:]):
        link = m.group(1).split("#")[0].strip()
        if not link or "://" in link or link.startswith("mailto:"):
            continue
        target_canon = (canon_md.parent / link).resolve()
        target_disc = (skill_dir / link).resolve()
        assert target_canon.exists(), f"Broken canonical link {link} in {canon_md}"
        assert target_disc.exists(), f"Broken discovery link {link} in {skill_md}"
        rel_links.append(link)

    skill_entrypoints.append({
        "name": fm["name"],
        "canonical_path": str(canon_md.relative_to(REPO)),
        "relative_links_checked": rel_links,
    })

assert len(bundle_links) == 9, f"Expected 9 bundle discovery links, got {len(bundle_links)}"
assert all(b["exists"] for b in bundle_links)

ui_yaml_files = sorted(REPO.glob("docs/methodology/dev-skills/*/agents/openai.yaml"))
assert len(ui_yaml_files) == 4, f"Expected 4 UI YAML files, got {len(ui_yaml_files)}"
ui_yaml_checks = []
for ypath in ui_yaml_files:
    data = yaml.safe_load(ypath.read_text(encoding="utf-8"))
    iface = data.get("interface", {}) if isinstance(data, dict) else {}
    ok = isinstance(iface.get("display_name"), str) and isinstance(iface.get("short_description"), str) and isinstance(iface.get("default_prompt"), str)
    assert ok, f"Invalid UI YAML {ypath}"
    ui_yaml_checks.append({
        "path": str(ypath.relative_to(REPO)),
        "display_name": iface["display_name"],
        "valid": ok,
    })

# Check 5c: Helper syntax via ast.parse & compile(source) in memory ONLY + --help offline
helper_path = REPO / "docs/methodology/dev-skills/babysit-pr/scripts/pr-wait"
helper_src = helper_path.read_text(encoding="utf-8")
ast_tree = ast.parse(helper_src, filename="<in-memory:pr-wait>")
code_obj = compile(helper_src, "<in-memory:pr-wait>", "exec")
help_proc = subprocess.run(
    [str(helper_path), "--help"],
    capture_output=True,
    text=True,
    check=True,
    env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
)

# Check 6: Exact 23-file canonical Practitioner Guide/HTML mirror; unchanged since runtime ref aa25aa8; frozen input manifest and checkpoint approval unchanged since aa25aa8
pg_canonical = sorted(p.name for p in (REPO / "docs/resources/practitioner-guide").iterdir() if p.is_file())
pg_mirror = sorted(p.name for p in (REPO / "docs/resources/practitioner-guide-html/content").iterdir() if p.is_file())
assert len(pg_canonical) == 23 and pg_canonical == pg_mirror, f"Guide mismatch: {len(pg_canonical)} vs {len(pg_mirror)}"
for fname in pg_canonical:
    c_sha = sha256_path(REPO / "docs/resources/practitioner-guide" / fname)
    m_sha = sha256_path(REPO / "docs/resources/practitioner-guide-html/content" / fname)
    assert c_sha == m_sha, f"Mirror SHA mismatch for {fname}"

pg_diff_since_runtime = subprocess.check_output(
    ["git", "diff", RUNTIME_REF, CANDIDATE, "--", "docs/resources/practitioner-guide", "docs/resources/practitioner-guide-html/content"],
    text=True,
)
assert pg_diff_since_runtime == "", "Practitioner guide changed since runtime ref"

frozen_manifest_diff = subprocess.check_output(
    ["git", "diff", RUNTIME_REF, CANDIDATE, "--", "docs/resources/evolution/v3-migration/input-manifest.json", "docs/resources/evolution/v3-migration/review/round-1/checkpoint-exception-approval.json"],
    text=True,
)
assert frozen_manifest_diff == "", "Frozen input manifest or checkpoint approval changed since runtime ref"

# Check 7: Runtime diff empty since aa25aa8; scope proof since delta base 8abacf4
runtime_diff = subprocess.check_output(
    ["git", "diff", RUNTIME_REF, CANDIDATE, "--", "scripts", "tests", ".github", "requirements-devboard.txt", "pyproject.toml", "uv.lock"],
    text=True,
)
assert runtime_diff == "", f"Runtime diff not empty: {runtime_diff}"

delta_changed_files = subprocess.check_output(
    ["git", "diff", "--name-only", DELTA_BASE, CANDIDATE],
    text=True,
).strip().splitlines()

expected_skill_files = {
    "docs/methodology/dev-skills/babysit-pr/SKILL.md",
    "docs/methodology/dev-skills/file-pr/SKILL.md",
    "docs/methodology/dev-skills/full-send/SKILL.md",
    "docs/methodology/dev-skills/full-stop/SKILL.md",
    "docs/methodology/dev-skills/sol-loop/SKILL.md",
}
actual_skill_or_exec_files = {
    f for f in delta_changed_files
    if f.startswith(("docs/methodology/", ".agents/", "scripts/", "tests/", ".github/", "website/"))
    or f in {"requirements-devboard.txt", "pyproject.toml", "uv.lock"}
}
assert actual_skill_or_exec_files == expected_skill_files, f"Unexpected skill/exec changes: {actual_skill_or_exec_files}"

# Check 8: Local gh pr create --help confirmation
gh_help = subprocess.check_output(["gh", "pr", "create", "--help"], text=True)
assert "-B, --base branch" in gh_help, "gh pr create --help missing -B, --base branch"

results = {
    "check_5": {
        "source_commit": src_git_head,
        "source_git_status_clean": src_git_status == "",
        "manifest_entries_verified": len(manifest_checks),
        "support_files_verified": support_files,
        "skill_entrypoints_verified": len(skill_entrypoints),
        "bundle_links_verified": bundle_links,
        "ui_yaml_verified": ui_yaml_checks,
        "helper_in_memory_ast_and_compile": True,
        "helper_help_exit_0": help_proc.returncode == 0,
        "helper_help_first_line": help_proc.stdout.splitlines()[0],
    },
    "check_6": {
        "practitioner_guide_count": len(pg_canonical),
        "mirror_exact_match": True,
        "practitioner_guide_unchanged_since_aa25aa8": pg_diff_since_runtime == "",
        "frozen_manifest_and_checkpoint_approval_unchanged_since_aa25aa8": frozen_manifest_diff == "",
    },
    "check_7": {
        "runtime_diff_empty_since_aa25aa8": runtime_diff == "",
        "delta_changed_files": delta_changed_files,
        "only_five_skill_files_changed_among_exec_and_skill_assets": actual_skill_or_exec_files == expected_skill_files,
    },
    "check_8": {
        "gh_pr_create_help_confirms_base_flag": "-B, --base branch" in gh_help,
    },
}

out_json = Path("/var/folders/dh/wfnmsgpn1yl83xlbmc109sf40000gn/T/v3-skills-council-round4-lk4zdm_d/gemini/checks-5-to-9.json")
out_json.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
print(json.dumps(results, indent=2))
