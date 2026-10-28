CHANGES_REQUESTED

1. Candidate and diff identity

Project/task: methodology-v3 / v3-baseline-migration. Full independent conformance review of migration steps 1–6 and RV-01–RV-10, including the additional human-authorized VAL-005 cycle.

- Repository: /Users/chuckrussell/Dev/gendev/methodology-v3
- Branch: integration/v3-migration
- Base: 54f0de27f2b59fdcc54e4f57bb9f73dc92843f4a
- Candidate: 6ca2ad10f7eb0c71b9a316d458a20ad667c21c4b
- Frozen ref: refs/review/v3/round-4, resolving to the candidate
- Full diff: git diff 54f0de27f2b59fdcc54e4f57bb9f73dc92843f4a 6ca2ad10f7eb0c71b9a316d458a20ad667c21c4b
- Remediation boundary also inspected: e69320fa2128f549162d633f14cd24463b743566..6ca2ad10f7eb0c71b9a316d458a20ad667c21c4b
- Full diff saved at /tmp/v3-review-round4-7c14hen7/candidate.diff. The range contains 219 changed paths: 111 non-raw paths and 108 historical evidence/archive paths classified in baseline-and-diff.json.

The initial and final checkout were clean on the named branch. HEAD, index, tracked working tree, all candidate refs, remote configuration and pinned authority remained unchanged. No product is initialized in this methodology source repository.

2. Authority and review mode

Controlling request: /Users/chuckrussell/Dev/gendev/methodology-v3-recovery/review/round-4/request.md, SHA256 7d630013efd257680d627aac80fa121b713adf9ebc3508a316af55965bc874f3.

Authority manifest: adjacent authority-manifest.json, SHA256 4a45b094d48ef6495a743297d0e4d3106c39ba29f4500ecb76200e01e7f02c0e. All 14 entries were verified against both their pinned Git objects and current file bytes, and rechecked at close. Every entry pins candidate 6ca2ad10f7eb0c71b9a316d458a20ad667c21c4b:

- AGENTS.md
- docs/methodology/constitution/gendev.md
- docs/policies/repository-engineering-policy.md
- docs/policies/development-task-lifecycle.md
- docs/policies/independent-validation-policy.md
- docs/policies/dev-board-integration.md
- docs/resources/evolution/v3-migration/README.md
- docs/resources/evolution/v3-migration/review-scope.md
- docs/methodology/dev-skills/independent-code-validator.md
- docs/methodology/guides/subagent-coordination-protocol.md
- docs/resources/evolution/v3-migration/review/round-1/checkpoint-exception-approval.json
- docs/resources/evolution/v3-migration/review/round-2/remediation-directive.md
- docs/resources/evolution/v3-migration/review/round-3/human-disposition.md
- docs/resources/evolution/v3-migration/review/round-3/remediation-directive.md

The migration README is the bounded construction directive for this baseline engineering task. Product PRD/architecture/G1 approvals were neither required nor invented. Review followed the pinned independent-code-validator skill. Authority-check.json records the pin checks.

3. Independence and provenance

Produced by: Codex independent reviewer, agent /root/v3_review_round_4. Exact backend model/version is not exposed; provider/model/reasoning settings were inherited unchanged, with no overrides or delegates. Fresh review context began with the frozen request and repository instructions; no builder transcript or private reasoning was supplied. Prior verdicts, historical test logs and builder self-checks were not used as proof. Tracking and disposition records necessarily describe prior outcomes; current conclusions come from primary code and newly executed checks. The controller later supplied a bounded question about excluded discovery/seed inputs, without prescribing a verdict; this report independently reproduces the behavior.

Recorded start: 2026-10-28T16:27:45.866930+00:00. Final state verification: 2026-10-28T16:36:04.257039+00:00. Host: Darwin 27.0.0, arm64. Evidence and fixture writes stayed in external disposable scratch, with permitted test scratch/cache activity. No governed file/ref, original-project file/ref, credential, remote service, push, merge, release or publication was changed. Local checks used UV_OFFLINE=1, existing dependencies, PYTHONDONTWRITEBYTECODE=1, GIT_OPTIONAL_LOCKS=0 and external TMPDIR.

4. Finding

VAL-005 — Medium, mandatory residual: excluded project-owned surfaces can still block fresh dry-run construction.

Location: scripts/create-dry-run.py:54–55, calling scripts/lib/distribution.py:93–107 and :121–136. Relevant contract: round-3/remediation-directive.md, Scope and contract; orchestration-validation.md, Dry-Run Setup; RV-03, RV-07, RV-08 and RV-09.

