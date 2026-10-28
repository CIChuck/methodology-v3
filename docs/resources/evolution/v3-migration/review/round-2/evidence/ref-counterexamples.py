from pathlib import Path
import tempfile,subprocess,os,importlib.util
ROOT=Path('/Users/chuckrussell/Dev/gendev/methodology-v3')
spec=importlib.util.spec_from_file_location('preservation',ROOT/'scripts/verify-migration-inputs.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
with tempfile.TemporaryDirectory(prefix='v3-review-refs-') as temp:
 root=Path(temp); prefix='refs/t3/orchestration-v2/checkpoints/fixture/ordinal/'
 def git(*args, data=None, email='t3code@users.noreply.github.com'):
  return subprocess.check_output(['git',*args],cwd=root,input=data,text=True,env={**os.environ,'GIT_AUTHOR_NAME':'T3 Code','GIT_AUTHOR_EMAIL':email,'GIT_COMMITTER_NAME':'T3 Code','GIT_COMMITTER_EMAIL':email}).strip()
 git('init','-q');(root/'x').write_text('x');git('add','x');tree=git('write-tree')
 def commit(ref,subject=None,email='t3code@users.noreply.github.com'):
  oid=git('commit-tree',tree,data=(subject or 't3 checkpoint ref='+ref)+'\n',email=email);git('update-ref',ref,oid);return oid
 commit(prefix+'5'); frozen=git('for-each-ref','--format=%(refname) %(objectname)')
 for label,ref,subject,email in [('higher',prefix+'6',None,'t3code@users.noreply.github.com'),('lower',prefix+'4',None,'t3code@users.noreply.github.com'),('equal_numeric',prefix+'05',None,'t3code@users.noreply.github.com'),('wrong_subject',prefix+'7','different','t3code@users.noreply.github.com'),('wrong_email',prefix+'8',None,'other@example.invalid')]:
  commit(ref,subject,email);errors,allowed=mod.compare_refs(root,frozen,git('for-each-ref','--format=%(refname) %(objectname)'),allow_identical_t3_checkpoints=True)
  assert (not errors and len(allowed)==1) if label=='higher' else (errors and not allowed),(label,errors,allowed)
  print(label,'allowed' if allowed else 'rejected',errors);git('update-ref','-d',ref)
 blob=git('hash-object','-w','x');git('update-ref',prefix+'9',blob)
 errors,allowed=mod.compare_refs(root,frozen,git('for-each-ref','--format=%(refname) %(objectname)'),allow_identical_t3_checkpoints=True);assert errors and not allowed
 print('non-commit rejected',errors)
