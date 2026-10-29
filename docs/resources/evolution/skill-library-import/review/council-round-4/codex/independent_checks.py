import os,pathlib,json,hashlib,stat,subprocess,re,ast,datetime,yaml
R=pathlib.Path('/Users/chuckrussell/Dev/gendev/methodology-v3'); O=pathlib.Path('/var/folders/dh/wfnmsgpn1yl83xlbmc109sf40000gn/T/v3-skills-council-round4-lk4zdm_d/codex'); Q=O.parent
os.environ.update(UV_OFFLINE='1',PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(O/'tmp'),GIT_OPTIONAL_LOCKS='0')
C='464cdec246996ebf5bc769174b22a4c62f82305e'; B='8abacf4b4b4a6d005cba3bdb92a68c9ce5d81376'; T='aa25aa89762974012c0243e6134e9785f5db970d'
def git(*a): return subprocess.check_output(['git',*a],cwd=R)
def sha(b): return hashlib.sha256(b).hexdigest()
def check(ok,msg):
 print(('PASS ' if ok else 'FAIL ')+msg,flush=True)
 if not ok: raise AssertionError(msg)
check(git('rev-parse','HEAD').decode().strip()==C,'HEAD pin')
check(git('branch','--show-current').decode().strip()=='fix/skills-council-follow-up','branch pin')
check(not git('status','--porcelain=v1'),'entry governed tree clean')
(O/'entry-state.txt').write_bytes(git('status','--porcelain=v1')+git('rev-parse','HEAD')+git('branch','--show-current'))
check(sha((Q/'request.md').read_bytes())=='45ea65467f403ba9ce791f1fdb0cfeb06579f697db64e6331aae211e42ce5472','request digest')
a=json.loads((Q/'authority-manifest.json').read_text())
for p,v in a.items():
 check(v['revision']==C and sha(git('show',C+':'+p))==v['sha256'] and sha((R/p).read_bytes())==v['sha256'],'authority '+p)
(O/'authority-manifest.json').write_text(json.dumps(a,indent=2))
paths=['docs/methodology/dev-skills/'+s+'/SKILL.md' for s in ['babysit-pr','file-pr','sol-loop','full-send','full-stop']]+['docs/resources/evolution/skill-library-import/import-manifest.json']
d=git('diff','--binary',B,C,'--',*paths); (O/'clarifications.diff').write_bytes(d)
check(sha(d)=='996a382e99702ce05055fe6b517847c609eb329052df9edcbd5b1ec165aa0731','exact clarification diff digest')
check(d==(Q/'clarifications.diff').read_bytes(),'adjacent diff byte equality')
changed=git('diff','--name-only',B,C).decode().splitlines(); (O/'delta-files.txt').write_text('\n'.join(changed)+'\n')
assets=[p for p in changed if p.startswith(('docs/methodology/dev-skills/','.agents/','scripts/','tests/','.github/'))]
check(set(assets)==set(paths[:-1]),'only five changed executable/skill assets since delta base')
rd=git('diff',T,C,'--','scripts','tests','.github','requirements-devboard.txt','pyproject.toml','uv.lock');(O/'runtime.diff').write_bytes(rd)
check(not rd,'runtime diff empty')
for p in ['docs/resources/evolution/v3-migration/input-manifest.json','docs/resources/evolution/v3-migration/review/round-1/checkpoint-exception-approval.json']:
 check(git('show',T+':'+p)==(R/p).read_bytes(),'frozen record unchanged '+p)
