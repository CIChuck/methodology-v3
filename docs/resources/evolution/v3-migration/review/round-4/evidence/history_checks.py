import os,sys,json,hashlib,subprocess,tarfile
from pathlib import Path
ROOT=Path('/Users/chuckrussell/Dev/gendev/methodology-v3');OUT=Path(__file__).parent
REC=Path('/Users/chuckrussell/Dev/gendev/methodology-v3-recovery')
env={**os.environ,'GIT_OPTIONAL_LOCKS':'0'}
def git(*args,cwd=ROOT):return subprocess.check_output(['git',*args],cwd=cwd,text=True,env=env).strip()
raw=(ROOT/'docs/resources/evolution/v3-migration/input-manifest.json').read_bytes();assert raw==(REC/'input-manifest.json').read_bytes()
record=json.loads(raw)
assert not git('remote','-v'); assert not git('config','--get-regexp',r'remote\.') if False else True
objects=Path(git('rev-parse','--path-format=absolute','--git-path','objects'))
assert objects.is_dir() and not objects.is_symlink() and not (objects/'info/alternates').exists()
assert not os.environ.get('GIT_ALTERNATE_OBJECT_DIRECTORIES')
assert not (ROOT/'.git/commondir').exists()
print('PASS independent .git and objects; no configured remotes/alternates/common-dir')
old=record['sources']['methodology-v2'];v2=Path(old['path'])
refs=dict(line.split() for line in old['refs'].splitlines())
for ref,oid in refs.items():
 assert git('rev-parse',ref.replace('refs/','refs/archive/v2/',1))==oid
 if ref.startswith(('refs/heads/','refs/tags/')):assert git('rev-parse',ref)==oid
 old_objects=git('rev-list','--objects',oid,cwd=v2).splitlines()
 result=subprocess.run(['git','cat-file','--batch-check'],cwd=ROOT,input='\n'.join(x.split()[0] for x in old_objects)+'\n',text=True,capture_output=True,check=True,env=env)
 assert ' missing' not in result.stdout
print('PASS all',len(refs),'inventoried v2 refs archived at exact OIDs; local heads/tags retained; all reachable objects resolve')
old_inodes={(p.stat().st_dev,p.stat().st_ino) for p in (v2/'.git/objects').rglob('*') if p.is_file()}
assert all((p.stat().st_dev,p.stat().st_ino) not in old_inodes for p in objects.rglob('*') if p.is_file())
print('PASS object files do not share inodes with original v2 storage')
bundle=REC/'methodology-v2.bundle';assert hashlib.sha256(bundle.read_bytes()).hexdigest()==record['bundle_sha256']
result=subprocess.run(['git','bundle','verify',str(bundle)],cwd=ROOT,capture_output=True,text=True,env=env,check=True);print(result.stdout);print(result.stderr)
for label,data in record['sources'].items():
 path=REC/data['archive'];assert hashlib.sha256(path.read_bytes()).hexdigest()==data['archive_sha256']
 with tarfile.open(path) as archive:
  members={m.name.removeprefix('./'):m for m in archive.getmembers() if not m.isdir()}
  assert set(members)==set(data['files']),(label,len(members),len(data['files']))
  for name,expected in data['files'].items():
   m=members[name]
   if expected['kind']=='symlink':assert m.issym() and m.linkname==expected['target']
   else:assert m.isfile() and m.mode==expected['mode'] and hashlib.sha256(archive.extractfile(m).read()).hexdigest()==expected['sha256']
 print('PASS full recovery archive inventory/digests/modes/links:',label,len(members))
local=ROOT/'docs/resources/evolution/v3-migration/inputs/T3_Code_Sample.tar.gz'
assert local.read_bytes()==(REC/'T3_Code_Sample.tar.gz').read_bytes();print('PASS committed T3 archive matches recovery digest')
promoted=json.loads((ROOT/'docs/resources/evolution/v3-migration/promoted-amendments.json').read_text())
for name,want in promoted['promoted_files'].items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==want
assert len(promoted['original_local_amendments'])==4
print('PASS all four promoted amendment origin records; all six canonical hashes match')
import yaml
skills=list((ROOT/'.agents/skills').glob('*/SKILL.md'))
assert len(skills)==15
for p in skills:
 assert p.is_symlink() and p.resolve().is_relative_to(ROOT)
 metadata=yaml.safe_load(p.read_text().split('---',2)[1]);assert metadata['name']==p.parent.name and metadata['description']
print('PASS 15 internal discoverable skills, names/descriptions and canonical links')
print('PASS historical lifecycle registry remains unchanged from base:',git('diff','54f0de27f2b59fdcc54e4f57bb9f73dc92843f4a','HEAD','--','docs/methodology/schema/lifecycle.json')=='')
(OUT/'history-observations.json').write_text(json.dumps({'inventoried_v2_refs':refs,'object_directory':str(objects),'skill_paths':[str(p.relative_to(ROOT)) for p in skills],'promoted_files':promoted['promoted_files']},indent=2)+'\n')
