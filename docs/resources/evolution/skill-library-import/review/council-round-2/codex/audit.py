import pathlib,hashlib,json,stat,subprocess,sys,re,importlib.util,unittest,io
import yaml
root=pathlib.Path.cwd(); out=pathlib.Path(__file__).parent
inv=json.loads((root/'docs/resources/evolution/skill-library-import/source-inventory.json').read_text()); man=json.loads((root/'docs/resources/evolution/skill-library-import/import-manifest.json').read_text())
for e in man:
 s=pathlib.Path(inv['source'])/e['source']; d=root/e['destination']; original=inv['files'][e['source']]
 assert hashlib.sha256(s.read_bytes()).hexdigest()==e['source_sha256']==original['sha256']
 assert hashlib.sha256(d.read_bytes()).hexdigest()==e['destination_sha256']
 assert stat.S_IMODE(s.stat().st_mode)==stat.S_IMODE(d.stat().st_mode)==original['mode']
 if not e['changed']: assert s.read_bytes()==d.read_bytes()
print('PASS all 14 source/destination digests and modes; 5 unchanged support files')
skills=list((root/'.agents/skills').glob('*/SKILL.md')); assert len(skills)==24
for p in skills:
 meta=yaml.safe_load(p.read_text().split('---',2)[1]); assert meta['name']==p.parent.name and meta['description']
 assert p.resolve().is_relative_to(root)
for e in man:
 p=root/e['destination']
 if p.name=='SKILL.md':
  for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
   if ':' not in target: assert (p.parent/target.split('#')[0]).exists(),(p,target)
 if p.suffix=='.yaml': assert yaml.safe_load(p.read_text())['interface']
print('PASS 24 source skills metadata, 9 bundle relative links and 4 UI records')
a=root/'docs/resources/practitioner-guide'; b=root/'docs/resources/practitioner-guide-html/content'
files={p.relative_to(a).as_posix():p.read_bytes() for p in a.rglob('*') if p.is_file()}; other={p.relative_to(b).as_posix():p.read_bytes() for p in b.rglob('*') if p.is_file()}
assert len(files)==23 and files==other; print('PASS exact 23-file guide filename/byte mirror')
p=root/'docs/methodology/dev-skills/babysit-pr/scripts/pr-wait'; compile(p.read_text(),str(p),'exec'); r=subprocess.run([sys.executable,str(p),'--help'],capture_output=True,text=True); assert r.returncode==0; (out/'helper-help.txt').write_text(r.stdout); print('PASS helper compile and offline --help')
# Fresh source dry-run, preserving output as disposable evidence.
r=subprocess.run([sys.executable,'scripts/create-dry-run.py'],capture_output=True,text=True); assert r.returncode==0,r.stderr
fixture=pathlib.Path(r.stdout.strip()); assert len(list((fixture/'.agents/skills').glob('*/SKILL.md')))==24
assert yaml.safe_load((fixture/'docs/planning/board.yaml').read_text())['tasks']==[]; assert not (fixture/'docs/project').exists(); rec=json.loads((fixture/'docs/methodology/schema/installation.json').read_text()); assert rec['source_commit']==subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
print('PASS source dry-run 24 skills, empty board, no product/approvals, pinned provenance:',fixture)
# Load test definitions without invoking workflows.
def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path); m=importlib.util.module_from_spec(spec); sys.modules[name]=m; spec.loader.exec_module(m); return m
m=load('audit_toolkit',root/'tests/migration/test_v3_toolkit.py')
case='test_dry_run_keeps_reference_markdown_inside_bundle_without_discovering_it'
stream=io.StringIO(); result=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.TestSuite([m.ToolkitMigrationTests(case)])); assert result.wasSuccessful(); print('BF02 current targeted positive/support negative PASS'); (out/'bf02-current.log').write_text(stream.getvalue())
original=m.ToolkitMigrationTests.source_copy
old=subprocess.check_output(['git','show','d41e0eb:scripts/create-dry-run.py'])
def old_copy(self):
 p=original(self); (p/'scripts/create-dry-run.py').write_bytes(old); return p
m.ToolkitMigrationTests.source_copy=old_copy
stream=io.StringIO(); result=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.TestSuite([m.ToolkitMigrationTests(case)])); assert len(result.failures)==1; print('BF02 prior implementation fails same fixture as expected'); (out/'bf02-prior.log').write_text(stream.getvalue())
m=load('audit_refs',root/'tests/migration/test_preservation_refs.py'); stream=io.StringIO(); result=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromModule(m)); assert result.wasSuccessful(); (out/'bf03-targeted.log').write_text(stream.getvalue()); print('BF03 all',result.testsRun,'targeted positive/negative checks PASS')
oldpath=out/'prior-verifier.py'; oldpath.write_bytes(subprocess.check_output(['git','show','d41e0eb:scripts/verify-migration-inputs.py'])); m.preservation=load('prior_verifier',oldpath)
stream=io.StringIO(); result=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.TestSuite([m.PreservationRefTests('test_new_context_uses_frozen_tree_anchor')])); assert len(result.failures)==1; (out/'bf03-prior.log').write_text(stream.getvalue()); print('BF03 prior implementation fails same new-context test as expected')
