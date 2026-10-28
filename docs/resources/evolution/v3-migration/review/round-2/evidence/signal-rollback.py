from pathlib import Path
import tempfile,subprocess,os,stat,json,sys
ROOT=Path('/Users/chuckrussell/Dev/gendev/methodology-v3')
def snapshot(root):
 return {p.relative_to(root).as_posix():('symlink',os.readlink(p)) if p.is_symlink() else ('dir',stat.S_IMODE(p.stat().st_mode)) if p.is_dir() else ('file',p.read_bytes(),stat.S_IMODE(p.stat().st_mode)) for p in root.rglob('*')}
wrapper='''import os,signal,runpy,sys
orig=os.replace
count=0
def replace(*args,**kw):
 global count
 result=orig(*args,**kw)
 count+=1
 if count==100: os.kill(os.getpid(),signal.SIGTERM)
 return result
os.replace=replace
sys.argv=sys.argv[1:]
runpy.run_path(sys.argv[0],run_name="__main__")
'''
with tempfile.TemporaryDirectory(prefix='v3-review-signal-') as temp:
 root=Path(temp)
 (root/'AGENTS.md').write_text('# Existing project instructions\n')
 (root/'.gitignore').write_text('local-runtime/\n')
 before=snapshot(root)
 p=subprocess.run([sys.executable,'-B','-c',wrapper,str(ROOT/'scripts/lib/distribution.py'),str(ROOT),str(root),'0','0','0','1','main'],capture_output=True,text=True)
 assert p.returncode==1 and "installation interrupted by signal 15" in p.stderr,p.stderr
 assert snapshot(root)==before
 print('SIGTERM after 100 real per-file replacements: installer exit 1; exact file/mode/link/directory state restored')
 print(p.stderr.strip())
