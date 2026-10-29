import sys, yaml
from pathlib import Path
ag = Path(sys.argv[1])/".agents/skills"; bad=0
for l in sorted(ag.iterdir()):
    t=(l/"SKILL.md").read_text()
    assert t.startswith("---\n"); fm=yaml.safe_load(t.split("---\n",2)[1])
    good = isinstance(fm,dict) and fm.get("name")==l.name and isinstance(fm.get("description"),str) and len(fm["description"])>=20 and len(fm["description"])<=1024
    bad += not good
    print(("PASS" if good else "FAIL"), l.name, sorted(fm), repr(fm.get("description"))[:110])
for y in sorted((ag.parent.parent/"docs/methodology/dev-skills").rglob("agents/*.yaml")):
    d=yaml.safe_load(y.read_text()); print("UI", y.parent.parent.name, d)
print("frontmatter failures:", bad); sys.exit(bad)
