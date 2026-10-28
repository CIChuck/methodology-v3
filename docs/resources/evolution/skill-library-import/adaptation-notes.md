# Skill Adaptation Notes

All nine skill folders were copied from the source recorded in source-inventory.json.
The source folder is unchanged. Four agents/openai.yaml files and the complete
babysit-pr/scripts/pr-wait helper retain their original bytes and modes. Each
imported SKILL.md now links to the shared skill execution contract. Discovery
uses whole-folder symlinks so relative scripts, references and UI metadata remain
usable. Existing flat-file skills retain their discovery format.

- babysit-pr: preserve unresolved older findings that still apply; obey actual
  repository review requirements; condition replies/resolution on authorization;
  replace background rate-limit waiting with the active harness's wait/resume rules.
- council: read-only review stays read-only; remediate only authorized scope;
  fresh contexts, bounded cycles and formal outcomes retain GenDev meaning.
- file-pr: honor user/repository draft preference rather than overriding it.
- full-send: scoped autonomy cannot waive accepted authority, required human
  approvals or harness permissions; silence is not approval.
- full-stop: an ordinary stop request remains a stop; only an explicit PR
  preparation workflow uses the full-stop sequence, without merge authority.
- leaving-pr-comments: preserve attribution rules; shared authorization applies.
- modernize: fetch the actual PR base without pulling unrelated branches;
  assessment-only requests remain read-only.
- sol-loop: fresh native/delegate context every round, live model resolution,
  proper dispatch, policy cycle limits, mandatory findings remain mandatory,
  and advisory APPROVE is distinct from formal VERIFIED.
- takeover: preserve credit and original intent; monitoring/comments/merges
  remain within the actual requested scope.

The library now contains 24 skills. create-dry-run.py was narrowly extended to
preserve packaged skills as directory links, including their support resources;
legacy single-file entries remain single-file links. Regression checks cover
both distribution and fresh initialized exercises. No imported workflow was
invoked, and no remote, PR, watcher, comment, merge or delegate was started.
