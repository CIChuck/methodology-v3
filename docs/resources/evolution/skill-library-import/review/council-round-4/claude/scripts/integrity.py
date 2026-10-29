"""Round-4 independent integrity checks (read-only; no bytecode writes)."""
import hashlib, json, os, re, stat, subprocess, sys
from pathlib import Path
REPO = Path("/Users/chuckrussell/Dev/gendev/methodology-v3")
SRC = Path("/Users/chuckrussell/Dev/gendev/tstack/skills")
CAND, REF, BASE = "464cdec246996ebf5bc769174b22a4c62f82305e", "aa25aa89762974012c0243e6134e9785f5db970d", "8abacf4b4b4a6d005cba3bdb92a68c9ce5d81376"
os.chdir(REPO)
fails = []
def chk(ok, msg):
    print(("PASS " if ok else "FAIL ") + msg)
    if not ok: fails.append(msg)
def sha(b): return hashlib.sha256(b).hexdigest()
def gshow(rev, p): return subprocess.run(["git", "show", f"{rev}:{p}"], capture_output=True, check=True).stdout
def gmode(rev, p):
    out = subprocess.run(["git", "ls-tree", rev, "--", p], capture_output=True, text=True, check=True).stdout.split()
    return out[0] if out else None

# 1. 14 import-manifest entries
man = json.loads(gshow(CAND, "docs/resources/evolution/skill-library-import/import-manifest.json"))
chk(len(man) == 14, f"manifest entries = {len(man)}")
for e in man:
    s = SRC / e["source"]; d = e["destination"]
    sb = s.read_bytes(); db = gshow(CAND, d); wb = (REPO / d).read_bytes()
    chk(sha(sb) == e["source_sha256"], f"source digest {e['source']}")
    chk(sha(db) == e["destination_sha256"] == sha(wb), f"dest digest (tree+worktree) {d}")
    chk((sb != db) == e["changed"], f"changed flag {d} = {e['changed']}")
    smode = "100755" if os.stat(s).st_mode & stat.S_IXUSR else "100644"
    chk(gmode(CAND, d) == smode, f"mode {d} git={gmode(CAND, d)} source={smode}")
    wmode = "100755" if os.stat(REPO / d).st_mode & stat.S_IXUSR else "100644"
    chk(wmode == smode, f"worktree mode {d}={wmode}")
# source tree contains exactly those 14 files
srcfiles = sorted(str(p.relative_to(SRC)) for p in SRC.rglob("*") if p.is_file())
chk(srcfiles == sorted(e["source"] for e in man), f"source tree file set ({len(srcfiles)}) == manifest")

# 2. five support helper/UI files identical to source AND runtime reference AND base
support = [e for e in man if not e["changed"]]
chk(len(support) == 5, f"unchanged support files = {len(support)}")
for e in support:
    d = e["destination"]
    chk(gshow(REF, d) == gshow(CAND, d) == gshow(BASE, d) == (SRC / e["source"]).read_bytes(), f"support byte-identical src/ref/base/cand {d}")
    chk(gmode(REF, d) == gmode(CAND, d), f"support mode unchanged since ref {d} ({gmode(CAND, d)})")

# 3. nine discovery links
nine = ["babysit-pr","council","file-pr","full-send","full-stop","leaving-pr-comments","modernize","sol-loop","takeover"]
for n in nine:
    link = REPO / ".agents/skills" / n
    tgt = os.readlink(link) if link.is_symlink() else None
    chk(tgt == f"../../docs/methodology/dev-skills/{n}", f"discovery link {n} -> {tgt}")
    chk(link.resolve() == (REPO / "docs/methodology/dev-skills" / n).resolve() and (link / "SKILL.md").is_file(), f"link resolves {n}")
    chk(gmode(CAND, f".agents/skills/{n}") == "120000", f"link committed as symlink {n}")

