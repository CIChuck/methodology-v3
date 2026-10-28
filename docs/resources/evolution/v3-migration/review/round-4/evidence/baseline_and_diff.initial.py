import io,tarfile,subprocess,json,os
from pathlib import Path
ROOT=Path('/Users/chuckrussell/Dev/gendev/methodology-v3');OUT=Path(__file__).parent;BASE='54f0de27f2b59fdcc54e4f57bb9f73dc92843f4a';CAND='6ca2ad10f7eb0c71b9a316d458a20ad667c21c4b'
fixture=OUT/'baseline-attester';fixture.mkdir()
with tarfile.open(fileobj=io.BytesIO(subprocess.check_output(['git','archive',BASE],cwd=ROOT))) as arc:arc.extractall(fixture,filter='data')
commands=[]
for args,expected in [(['./scripts/init-project.sh','Baseline Preapproval Fixture'],0),(['./scripts/check-methodology.sh'],1)]:
 r=subprocess.run(args,cwd=fixture,env={**os.environ,'TMPDIR':str(OUT),'GIT_OPTIONAL_LOCKS':'0'},capture_output=True,text=True);assert r.returncode==expected
 commands.append({'argv':args,'cwd':str(fixture),'exit':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
 if args[0].endswith('check-methodology.sh'):
  errors=[line for line in r.stdout.splitlines() if line.startswith('ERROR:')];assert len(errors)==1 and 'GENDEV-MANIFEST-ENFORCEMENT-002' in errors[0]
print('PASS inherited base independently reproduces sole missing required_attester preapproval error')
paths=subprocess.check_output(['git','diff','--name-only',BASE,CAND],cwd=ROOT,text=True).splitlines()
# Raw historical reports/logs are not current behavior evidence.
raw=[p for p in paths if p.endswith(('.log','.diff','.tar.gz')) or '/evidence/' in p or '/remediation-evidence/' in p]
active=[p for p in paths if p not in raw]
r=subprocess.run(['git','diff','--check',BASE,CAND,'--',*active],cwd=ROOT,capture_output=True,text=True);assert r.returncode==0,(r.stdout,r.stderr)
print('PASS git diff --check for',len(active),'non-raw changed paths;',len(raw),'raw evidence/archive paths classified separately')
(OUT/'baseline-and-diff.json').write_text(json.dumps({'baseline_commands':commands,'active_changed_paths':active,'raw_evidence_paths':raw,'nonraw_diff_check_exit':r.returncode},indent=2)+'\n')
