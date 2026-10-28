import concurrent.futures,hashlib,json,os,pathlib,subprocess,time
ROOT=pathlib.Path('/Users/chuckrussell/Dev/gendev/methodology-v3')
OUT=pathlib.Path('/tmp/v3-independent-round5.x5446H')
ENV={**os.environ,'UV_OFFLINE':'1','GIT_OPTIONAL_LOCKS':'0','PYTHONDONTWRITEBYTECODE':'1','TMPDIR':str(OUT/'fixtures')}
(OUT/'fixtures').mkdir(exist_ok=True)
def run(name,argv,cwd=ROOT,expected=0):
 t=time.time(); p=subprocess.run(argv,cwd=cwd,env=ENV,capture_output=True,text=True)
 (OUT/(name+'.log')).write_text(p.stdout+p.stderr)
 r={'argv':argv,'cwd':str(cwd),'returncode':p.returncode,'expected':expected,'seconds':round(time.time()-t,3)}
 (OUT/(name+'.result.json')).write_text(json.dumps(r,indent=2)+'\n'); print(name,r,flush=True); return r
if __name__=='__main__':
 uv=['uv','run','--frozen','--group','devboard','python','-B']
 jobs=[('doctor',['./scripts/gendev-doctor.sh']),('checker',['./scripts/check-methodology.sh']),('board-validate',uv+['scripts/devboard.py','validate']),('board-next',uv+['scripts/devboard.py','next']),('board-show',uv+['scripts/devboard.py','show','v3-baseline-migration']),('full-suite',['./scripts/test-methodology.sh','--suite','all']),('board-tests',uv+['-m','unittest','discover','-s','tests/devboard','-v']),('migration-tests',uv+['-m','unittest','discover','-s','tests/migration','-v']),('replay',uv+['scripts/exercise-v3-toolkit.py',str(OUT/'experiments.json')]),('preservation',['python3','-B','scripts/verify-migration-inputs.py']),('fsck',['git','fsck','--full','--connectivity-only'])]
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
  list(ex.map(lambda p:run(*p),jobs))