# 4. 24 skill entrypoints: frontmatter name/description, relative links resolve
entries = sorted(p for p in (REPO / ".agents/skills").iterdir())
chk(len(entries) == 24, f"skill entries = {len(entries)}")
fm_re = re.compile(r"\A---\n(.*?)\n---\n", re.S)
link_re = re.compile(r"\]\(([^)#\s]+)(?:#[^)]*)?\)")
for e in entries:
    sk = e / "SKILL.md"
    txt = sk.read_text()
    m = fm_re.match(txt)
    chk(bool(m), f"frontmatter {e.name}")
    if not m: continue
    fm = m.group(1)
    name = re.search(r"^name:\s*(.+)$", fm, re.M)
    chk(bool(name) and name.group(1).strip() == e.name, f"name matches dir {e.name}")
    desc = re.search(r"^description:\s*(.*)$", fm, re.M)
    dv = desc.group(1).strip() if desc else ""
    if dv in (">-", ">", "|", "|-"):
        dv = " ".join(l.strip() for l in fm[desc.end():].splitlines() if l.startswith("  "))
    chk(len(dv) > 10, f"description non-empty {e.name}")
    base = sk.resolve().parent
    for target in link_re.findall(txt):
        if re.match(r"^[a-z]+:", target): continue
        chk((base / target).exists(), f"link {e.name}: {target}")

# 5. four UI YAML files parse (structure check without PyYAML: compile via ast is not applicable); delegated to uv yaml step
# 6. helper syntax in memory
import ast
helper = REPO / "docs/methodology/dev-skills/babysit-pr/scripts/pr-wait"
src = helper.read_text()
ast.parse(src, filename=str(helper)); compile(src, str(helper), "exec", dont_inherit=True)
chk(True, "pr-wait ast.parse+compile in memory")
chk(src.startswith("#!"), f"pr-wait shebang: {src.splitlines()[0]}")

# 7. 23-file guide mirror exact; unchanged since runtime reference
g = REPO / "docs/resources/practitioner-guide"; h = REPO / "docs/resources/practitioner-guide-html/content"
exp = {p.name: p.read_bytes() for p in g.glob("*.md")}; act = {p.name: p.read_bytes() for p in h.glob("*.md")}
chk(len(exp) == 23 and exp == act, f"guide mirror exact {len(exp)}/{len(act)}")
d = subprocess.run(["git","diff","--name-only",REF,CAND,"--","docs/resources/practitioner-guide","docs/resources/practitioner-guide-html"],capture_output=True,text=True,check=True).stdout
chk(d == "", "guide + HTML unchanged since aa25aa8")
d = subprocess.run(["git","diff","--name-only",REF,CAND,"--","docs/resources/evolution/v3-migration/input-manifest.json","docs/resources/evolution/v3-migration/review/round-1/checkpoint-exception-approval.json"],capture_output=True,text=True,check=True).stdout
chk(d == "", "frozen input manifest + checkpoint approval unchanged since aa25aa8")

# 8. delta scope: only five SKILL.md among skill/executable assets since BASE
names = subprocess.run(["git","diff","--name-only",BASE,CAND],capture_output=True,text=True,check=True).stdout.split()
asset = [n for n in names if n.startswith(("docs/methodology/","scripts/","tests/",".agents/",".github/","t3.json","pyproject","uv.lock","requirements"))]
chk(sorted(asset) == sorted(f"docs/methodology/dev-skills/{s}/SKILL.md" for s in ["babysit-pr","file-pr","sol-loop","full-send","full-stop"]), f"methodology/executable/skill asset changes since base: {asset}")
other = [n for n in names if n not in asset]
chk(all(n.startswith(("docs/planning/","docs/resources/evolution/skill-library-import/")) for n in other), f"other changes confined to tracking/evidence: {len(other)} files")
print("\nRESULT:", "FAIL" if fails else "PASS", len(fails))
sys.exit(1 if fails else 0)