Requirement: construct a fresh exercise from declared baseline inventory/ownership, with canonical policy/discovery seeds and an empty board, excluding adapted project-owned AGENTS/policies/skills, task history, credentials and runtime. The helper is documented as usable from initialized installed products and as excluding unrecorded local additions. Project-owned discovery/policies are expressly outside baseline integrity ownership.

Evidence: source_entries returns a fully materialized list. The helper's `if entry.owned and entry.path in allowed` filter therefore runs only after source_entries has required and inspected every distribution group, including the excluded `agents` and `project` groups. Missing AGENTS.md, .agents/skills or docs/policies raises at distribution.py:106–107. An external project-owned discovery symlink raises at :126–127 before that entry can be excluded. The fixture itself would regenerate those surfaces from canonical baseline assets at create-dry-run.py:58–81.

Independent reproduction, using only external fixtures:

1. Install candidate into a disposable directory and initialize it normally. Add a synthetic private skill outside that directory and link .agents/skills/private/SKILL.md to it. Baseline doctor returns 0 with verified integrity.
2. Run `python scripts/create-dry-run.py` in that installed source. It exits 1 with `Cannot create dry run: external source symlink: .agents/skills/private/SKILL.md`, produces no fixture path, and leaves the complete source inventory unchanged.
3. Remove that synthetic link. Independently move AGENTS.md, .agents/skills, and docs/policies out of the installed fixture, restoring each after its test. Doctor still returns 0 in every case, but fresh construction exits 1 with `Cannot create dry run: Distribution source missing: <surface>`.

Exact setup, per-command argv/cwd/stdout/stderr/exit and inventory assertions are in counterexamples.py, counterexamples.log and counterexamples-commands.json. The installed test input remains at /tmp/v3-review-round4-7c14hen7/initialized-installed-source; the synthetic external skill remains at /tmp/v3-review-round4-7c14hen7/external-private-skill.md. No live external skill or credential was accessed. The failing link was restored/removed solely within the disposable fixture.

Risk: otherwise integrity-valid installed products cannot use the essential fresh exercise merely because excluded project-owned discovery contains a common external skill link or a seed surface is absent. Excluded live configuration remains an operational dependency of the fresh builder. This is a functional boundary failure, not a preference about helper structure. Ordinary fresh setup now works; this remaining boundary prevents full closure of VAL-005.

Required mitigation: select baseline-owned/tracked groups and paths before existence checks, traversal, symlink validation and content reads. Keep the normal installer's source/symlink protections intact. Build fresh project-owned surfaces only from canonical seeds. Do not require restoring or editing live project-owned adaptations to run the exercise.

Required verification: add focused initialized-installed-source cases with an external project-owned discovery link, omitted project-owned seed surfaces, and unowned additions. Require successful complete fresh construction, verified fixture integrity/provenance, 15 working canonical skill links, canonical policies, empty board/NO_OPEN_TASK, the sole inherited unset-attester checker error, absence of planted live content and exact preservation of the input. Retain refusal of changed/missing owned baseline assets and unsafe owned sources. Re-run appropriate suites and obtain a new authorized frozen-candidate review if Chuck authorizes further work.

Documentation/configuration impact: keep the documented exclusion contract accurate and add the missing regression coverage. No product authority or new dependency is required. This review does not authorize remediation: the one additional cycle is exhausted and the finding must return to Chuck.

5. Requirement-to-evidence matrix

