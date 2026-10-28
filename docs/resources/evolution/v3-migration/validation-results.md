# Methodology-v3: Steps 1–6 Validation Results

Status: Implementation and local deterministic checks finished; independent review pending
Requested by: Chuck Russell
Authority: README.md in this migration record
Tooling checkpoint: 916beff
Reproducible experiment checkpoint: 4ac6397
Independent review: pending, step 7
Human acceptance: pending
Final documentation refresh: pending, step 8
Publication: not performed; no remote configured

## Result and scope

The authorized migration steps 1–6 are implemented in the isolated local
methodology-v3 repository on integration/v3-migration. Both original projects
match the input inventory: methodology-v2 has 284 tracked files/links, and
T3_Code_Sample has 208 nonignored files/links. Their bytes, modes, symlinks,
Git refs and working state remain unchanged. All 21 v2 refs are preserved under
refs/archive/v2; original local branches and tags remain available. The v3 Git
object store is independent, with no alternate and no push remote.

The source v2 commit is 54f0de27f2b59fdcc54e4f57bb9f73dc92843f4a. Full v2 Git
and file recovery archives remain in the sibling methodology-v3-recovery
directory. The pinned T3 archive is also stored in inputs/ here, so replay does
not depend on the disposable original project. Historical source refs and
draft/concept statuses are preserved, including the older local-only release
commit. No historical proposal has been silently implemented or approved.

## Implemented changes

- Generalized engineering, lifecycle and independent-validation policies,
  empty debt register, board integration and code-generation start contract.
- Fifteen skill discovery links with canonical sources, provider-neutral
  handoffs and separate optional T3 action examples. Raw historical hosting
  notes are retained as migration evidence rather than active skills.
- Standard board CLI, schema, templates and tests; standalone tooling
  requirements and an empty installation seed. Product dependencies, board
  approvals, project authority and named project assignments are not inherited.
- Six canonical files incorporate four approved T3 clarification records:
  NAA local detail, architecture-impact reconciliation, rolling-wave drafting
  and architecture wording alignment. Original records remain historical evidence.
- Distribution ownership/preflight, conflict refusal, preservation of extras,
  amendment/installation history and per-file atomic writes with rollback.
- Shared literal scaffold renderer for Phase 1 and later directives, including
  the complete six-principle anti-drift contract. Initialized-product dry-run
  instructions use an isolated fresh fixture rather than replacing authority.
- Archive-history JSON Schema and runtime validation agree; formal reviewer
  guidance explicitly preserves its read-only role.
- Separate unreleased distribution identity in doctor and installation records.
  The inherited 1.0.2 lifecycle contract and historical release records remain
  clearly distinct from this unaccepted candidate.

## Commands and evidence

Executed locally on macOS with Python 3.13.10. Exact platform metadata and
log hashes are in validation-summary.json. Final experiments pin source
revision 4ac6397; the baseline tooling checked by the full suite is unchanged
from 916beff. Later changes are experiment/evidence/operating-document updates.

| Check | Result | Evidence |
| --- | --- | --- |
| Pristine copied v2, all 13 inherited suites | PASS | v2-copy-tests.log |
| Integrated v3, all 13 inherited suites | PASS | validation/v3-full-tests-final.log |
| Board runtime and real JSON Schema regression tests | 17 passed | validation/board-tests-final.log |
| Fresh install, actual upgrade, conflict, symlink, rollback, rendering and dry-run regressions | 17 passed | validation/toolkit-tests-final.log |
| Disposable fresh, v2 upgrade, T3-copy upgrade and helper-build scenarios | 4 passed | experiments.json; validation/experiments-final.log |
| Synthetic helper positive/empty/case-sensitive behavior | 3 passed | experiments.json command evidence |
| Skill metadata and portable discovery links | 15 passed | local skill-creator quick_validate plus frozen installation tests |
| Doctor and methodology coherence | PASS, zero warnings | final commands below |
| Staged and committed-range guards | PASS | final commands below; no product project initialized |
| Original source preservation | PASS | input-manifest.json; verify-migration-inputs.py |
| Original refs, object independence and Git connectivity | PASS | 21 archived ref OIDs compared with input-manifest.json; git fsck --connectivity-only |

Reproduction commands from the source repository:

```bash
./scripts/gendev-doctor.sh
./scripts/check-methodology.sh
./scripts/test-methodology.sh --suite all
uv run --frozen --group devboard python -B -m unittest discover -s tests/devboard -v
uv run --frozen --group devboard python -B -m unittest discover -s tests/migration -v
uv run --frozen --group devboard python -B scripts/exercise-v3-toolkit.py
uv run --frozen --group devboard python scripts/devboard.py validate
uv run --frozen --group devboard python scripts/devboard.py next
python3 scripts/verify-migration-inputs.py
git fsck --connectivity-only
```

The source-preservation comparison intentionally needs the originals to remain
available. The four migration/build experiments instead use this repository's
history and its pinned T3 archive; they remain reproducible after T3 disposal.
Only experiment/evidence output is updated by the experiment command. Unit tests
use temporary directories and do not need either original source project.

## Upgrade findings and explicit reconciliation

The clean disposable v2 installation upgraded successfully. Its project
authority stayed byte-for-byte unchanged and installation history was retained.

The T3 copy initially refused an unowned collision in the imported board skill,
with zero file changes. The fixture then explicitly adopted six shared toolkit
paths into recorded baseline ownership, pinning their actual old bytes before
the upgrade. This decision affected the temporary copy only; the adopted paths
and rationale are in experiments.json. Its four local amendment entries,
canonical project authority and local policies survived the successful upgrade.
This is evidence of controlled reconciliation, not automatic semantic merging.

An updated renderer made T3's preserved generated dashboard stale. Explicit
rendering refreshed that view without changing board.yaml. The operating guide
now states this post-upgrade step. The installer does not silently change task
state or execute a target's code to refresh derived files.

The synthetic helper task produced and executed a bounded Python helper and
three tests. It retained the actual scaffold's pending G1 authority unchanged
and remained started with independent review/acceptance pending. It is baseline
tooling test data, not product generation, a real human approval or a complete
GenDev product traversal.

## Encountered failures and remediation

1. An initial directive regression failed for project names containing slash
   and ampersand. The shared literal renderer replaced fragile sed replacement
   logic. Initial and later phase tests now pass with the same canonical
   anti-drift rules and escaped-name behavior. The original failure is retained
   in validation/toolkit-tests-first.log.
2. The first T3-copy experiment reached the expected stale-dashboard error
   after its successful upgrade. The experiment now explicitly renders the
   derived view and verifies unchanged task data before validation. The original
   failure is retained in validation/experiments-first.log.

Both issues are resolved in the recorded final deterministic checks. There is
no claim of independent validation of the builder's own remediation.

## Limits and next authorized decision

No Linux execution or hosted CI result is claimed. The source workflow defines
macOS/Linux toolkit jobs, but this local-only repository has no remote. No
fresh-context reviewer, actual product gate traversal, production deployment,
release, push or external publication has occurred. Formal review is step 7;
final practitioner/HTML/example/release/adoption documentation refresh is step 8.

The migration task remains started; its delivery is local. It must not become
completed or accepted on the strength of these self-checks. Chuck's next
decision is whether to authorize step 7 and its independent context. Any later
behavioral or governing-authority changes require corresponding checks and a
fresh independent review rather than reuse of this candidate's evidence.
