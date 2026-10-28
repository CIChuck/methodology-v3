import importlib.util,os,pathlib,signal,sys
sys.dont_write_bytecode=True
source,target,kind=sys.argv[1:]
sys.path.insert(0,str(pathlib.Path(source)/'scripts/lib'))
import distribution as d
original=d.os.replace; fired=False

def replace(src,dst):
 global fired
 original(src,dst)
 if not fired and str(dst).endswith('/'+d.RECORD):
  fired=True;os.kill(os.getpid(),getattr(signal,kind))
d.os.replace=replace
sys.argv=['distribution.py',source,target,'1','0','0','1','main']
raise SystemExit(d.main())
