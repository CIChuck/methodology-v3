import hashlib, json, os, pathlib, signal, stat, subprocess, sys, tempfile
import yaml
ROOT=pathlib.Path('/Users/chuckrussell/Dev/gendev/methodology-v3')

def inventory(root):
 result={}
 for p in root.rglob('*'):
  n=str(p.relative_to(root))
  if p.is_symlink(): result[n]=('link',os.readlink(p))
  elif p.is_dir(): result[n]=('dir',stat.S_IMODE(p.stat().st_mode))
  else: result[n]=('file',p.read_bytes(),stat.S_IMODE(p.stat().st_mode))
 return result

def run(*args,cwd=ROOT):
 return subprocess.run(args,cwd=cwd,capture_output=True,text=True,env={**os.environ,'UV_OFFLINE':'1'})
with tempfile.TemporaryDirectory(prefix='v3-independent-') as tmp:
 target=pathlib.Path(tmp)/'target'; target.mkdir()
 (target/'AGENTS.md').write_text('# Local instructions\n')
 (target/'.gitignore').write_text('runtime/\n')
 before=inventory(target)
 for sig in (signal.SIGINT,signal.SIGTERM,signal.SIGHUP):
  wrapper='''import os,runpy,signal,sys
original=os.replace
fired=False
def replace(src,dst):
 global fired
 original(src,dst)
 if str(dst).endswith('docs/methodology/schema/installation.json') and not fired:
  fired=True
  os.kill(os.getpid(),int(sys.argv[1]))
os.replace=replace
sys.argv=[str(sys.argv[2]),*sys.argv[3:]]
runpy.run_path(sys.argv[0],run_name='__main__')
'''
  r=run(sys.executable,'-c',wrapper,str(sig),str(ROOT/'scripts/lib/distribution.py'),str(ROOT),str(target),'0','0','0','1','main')
  assert r.returncode==1,(sig,r.stdout,r.stderr)
  assert inventory(target)==before,sig
  print('PASS caught interrupt restores full target after final metadata write:',sig.name)
 r=run(str(ROOT/'scripts/install-methodology.sh'),'--integrate-agents',str(target)); assert r.returncode==0,r.stderr
 name='Alpha "QA" O\'Brien \\ path [Project Name] [YYYY-MM-DD] / A&B café 💡'
 r=run('./scripts/init-project.sh',name,cwd=target); assert r.returncode==0,r.stderr
 m=yaml.safe_load((target/'docs/project/project.yaml').read_text()); assert m['project']['name']==name
 for phase in ('1','2'):
  if phase=='2': assert run('./scripts/init-phase.sh',phase,name,cwd=target).returncode==0
  text=(target/f'docs/project/build-plan/phases/phase-{phase}-construction-directive.md').read_text()
  assert name in text and f'Position: G5.{phase}.3' in text
  assert f'phase-{phase}-tactical-implementation-plan.md' in text
 print('PASS combined quotes/backslash/unicode/scaffold tokens round-trip YAML and literal Markdown through initial/later directives')
 before=inventory(target/'docs/project')
 for name in ('\n','Alpha\u2028Beta','Alpha\x85Beta','\t','   '):
  r=run('./scripts/init-project.sh','--force',name,cwd=target); assert r.returncode==2,r.stderr
  assert inventory(target/'docs/project')==before
 print('PASS all independent invalid --force names refused before replacement')
 record=target/'docs/methodology/schema/installation.json'
 data=json.loads(record.read_text()); data['file_modes']['unknown/file']=420; record.write_text(json.dumps(data))
 before=inventory(target)
 r=run(str(ROOT/'scripts/install-methodology.sh'),'--force','--integrate-agents',str(target)); assert r.returncode==1 and 'permission ownership' in r.stderr,r.stderr
 assert inventory(target)==before
 print('PASS orphan permission-ownership metadata refused with zero writes')
print('PASS all independent counterexamples')
