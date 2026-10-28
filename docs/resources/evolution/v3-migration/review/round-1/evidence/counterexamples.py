from pathlib import Path
import os, subprocess, json, stat, shutil, sys, importlib.util, tempfile
ROOT=Path('/Users/chuckrussell/Dev/gendev/methodology-v3')
OUT=Path('/tmp/methodology-v3-review-round-1.6t7cpb')
TARGET=Path(tempfile.mkdtemp(prefix='mode-target-',dir=OUT))
env={**os.environ,'UV_OFFLINE':'1','PYTHONDONTWRITEBYTECODE':'1','GIT_OPTIONAL_LOCKS':'0'}
def install(*args):
 p=subprocess.run([str(ROOT/'scripts/install-methodology.sh'),*args,str(TARGET)],capture_output=True,text=True,env=env)
 return p
p=install();assert p.returncode==0,p.stderr
managed=TARGET/'scripts/check-methodology.sh'
managed.chmod(0o700)
before=stat.S_IMODE(managed.stat().st_mode)
p=install('--force')
after=stat.S_IMODE(managed.stat().st_mode)
print('mode-only customization:',oct(before),'->',oct(after),'installer exit',p.returncode)
print('mode-only preflight rejected?',p.returncode!=0)
assert p.returncode==0 and after==0o755
print('seed task project line:',next(x for x in (TARGET/'docs/planning/task-template.md').read_text().splitlines() if x.startswith('Project:')))
# A one-pass token substitution should preserve literal bracket tokens supplied by a user.
p=subprocess.run([str(TARGET/'scripts/init-project.sh'),'Literal [id] / A&B'],capture_output=True,text=True,env=env)
assert p.returncode==0,p.stderr
p=subprocess.run([str(TARGET/'scripts/init-phase.sh'),'2','Literal [id] / A&B'],capture_output=True,text=True,env=env)
assert p.returncode==0,p.stderr
for phase in (1,2):
 d=(TARGET/f'docs/project/build-plan/phases/phase-{phase}-construction-directive.md').read_text()
 assert 'Literal [id] / A&B' in d
 assert f'Position: G5.{phase}.3' in d
print('literal bracket tokens, slash and ampersand in initial/later directives: PASS')
# Import the primary verifier and capture its own source reads, without additional original-repo operations.
spec=importlib.util.spec_from_file_location('verify',ROOT/'scripts/verify-migration-inputs.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
orig=m.subprocess.check_output; observed=[]
def capture(argv,*a,**k):
 result=orig(argv,*a,**k)
 if 'for-each-ref' in argv: observed.append({'source':str(k['cwd']),'refs':result})
 return result
m.subprocess.check_output=capture;sys.argv=[str(ROOT/'scripts/verify-migration-inputs.py')]
rc=m.main(); print('preservation verifier exit',rc)
frozen=json.loads((ROOT/'docs/resources/evolution/v3-migration/input-manifest.json').read_text())
for record in observed:
 old=next(v['refs'] for v in frozen['sources'].values() if v['path']==record['source']);before=set(old.splitlines());now=set(record['refs'].splitlines());print(record['source'],'added=',sorted(now-before),'removed=',sorted(before-now))