| Criterion | Result and independently checked evidence |
| --- | --- |
| RV-01 preservation/history/isolation | PASS under the recorded exception. preservation.log and final-preservation.log verify 284 v2 and 208 T3 inventoried files/links, bytes/modes, status and frozen refs. history-checks.py/.log verify 21 archived v2 refs at exact OIDs, retained local heads/tags, all reachable objects, no remotes/alternates/shared object inodes, recovery archive/bundle digests and complete inventories. fsck.log exits 0. Allowed additive checkpoints are enumerated below. |
| RV-02 baseline/candidate identity | PASS. candidate.json and doctor.log distinguish unreleased methodology-v3 from inherited 1.0.2; history-checks.log confirms unchanged lifecycle registry, exact recovery inputs and four historical amendment origins. No source product initialization or transfer of historical approval was observed. |
| RV-03 reusable toolkit/portability | PARTIAL; VAL-005. Fresh install tests and experiments verify empty board, 15 discovery entries, general policies, no sample product/approver/task state and unchanged product pyproject/lockfiles. The documented standalone command succeeds with a disposable copied local environment. Excluded project-owned surfaces still block fresh construction. |
| RV-04 four clarifications | PASS. Primary diffs of architecture/directive/phase templates, phase-build-planner, phase-loop and subagent guidance preserve the constitutional implementation-local allowance, amendment impact test and draft/acceptance distinction. history-checks.log verifies all six promoted canonical hashes against all four origin records. Directive rendering tests exercise their canonical output. |
| RV-05 ownership/preflight | PASS. distribution.py and migration-tests.log cover actual upstream updates; edited/removed/mode-changed owned files; unsafe target parents/files; unowned collisions; malformed/duplicate ownership and amendment records; legacy mode adoption. Independent traversal-path, boolean-mode and malformed-amendment counterexamples reject with identical before/after target inventories. |
| RV-06 preservation/rollback | PASS within the documented caught-failure/interrupt contract. Migration tests preserve authority, approvals, adapted policies, board, extra skills and prior installation/amendment records; arbitrary extras remain outside ownership. Failure injection tests cover early/final writes and upgrade. counterexamples.log additionally proves exact rollback for SIGINT, SIGTERM and SIGHUP after first and final replacement, including files/directories, managed include, ignore data and metadata. Four-scenario replay verifies explicit T3 fixture reconciliation and unchanged authority/policies/task state on dashboard refresh. |
| RV-07 directives/dry-run/schema | PARTIAL; VAL-005. Migration tests and independent counterexamples verify literal quote/backslash/Unicode/bracket-token names, YAML round trip, first/later canonical directives and phase references. Both ordinary fresh recipes pass complete orientation with only the declared attester error. Board/schema tests cover accepted archive and completed planning backing records, cross-state rejection and tampering. Excluded-source boundary cases fail. |
| RV-08 safety/contracts/quality | PARTIAL; the finding identifies the source-selection boundary and least-astonishment defect. Inspected changed modules use explicit essential runtime checks, bounded backing-record parsing, local transactional writes and no blanket type suppressions. Shared rendering/ownership helpers and the required policy snapshot consistency test support proportionate KISS/DRY/SRP. No separate concrete scope, NAA, credential or security weakening was found. This is a bounded review, not proof of all possible malformed inputs or races. |
| RV-09 reproducible verification | PARTIAL; required suites and four scenarios pass, but independent counterexamples expose the missing exclusion coverage. Fresh fixture and base checks independently reproduce the single inherited pre-approval attester error. No result is inferred from a builder report, prose match, hosted CI or synthetic approval. |
| RV-10 independence/state/effects | PASS. authority-check.json, initial-state.json, final-state.json, board-show.log and the recorded request establish exact pins, independent context and unchanged candidate/originals. Board remains started/granted on integration/v3-migration; verification, completion, human acceptance and publication remain separate. |

Approved additive T3 checkpoint observations, all in frozen context `ZjhjNzIxNWU0NTJkYzY2OTVlOGEwY2E3YTc3YTIwMDM` and anchored to frozen ordinal 36:

- ordinal 37: fcf10939b9b10f07b0eadf4a4668617c726f79da
- ordinal 38: 0da4ddc97a0eb29a69f1573f8e30f61914fae562
- ordinal 39: 5a8b5eb69a97d7a9fee0ea9c78024b7f91fecbdd

The verifier checks expected T3 author/subject metadata, higher ordinals, commit objects and identical trees. No frozen ref changed and no inventory was rewritten; this is not exact ref-set equality or caller authentication.

6. Commands and exact results

All paths below are under /tmp/v3-review-round4-7c14hen7 unless otherwise noted. run.py and each *.result.json retain exact argv, cwd, exit, duration and log path. Counterexample/standalone/baseline JSON additionally captures nested commands.

