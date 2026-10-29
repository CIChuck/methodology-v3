import hashlib, json, os, re, stat, subprocess, sys
from pathlib import Path
R = Path(sys.argv[1]); S = Path("/Users/chuckrussell/Dev/gendev/tstack/skills")
ok = True
def rep(c, msg):
    global ok
    ok &= c; print(("PASS " if c else "FAIL ") + msg)
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
inv = json.loads((R/"docs/resources/evolution/skill-library-import/source-inventory.json").read_text())
man = json.loads((R/"docs/resources/evolution/skill-library-import/import-manifest.json").read_text())
# source still matches inventory
for rel, v in inv["files"].items():
    p = S/rel
    rep(p.is_file() and sha(p)==v["sha256"] and stat.S_IMODE(p.stat().st_mode)==v["mode"], f"source inventory {rel}")
srcfiles = sorted(str(p.relative_to(S)) for p in S.rglob("*") if p.is_file() and ".git" not in p.parts)
imported = {r.split("/")[0] for r in inv["files"]}
rep(sorted(f for f in srcfiles if f.split("/")[0] in imported) == sorted(inv["files"]), "inventory covers every file in the nine source folders")
print("source top-level folders:", sorted({f.split('/')[0] for f in srcfiles}))
rep(len(imported)==9, f"nine imports: {sorted(imported)}")
for m in man:
    d = R/m["destination"]; s = S/m["source"]
    rep(d.is_file() and sha(d)==m["destination_sha256"], f"dest digest {m['destination']}")
    rep(m["source_sha256"]==inv["files"][m["source"]]["sha256"], f"manifest source digest {m['source']}")
    if not m["changed"]:
        rep(d.read_bytes()==s.read_bytes() and stat.S_IMODE(d.stat().st_mode)==stat.S_IMODE(s.stat().st_mode), f"unchanged bytes+mode {m['destination']}")
rep(len(man)==len(inv["files"]), "manifest has one row per source file")
# discovery
ds = R/"docs/methodology/dev-skills"; ag = R/".agents/skills"
links = sorted(ag.iterdir()); rep(len(links)==24, f"24 discovery entries ({len(links)})")
names=set()
for l in links:
    if l.is_symlink():
        print(f"INFO {l.name} dir symlink -> {os.readlink(l)}"); t = l.resolve(); sk = t/"SKILL.md"
    else:
        e = l/"SKILL.md"; rep(e.is_symlink(), f"{l.name}/SKILL.md symlink -> {os.readlink(e)}"); sk = e.resolve(); t = sk
    rep((l/"SKILL.md").is_file(), f"{l.name}/SKILL.md readable through discovery")
    rep(sk.is_file(), f"{l.name} resolves to {sk.relative_to(R)}")
    txt = sk.read_text(); m = re.match(r"---\nname: ([a-z0-9-]+)\ndescription: (.+?)\n(?:[a-z_-]+: .*\n)*---\n", txt)
    rep(bool(m) and m[1]==l.name and len(m[2])>20, f"{l.name} frontmatter name/description")
    if t.is_dir():
        for md in t.rglob("*.md"):
            for tgt in re.findall(r"\]\(([^)#\s]+)(?:#[^)]*)?\)", md.read_text()):
                if re.match(r"[a-z]+:", tgt): continue
                rep((md.parent/tgt).exists(), f"link {md.relative_to(R)} -> {tgt}")
        for y in t.rglob("*.yaml"):
            yt=y.read_text(); rep("display_name" in yt or "interface" in yt, f"UI metadata present {y.relative_to(R)}")
    names.add(m[1] if m else None)
# nested SKILL.md (non-entry) count in canonical tree
nested=[p for p in ds.rglob("SKILL.md") if p.parent.parent!=ds]
print("nested non-entry SKILL.md in source tree:", [str(p.relative_to(R)) for p in nested])
# pr-wait
pw = ds/"babysit-pr/scripts/pr-wait"
rep(os.access(pw, os.X_OK), "pr-wait executable")
first = pw.read_text().splitlines()[0]; print("pr-wait shebang:", first)
