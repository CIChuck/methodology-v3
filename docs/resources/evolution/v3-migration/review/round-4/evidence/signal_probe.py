import os,sys,importlib.util,signal
from pathlib import Path
src=Path(sys.argv[1]);target=Path(sys.argv[2]);sig=int(sys.argv[3]);at=sys.argv[4]
spec=importlib.util.spec_from_file_location("probe_distribution",src/"scripts/lib/distribution.py")
m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
replace=m.os.replace;fired=False
def inject(srcpath,dst):
 global fired
 replace(srcpath,dst)
 if not fired and (at=="first" or str(dst).endswith("/docs/methodology/schema/installation.json")):
  fired=True;os.kill(os.getpid(),sig)
m.os.replace=inject
sys.argv=[str(src/"scripts/lib/distribution.py"),str(src),str(target),"0","0","0","1","main"]
raise SystemExit(m.main())