| Command from methodology-v3 unless stated otherwise | Result | Evidence |
| --- | --- | --- |
| ./scripts/gendev-doctor.sh | 0; prerequisites present, source context, unreleased candidate | doctor.log |
| ./scripts/check-methodology.sh | 0; 0 warnings, uninitialized source context | checker.log |
| UV_OFFLINE=1 uv run --frozen --group devboard python scripts/devboard.py validate | 0; 1 task | board-validate.log |
| Same prefix, scripts/devboard.py next | 0; IN_PROGRESS v3-baseline-migration | board-next.log |
| Same prefix, scripts/devboard.py show v3-baseline-migration | 0; started/granted, named integration branch | board-show.log |
| ./scripts/test-methodology.sh --suite all | 0; all 13 suites, 409 checks, zero failures | full-suite.log |
| UV_OFFLINE=1 uv run --frozen --group devboard python -B -m unittest discover -s tests/devboard -v | 0; 17 tests | board-tests.log |
| Same prefix, -m unittest discover -s tests/migration -v | 0; 37 tests | migration-tests.log |
| Same prefix, scripts/exercise-v3-toolkit.py /tmp/v3-review-round4-7c14hen7/experiments.json | 0; 4 scenarios | experiments.log/.json |
| Same prefix, /tmp/v3-review-round4-7c14hen7/counterexamples.py | 0 as an investigative harness; four expected dry-run failures reproduced, other assertions pass | counterexamples.log, counterexamples-commands.json, signal_probe.py |
| Documented fresh setup recipe from source and initialized installed fixture | Both 0; fixture doctor/board 0; next NO_OPEN_TASK; checker 1 with only GENDEV-MANIFEST-ENFORCEMENT-002 | counterexamples-commands.json; retained fixtures methodology-dry-run.6bp2qi34 and methodology-dry-run.1thp84_n |
| uv run --no-project --with-requirements requirements-devboard.txt python scripts/devboard.py validate / next in fresh fixture | Both 0; 0 tasks / NO_OPEN_TASK; offline with disposable copied VIRTUAL_ENV and external UV_CACHE_DIR | documented-standalone-command.json |
| python3 scripts/verify-migration-inputs.py, initial and final | Both 0, with exactly the approved additions above | preservation.log, final-preservation.log |
| UV_OFFLINE=1 uv run --frozen --group devboard python -B /tmp/v3-review-round4-7c14hen7/history_checks.py | 0; refs/history/recovery/skills/promotion checks | history-checks.log, history-observations.json |
| git fsck --full --no-reflogs | 0; no errors | fsck.log |
| ./scripts/methodology-guard.sh --range <base> <candidate> | 0 | range-guard.log |
| ./scripts/methodology-guard.sh | 0 | staged-guard.log |
| python3 /tmp/v3-review-round4-7c14hen7/baseline_and_diff.py | 0; base checker reproduces sole attester error; git diff --check over 111 non-raw paths passes | baseline-and-diff.log/.json |
| Final HEAD/ref/status/index/authority comparison | All unchanged; clean | initial-state.json, final-state.json, authority-check.json |

The 13 inherited suites are shell-syntax 40, checker 31, lifecycle 236, runtime-tools 23, distribution-tools 12, enforcement-tools 22, reference-graph 3, documentation-coherence 7, metrics 3, examples 7, migration 6, release-coherence 11 and installed-context 8. The separate migration suite includes preservation-ref negative controls. Four-scenario replay covers fresh install, v2 upgrade, copied T3 upgrade with explicit fixture-only ownership reconciliation, and a synthetic helper task with three executed tests and unchanged product authority. That synthetic task remains started, with independent review/human acceptance pending.

An initial reviewer whitespace harness classified historical report Markdown and a retained legacy note too broadly and exited 1. Its log/script are retained as baseline-and-diff.initial.* and baseline_and_diff.initial.py. The corrected classification excludes historical evidence/report formatting and retained legacy bytes; the final check passes. That harness issue is not a product regression. Excluded raw-log/Markdown whitespace was not treated as behavioral drift.

7. Skipped checks and limitations

No required local suite was omitted. Linux/hosted CI, authenticated actor approval, real product gate traversal, real fresh-agent orchestration behavior, deployment, power-loss/SIGKILL atomicity and automatic semantic merging were not performed or claimed. The required scope excludes those effects/evidence classes. Unchanged historical proposals/material were retained and identified rather than exhaustively re-audited. No new lint/type-check tooling or dependencies were installed. The standalone board exercise used an external copy of the existing environment with offline resolution; no downloads occurred.

8. Baseline versus regression classification

The sole GENDEV-MANIFEST-ENFORCEMENT-002 missing required_attester error was independently reproduced at the inherited base and in both fresh candidate fixtures. It is the declared pre-approval baseline condition, not a warning or migration regression, and no real identity/approval was invented to bypass it. The source repository checker correctly passes without product initialization.

VAL-005's excluded-surface dependency is in the newly added candidate helper, not an inherited baseline failure. The ordinary incomplete-environment problem is corrected, but mandatory fresh-construction boundaries remain incomplete. Existing required suites are green because their planted local inputs are regular files and they do not omit the project-owned distribution sources or add an external discovery link.

9. Residual risk and next gate

One mandatory medium finding remains; therefore this candidate cannot receive VERIFIED or be proposed as completed on this review. No additional blocker, critical or high finding was identified within this bounded full pass. Green deterministic suites do not eliminate untested concurrency, OS or semantic risks.

Return VAL-005 and this evidence to Chuck Russell for disposition. The expressly authorized one additional cycle is exhausted; no automatic remediation or further reviewer dispatch is authorized by this report. Keep the board task started and record the unresolved finding/decision boundary. Human acceptance, step 8 final refresh, release numbering, push/merge and publication remain pending. The controller may preserve this identical report and external logs at the request's declared round-4 destinations without changing the reviewed source candidate.
