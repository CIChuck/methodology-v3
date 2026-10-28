import hashlib,importlib.util,json,os,pathlib,shutil,signal,stat,subprocess,sys,tempfile
from unittest.mock import patch
from run import ROOT,OUT,ENV
import yaml
BASE=OUT/'fixtures'/'boundary'; BASE.mkdir(exist_ok=True)
commands=[]
def run(cwd,*argv,expected=0):
 p=subprocess.run(argv,cwd=cwd,env=ENV,capture_output=True,text=True)
 commands.append({'cwd':str(cwd),'argv':argv,'actual':p.returncode,'expected':expected,'stdout':p.stdout,'stderr':p.stderr})
 assert p.returncode==expected,(argv,p.returncode,p.stdout,p.stderr)
 return p

def inventory(root):
 return {str(p.relative_to(root)):(stat.S_IMODE(p.lstat().st_mode),'link',os.readlink(p)) if p.is_symlink() else (stat.S_IMODE(p.stat().st_mode),'directory','') if p.is_dir() else (stat.S_IMODE(p.stat().st_mode),'file',hashlib.sha256(p.read_bytes()).hexdigest()) for p in sorted(root.rglob('*'))}

def install(name):
 p=BASE/name; p.mkdir(); run(ROOT,str(ROOT/'scripts/install-methodology.sh'),str(p)); run(p,'./scripts/init-project.sh','Independent Synthetic Source'); return p

marker=b'SYNTHETIC-EXCLUDED-BOUNDARY-MARKER-ROUND5'
external=BASE/'external'; external.mkdir(); (external/'private.txt').write_bytes(marker)
results=[]
for case in ['ordinary','AGENTS.md','.agents/skills','docs/policies','extras']:
 source=install(case.replace('/','_')); excluded=[]
 (source/'.env').write_bytes(marker); (source/'runtime').mkdir(); (source/'runtime/session.txt').write_bytes(marker)
 (source/'docs/planning/active/live-task').mkdir(); (source/'docs/planning/active/live-task/README.md').write_bytes(marker)
 if case in ['AGENTS.md','.agents/skills','docs/policies']:
  p=source/case; shutil.rmtree(p) if p.is_dir() else p.unlink()
 if case=='extras':
  for parent in ['docs/methodology','docs/project-template','docs/project-template/planning','docs/project-template/dry-run-policies','tests/methodology','tests/devboard','scripts/lib','docs/gendev-licenses']:
   p=source/parent; p.mkdir(parents=True,exist_ok=True)
   (p/'unowned.txt').write_bytes(marker); (p/'unowned-link').symlink_to(external/'private.txt'); (p/'unowned-dir-link').symlink_to(external,target_is_directory=True)
   (p/'unowned-directory').mkdir(); (p/'unowned-directory/child.txt').write_bytes(marker)
   excluded.extend([p/'unowned.txt',p/'unowned-link',p/'unowned-dir-link',p/'unowned-directory'])
  p=source/'.agents/skills/private/SKILL.md'; p.parent.mkdir(); p.symlink_to(external/'private.txt'); excluded.append(p)
 before=inventory(source); outside=inventory(external)
 fixture=pathlib.Path(run(source,sys.executable,'-B','scripts/create-dry-run.py').stdout.strip())
 run(fixture,'./scripts/init-project.sh','Independent Fresh Exercise')
 doctor=run(fixture,'./scripts/gendev-doctor.sh'); assert 'Integrity: verified' in doctor.stdout
 run(fixture,sys.executable,'-B','scripts/devboard.py','validate'); assert run(fixture,sys.executable,'-B','scripts/devboard.py','next').stdout.strip()=='NO_OPEN_TASK'
 checker=run(fixture,'./scripts/check-methodology.sh',expected=1); errors=[s for s in checker.stdout.splitlines() if s.startswith('ERROR:')]; assert len(errors)==1 and 'GENDEV-MANIFEST-ENFORCEMENT-002' in errors[0]
 rec=json.loads((fixture/'docs/methodology/schema/installation.json').read_text()); origin=json.loads((source/'docs/methodology/schema/installation.json').read_text())
 assert rec['fixture'] and rec['source_commit']==origin['source_commit'] and rec['source_tag']==origin['source_tag'] and rec['methodology_version']==origin['methodology_version']
 assert not rec['installation_history'] and not rec['local_amendments'] and rec['distribution_candidate']['status']=='unreleased'
 skills=list((fixture/'.agents/skills').glob('*/SKILL.md')); assert len(skills)==15 and all(p.is_symlink() and p.is_file() for p in skills)
 for p in (ROOT/'docs/project-template/dry-run-policies').glob('*.md'):assert (fixture/'docs/policies'/p.name).read_bytes()==p.read_bytes()
 for p in fixture.rglob('*'):
  if p.is_file(): assert marker not in p.read_bytes(),p
 assert not (fixture/'.env').exists() and not (fixture/'runtime').exists() and not (fixture/'.git').exists()
 data=yaml.safe_load((fixture/'docs/project/project.yaml').read_text()); assert data['approvals']['current_gate']['gate']=='G1' and data['approvals']['current_gate']['status']=='pending'
 assert not yaml.safe_load((fixture/'docs/planning/board.yaml').read_text())['tasks']
 assert inventory(source)==before and inventory(external)==outside
 results.append({'case':case,'result':'PASS','input_entries_preserved':len(before),'fixture':str(fixture),'checker_errors':errors})
 print('PASS fresh installed-source boundary',case,flush=True)
 # Independently instrument the shared selector to forbid any tree traversal,
 # and any content read/metadata call on excluded project or unknown paths.
 if case=='extras':
  sys.path.insert(0,str(source/'scripts/lib')); import distribution as d
  allowed=set(origin['files']); original_read=pathlib.Path.read_bytes; original_text=pathlib.Path.read_text
  forbidden=[source/'AGENTS.md',source/'docs/policies',source/'.agents',*excluded]
  def guard(p):
   assert not any(p==x or p.is_relative_to(x) for x in forbidden),f'excluded path touched: {p}'
  def read(p,*a,**kw):guard(p);return original_read(p,*a,**kw)
  def text(p,*a,**kw):guard(p);return original_text(p,*a,**kw)
  with patch.object(pathlib.Path,'rglob',side_effect=AssertionError('source traversal attempted')),patch.object(pathlib.Path,'read_bytes',read),patch.object(pathlib.Path,'read_text',text):
   selected=d.source_entries(source,False,'master',owned_only=True,allowed_paths=allowed)
  assert all(e.owned and e.path in allowed for e in selected)
  results.append({'case':'instrumented-preselection','result':'PASS','selected_owned_entries':len(selected),'no_rglob':True,'no_excluded_content_reads':True})
