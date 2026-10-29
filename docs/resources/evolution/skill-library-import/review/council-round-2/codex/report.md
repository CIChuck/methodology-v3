# Independent full skills review — round 2

Formal outcome: **CHANGES_REQUESTED**
Advisory score: **8/10** (not acceptance).

One mandatory instruction conflict remains. Required offline commands pass; this is not a prerequisite or infrastructure block.

## Identity and context provenance

- Reviewer: GPT-6.1 Sol, high reasoning, Codex harness in T3 Code; member evidence folder `codex`.
- Produced on: 2026-10-28 UTC; fresh review context created for this request during the 23:48 UTC minute. Exact context creation timestamp is not exposed.
- Repository: `/Users/chuckrussell/Dev/gendev/methodology-v3`.
- Branch: `fix/skills-council-follow-up`.
- Base: `ee82653ed6cacb9e1157cd791f12d0fb774f12af`.
- Prior candidate used only for remediation comparisons: `d41e0ebfdc587ecc6d8c3ab336afc530ce90654f`.
- Frozen candidate: `aa25aa89762974012c0243e6134e9785f5db970d`.
- Request SHA256: `d3982d502fe00042f9e274ec66ee9809e2b2a10668fc9fe127f84fdb729477ba`.
- Exact selected diff SHA256: `d34f9b633a639eebe2e9b6bb31cc50ce941b777c3a59cba1c18d1363a88ba0ca`; independently reproduced and saved as [selected.diff](selected.diff).
- All twelve authority entries were hash-checked and read. Every authority revision is the frozen candidate above; hashes appear below and in [authority-manifest.json](authority-manifest.json). [authority-read.txt](authority-read.txt) preserves the pinned authority text.
- Inputs: user assignment, pinned request/authority, exact selected diff, relevant surrounding source/tests, source inventory/import manifest, original source skill comparison, and independently collected local evidence. The findings ledger supplied reproduction targets only.
- Builder transcript/private reasoning/conclusions and sibling/round-1 reports were not read as review inputs or proof. No delegated agents were started. No product initialization in the source, governed edits, ref/branch changes, remediation, network, credential, PR, watcher, or provider workflow effects were performed.
- The inherited initial repository instructions concerned T3_Code_Sample; review operations explicitly targeted methodology-v3 and its local AGENTS.md. A quick memory registry search found no relevant methodology-v3/council entry; no memory facts informed this verdict.

## Mandatory finding

### COD-R2-001 — Major — Full-send still mandates the wrong integration base

**Locations:** `docs/methodology/dev-skills/full-send/SKILL.md:41` (step 4, continues at 42), and `:85` (merge gate). `docs/methodology/dev-skills/full-stop/SKILL.md:14` inherits that workflow/readiness gate.

**Violated requirements:** SK-02, BF-01 actual PR base/merge requirements, and `docs/methodology/guides/skill-execution-contract.md:65-67`: use verified requirements rather than a hard-coded default branch; resolve and recheck the actual PR base/head before mutations. The import directive requires contradictions with GenDev/provider rules to be reconciled.

**Evidence/reproduction:** Full-send step 4 says to rebase onto the latest **default** branch; its gate requires the branch to be up to date with the **default** branch. For an existing maintenance PR targeting `release/1.x`, where `main` has incompatible unreleased changes, those instructions demand integration of `main` instead of the authorized release base. A stacked PR targeting a feature branch has the same problem. The shared contract and the corrected babysit-pr instruction (`:111`) require the actual PR base. Full-stop explicitly inherits full-send's workflow and merge gate, so it inherits the contradiction too. This is directly reproducible by reading those pinned lines; [finding-base-branch.txt](finding-base-branch.txt) contains numbered text and the counterexample. No live PR or rebase was needed or authorized.

**Risk:** A controller following the specific step may introduce unrelated commits into a release/stacked PR, or fail readiness for a correctly prepared PR. A shared instruction to use the actual base reduces risk but leaves conflicting imperative instructions at the action and gate points. That conflict is the defect; this report does not claim a live unsafe mutation occurred.

**Required correction:** Resolve/retain the actual target base for existing PRs and use that base consistently for rebasing and readiness. For a new PR, explicitly select its intended target; default-branch choice may be used when appropriate. Ensure full-stop inherits the corrected behavior. No helper-byte or dependency change is needed.

**Required recheck:** Static counterexamples for an existing release-base PR, a stacked PR, and an ordinary default-base new PR; verify full-send, full-stop, babysit-pr and shared contract agree. Obtain any further implementation/review authority from Chuck; this reviewer does not remediate or initiate another round.

**Origin/documentation impact:** Residual from imported full-send, present at the prior candidate; not a new runtime regression from BF-02/BF-03. It remains inside this requested FULL review of all nine imports. Update the adapted skill digest when authorized to change its text.

