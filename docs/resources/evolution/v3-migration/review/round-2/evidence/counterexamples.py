from pathlib import Path
import tempfile, subprocess, os, json, sys, stat, importlib.util
import yaml
ROOT=Path('/Users/chuckrussell/Dev/gendev/methodology-v3')

def run(cwd,*args):
 p=subprocess.run(args,cwd=cwd,capture_output=True,text=True,env={**os.environ,'UV_OFFLINE':'1','GIT_OPTIONAL_LOCKS':'0'})
 return p

def inventory(root):
 return {p.relative_to(root).as_posix():('link',os.readlink(p)) if p.is_symlink() else ('dir',stat.S_IMODE(p.stat().st_mode)) if p.is_dir() else ('file',p.read_bytes(),stat.S_IMODE(p.stat().st_mode)) for p in root.rglob('*')}

with tempfile.TemporaryDirectory(prefix='v3-review-counterexamples-') as tmp:
 base=Path(tmp)
 # Independent rendering edge cases: assert initializer input is literal data.
 for i,name in enumerate(['Widget "QA"',r'Widget \tools','Literal [id] / A&B']):
  t=base/str(i);t.mkdir(); assert run(ROOT,str(ROOT/'scripts/install-methodology.sh'),str(t)).returncode==0
  p=run(t,'./scripts/init-project.sh',name)
  try:
   got=yaml.safe_load((t/'docs/project/project.yaml').read_text())['project']['name']
   print('rendering',repr(name),'initializer exit',p.returncode,'parsed name',repr(got),'literal?',name==got)
  except yaml.YAMLError as e:
   print('rendering',repr(name),'initializer exit',p.returncode,'YAML ERROR',str(e))
  if i==0:
   q=run(t,'./scripts/project-state.sh'); print('quoted-name project-state exit',q.returncode, q.stdout[-500:],q.stderr[-500:])
 # Permission/malformed metadata negative controls and exact zero writes.
 t=base/'mode';t.mkdir(); assert run(ROOT,str(ROOT/'scripts/install-methodology.sh'),str(t)).returncode==0
 record=t/'docs/methodology/schema/installation.json'; pristine=record.read_bytes()
 for val in [True,-1,4096,'0755']:
  data=json.loads(pristine); data['file_modes']['scripts/check-methodology.sh']=val; record.write_text(json.dumps(data));before=inventory(t)
  p=run(ROOT,str(ROOT/'scripts/install-methodology.sh'),'--force',str(t))
  assert p.returncode==1 and inventory(t)==before,(val,p.returncode)
  print('invalid mode',repr(val),'rejected before writes:',p.stderr.strip())
 record.write_bytes(pristine)
 for mode in [0o700,0o644]:
  f=t/'scripts/check-methodology.sh';f.chmod(mode); before=inventory(t)
  p=run(ROOT,str(ROOT/'scripts/install-methodology.sh'),'--force',str(t))
  assert p.returncode==1 and inventory(t)==before
  print('permission-only',oct(mode),'rejected with exact zero writes')
  f.chmod(0o755)
