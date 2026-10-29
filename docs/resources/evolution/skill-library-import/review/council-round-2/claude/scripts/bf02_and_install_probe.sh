# usage: bf02_and_install_probe.sh <clone-with-probe-commit> <methodology-v3>
set -u; C=$1; R=$2; cd "$C"
echo "probe clone HEAD $(git rev-parse HEAD) parent $(git rev-parse HEAD^)"
git show --stat --format=%s HEAD | sed -n 1,12p
for ver in candidate prior; do
  if [ $ver = prior ]; then git -C "$R" show d41e0eb:scripts/create-dry-run.py > scripts/create-dry-run.py; fi
  out=$(python3 scripts/create-dry-run.py 2>&1); rc=$?; echo "### dry-run $ver rc=$rc"
  [ $rc = 0 ] || { echo "$out"; continue; }
  echo "entries: $(ls "$out/.agents/skills" | wc -l | tr -d ' ')"
  for f in council/references/notes.md council/references/example/SKILL.md council/extra.md council/examples/deep/x/SKILL.md babysit-pr/scripts/pr-wait full-send/agents/openai.yaml; do cmp -s docs/methodology/dev-skills/$f "$out/docs/methodology/dev-skills/$f" && echo "support copied: $f" || echo "support MISSING: $f"; done
  for s in note-a example-b direct-child-c deep-d flat-probe probebundle; do [ -e "$out/.agents/skills/$s" ] && echo "discovered: $s" || echo "not discovered: $s"; done
  echo "pr-wait mode $(stat -f %Lp "$out/docs/methodology/dev-skills/babysit-pr/scripts/pr-wait")"
  (cd "$out" && python3 -c "import json;d=json.load(open('docs/planning/board.yaml')) if False else None" ; ls docs/planning; grep -c "^  - id:" docs/planning/board.yaml 2>/dev/null || echo "board task rows: 0"; test -d docs/project && echo "docs/project PRESENT" || echo "docs/project absent (G1 not initialized)")
  rm -rf "$out"
done
git checkout -q scripts/create-dry-run.py
T=$(mktemp -d "${TMPDIR}fresh-install.XXXX"); git -C "$T" init -q
echo "### fresh install from probe clone into $T"
./scripts/install-methodology.sh "$T" > "$TMPDIR/install.out" 2>&1; echo "install rc=$?"; tail -3 "$TMPDIR/install.out"
echo "entries: $(ls "$T/.agents/skills" | wc -l | tr -d ' ')"
n=0; for e in "$T"/.agents/skills/*; do test -f "$e/SKILL.md" && n=$((n+1)); done; echo "resolving SKILL.md: $n"
for s in note-a example-b direct-child-c deep-d; do [ -e "$T/.agents/skills/$s" ] && echo "discovered: $s" || echo "not discovered: $s"; done
for f in council/references/example/SKILL.md babysit-pr/scripts/pr-wait; do cmp -s docs/methodology/dev-skills/$f "$T/docs/methodology/dev-skills/$f" && echo "support copied: $f" || echo "support MISSING: $f"; done
echo "installed pr-wait mode $(stat -f %Lp "$T/docs/methodology/dev-skills/babysit-pr/scripts/pr-wait")"
(cd "$T" && ./scripts/gendev-doctor.sh | grep -E "Context|integrity|Project initialized"; echo "doctor rc=${PIPESTATUS[0]}")
rm -rf "$T"