## Criteria and evidence

| Criterion | Result and evidence |
| --- | --- |
| SK-01 | Packaging/traceability established. [audit.py](audit.py), [audit.log](audit.log): all 14 source/destination file hashes and modes match inventories; helper plus four UI files are byte-identical to originals; all 24 source entries resolve with valid name/description; nine bundle links and relative resources resolve. Fresh install and initialized/source dry-run checks appear in check-08.log, exercise.json, and targeted BF-02 evidence. All nine SKILL.md were inspected end-to-end and compared against original text; capability-preserving adaptations retain monitoring, council, PR filing, end-to-end/human-merge workflows, comments, modernization, bounded Sol review and takeover. |
| SK-02 | **Not satisfied: COD-R2-001.** Shared contract and all nine skills otherwise retain actual human scope, stop semantics, scoped external effects, frozen formal validation versus advisory scores, mandatory rare-path findings, fresh contexts and bounded review. [bf01-static.json](bf01-static.json) records six prior/current instruction assertions and four classification counterexamples: rare permission/contract/data-loss defects stay mandatory; preference-only style may remain a nit. Full-stop plain stop wording and council explicit invocation/PR-edit limits are explicit. |
| SK-03 | Static conformance established within authorized evidence. Council resolves provider capabilities; unavailable members cannot be substituted. Sol uses fresh delegate tasks and no nested reviewers; supported parent-owned T3 watch/unwatch replaces fallback polling. Shared contract binds current harness dispatch/link/cancel/credential parameters. pr-wait was compiled and run only with --help ([helper-help.txt](helper-help.txt)); no live watcher/provider behavior is claimed. |
| SK-04 | Established. Inspected create-dry-run.py plus distribution.py and manifest: ownership/tracked selection precedes traversal, unsafe selected parents/links fail, full bundles and support survive. [bf02-current.log](bf02-current.log) tests both nested notes.md and nested example/SKILL.md as support without discovery, retaining exactly 24 entries and unchanged source inventory. [bf02-prior.log](bf02-prior.log) shows the same fixture fails against prior create-dry-run.py. check-08.log covers omitted live surfaces, unowned external files/links, unsafe owned sources, empty board and G1 pending. |
| SK-05 | Required dynamic checks pass. check-10.log actually exits 0 against live preserved inputs; no failed preservation check was waived. Frozen inventory/approval have zero diff from base. Inspected compare_refs: anchors come only from frozen before-map, frozen refs cannot change/disappear, existing contexts require increasing ordinals, exact commit author/email/subject and matching tree required. [bf03-targeted.log](bf03-targeted.log) has 13 positive/negative ref cases; [bf03-prior.log](bf03-prior.log) confirms prior verifier rejects the now-authorized new context. Guide mirror is exactly 23 files/bytes (audit.log). Final candidate/authority state is clean and pinned (stability.json). Current board remains started/granted; next selects migration per priority, without changing it. |

## Commands and results

Every shell batch after reading the request prepended the supplied real rg directory and removed a possible shadowing function before doctor. No stub, install or download was used. Required checks used `UV_OFFLINE=1`, `PYTHONDONTWRITEBYTECODE=1`, and external `TMPDIR` under this evidence folder. The initial request-read/memory-search shell preceded those instructions being available; all review checks ran with the prerequisite setup.

All commands below ran from the absolute methodology-v3 repository. [commands.json](commands.json) records exact argv, exit code, duration and log. All exited 0.

| Exact command | Exit | Evidence |
| --- | ---: | --- |
| `./scripts/gendev-doctor.sh` | 0 | [check-00.log](check-00.log) |
| `./scripts/check-methodology.sh` | 0 | [check-01.log](check-01.log) |
| `./scripts/check-doc-coherence.sh` | 0 | [check-02.log](check-02.log) |
| `uv run --frozen --group devboard python scripts/devboard.py validate` | 0 | [check-03.log](check-03.log) |
| `uv run --frozen --group devboard python scripts/devboard.py next` | 0 | [check-04.log](check-04.log) |
| `uv run --frozen --group devboard python scripts/devboard.py show skill-library-import` | 0 | [check-05.log](check-05.log) |
| `./scripts/test-methodology.sh` | 0 | [check-06.log](check-06.log) |
| `uv run --frozen --group devboard python -m unittest discover -s tests/devboard -v` | 0 | [check-07.log](check-07.log) |
| `uv run --frozen --group devboard python -m unittest discover -s tests/migration -v` | 0 | [check-08.log](check-08.log) |
| `uv run --frozen --group devboard python scripts/exercise-v3-toolkit.py /var/folders/dh/wfnmsgpn1yl83xlbmc109sf40000gn/T/v3-skills-council-round2-278hync6/codex/exercise.json` | 0 | [check-09.log](check-09.log) |
| `python3 scripts/verify-migration-inputs.py` | 0 | [check-10.log](check-10.log) |