# Refusal before output and preservation: changed/missing/unsafe selected files.
for case in ['changed','missing','symlink','parent-symlink']:
 source=install('unsafe-'+case); owned=source/'docs/methodology/templates/architecture-template.md'
 if case=='changed':owned.write_bytes(owned.read_bytes()+b'changed')
 if case=='missing':owned.unlink()
 if case=='symlink':owned.unlink();owned.symlink_to(external/'private.txt')
 if case=='parent-symlink':
  p=source/'docs/methodology/templates'; shutil.move(p,BASE/'moved-templates');p.symlink_to(BASE/'moved-templates',target_is_directory=True)
 before=inventory(source); result=run(source,sys.executable,'-B','scripts/create-dry-run.py',expected=1); assert not result.stdout and inventory(source)==before
 results.append({'case':'owned-'+case,'result':'PASS','error':result.stderr.strip()});print('PASS refused selected owned',case,flush=True)
# Normal installer default must still inspect/exclude unsafe external source links.
source=install('normal-source');p=source/'.agents/skills/private/SKILL.md';p.parent.mkdir();p.symlink_to(external/'private.txt')
target=BASE/'normal-target';target.mkdir(); before=inventory(target); source_before=inventory(source)
r=run(source,str(source/'scripts/install-methodology.sh'),str(target),expected=1);assert 'external source symlink' in r.stderr and inventory(target)==before and inventory(source)==source_before
results.append({'case':'normal-installer-external-link','result':'PASS','error':r.stderr.strip()})
(OUT/'boundaries-results.json').write_text(json.dumps(results,indent=2)+'\n');(OUT/'boundaries-commands.json').write_text(json.dumps(commands,indent=2)+'\n')
print('PASS',len(results),'independent boundary probes')
