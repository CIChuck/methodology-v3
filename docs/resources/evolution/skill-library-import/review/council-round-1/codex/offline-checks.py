import ast, hashlib, json, os, re, stat, subprocess, tempfile
from pathlib import Path
import yaml
R=Path.cwd(); O=Path(__file__).parent; Q=O.parent
sha=lambda b:hashlib.sha256(b).hexdigest()
pins=json.loads((Q/'authority-manifest.json').read_text())
for name,pin in pins.items():
 assert sha((R/name).read_bytes())==pin['sha256'], name
 assert subprocess.check_output(['git','show',pin['revision']+':'+name])==(R/name).read_bytes(),name
print('PASS all',len(pins),'authority pins match candidate and checkout')
paths=['.agents/skills','docs/methodology/dev-skills','docs/methodology/guides/skill-execution-contract.md','scripts/create-dry-run.py','tests/migration/test_v3_toolkit.py']
diff=subprocess.check_output(['git','diff','ee82653ed6cacb9e1157cd791f12d0fb774f12af','d41e0ebfdc587ecc6d8c3ab336afc530ce90654f','--',*paths])
assert sha(diff)=='6818fab01b30764ed63cee1b214fd63b3fceed8f6a5062fcdcf450ccd4100b1c'
assert diff==(Q/'selected.diff').read_bytes()
print('PASS selected diff hash',sha(diff))
D=R/'docs/resources/evolution/skill-library-import'
inv=json.loads((D/'source-inventory.json').read_text()); manifest=json.loads((D/'import-manifest.json').read_text())
S=Path(inv['source']); actual={p.relative_to(S).as_posix() for p in S.rglob('*') if p.is_file()}
assert actual==set(inv['files'])
for name,record in inv['files'].items():
 p=S/name
 assert sha(p.read_bytes())==record['sha256'],name
 assert stat.S_IMODE(p.stat().st_mode)==record['mode'],name
assert subprocess.check_output(['git','-C',str(S),'rev-parse','HEAD'],text=True).strip()==inv['source_commit']
assert {m['source'] for m in manifest}==actual
for m in manifest:
 src=S/m['source']; dst=R/m['destination']
 assert sha(src.read_bytes())==m['source_sha256']
 assert sha(dst.read_bytes())==m['destination_sha256']
 assert (src.read_bytes()!=dst.read_bytes())==m['changed']
 assert stat.S_IMODE(src.stat().st_mode)==stat.S_IMODE(dst.stat().st_mode)
print('PASS all 14 original/import file digests, modes, inventory and source commit; 5 support files unchanged')
names={Path(m['source']).parts[0] for m in manifest}
def check(root):
 skills=list((root/'.agents/skills').glob('*/SKILL.md')); assert len(skills)==24
 for skill in skills:
  meta=yaml.safe_load(skill.read_text().split('---',2)[1]); assert meta['name']==skill.parent.name; assert isinstance(meta['description'],str) and meta['description']
 for name in names:
  folder=root/'.agents/skills'/name; assert folder.is_symlink(); assert folder.resolve()==(root/'docs/methodology/dev-skills'/name).resolve()
  for link in re.findall(r'\]\(([^)]+)\)',(folder/'SKILL.md').read_text()):
   assert (folder.resolve()/link).is_file(),(name,link)
  for ui in folder.glob('agents/*.yaml'):
   x=yaml.safe_load(ui.read_text())['interface']; assert all(isinstance(x[k],str) and x[k] for k in ['display_name','short_description','default_prompt']); assert 25<=len(x['short_description'])<=64
 helper=root/'.agents/skills/babysit-pr/scripts/pr-wait'; compile(helper.read_text(),str(helper),'exec')
 out=subprocess.check_output(['python3',str(helper),'--help'],text=True); assert 'Watch a GitHub PR' in out
 print('PASS',root,': 24 metadata entries; 9 bundles, all Markdown links, 4 UI metadata; helper syntax/help')
check(R)
with tempfile.TemporaryDirectory(dir=O/'tmp',prefix='independent-install-') as t:
 target=Path(t)
 subprocess.run([str(R/'scripts/install-methodology.sh'),str(target)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True)
 check(target)
 p=subprocess.check_output(['python3',str(target/'scripts/create-dry-run.py')],text=True).strip(); fixture=Path(p)
 check(fixture)
 assert yaml.safe_load((fixture/'docs/planning/board.yaml').read_text())['tasks']==[]
 rec=json.loads((fixture/'docs/methodology/schema/installation.json').read_text()); assert rec['fixture'] and not rec['installation_history'] and not rec['local_amendments']
 assert not (fixture/'docs/project').exists()
 print('PASS disposable exercise empty board, no inherited project, fresh provenance')
print('PASS all independent offline assertions')
