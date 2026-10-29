
import os, json, hashlib, stat, subprocess, re
import yaml

os.chdir("/Users/chuckrussell/Dev/gendev/methodology-v3")
ev_dir = "/var/folders/dh/wfnmsgpn1yl83xlbmc109sf40000gn/T/v3-skills-council-round3-k749snd7/gemini"

def sha256_file(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def file_mode_str(path):
    return oct(os.stat(path, follow_symlinks=False).st_mode & 0o777)[2:].zfill(4)

results = {}

with open("docs/resources/evolution/skill-library-import/import-manifest.json") as f:
    imp = json.load(f)

source_root = "/Users/chuckrussell/Dev/gendev/tstack/skills"
results["import_manifest_summary"] = {
    "source_root": source_root,
    "entry_count": len(imp),
}

entry_checks = []
skills_seen = set()
for fentry in imp:
    src_rel = fentry["source"]
    skill_name = src_rel.split("/")[0]
    skills_seen.add(skill_name)
    src_path = os.path.join(source_root, src_rel)
    dst_path = fentry["destination"]
    src_sha = sha256_file(src_path)
    dst_sha = sha256_file(dst_path)
    src_mode = file_mode_str(src_path)
    dst_mode = file_mode_str(dst_path)
    src_match = (src_sha == fentry["source_sha256"])
    dst_match = (dst_sha == fentry["destination_sha256"])
    mode_match = (src_mode == dst_mode)
    unchanged_match = ((src_sha == dst_sha) == (not fentry["changed"]))
    ok = src_match and dst_match and mode_match and unchanged_match
    entry_checks.append({
        "source": src_rel,
        "destination": dst_path,
        "changed": fentry["changed"],
        "src_sha_ok": src_match,
        "dst_sha_ok": dst_match,
        "src_mode": src_mode,
        "dst_mode": dst_mode,
        "mode_ok": mode_match,
        "unchanged_flag_ok": unchanged_match,
        "all_ok": ok,
    })

symlink_checks = []
for name in sorted(skills_seen):
    link_path = os.path.join(".agents/skills", name)
    is_sym = os.path.islink(link_path)
    target = os.readlink(link_path) if is_sym else None
    resolved = os.path.realpath(link_path)
    expected_resolved = os.path.realpath(os.path.join("docs/methodology/dev-skills", name))
    sym_ok = is_sym and (target == f"../../docs/methodology/dev-skills/{name}") and (resolved == expected_resolved)
    symlink_checks.append({
        "name": name,
        "symlink_ok": sym_ok,
        "symlink_target": target,
    })

results["imported_entries"] = entry_checks
results["imported_9_symlinks"] = symlink_checks
print("14 manifest entries all ok:", all(e["all_ok"] for e in entry_checks))
print("9 imported skill whole-folder symlinks ok:", len(symlink_checks), all(s["symlink_ok"] for s in symlink_checks))

src_all_files = []
for root, dirs, files in os.walk(source_root):
    for fn in files:
        if fn == ".DS_Store":
            continue
        rel = os.path.relpath(os.path.join(root, fn), source_root)
        src_all_files.append(rel)
manifest_src_files = [fe["source"] for fe in imp]
results["source_inventory_complete"] = (sorted(src_all_files) == sorted(manifest_src_files))
print("source_inventory_complete:", results["source_inventory_complete"], len(src_all_files))

agent_entries = sorted(os.listdir(".agents/skills"))
skills_24 = []
for entry in agent_entries:
    p = os.path.join(".agents/skills", entry)
    skill_md = os.path.join(p, "SKILL.md")
    with open(skill_md) as f:
        text = f.read()
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    fm = yaml.safe_load(m.group(1)) if m else {}
    links = re.findall(r"\[[^\]]+\]\(([^)]+)\)", text)
    rel_links_ok = True
    checked_links = []
    for lk in links:
        if "://" in lk or lk.startswith("#"):
            continue
        lk_clean = lk.split("#")[0]
        canon_dir = os.path.dirname(os.path.realpath(skill_md))
        p1 = os.path.normpath(os.path.join(canon_dir, lk_clean))
        p2 = os.path.normpath(os.path.join(p, lk_clean))
        ok1 = os.path.exists(p1)
        ok2 = os.path.exists(p2)
        checked_links.append({"link": lk, "canon_exists": ok1, "agent_exists": ok2})
        if not ok1:
            rel_links_ok = False
    skills_24.append({
        "entry": entry,
        "is_dir_symlink": os.path.islink(p),
        "has_skill_md_symlink": os.path.islink(skill_md),
        "name": fm.get("name"),
        "name_matches_dir": fm.get("name") == entry,
        "has_description": bool(fm.get("description") and isinstance(fm.get("description"), str)),
        "canon_links_ok": rel_links_ok,
        "links": checked_links,
    })

results["skills_24_count"] = len(skills_24)
results["skills_24_all_valid"] = all(s["name_matches_dir"] and s["has_description"] and s["canon_links_ok"] for s in skills_24)
print("24 skills valid:", results["skills_24_count"], results["skills_24_all_valid"])

ui_files = []
for fe in imp:
    if fe["destination"].endswith("openai.yaml"):
        with open(fe["destination"]) as yf:
            ydata = yaml.safe_load(yf)
        iface = ydata.get("interface", {})
        ui_ok = all(k in iface and isinstance(iface[k], str) and iface[k].strip() for k in ["display_name", "short_description", "default_prompt"])
        ui_files.append({"path": fe["destination"], "ui_ok": ui_ok, "keys": list(iface.keys())})
results["ui_files"] = ui_files
print("UI files valid:", len(ui_files), all(u["ui_ok"] for u in ui_files))

pr_wait_path = "docs/methodology/dev-skills/babysit-pr/scripts/pr-wait"
c_res = subprocess.run(["python3", "-m", "py_compile", pr_wait_path], capture_output=True, text=True)
h_res = subprocess.run(["python3", pr_wait_path, "--help"], capture_output=True, text=True)
results["pr_wait_check"] = {
    "path": pr_wait_path,
    "mode": file_mode_str(pr_wait_path),
    "py_compile_exit": c_res.returncode,
    "help_exit": h_res.returncode,
    "help_first_line": h_res.stdout.splitlines()[0] if h_res.stdout else "",
}
print("pr-wait check:", results["pr_wait_check"])

guide_dir = "docs/resources/practitioner-guide"
html_dir = "docs/resources/practitioner-guide-html/content"
guide_files = sorted(f for f in os.listdir(guide_dir) if f.endswith(".md"))
html_files = sorted(f for f in os.listdir(html_dir) if f.endswith(".md"))
mirror_matches = []
for gf in guide_files:
    p1 = os.path.join(guide_dir, gf)
    p2 = os.path.join(html_dir, gf)
    s1 = sha256_file(p1)
    s2 = sha256_file(p2) if os.path.exists(p2) else None
    mirror_matches.append({"file": gf, "sha256": s1, "match": s1 == s2})

guide_diff_aa25 = subprocess.check_output([
    "git", "diff",
    "aa25aa89762974012c0243e6134e9785f5db970d",
    "5e2ab4047a69c82fc883735134c23527197b3c1e",
    "--", guide_dir, html_dir, "docs/resources/practitioner-guide-html"
])
results["practitioner_guide_mirror"] = {
    "guide_count": len(guide_files),
    "html_count": len(html_files),
    "filenames_identical": guide_files == html_files,
    "all_bytes_identical": all(m["match"] for m in mirror_matches),
    "diff_from_aa25aa8_bytes": len(guide_diff_aa25),
}
print("practitioner guide mirror:", results["practitioner_guide_mirror"])

diff_skills_from_aa25 = subprocess.check_output([
    "git", "diff", "--name-only",
    "aa25aa89762974012c0243e6134e9785f5db970d",
    "5e2ab4047a69c82fc883735134c23527197b3c1e",
    "--", ".agents/skills", "docs/methodology/dev-skills", "docs/methodology/skills", "docs/methodology/guides/skill-execution-contract.md"
], text=True).strip().splitlines()
results["skills_changed_since_aa25aa8"] = diff_skills_from_aa25
print("skills changed since aa25aa8:", diff_skills_from_aa25)

with open(os.path.join(ev_dir, "independent-verification.json"), "w") as out_f:
    json.dump(results, out_f, indent=2)