inv=json.loads((R/'docs/resources/evolution/skill-library-import/source-inventory.json').read_text()); src=pathlib.Path(inv['source']); imp=json.loads((R/'docs/resources/evolution/skill-library-import/import-manifest.json').read_text())
check(len(inv['files'])==len(imp)==14,'14 source/import records')
check(subprocess.check_output(['git','rev-parse','HEAD'],cwd=src).decode().strip()==inv['source_commit'],'source HEAD unchanged')
check(not subprocess.check_output(['git','status','--porcelain=v1'],cwd=src),'source tree clean')
for e in imp:
 p=e['source']; s=src/p; dst=R/e['destination']; mode=stat.S_IMODE(s.stat().st_mode)
 check(sha(s.read_bytes())==inv['files'][p]['sha256']==e['source_sha256'] and mode==inv['files'][p]['mode'],'source bytes/mode '+p)
 check(sha(dst.read_bytes())==e['destination_sha256'] and stat.S_IMODE(dst.stat().st_mode)==mode,'import bytes/mode '+p)
 if not e['changed']:
  check(dst.read_bytes()==s.read_bytes()==git('show',T+':'+e['destination']),'support byte equality source/runtime '+p)
  check(git('ls-tree',T,'--',e['destination']).split()[0].decode()==format(dst.stat().st_mode & 0o177777,'o'),'support runtime mode '+p)
entries=sorted((R/'.agents/skills').glob('*/SKILL.md')); check(len(entries)==24,'24 discovery entrypoints')
for p in entries:
 t=p.read_text(); fm=yaml.safe_load(t.split('---',2)[1]);check(fm.get('name')==p.parent.name and isinstance(fm.get('description'),str) and bool(fm['description'].strip()),'metadata '+p.parent.name)
 # Resolve actual canonical-file links, excluding URLs and templated examples.
 for link in re.findall(r'\]\(([^)]+)\)',t):
  target=link.split('#')[0]
  if not target or '://' in target or any(x in target for x in '<>{} '): continue
  if target.startswith(('./','../')):
   check((p.resolve().parent/target).exists(),'relative resource '+p.parent.name+':'+target)
for s in sorted({e['source'].split('/')[0] for e in imp}):
 p=R/'.agents/skills'/s; check(p.is_symlink() and p.resolve()==R/'docs/methodology/dev-skills'/s,'whole-bundle discovery '+s)
for p in sorted((R/'docs/methodology/dev-skills').glob('*/agents/openai.yaml')):
 v=yaml.safe_load(p.read_text());check(all(isinstance(v['interface'].get(k),str) and v['interface'][k] for k in ['display_name','short_description','default_prompt']),'UI YAML '+str(p.relative_to(R)))
p=R/'docs/methodology/dev-skills/babysit-pr/scripts/pr-wait'; text=p.read_text(); ast.parse(text,filename=str(p)); compile(text,str(p),'exec');check(True,'helper ast.parse and compile in memory')
r=subprocess.run(['python3',str(p),'--help'],cwd=R,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(O/'helper-help.log').write_text(r.stdout+'\nEXIT '+str(r.returncode));check(r.returncode==0,'helper --help only')
g=R/'docs/resources/practitioner-guide'; m=R/'docs/resources/practitioner-guide-html/content'; gf={p.name:p for p in g.glob('*.md')};mf={p.name:p for p in m.glob('*.md')};check(len(gf)==len(mf)==23 and gf.keys()==mf.keys(),'exact 23-file guide inventory')
for n,p in sorted(gf.items()):check(p.read_bytes()==mf[n].read_bytes(),'guide mirror '+n)
check(not git('diff',T,C,'--','docs/resources/practitioner-guide','docs/resources/practitioner-guide-html'),'entire guide/HTML unchanged since runtime reference')
# Save numbered primary text, not earlier reviewers or builder assertions.
primary=list(a)+paths[:-1]+['docs/methodology/dev-skills/'+s+'/SKILL.md' for s in ['modernize','takeover','leaving-pr-comments']]
with (O/'primary-evidence.txt').open('w') as f:
 for p in dict.fromkeys(primary):
  f.write('\n===== '+p+' @ '+C+' =====\n')
  for i,line in enumerate((R/p).read_text().splitlines(),1):f.write(f'{i:4}: {line}\n')
check(not git('status','--porcelain=v1') and git('rev-parse','HEAD').decode().strip()==C,'exit candidate clean/pinned')
(O/'exit-state.txt').write_bytes(git('status','--porcelain=v1')+git('rev-parse','HEAD')+git('branch','--show-current'))
print('ALL INDEPENDENT CHECKS PASSED '+datetime.datetime.now(datetime.timezone.utc).isoformat())
