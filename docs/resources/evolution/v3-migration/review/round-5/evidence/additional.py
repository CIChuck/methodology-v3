import contextlib,hashlib,json,os,pathlib,shutil,stat,subprocess,sys
from unittest.mock import patch
from run import ROOT,OUT,ENV
BASE=OUT/'fixtures/additional';BASE.mkdir(exist_ok=True)
commands=[];results=[]
def run(cwd,*argv,expected=0):
 p=subprocess.run(argv,cwd=cwd,env=ENV,capture_output=True,text=True);commands.append({'cwd':str(cwd),'argv':argv,'actual':p.returncode,'expected':expected,'stdout':p.stdout,'stderr':p.stderr});assert p.returncode==expected,(argv,p.returncode,p.stdout,p.stderr);return p

def inv(root):
 return {str(p.relative_to(root)):(stat.S_IMODE(p.lstat().st_mode),'link',os.readlink(p)) if p.is_symlink() else (stat.S_IMODE(p.stat().st_mode),'dir','') if p.is_dir() else (stat.S_IMODE(p.stat().st_mode),'file',hashlib.sha256(p.read_bytes()).hexdigest()) for p in root.rglob('*')}
source=OUT/'fixtures/boundary/extras';rec=json.loads((source/'docs/methodology/schema/installation.json').read_text())
sys.path.insert(0,str(ROOT/'scripts/lib'));import distribution as d
forbidden=[source/'AGENTS.md',source/'docs/policies',source/'.agents']
def guard(p):
 if p.is_relative_to(source):
  rel=p.relative_to(source)
  assert not any(part.startswith('unowned') for part in rel.parts),('unowned inspected',str(p))
  assert not any(p==x or p.is_relative_to(x) for x in forbidden),('project surface inspected',str(p))
def wrap(original):
 def wrapped(p,*args,**kwargs):guard(p);return original(p,*args,**kwargs)
 return wrapped
with contextlib.ExitStack() as stack:
 stack.enter_context(patch.object(pathlib.Path,'rglob',side_effect=AssertionError('source traversal')))
 for name in ['stat','lstat','exists','is_dir','is_file','is_symlink','read_bytes','read_text','open','resolve']:
  stack.enter_context(patch.object(pathlib.Path,name,wrap(getattr(pathlib.Path,name))))
 selected=d.source_entries(source,False,'master',owned_only=True,allowed_paths=set(rec['files']))
results.append({'probe':'preselection-metadata-and-content-guards','result':'PASS','selected_entries':len(selected),'guarded_methods':['rglob','stat','lstat','exists','is_dir','is_file','is_symlink','read_bytes','read_text','open','resolve']})
print('PASS preselection before excluded metadata/traversal/content operations',flush=True)
incoming=BASE/'incoming';shutil.copytree(ROOT,incoming,symlinks=True,ignore=shutil.ignore_patterns('.git','.venv','.tmp','__pycache__'))
(incoming/'docs/methodology/templates/architecture-template.md').write_text((incoming/'docs/methodology/templates/architecture-template.md').read_text()+'\nIndependent incoming upgrade fixture.\n')
for mode in ['fresh','upgrade']:
 for sig in ['SIGINT','SIGTERM','SIGHUP']:
  target=BASE/(mode+'-'+sig);target.mkdir();(target/'AGENTS.md').write_text('# Private fixture instructions\n');(target/'.gitignore').write_text('private-runtime/\n')
  if mode=='upgrade':
   run(ROOT,str(ROOT/'scripts/install-methodology.sh'),'--integrate-agents',str(target));run(target,'./scripts/init-project.sh','Independent Signal Fixture')
   (target/'docs/policies/local.md').write_text('# preserved local policy\n')
  before=inv(target);r=run(ROOT,sys.executable,'-B',str(OUT/'signal-child.py'),str(incoming),str(target),sig,expected=1)
  assert inv(target)==before,('rollback mismatch',mode,sig)
  assert ('interrupted by signal' in r.stderr if sig!='SIGINT' else 'blocked:' in r.stderr)
  results.append({'probe':'metadata-write-interrupt-rollback','mode':mode,'signal':sig,'result':'PASS','entries_preserved':len(before),'stderr':r.stderr.strip()})
  print('PASS signal rollback',mode,sig,flush=True)
# Execute documented standalone command using cached packages and disposable env.
fixture=BASE/'standalone';fixture.mkdir();run(ROOT,str(ROOT/'scripts/install-methodology.sh'),str(fixture));run(fixture,'uv','run','--no-project','--with-requirements','requirements-devboard.txt','python','scripts/devboard.py','validate')
results.append({'probe':'documented-standalone-board-command-offline','result':'PASS'})
(OUT/'additional-results.json').write_text(json.dumps(results,indent=2)+'\n');(OUT/'additional-commands.json').write_text(json.dumps(commands,indent=2)+'\n')
