"""Disposable probe: build dry-run fixture via create-dry-run.build with ONLY the doctor
subprocess stubbed (rg unavailable here). Labeled non-substitute evidence."""
import importlib.util, json, os, subprocess, sys
from pathlib import Path
repo = Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("cdr", repo / "scripts/create-dry-run.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
real = subprocess.run
def fake(args, *a, **k):
    if isinstance(args, list) and str(args[0]).endswith("gendev-doctor.sh"):
        return subprocess.CompletedProcess(args, 0, "", "")
    return real(args, *a, **k)
m.subprocess.run = fake
t = m.build(repo)
print("TARGET", t)
sk = t / ".agents/skills"
names = sorted(p.name for p in sk.iterdir())
print("count", len(names))
for p in sorted(sk.iterdir()):
    s = p / "SKILL.md"
    print(p.name, "dirlink" if p.is_symlink() else "dir", os.readlink(p) if p.is_symlink() else os.readlink(s), s.is_file())
pw = sk / "babysit-pr/scripts/pr-wait"
print("pr-wait exec", os.access(pw, os.X_OK), oct(pw.stat().st_mode & 0o777))
for n in ("full-send","full-stop","leaving-pr-comments","modernize"):
    print(n, (sk / n / "agents/openai.yaml").is_file())
# contract link from skill resolves
c = (sk / "council" / "../../guides/skill-execution-contract.md")
print("contract via symlink path (lexical)", os.path.exists(os.path.normpath(str(c))), "resolved", (sk/"council").resolve().joinpath("../../guides/skill-execution-contract.md").resolve().is_file())
board = (t/"docs/planning/board.yaml")
print("board", board.read_text()[:300] if board.exists() else None)
rec = json.loads((t/"docs/methodology/schema/installation.json").read_text())
print("record prov", {k: rec.get(k) for k in ("methodology_version","source_commit","source_tag","source_worktree_dirty","fixture")})
print("record has .agents", [k for k in rec["files"] if k.startswith(".agents")][:3])
print("project dir exists", (t/"docs/project").exists(), "resources", (t/"docs/resources").exists(), "evolution", (t/"docs/resources/evolution").exists())
print("AGENTS head", (t/"AGENTS.md").read_text()[:120].replace("\n"," | "))
print("pr-wait digest", __import__("hashlib").sha256(pw.read_bytes()).hexdigest())
