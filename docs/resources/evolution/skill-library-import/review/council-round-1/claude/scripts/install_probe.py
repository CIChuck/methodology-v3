import sys
from pathlib import Path
repo = Path(sys.argv[1]); sys.path.insert(0, str(repo/"scripts/lib"))
sys.dont_write_bytecode=True
from distribution import source_entries
print(sys.version.split()[0])
es = source_entries(repo, False, "main")
ag = [e for e in es if e.path.startswith(".agents/skills")]
print("agents entries", len(ag))
for e in ag: print(e.path, "link" if e.link else "file", e.data.decode() if e.link else "", "owned" if e.owned else "project")
pw = [e for e in es if e.path.endswith("babysit-pr/scripts/pr-wait")]
print("pr-wait", [(e.path, oct(e.mode), e.owned) for e in pw])
oy = [e.path for e in es if e.path.endswith("openai.yaml")]
print("yaml", oy)
