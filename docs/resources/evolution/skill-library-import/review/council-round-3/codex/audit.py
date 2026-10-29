import hashlib,json,os,pathlib,re,stat,subprocess,datetime,yaml
R=pathlib.Path.cwd(); O=pathlib.Path('/var/folders/dh/wfnmsgpn1yl83xlbmc109sf40000gn/T/v3-skills-council-round3-k749snd7/codex'); C='5e2ab4047a69c82fc883735134c23527197b3c1e'; B='ee82653ed6cacb9e1157cd791f12d0fb774f12af'; D='f6de7a2e121a2bf26c0d306f7451568854c5d2d5'; V='aa25aa89762974012c0243e6134e9785f5db970d'
def git(*a): return subprocess.check_output(['git',*a])
def sha(b): return hashlib.sha256(b).hexdigest()
def prior(p,ref=V): return git('show',f'{ref}:{p}')
def mode(p,ref=C): return git('ls-tree',ref,'--',str(p)).decode().split()[0]
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'candidate':C,'base':B,'wording_base':D,'runtime_reference':V}
assert git('rev-parse','HEAD').decode().strip()==C
assert git('branch','--show-current').decode().strip()=='fix/skills-council-follow-up'
assert not git('status','--porcelain=v1','--untracked-files=all')
result['authority_manifest_sha256']=sha((O.parent/'authority-manifest.json').read_bytes())
result['authority_pins']=json.loads((O.parent/'authority-manifest.json').read_text())
for p,m in result['authority_pins'].items():
 assert m['revision']==C
 assert sha(pathlib.Path(p).read_bytes())==m['sha256']
 assert pathlib.Path(p).read_bytes()==prior(p,C)
paths=['.agents/skills','docs/methodology/dev-skills','docs/methodology/guides/skill-execution-contract.md','docs/resources/evolution/skill-library-import/import-manifest.json']
for name,base,expected in [('skills',B,'c39031a5c45b63fb344bd12c71a9e20f195fe2616590155529b93e51c89db0c9'),('wording',D,'a87b5c759d315026f296dca18fa52cb871ee4aad7ba4d6e1f238ab796aa09423')]:
 b=git('diff','--binary',base,C,'--',*paths); (O/(name+'.diff')).write_bytes(b); assert sha(b)==expected
 result[name+'_diff_sha256']=sha(b)
runtime=['scripts','tests','.github','requirements-devboard.txt','pyproject.toml','uv.lock']
b=git('diff',V,C,'--',*runtime); (O/'runtime.diff').write_bytes(b); assert not b
result['runtime_diff_bytes']=len(b)
for p in ['docs/resources/evolution/v3-migration/input-manifest.json','docs/resources/evolution/v3-migration/review/round-1/checkpoint-exception-approval.json']:
 assert prior(p)==pathlib.Path(p).read_bytes(); result[p]={'sha256':sha(prior(p)),'identical_to':V}
manifest=json.loads(pathlib.Path(paths[-1]).read_text()); source=pathlib.Path('/Users/chuckrussell/Dev/gendev/tstack/skills'); result['import']=[]
assert len(manifest)==14
assert sorted(str(p.relative_to(source)) for p in source.rglob('*') if p.is_file())==sorted(x['source'] for x in manifest)
for x in manifest:
 s=source/x['source']; d=pathlib.Path(x['destination']); sb=s.read_bytes(); db=d.read_bytes()
 assert sha(sb)==x['source_sha256'] and sha(db)==x['destination_sha256']
 assert x['changed']==(sb!=db)
 sm=stat.S_IMODE(s.stat().st_mode); dm=stat.S_IMODE(d.stat().st_mode); assert sm==dm
 assert mode(d)== ('100755' if dm&0o111 else '100644')
 if x['source']!='babysit-pr/SKILL.md' and x['source']!='full-send/SKILL.md': assert db==prior(d)
 result['import'].append({**x,'source_mode':oct(sm),'destination_mode':oct(dm)})
result['metadata']=[]; entries=list(pathlib.Path('.agents/skills').iterdir()); assert len(entries)==24
for entry in sorted(entries):
 p=entry/'SKILL.md'; text=p.read_text(); assert text.startswith('---\n'); meta=yaml.safe_load(text.split('---',2)[1]); assert meta['name']==entry.name
 assert isinstance(meta['description'],str) and meta['description'].strip()
 result['metadata'].append({'entry':str(entry),'name':meta['name'],'description':meta['description']})
new=set(x['source'].split('/')[0] for x in manifest); assert len(new)==9
result['links']=[]; result['ui']=[]
for n in sorted(new):
 entry=pathlib.Path('.agents/skills')/n; target=pathlib.Path('docs/methodology/dev-skills')/n
 assert entry.is_symlink() and entry.resolve()==target.resolve()
 assert os.readlink(entry)==f'../../docs/methodology/dev-skills/{n}'
 for rel in re.findall(r'\]\(([^)]+)\)',(entry/'SKILL.md').read_text()):
  if '://' not in rel and not rel.startswith('#'):
   assert (entry/rel.split('#')[0]).exists(),(entry,rel)
   assert (target/rel.split('#')[0]).exists()
 result['links'].append({'entry':str(entry),'target':os.readlink(entry)})
 if (entry/'agents/openai.yaml').exists():
  p=entry/'agents/openai.yaml'; ui=yaml.safe_load(p.read_text())['interface']; assert set(ui)=={'display_name','short_description','default_prompt'}
  assert all(isinstance(v,str) and v.strip() for v in ui.values()); assert '$'+n in ui['default_prompt']
  result['ui'].append({'path':str(p),'interface':ui})
assert len(result['ui'])==4
assert (pathlib.Path('.agents/skills/babysit-pr/scripts/pr-wait')).is_file()
old=git('ls-tree','-r',B,'--','.agents/skills','docs/methodology/dev-skills').decode().splitlines()
for line in old:
 meta,p=line.split('\t'); now=git('ls-tree',C,'--',p).decode().strip(); assert now==line,(p,now,line)
result['preexisting_skill_tree_entries_preserved']=len(old)
a=pathlib.Path('docs/resources/practitioner-guide'); h=pathlib.Path('docs/resources/practitioner-guide-html/content')
files=sorted(p.name for p in a.iterdir() if p.is_file()); assert len(files)==23 and files==sorted(p.name for p in h.iterdir() if p.is_file())
result['guide_mirror']=[]
for n in files:
 p=a/n; q=h/n; assert p.read_bytes()==q.read_bytes()==prior(p)==prior(q)
 result['guide_mirror'].append({'filename':n,'sha256':sha(p.read_bytes())})
assert not git('status','--porcelain=v1','--untracked-files=all')
assert git('rev-parse','HEAD').decode().strip()==C
(O/'audit.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS authority/diff pins; runtime diff empty; frozen manifest/exception unchanged; all 14 source/destination hashes and modes; 24 metadata; nine whole-folder links/resources; four UI; five support unchanged; existing skill entries unchanged; exact 23-file guide mirror unchanged; clean candidate')
