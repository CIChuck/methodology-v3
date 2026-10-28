from __future__ import annotations
import os,sys,json,stat,hashlib,subprocess,shutil
from pathlib import Path
ROOT=Path('/Users/chuckrussell/Dev/gendev/methodology-v3'); OUT=Path(__file__).parent
ENV={**os.environ,'UV_OFFLINE':'1','PYTHONDONTWRITEBYTECODE':'1','TMPDIR':str(OUT),'GIT_OPTIONAL_LOCKS':'0'}
commands=[]
def run(cwd,*args,expected=None,env=None):
 r=subprocess.run(args,cwd=cwd,capture_output=True,text=True,env={**ENV,**(env or {})})
 commands.append({'cwd':str(cwd),'argv':list(args),'exit':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
 if expected is not None and r.returncode!=expected:raise RuntimeError((args,r.returncode,r.stdout,r.stderr))
 return r
def inventory(root):
 result={}
 for p in root.rglob('*'):
  name=str(p.relative_to(root))
  if p.is_symlink():result[name]=('link',os.readlink(p))
  elif p.is_file():result[name]=('file',hashlib.sha256(p.read_bytes()).hexdigest(),stat.S_IMODE(p.stat().st_mode))
  elif p.is_dir():result[name]=('dir',stat.S_IMODE(p.stat().st_mode))
 return result

def exercise(cwd,label):
 before=inventory(cwd)
 guide=(ROOT/'docs/methodology/guides/orchestration-validation.md').read_text()
 recipe=guide.split('```bash\n',1)[1].split('```',1)[0]
 r=run(cwd,'bash','-e','-c',recipe+'\nprintf "REVIEW_FIXTURE=%s\\n" "$PWD"\n',expected=0)
 fixture=Path(next(s.split('=',1)[1] for s in r.stdout.splitlines() if s.startswith('REVIEW_FIXTURE=')))
 assert inventory(cwd)==before
 r=run(fixture,'./scripts/gendev-doctor.sh',expected=0);assert 'Integrity: verified' in r.stdout
 run(fixture,sys.executable,'scripts/devboard.py','validate',expected=0)
 assert run(fixture,sys.executable,'scripts/devboard.py','next',expected=0).stdout.strip()=='NO_OPEN_TASK'
 r=run(fixture,'./scripts/check-methodology.sh',expected=1)
 errors=[s for s in r.stdout.splitlines() if s.startswith('ERROR:')]
 assert len(errors)==1 and 'GENDEV-MANIFEST-ENFORCEMENT-002' in errors[0] and 'required_attester' in errors[0]
 manifest=__import__('yaml').safe_load((fixture/'docs/project/project.yaml').read_text())
 assert manifest['approvals']['current_gate']['gate']=='G1' and manifest['approvals']['current_gate']['status']=='pending'
 record=json.loads((fixture/'docs/methodology/schema/installation.json').read_text())
 assert record['fixture'] and record['source_commit']=='6ca2ad10f7eb0c71b9a316d458a20ad667c21c4b'
 assert record['installation_history']==[] and record['local_amendments']==[]
 assert all(not (fixture/p).exists() for p in ['.git','.env','runtime','docs/planning/active/live-only','docs/methodology/local-secret.env'])
 assert len(list((fixture/'.agents/skills').glob('*/SKILL.md')))==15
 for seed in (ROOT/'docs/project-template/dry-run-policies').glob('*.md'):assert (fixture/'docs/policies'/seed.name).read_bytes()==seed.read_bytes()
 assert all(b'REVIEW LIVE ONLY' not in p.read_bytes() for p in fixture.rglob('*') if p.is_file())
 print('PASS complete documented fresh setup:',label,fixture)
 return fixture

# Actual frozen source: no source edits, capture its full inventory before/after.
source_fixture=exercise(ROOT,'frozen methodology source')
product=OUT/'initialized-installed-source';product.mkdir()
run(ROOT,'./scripts/install-methodology.sh',str(product),expected=0)
name='Review "QA" O\'Brien \\ [Project Name] [id] / A&B Café'
run(product,'./scripts/init-project.sh',name,expected=0)
run(product,'./scripts/init-phase.sh','2',name,expected=0)
manifest=__import__('yaml').safe_load((product/'docs/project/project.yaml').read_text());assert manifest['project']['name']==name
for phase in ['1','2']:
 directive=(product/f'docs/project/build-plan/phases/phase-{phase}-construction-directive.md').read_text()
 assert name in directive and f'Position: G5.{phase}.3' in directive
for rel in ['.env','docs/methodology/local-secret.env','docs/policies/local-only.env','runtime/session.txt','docs/planning/active/live-only/README.md']:
 p=product/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text('REVIEW LIVE ONLY\n')
for rel in ['AGENTS.md','docs/policies/repository-engineering-policy.md']:
 p=product/rel;p.write_text(p.read_text()+'\nREVIEW LIVE ONLY\n')
installed_fixture=exercise(product,'initialized installed product with local state')

# Excluded surfaces: a canonical baseline remains integrity-valid while project-owned
# discovery can legitimately reference an external local skill.
external=OUT/'external-private-skill.md';external.write_text('---\nname: private\ndescription: REVIEW LIVE ONLY\n---\n')
link=product/'.agents/skills/private/SKILL.md';link.parent.mkdir();link.symlink_to(external)
before=inventory(product);run(product,'./scripts/gendev-doctor.sh',expected=0)
r=run(product,sys.executable,'scripts/create-dry-run.py');assert inventory(product)==before
print('OBSERVATION excluded external discovery link:',r.returncode,r.stderr.strip())
link.unlink();link.parent.rmdir()
for rel in ['AGENTS.md','.agents/skills','docs/policies']:
 path=product/rel;held=OUT/('held-'+rel.replace('/','-'));path.rename(held)
 before=inventory(product);run(product,'./scripts/gendev-doctor.sh',expected=0)
 r=run(product,sys.executable,'scripts/create-dry-run.py');assert inventory(product)==before
 print('OBSERVATION excluded project-owned surface absent:',rel,r.returncode,r.stderr.strip())
 held.rename(path)

# Verify fail-closed invalid path/mode/amendment records and overlapping source/target.
record_path=product/'docs/methodology/schema/installation.json';original=record_path.read_bytes()
for label, mutate in [
 ('traversal ownership',lambda r:r['files'].update({'../outside':'0'*64})),
 ('boolean mode',lambda r:r['file_modes'].update({'scripts/check-methodology.sh':True})),
 ('malformed amendment',lambda r:r.update(local_amendments=[{'files':[]}]))]:
 rec=json.loads(original);mutate(rec);record_path.write_text(json.dumps(rec));before=inventory(product)
 r=run(ROOT,'./scripts/install-methodology.sh','--force',str(product),expected=1)
 assert inventory(product)==before
 print('PASS no writes on',label, r.stderr.strip().splitlines()[-1])
 record_path.write_bytes(original)

# SIGINT, SIGTERM, SIGHUP injection at the first and final replace via the real main.
probe=OUT/'signal_probe.py'
probe.write_text('''import os,sys,importlib.util,signal\nfrom pathlib import Path\nsrc=Path(sys.argv[1]);target=Path(sys.argv[2]);sig=int(sys.argv[3]);at=sys.argv[4]\nspec=importlib.util.spec_from_file_location("probe_distribution",src/"scripts/lib/distribution.py")\nm=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)\nreplace=m.os.replace;fired=False\ndef inject(srcpath,dst):\n global fired\n replace(srcpath,dst)\n if not fired and (at=="first" or str(dst).endswith("/docs/methodology/schema/installation.json")):\n  fired=True;os.kill(os.getpid(),sig)\nm.os.replace=inject\nsys.argv=[str(src/"scripts/lib/distribution.py"),str(src),str(target),"0","0","0","1","main"]\nraise SystemExit(m.main())\n''')
for sig in [2,15,1]:
 for at in ['first','last']:
  target=OUT/f'signal-{sig}-{at}';target.mkdir();(target/'AGENTS.md').write_text('# Local review fixture\n');(target/'.gitignore').write_text('local-runtime/\n')
  before=inventory(target);run(ROOT,sys.executable,str(probe),str(ROOT),str(target),str(sig),at,expected=1)
  assert inventory(target)==before
  print('PASS exact rollback after signal',sig,at)
(OUT/'counterexamples-commands.json').write_text(json.dumps(commands,indent=2)+'\n')
print('COUNTEREXAMPLES COMPLETE')
