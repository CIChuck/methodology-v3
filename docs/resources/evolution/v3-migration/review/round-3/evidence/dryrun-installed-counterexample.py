import pathlib,subprocess,tempfile,os,json,hashlib,sys
root=pathlib.Path('/Users/chuckrussell/Dev/gendev/methodology-v3'); output=pathlib.Path('/tmp/v3-round3-review.DruBam')
def command(cwd,args):
 r=subprocess.run(args,cwd=cwd,capture_output=True,text=True,env={**os.environ,'UV_OFFLINE':'1','TMPDIR':str(output)})
 print('COMMAND',args,'RC',r.returncode); print(r.stdout[-900:]); print(r.stderr[-3000:]); return r
source=output/'initialized-product'; source.mkdir()
assert command(root,[str(root/'scripts/install-methodology.sh'),str(source)]).returncode==0
assert command(source,['./scripts/init-project.sh','Existing Product']).returncode==0
before={str(p.relative_to(source)):p.read_bytes() for p in (source/'docs/project').rglob('*') if p.is_file()}
guide=(root/'docs/methodology/guides/orchestration-validation.md').read_text(); commands=guide.split('bash\n',1)[1].split(chr(96)*3,1)[0]
r=command(source,['bash','-e','-c',commands+'\nprintf "FIXTURE=%s\\n" "$PWD"\n']); assert r.returncode==0
copy=pathlib.Path(next(x.split('=',1)[1] for x in r.stdout.splitlines() if x.startswith('FIXTURE=')))
assert before=={str(p.relative_to(source)):p.read_bytes() for p in (source/'docs/project').rglob('*') if p.is_file()}
print('PASS live initialized authority preserved')
for args in (['./scripts/gendev-doctor.sh'],['./scripts/check-methodology.sh'],[sys.executable,'scripts/devboard.py','validate']): command(copy,args)
# Compare the inherited source baseline procedure to separate the pre-approval error.
baseline=output/'baseline'; baseline.mkdir()
archive=subprocess.check_output(['git','archive','54f0de27f2b59fdcc54e4f57bb9f73dc92843f4a'],cwd=root)
subprocess.run(['tar','-xf','-','-C',str(baseline)],input=archive,check=True)
assert command(baseline,['./scripts/init-project.sh','Baseline Product']).returncode==0
command(baseline,['./scripts/check-methodology.sh'])
