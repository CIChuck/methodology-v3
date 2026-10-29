import subprocess,os,pathlib,json,datetime
out=pathlib.Path('/var/folders/dh/wfnmsgpn1yl83xlbmc109sf40000gn/T/v3-skills-council-round4-lk4zdm_d/codex')
os.environ.update(UV_OFFLINE='1',PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(out/'tmp'))
commands=[['./scripts/gendev-doctor.sh'],['./scripts/check-methodology.sh'],['./scripts/check-doc-coherence.sh']]+[['uv','run','--frozen','--group','devboard','python','scripts/devboard.py',*args] for args in [('validate',),('next',),('show','skill-library-import')]]+[['python3','scripts/verify-migration-inputs.py'],['gh','pr','create','--help']]
results=[]
for i,c in enumerate(commands):
 p=subprocess.run(c,cwd='/Users/chuckrussell/Dev/gendev/methodology-v3',text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 (out/f'check-{i}.log').write_text('$ '+ ' '.join(c)+'\n'+p.stdout+f'\nEXIT {p.returncode}\n')
 results.append({'command':c,'exit':p.returncode,'log':f'check-{i}.log'})
 print(i,p.returncode,p.stdout[-700:],flush=True)
 if i==0 and p.returncode: break
(out/'commands.json').write_text(json.dumps(results,indent=2))
