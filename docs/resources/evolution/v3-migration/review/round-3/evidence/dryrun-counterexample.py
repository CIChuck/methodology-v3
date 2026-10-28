import pathlib, subprocess, os, sys
root=pathlib.Path('/Users/chuckrussell/Dev/gendev/methodology-v3')
guide=(root/'docs/methodology/guides/orchestration-validation.md').read_text()
commands=guide.split('OptionsNonexistent',1)[0].split('+++Nonexistent',1)[0] if False else guide.split('bash\n',1)[1].split(chr(96)*3,1)[0]
# Preserve the copied fixture for the lead to inspect; output remains outside governed files.
r=subprocess.run(['bash','-e','-c',commands+'\nprintf "FIXTURE=%s\\n" "$PWD"\n'],cwd=root,capture_output=True,text=True,env={**os.environ,'TMPDIR':'/tmp/v3-round3-review.DruBam'})
print('documented setup rc',r.returncode); print(r.stdout); print(r.stderr)
fixture=pathlib.Path(next(x.split('=',1)[1] for x in r.stdout.splitlines() if x.startswith('FIXTURE=')))
for name in ('docs/policies/repository-engineering-policy.md','docs/policies/development-task-lifecycle.md','docs/policies/independent-validation-policy.md','docs/policies/dev-board-integration.md','docs/planning/board.yaml','docs/planning/board.schema.json','requirements-devboard.txt','.agents/skills/independent-code-validator/SKILL.md'):
 print(name,'PRESENT' if (fixture/name).exists() else 'MISSING')
for command in ([sys.executable,'scripts/devboard.py','validate'],['./scripts/gendev-doctor.sh'],['./scripts/check-methodology.sh']):
 r=subprocess.run(command,cwd=fixture,capture_output=True,text=True,env={**os.environ,'UV_OFFLINE':'1'})
 print('COMMAND',command,'RC',r.returncode); print(r.stdout); print(r.stderr)