`test-methodology.sh`: 13 suites, **409 passed, 0 failed** including checker (31), lifecycle (236), and migration shell suite (6); [suite-counts.json](suite-counts.json) reconciles differing summary formats. Board unittest: **17 passed**. Migration unittest: **48 passed**. Exercise: **four scenarios passed** with mandatory explicit external JSON output: fresh, v2-to-v3, copied-T3-to-v3, and synthetic development exercise. This tests disposable copies, not real product upgrade or acceptance.

Supplemental checks: audit.py completed successfully; source dry-run has 24 entries, empty board, no docs/project/approval history, and exact candidate provenance. Targeted before/after fixture checks were expected failures on prior code and passes on the candidate. Helper syntax/help, UI YAML, metadata, links, mode/hash inventories and 23-file mirror passed. BF-01 checks are static because provider workflows are unauthorized. Supplemental evidence assertions initially used wording from the original source instead of d41e0eb, then were corrected to the actual prior phrase; the first inherited-count parser omitted checker/lifecycle's different summary format, then reconciled all 409. These were reviewer evidence-script errors, not candidate check failures or extra review rounds.

## Authority hashes

All paths below are pinned to `aa25aa89762974012c0243e6134e9785f5db970d`.

| Path | SHA256 |
| --- | --- |
| `AGENTS.md` | `ea0209eb0399d4a1f5cb6e9c65c729a9a4f6932bda1dc72484e7dacccc4f4c27` |
| `docs/methodology/constitution/gendev.md` | `f7073cd6d2e9f26ad13e97839e80456ce617a63d3d8f5df3660c7e07500dad4f` |
| `docs/policies/repository-engineering-policy.md` | `7477396d2d8487552866bd19c41e49542dca54fc15b9a7847512229e1a6a1b9e` |
| `docs/policies/development-task-lifecycle.md` | `33321bf308f42a645714f95ee1f9463f4b43b197964e540e5aa03f25eb5a9058` |
| `docs/policies/independent-validation-policy.md` | `ab022a5f6fa019f0e6631f3244e65c38a07ff110a90a391300267cff645e7bff` |
| `docs/policies/dev-board-integration.md` | `af36991dc3ae53977aeb347db84a35aed307a58882394319ee49aec3931f5289` |
| `docs/methodology/guides/skill-execution-contract.md` | `ea5381d2c26dcb4f6a7902a97200a3a95132c444b12ad34e9ebb6bea4fd5f901` |
| `docs/methodology/dev-skills/council/SKILL.md` | `50206528c99440954bf844a24abc4dced180a30da1b21b4c846780f504479ea0` |
| `docs/resources/evolution/skill-library-import/README.md` | `3bbf604c7d14c41a194cd36aaf54cb73002f683001a521a6e6adb13d93f8f8de` |
| `docs/resources/evolution/skill-library-import/review/bounded-follow-up.md` | `ac8cc6421617a46aed4cd05e7b28726e78161c342fdaa906ac1a6771402c9a52` |
| `docs/resources/evolution/skill-library-import/review/findings-ledger.json` | `de81397cb6cfcc0d1ae4c2622483ca9244a1901829176b781c52e20110179101` |
| `docs/resources/evolution/v3-migration/review/round-1/checkpoint-exception-approval.json` | `37c9fa3d8d5ace42e6822b93a87bf4c54c6a35234f7f860c57146de703d15dd7` |

## Limits and disposition

One bounded full pass only. No required listed offline command was skipped. project-state was not applicable to this uninitialized reusable source. Live provider/model availability, dispatch, watch continuation, GitHub reviews/protection, hosted/Linux CI, deployment, product UAT and real gate traversal were not exercised and are not inferred from local checks. Synthetic fixtures may use explicitly synthetic identities; those do not supply a real attester or approval. Inherited lifecycle 1.0.2 and unreleased v3 remain distinct. Historical receipts were not rewritten; delivery/merged PR #1 is not acceptance. Original-input preservation reports only the recorded approved identical-tree T3 additions; it does not grant new ref mutation authority to this reviewer.

The final checkout is clean at the frozen candidate; temporary `.tmp/` appeared during the authorized self-cleaning suite and was absent at final check. Original skill bytes/modes and migration originals/frozen refs/state passed their recorded comparisons. No source-project resync or recovery deletion was performed. Return COD-R2-001 to Chuck for disposition before any additional fix/review cycle. The advisory score grants no acceptance, release or gate authority.
