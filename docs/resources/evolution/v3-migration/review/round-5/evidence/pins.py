import hashlib,json,os,pathlib,subprocess,sys
ROOT=pathlib.Path('/Users/chuckrussell/Dev/gendev/methodology-v3'); OUT=pathlib.Path('/tmp/v3-independent-round5.x5446H')
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT,env={**os.environ,'GIT_OPTIONAL_LOCKS':'0'},text=True).strip()
request=pathlib.Path('/Users/chuckrussell/Dev/gendev/methodology-v3-recovery/review/round-5')
auth=json.loads((request/'authority-manifest.json').read_text()); checks={}
for name,pin in auth.items():
 blob=subprocess.check_output(['git','show',pin['revision']+':'+name],cwd=ROOT)
 sha=hashlib.sha256(blob).hexdigest(); assert sha==pin['sha256']; assert (ROOT/name).read_bytes()==blob
 checks[name]={**pin,'verified':True}
assert git('rev-parse','HEAD')=='98f8bec4597cd3307fc26e5c28dc86592e01ca08'
assert git('rev-parse','refs/review/v3/round-5')==git('rev-parse','HEAD')
assert git('status','--porcelain=v1','--untracked-files=all')==''
refs=git('for-each-ref','--format=%(refname) %(objectname)'); names=git('ls-files','-z').split('\0'); inv={}
for n in names:
 if n:
  p=ROOT/n; inv[n]={'mode':p.lstat().st_mode,'sha256':hashlib.sha256(os.fsencode(os.readlink(p)) if p.is_symlink() else p.read_bytes()).hexdigest()}
state={'head':git('rev-parse','HEAD'),'branch':git('branch','--show-current'),'status':git('status','--porcelain=v1','--untracked-files=all'),'refs':refs,'tracked_inventory':inv}
(OUT/(sys.argv[1]+'-state.json')).write_text(json.dumps(state,indent=2)+'\n')
(OUT/'authority-check.json').write_text(json.dumps(checks,indent=2)+'\n')
manifest=json.loads((ROOT/'docs/resources/evolution/v3-migration/input-manifest.json').read_text()); old=manifest['sources']['methodology-v2']; checked=[]
for line in old['refs'].splitlines():
 name,oid=line.split(); archived='refs/archive/v2/'+name.removeprefix('refs/'); assert git('rev-parse',archived)==oid
 assert subprocess.run(['git','cat-file','-e',oid],cwd=ROOT).returncode==0
 if name.startswith(('refs/heads/','refs/tags/')):assert git('rev-parse',name)==oid
 checked.append({'original':name,'archived':archived,'oid':oid})
assert git('remote')==''; gitdir=pathlib.Path(git('rev-parse','--absolute-git-dir'))
assert not (gitdir/'objects/info/alternates').exists(); assert not gitdir.is_symlink()
original=pathlib.Path(old['path'])/'.git'; assert not os.path.samefile(gitdir,original)
# Independent loose-object storage must not hardlink the source's objects.
shared=[]
for p in (gitdir/'objects').glob('*/*'):
 q=original/'objects'/p.relative_to(gitdir/'objects')
 if p.is_file() and q.is_file() and os.path.samefile(p,q):shared.append(str(p))
assert not shared
archives={}
for label,s in manifest['sources'].items():
 p=ROOT.parent/'methodology-v3-recovery'/s['archive']; assert hashlib.sha256(p.read_bytes()).hexdigest()==s['archive_sha256']; archives[label]=str(p)
p=ROOT.parent/'methodology-v3-recovery/methodology-v2.bundle'; assert hashlib.sha256(p.read_bytes()).hexdigest()==manifest['bundle_sha256']
bundle=subprocess.run(['git','bundle','verify',str(p)],cwd=ROOT,capture_output=True,text=True); assert bundle.returncode==0
promoted=json.loads((ROOT/'docs/resources/evolution/v3-migration/promoted-amendments.json').read_text())
for name,sha in promoted['promoted_files'].items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==sha
skills=[]
for p in sorted((ROOT/'.agents/skills').glob('*/SKILL.md')):
 assert p.is_symlink() and p.resolve().is_relative_to(ROOT/'docs/methodology/dev-skills') and p.is_file(); skills.append(str(p.relative_to(ROOT)))
assert len(skills)==15
r={'archived_refs':checked,'archive_paths':archives,'bundle_verification':bundle.stdout+bundle.stderr,'remotes':git('remote'),'alternates':False,'independent_storage':True,'promoted_files':promoted['promoted_files'],'canonical_skill_links':skills,'diff_stat':git('diff','--shortstat',old['head'],'HEAD')}
(OUT/'history-and-skills.json').write_text(json.dumps(r,indent=2)+'\n')
print('PASS authority hashes, frozen candidate, clean state, 21 archived refs/local heads/tags, recovery archives/bundle, independent objects, no remotes/alternates, 6 promoted canonical hashes, 15 skills')
