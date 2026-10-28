from pathlib import Path
import importlib.util,sys,os,signal,json,stat,tempfile
ROOT=Path('/Users/chuckrussell/Dev/gendev/methodology-v3')
OUT=Path('/tmp/methodology-v3-review-round-1.6t7cpb')
target=Path(tempfile.mkdtemp(prefix='signal-target-',dir=OUT))
(target/'AGENTS.md').write_text('# Local instructions\n');(target/'.gitignore').write_text('state/\n')
def inventory(root):
 result={}
 for p in sorted(root.rglob('*')):
  n=str(p.relative_to(root));mode=stat.S_IMODE(p.lstat().st_mode)
  result[n]=('link',os.readlink(p),mode) if p.is_symlink() else ('directory',None,mode) if p.is_dir() else ('file',p.read_bytes().hex(),mode)
 return result
before=inventory(target)
spec=importlib.util.spec_from_file_location('distro',ROOT/'scripts/lib/distribution.py');mod=importlib.util.module_from_spec(spec);sys.modules[spec.name]=mod;spec.loader.exec_module(mod)
original=mod.os.replace
calls=0
injected=False
def replace(*args):
 global calls,injected
 original(*args);calls+=1
 if calls==4 and not injected:
  injected=True
  os.kill(os.getpid(),signal.SIGTERM)
mod.os.replace=replace
sys.argv=['distribution.py',str(ROOT),str(target),'0','0','0','1','main']
rc=mod.main()
after=inventory(target)
print('signal injected after fourth atomic replacement:',injected,'installer exit',rc,'exact inventory restored',before==after)
assert injected and rc==1 and before==after
