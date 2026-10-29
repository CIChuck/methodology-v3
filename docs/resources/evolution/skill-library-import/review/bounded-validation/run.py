from pathlib import Path
import os,subprocess,json,sys
out=Path(__file__).parent
commands=[['./scripts/gendev-doctor.sh'],['./scripts/check-methodology.sh'],['./scripts/check-doc-coherence.sh'],['uv','run','--frozen','--group','devboard','python','scripts/devboard.py','validate'],['uv','run','--frozen','--group','devboard','python','scripts/devboard.py','next'],['uv','run','--frozen','--group','devboard','python','scripts/devboard.py','show','skill-library-import'],['./scripts/test-methodology.sh'],['uv','run','--frozen','--group','devboard','python','-m','unittest','discover','-s','tests/devboard','-v'],['uv','run','--frozen','--group','devboard','python','-m','unittest','discover','-s','tests/migration','-v'],['uv','run','--frozen','--group','devboard','python','scripts/exercise-v3-toolkit.py',str(out/'experiments.json')],['python3','scripts/verify-migration-inputs.py'],['uv','run','--frozen','--group','devboard','python',str(out/'offline-checks.py')]]
results=[]
for i,args in enumerate(commands):
 log=out/f'check-{i:02d}.log'
 with log.open('w') as f:
  p=subprocess.run(args,stdout=f,stderr=subprocess.STDOUT,env={**os.environ,'UV_OFFLINE':'1','PYTHONDONTWRITEBYTECODE':'1','TMPDIR':str(out/'tmp')})
 results.append({'command':args,'exit':p.returncode,'log':log.name})
 print(i,p.returncode,' '.join(args),flush=True)
(out/'checks.json').write_text(json.dumps(results,indent=2)+'\n')
sys.exit(any(r['exit'] for r in results))
