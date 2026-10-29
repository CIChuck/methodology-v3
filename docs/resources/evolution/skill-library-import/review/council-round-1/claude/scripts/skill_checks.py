import re, sys, os, yaml
from pathlib import Path
repo = Path(sys.argv[1]); base = repo/"docs/methodology/dev-skills"; disc = repo/".agents/skills"
NINE = ["babysit-pr","council","file-pr","full-send","full-stop","leaving-pr-comments","modernize","sol-loop","takeover"]
allnames = {p.name for p in disc.iterdir()}
print("discovery count", len(allnames))
ok = True
for n in NINE:
    d = base/n; s = d/"SKILL.md"; t = s.read_text()
    assert t.startswith("---\n"), n
    fm = yaml.safe_load(t.split("---",2)[1])
    errs = []
    if fm.get("name") != n: errs.append("name mismatch")
    if not fm.get("description") or len(fm["description"])>1024: errs.append("description")
    if set(fm) - {"name","description","license","allowed-tools","metadata"}: errs.append(f"keys {set(fm)}")
    if re.search(r"[<>]", fm["description"]): errs.append("angle bracket in description")
    link = disc/n
    if not (link.is_symlink() and os.readlink(link)==f"../../docs/methodology/dev-skills/{n}" and (link/"SKILL.md").resolve()==s.resolve()): errs.append("discovery link")
    for m in re.finditer(r"\]\(([^)#\s]+)", t):
        tgt = m.group(1)
        if "://" in tgt: continue
        if not (d/tgt).exists(): errs.append(f"broken link {tgt}")
        if not (link/tgt).exists(): errs.append(f"broken link via discovery {tgt}")
    for ref in set(re.findall(r"`([a-z-]+)` skill", t)) | set(re.findall(r"use `([a-z-]+)`", t)):
        if ref not in allnames: errs.append(f"unknown skill ref {ref}")
    y = d/"agents/openai.yaml"
    if y.exists():
        ui = yaml.safe_load(y.read_text())["interface"]
        for k in ("display_name","short_description","default_prompt"):
            if not ui.get(k): errs.append(f"ui {k}")
        for ref in re.findall(r"\$([a-z-]+)", ui["default_prompt"]):
            if ref != n: errs.append(f"ui prompt refs {ref}")
    print(n, "OK" if not errs else errs, "| ui" if y.exists() else "")
    ok &= not errs
# contract links
c = repo/"docs/methodology/guides/skill-execution-contract.md"
for m in re.finditer(r"\]\(([^)#\s]+)", c.read_text()):
    print("contract link", m.group(1), (c.parent/m.group(1)).exists())
print("ALL OK" if ok else "FAILURES")
