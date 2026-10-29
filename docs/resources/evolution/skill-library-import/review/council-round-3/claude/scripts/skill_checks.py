import json, hashlib, os, re, subprocess, sys
from pathlib import Path
root=Path('.').resolve(); src=Path('/Users/chuckrussell/Dev/gendev/tstack/skills')
C='5e2ab4047a69c82fc883735134c23527197b3c1e'; AA='aa25aa89762974012c0243e6134e9785f5db970d'; EE='ee82653ed6cacb9e1157cd791f12d0fb774f12af'
def h(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def gitblob(rev,p):
    r=subprocess.run(['git','show',f'{rev}:{p}'],capture_output=True); return r.stdout if r.returncode==0 else None
fail=0
man=json.load(open('docs/resources/evolution/skill-library-import/import-manifest.json'))
print('manifest entries',len(man))
for e in man:
    s=src/e['source']; d=root/e['destination']
    sh=h(s); dh=h(d); sm=oct(s.stat().st_mode&0o777); dm=oct(d.stat().st_mode&0o777)
    gm=subprocess.run(['git','ls-files','-s',e['destination']],capture_output=True,text=True).stdout.split()[0]
    ok = sh==e['source_sha256'] and dh==e['destination_sha256'] and ((sh!=dh)==e['changed'])
    fail+= not ok
    print('OK ' if ok else 'BAD', e['destination'], 'src_mode',sm,'dst_mode',dm,'git_mode',gm, 'changed',e['changed'])
# source tree: every file under src in manifest?
srcfiles=sorted(str(p.relative_to(src)) for p in src.rglob('*') if p.is_file() and '.DS_Store' not in p.name)
mset={e['source'] for e in man}
print('source files not in manifest:',[f for f in srcfiles if f not in mset])
# destination tree complete?
nine=['babysit-pr','council','file-pr','full-send','full-stop','leaving-pr-comments','modernize','sol-loop','takeover']
dfiles=sorted(str(p.relative_to(root)) for n in nine for p in (root/'docs/methodology/dev-skills'/n).rglob('*') if p.is_file())
dset={e['destination'] for e in man}
print('dest files not in manifest:',[f for f in dfiles if f not in dset])
# support files unchanged vs EE (pre-import? check vs AA & f6de) and vs source
for e in man:
    if not e['destination'].endswith('SKILL.md'):
        for rev in (AA,'f6de7a2e121a2bf26c0d306f7451568854c5d2d5'):
            b=gitblob(rev,e['destination']); print(' support',e['destination'],rev[:7],'same' if b is not None and hashlib.sha256(b).hexdigest()==h(root/e['destination']) else 'DIFF')
# Only babysit-pr and full-send SKILL changed since AA among skills
for e in man:
    b=gitblob(AA,e['destination']); same= hashlib.sha256(b).hexdigest()==h(root/e['destination'])
    print(' vsAA', 'same' if same else 'CHANGED', e['destination'])
# links
for n in nine:
    l=root/'.agents/skills'/n
    print('link',n, os.readlink(l), (l/'SKILL.md').resolve()==(root/'docs/methodology/dev-skills'/n/'SKILL.md').resolve())
# 24 skills metadata
fm=re.compile(r'\A---\n(.*?)\n---\n',re.S)
skills=sorted(os.listdir(root/'.agents/skills'))
print('skill entries',len(skills))
for n in skills:
    p=root/'.agents/skills'/n/'SKILL.md'
    t=p.read_text(); m=fm.match(t)
    if not m: print('NOFM',n); fail+=1; continue
    body=m.group(1)
    name=re.search(r'^name:\s*(.+)$',body,re.M); desc=re.search(r'^description:\s*(.*)$',body,re.M)
    dval=desc.group(1).strip() if desc else ''
    if dval in ('>-','>','|','|-'):
        dval=' '.join(l.strip() for l in body.split('description:')[1].splitlines()[1:] if l.startswith('  '))
    ok= name and name.group(1).strip()==n and len(dval)>10 and len(dval)<=1024
    fail+= not ok
    tgt=os.path.realpath(p)
    print('meta','OK ' if ok else 'BAD', n, 'symlink' if os.path.islink(root/'.agents/skills'/n) else 'dir', len(dval))
    # relative links
    for lk in re.findall(r'\]\(([^)#\s]+)',t):
        if lk.startswith(('http','mailto')): continue
        rp=(Path(tgt).parent/lk)
        if not rp.exists(): print('  BROKEN',n,lk); fail+=1
# 24 existing non-imported skill files unchanged vs EE except none
print('FAIL',fail)
