from pathlib import Path
import tempfile,subprocess,tarfile,io,os
import yaml
ROOT=Path('/Users/chuckrussell/Dev/gendev/methodology-v3')
with tempfile.TemporaryDirectory(prefix='v3-review-base-rendering-') as tmp:
 root=Path(tmp)
 raw=subprocess.check_output(['git','archive','54f0de27f2b59fdcc54e4f57bb9f73dc92843f4a'],cwd=ROOT)
 with tarfile.open(fileobj=io.BytesIO(raw)) as t:t.extractall(root,filter='data')
 name='Widget "QA"'
 p=subprocess.run(['./scripts/init-project.sh',name],cwd=root,text=True,capture_output=True)
 print('base initializer exit',p.returncode)
 try: print(yaml.safe_load((root/'docs/project/project.yaml').read_text())['project']['name'])
 except yaml.YAMLError as e:print('base YAML ERROR',e)
