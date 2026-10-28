import os,sys,subprocess,json,time
from pathlib import Path
root=Path("/Users/chuckrussell/Dev/gendev/methodology-v3")
out=Path(__file__).parent
label=sys.argv[1];args=sys.argv[2:]
env={**os.environ,"UV_OFFLINE":"1","PYTHONDONTWRITEBYTECODE":"1","TMPDIR":str(out),"GIT_OPTIONAL_LOCKS":"0"}
start=time.time()
with (out/(label+".log")).open("w") as log:
 log.write("COMMAND: "+repr(args)+"\n");log.flush()
 result=subprocess.run(args,cwd=root,env=env,stdout=log,stderr=subprocess.STDOUT)
record={"argv":args,"cwd":str(root),"exit":result.returncode,"seconds":round(time.time()-start,2),"log":str(out/(label+".log"))}
(out/(label+".result.json")).write_text(json.dumps(record,indent=2)+"\n")
print(json.dumps(record))
