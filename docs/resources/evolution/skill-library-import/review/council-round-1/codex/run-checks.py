import os, subprocess, json
from pathlib import Path
p=Path(__file__).parent
env={**os.environ,"TMPDIR":str(p/"tmp"),"PYTHONDONTWRITEBYTECODE":"1","UV_OFFLINE":"1","GIT_OPTIONAL_LOCKS":"0"}
uv="uv run --frozen --group devboard python "
commands=["./scripts/gendev-doctor.sh","./scripts/check-methodology.sh","./scripts/check-doc-coherence.sh",uv+"scripts/devboard.py validate",uv+"scripts/devboard.py next",uv+"scripts/devboard.py show skill-library-import"]
commands += [str(x) for x in sorted(Path("tests/methodology").glob("test-*.sh")) if x.name!="test-migration.sh"]
commands += [uv+"-m unittest discover -s tests/devboard -v",uv+"-m unittest discover -s tests/migration -v",uv+"scripts/exercise-v3-toolkit.py "+str(p/"exercise.json"),"python3 scripts/verify-migration-inputs.py"]
results=[]
for i,cmd in enumerate(commands):
 log=p/f"check-{i:02}.log"
 with log.open("w") as f:
  f.write("$ "+cmd+"\n"); f.flush()
  r=subprocess.run(cmd,shell=True,env=env,stdout=f,stderr=subprocess.STDOUT)
 results.append({"command":cmd,"exit":r.returncode,"log":log.name})
 p.joinpath("checks.json").write_text(json.dumps(results,indent=2))
 print(r.returncode,cmd,flush=True)
