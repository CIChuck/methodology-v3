import hashlib,json,os,pathlib,subprocess
from run import ROOT,OUT,run
BASE='54f0de27f2b59fdcc54e4f57bb9f73dc92843f4a'; CANDIDATE='98f8bec4597cd3307fc26e5c28dc86592e01ca08'
raw=subprocess.check_output(['git','diff','--no-ext-diff','--binary',BASE,CANDIDATE],cwd=ROOT)
changed=subprocess.check_output(['git','diff','--name-only',BASE,CANDIDATE],cwd=ROOT,text=True).splitlines();items=[]
for name in changed:
 p=ROOT/name
 group='primary implementation and portable guidance'
 if name.startswith('docs/resources/evolution/v3-migration/'):
  group='historical review/self-check evidence or frozen input inventory'
  if name.endswith(('README.md','review-scope.md','human-disposition.md','remediation-directive.md','checkpoint-exception-approval.json')):group='migration authority and human dispositions'
 if p.is_symlink():sha=hashlib.sha256(os.fsencode(os.readlink(p))).hexdigest();size=len(os.fsencode(os.readlink(p)))
 elif p.is_file():sha=hashlib.sha256(p.read_bytes()).hexdigest();size=p.stat().st_size
 else:sha=None;size=None
 items.append({'path':name,'classification':group,'sha256':sha,'size':size})
check=subprocess.run(['git','diff','--check',BASE,CANDIDATE],cwd=ROOT,capture_output=True,text=True)
(OUT/'diff-check.log').write_text(check.stdout+check.stderr)
paths=[]
for line in check.stdout.splitlines():
 if ': trailing whitespace.' in line or ': new blank line at EOF.' in line:paths.append(line.rsplit(':',2)[0])
assert check.returncode in [0,2]
assert all(p.startswith('docs/resources/evolution/v3-migration/') and ('/evidence/' in p or '/remediation-evidence/' in p or '/validation/' in p or p.endswith('v2-copy-tests.log')) for p in paths),paths
assert json.loads((OUT/'initial-state.json').read_text())==json.loads((OUT/'final-state.json').read_text())
manifest=json.loads((ROOT/'docs/resources/evolution/v3-migration/input-manifest.json').read_text())
v2=manifest['sources']['methodology-v2'];actual=subprocess.check_output(['git','rev-parse','HEAD'],cwd=v2['path'],text=True).strip();assert actual==v2['head']
r={'base':BASE,'candidate':CANDIDATE,'full_binary_diff_sha256':hashlib.sha256(raw).hexdigest(),'changed_paths':items,'whitespace_exit':check.returncode,'whitespace_paths':sorted(set(paths)),'initial_equals_final_candidate':True,'v2_original_head':actual}
(OUT/'diff-audit.json').write_text(json.dumps(r,indent=2)+'\n');print('PASS',len(items),'changed paths inventoried; complete diff hash',r['full_binary_diff_sha256'],'whitespace only historical raw evidence; candidate tracked bytes/modes/refs unchanged')
run('final-preservation',['python3','-B','scripts/verify-migration-inputs.py'])
