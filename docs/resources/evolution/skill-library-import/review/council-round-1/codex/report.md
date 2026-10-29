# Independent skills conformance review — GPT-6.1 Sol

Formal outcome: **BLOCKED**  
Advisory score: **9/10** (selected import quality; not acceptance or permission to ship)

No mandatory defect was identified in the selected skills import. Formal verification is blocked by the required original-input preservation command exiting 1 on three additive T3 checkpoint refs in new streams. Their trees match a frozen checkpoint exactly; the verifier only recognizes additions in an already inventoried stream. This is an evidence/exception reconciliation blocker, not evidence of source-content loss or an import-code regression.

## Provenance and identity

Produced by: GPT-6.1 Sol. Produced with: Codex harness in T3 Code, model gpt-6.1-sol, high reasoning. Review mode: one full independent fresh-context read-only pass; no remediation or delegates. Project: reusable methodology-v3 source baseline, task skill-library-import; no initialized real product. Review completion: 2026-10-28T23:33:10.905104+00:00.

This context received the user's reviewer assignment, repository instructions and the pinned request. It did not receive the builder transcript/private reasoning, consult memory, read sibling council outputs, or use prior validator conclusions as proof. Historical readiness/adaptation statements were read as named authority/context and independently checked against files and commands. Original skill text/digests and original-project metadata were read only within the request's permission. No imported workflow was invoked.

Repository: /Users/chuckrussell/Dev/gendev/methodology-v3, main.  
Base: ee82653ed6cacb9e1157cd791f12d0fb774f12af.  
Candidate: d41e0ebfdc587ecc6d8c3ab336afc530ce90654f.  
Request: ../request.md, SHA256 bf0fa2f8c6cdd08e379d21067cb95b1353017cea76989d8593cc7d88f17ed5ea.  
Selected diff: ../selected.diff, SHA256 6818fab01b30764ed63cee1b214fd63b3fceed8f6a5062fcdcf450ccd4100b1c, reproduced byte-for-byte with the request's git diff command.

All ten authority manifest SHA256 pins match both candidate blobs and checkout files. The complete named authorities were read. Additional named construction/provenance inputs: import README, source-inventory.json, import-manifest.json and adaptation-notes.md under docs/resources/evolution/skill-library-import; approved checkpoint-exception-approval.json and its referenced input manifest. The full selected diff and relevant distribution implementation/manifest, installer, regression tests and bundled helper were inspected. Candidate was pinned and clean at entry and clean at final observation; no candidate drift. See candidate-final.json. candidate-observation.json captured transient self-cleaning runtime-suite fixtures under .tmp during the required suite; these were removed by the suite's cleanup. No governed file was changed. No checkout, ref, board, original, remote, credential, dependency or persistent application mutation was performed by this reviewer.

## Findings

### COD-SK-001 — Required preservation evidence cannot pass (BLOCKER; environmental/evidence boundary)

- Location: scripts/verify-migration-inputs.py:39–43, with related ordinal constraint at :51; docs/resources/evolution/v3-migration/review/round-1/checkpoint-exception-approval.json:5; external check-21.log:2–4.
- Requirement: SK-05 and the request's mandatory original-input check, preserving originals/frozen refs under the approved narrow checkpoint exception. Required check failure cannot be silently represented as a pass.
- Reproduction: from the candidate repository run `PYTHONDONTWRITEBYTECODE=1 GIT_OPTIONAL_LOCKS=0 python3 scripts/verify-migration-inputs.py`. Exit 1 reports three `T3_Code_Sample: unapproved added ref` lines. See check-21.log for complete output.
- Exact rejected additions:
  - refs/t3/orchestration-v2/checkpoints/MDk3YTg2ZmI5MWFiZTMxM2I0NjY0YjhjMTk4OTZiZTg/ordinal/0 — 1e606430be4f3e4d5b90916a79574ba9f2dc5cd2
  - refs/t3/orchestration-v2/checkpoints/MjEzMGJjNWYxNjMyYWJiMjAzODUxOGZjYjQ0ZGM0N2E/ordinal/0 — 7c259fd2739c341a177511ce13923d496e91e221
  - refs/t3/orchestration-v2/checkpoints/YTllMDRjMzhmMjNlNjNjNzZmZmRlZWMzMGIzNGIwNmY/ordinal/0 — 784cbc898e67be11614abce8feb71c744064361d
- Independent characterization: all three have tree 79f1f35afd2bef7fb6427129af0e05669391e243, matching the frozen stream ZjhjNzIxNWU0NTJkYzY2OTVlOGEwY2E3YTc3YTIwMDM at ordinal/36 (and several preceding frozen checkpoints). Author name/email are T3 Code / t3code@users.noreply.github.com; each subject is `t3 checkpoint ref=<exact ref>`. See added-ref-analysis.json. Reproduce with `git -C /Users/chuckrussell/Dev/gendev/T3_Code_Sample rev-parse '<ref>^{tree}'` and `git ... show --no-patch --format='%an%n%ae%n%s' '<ref>'`, comparing frozen refs in input-manifest.json. No checkpoint payload or other review context was read.
- Cause: compare_refs requires an anchor with the same stream identifier before considering matching tree/metadata. These new ordinal/0 streams have no such anchor. All other preservation checks completed without reported errors: methodology-v2 284 files/links and T3_Code_Sample 208 files/links, frozen refs, bytes, modes, inventories and working states. Existing same-stream additions were explicitly recognized by the verifier.
- Risk: asserting VERIFIED would conceal a failed mandatory evidence command or implicitly broaden the recorded mechanical exception. There is no observed content corruption and no identified selected-import defect.
- Required disposition/proposed fix: lead/human must reconcile whether the existing same-tree exception covers these newly created streams and establish permitted reproducible passing preservation evidence. If a verifier change is needed, authorize it separately, keep all frozen refs/content protected, and review the changed candidate as applicable. Do not delete/reset refs, edit the frozen inventory, or remediate under this review.
- Required recheck: original-input verifier and explicit negative cases for changed/deleted frozen refs, different-tree additions, and non-T3 additions if its exception logic changes. Re-pin any changed authority/candidate and obtain the required independent review. No product configuration change is proposed.

### COD-INFO-001 — Historical task/readiness tracking lag (informational; outside selected remediation)

Locations: docs/planning/board.yaml:41–43; docs/resources/evolution/skill-library-import/review-readiness.md:3–13; AGENTS.md availability paragraph. `devboard.py show skill-library-import` still names pushed candidate 1516712/integration branch and pending review authorization while this request pins merged main d41e0eb and authorizes this round. Reproduction: check-05.log. Risk is confusing delivery with review/acceptance. The request explicitly classifies this as tracking lag, so it is not the formal blocker or an import finding. Lead can reconcile tracking/evidence in a separately authorized closeout after receiving this round's reports; preserve human acceptance as pending. Recheck board validate and next/show after that update. Reviewer made no tracking edits.

## Criteria-to-evidence mapping

| Criterion | Assessment and primary evidence |
| --- | --- |
| SK-01 | Satisfied locally. All nine skills retain their workflow capabilities with deliberate governance adaptations. Four UI YAMLs and the helper preserve exact bytes/modes. All 14 source and destination digests/modes, complete source inventory and source commit 1085050f3baed1ac724caa4a8166145fb2ac88af checked. offline-checks-rerun.log verifies 24 metadata entries, nine directory discovery links, all Markdown resource links for the imported skills, four usable UI metadata records and helper syntax/help in source, fresh install and dry-run fixture. |
| SK-02 | Satisfied by static conformance review. All nine SKILL.md files link the controlling shared contract. Contract lines 6–47 preserve actual human scope, stop semantics, governing authority, external-effect boundaries, frozen candidates/fresh contexts, formal outcomes and bounded remediation. full-stop explicitly protects plain stop requests and forbids merge/auto-merge; full-send cannot waive gates/attestation/human approvals; council/sol-loop scores remain advisory. Template/advisory review language does not supersede this formal contract. |
| SK-03 | Satisfied statically, live behavior untested. Contract lines 51–68 and council/sol-loop/babysit-pr use runtime capability resolution, prohibit substitution, require fresh tasks and parent-owned T3 watches, prohibit polling/fallback watcher in T3, and defer tool parameters/cancellation/linking to the active harness. No provider or watcher invocation occurred. |
| SK-04 | Satisfied locally. create-dry-run.py:27–54 retains doctor/integrity checks and tracked/owned selection before traversal; :75–87 adds only whole-folder links; :92–101 supplies honest new fixture provenance. distribution.py source_entries still enumerates allowed owned paths without traversing excluded trees; installer planning checks conflicts and owned-source integrity before transactional apply. Migration regressions cover upgrades, rollback, permissions, local state, unowned external links, selected symlink parents, empty boards and pending G1. |
| SK-05 | Partial; formally BLOCKED solely by COD-SK-001. All selected local checks, syntax/help, exact support preservation, board/migration unit tests, applicable shell suites and explicit-output isolated replay passed. Original-input verifier returned 1; its full output and independently characterized refs are retained. No release/Linux/hosted CI/live watcher/product-gate claim. |

Engineering assessment: the ten-line packaging delta is proportionate and reuses distribution Entry/apply contracts, with typed existing boundaries intact. No new dependency, abstraction layer, scope expansion or duplicated installation engine was introduced. Regression additions exercise observable bundle/helper discovery rather than just reproducing implementation text. Runtime-essential safety checks remain explicit exceptions. The unchanged helper remains a Unix/Python/gh fallback only outside T3 and its ready/green output is explicitly not merge authority.

## Commands and results

All commands below ran from the candidate repository with UV_OFFLINE=1, PYTHONDONTWRITEBYTECODE=1, GIT_OPTIONAL_LOCKS=0 and TMPDIR under this external codex/tmp. `run-checks.py` preserves exact invocations; `checks.json` indexes the logs. 21 of 22 required command invocations exited 0; original-input preservation exited 1. There are 13 test-*.sh files at this candidate, including test-migration.sh; its requested exclusion leaves **12** suites, all run. The request's wording “13 ... except test-migration.sh” is treated by its explicit file pattern/exclusion rather than inventing a nonexistent thirteenth eligible suite.

| Command | Exit | Evidence |
| --- | --- | --- |
| `./scripts/gendev-doctor.sh` | 0 | check-00.log |
| `./scripts/check-methodology.sh` | 0 | check-01.log |
| `./scripts/check-doc-coherence.sh` | 0 | check-02.log |
| `uv run --frozen --group devboard python scripts/devboard.py validate` | 0 | check-03.log |
| `uv run --frozen --group devboard python scripts/devboard.py next` | 0 | check-04.log |
| `uv run --frozen --group devboard python scripts/devboard.py show skill-library-import` | 0 | check-05.log |
| `tests/methodology/test-checker.sh` | 0 | check-06.log |
| `tests/methodology/test-distribution-tools.sh` | 0 | check-07.log |
| `tests/methodology/test-documentation-coherence.sh` | 0 | check-08.log |
| `tests/methodology/test-enforcement-tools.sh` | 0 | check-09.log |
| `tests/methodology/test-examples.sh` | 0 | check-10.log |
| `tests/methodology/test-installed-context.sh` | 0 | check-11.log |
| `tests/methodology/test-lifecycle-coherence.sh` | 0 | check-12.log |
| `tests/methodology/test-metrics.sh` | 0 | check-13.log |
| `tests/methodology/test-reference-graph.sh` | 0 | check-14.log |
| `tests/methodology/test-release-coherence.sh` | 0 | check-15.log |
| `tests/methodology/test-runtime-tools.sh` | 0 | check-16.log |
| `tests/methodology/test-shell-syntax.sh` | 0 | check-17.log |
| `uv run --frozen --group devboard python -m unittest discover -s tests/devboard -v` | 0 | check-18.log |
| `uv run --frozen --group devboard python -m unittest discover -s tests/migration -v` | 0 | check-19.log |
| `uv run --frozen --group devboard python scripts/exercise-v3-toolkit.py /var/folders/dh/wfnmsgpn1yl83xlbmc109sf40000gn/T/v3-skills-council-round1-wtbrfdg6/codex/exercise.json` | 0 | check-20.log |
| `python3 scripts/verify-migration-inputs.py` | 1 | check-21.log |

Shell suite results: checker 31; distribution 12; documentation coherence 7; enforcement 22; examples 7; installed context 8; lifecycle coherence 236; metrics 3; reference graph 3; release coherence 11; runtime tools 23; shell syntax 40; all passed with zero failures. Board unittest discovery: 17 tests, OK. Migration unittest discovery: 42 tests, OK. Isolated exercise: 4 scenarios PASS, evidence exercise.json. Its synthetic reviews/approvals are fixture behavior, not formal review or real human acceptance.

Additional check: `UV_OFFLINE=1 PYTHONDONTWRITEBYTECODE=1 TMPDIR=<codex/tmp> uv run --frozen --group devboard python <codex/offline-checks.py>` passed (offline-checks-rerun.log). The first reviewer-owned assertion run stopped on macOS /var versus /private/var path spelling in a resolved-path comparison; canonicalizing both sides corrected the external assertion, and the full rerun passed. Both logs are retained. This was a reviewer fixture assertion error, not a candidate defect. Python compile used in-memory compile(), not a repository bytecode write. No package installation/download occurred.

## Limits and handoff

The intentionally excluded test-migration.sh historical audit was not run. No Linux or hosted CI, live delegate resolution, GitHub/helper polling, authenticated watcher, PR action, external message, real installation, production test or real product gate UAT was performed. The fresh synthetic initialized project's sole missing required-attester invariant remains expected; existing regression tests check it before explicitly labeling a synthetic fixture attester. No real approval was fabricated. The baseline remains unreleased and human acceptance remains pending.

This is a completed bounded review with a BLOCKED formal outcome. Resolve COD-SK-001 through permitted evidence/authority reconciliation before claiming VERIFIED; do not infer acceptance or remediation permission from the advisory score. No second round or corrective work was started.

## Authority pins

All rows are at candidate d41e0ebfdc587ecc6d8c3ab336afc530ce90654f, independently hash-checked against candidate blobs and checkout.

| Path | SHA256 |
| --- | --- |
| AGENTS.md | 3a508c7abb748015ff8710c6808fa8a95333b1ac77e7de217f21371e90e9aceb |
| docs/methodology/constitution/gendev.md | f7073cd6d2e9f26ad13e97839e80456ce617a63d3d8f5df3660c7e07500dad4f |
| docs/policies/repository-engineering-policy.md | 7477396d2d8487552866bd19c41e49542dca54fc15b9a7847512229e1a6a1b9e |
| docs/policies/development-task-lifecycle.md | 33321bf308f42a645714f95ee1f9463f4b43b197964e540e5aa03f25eb5a9058 |
| docs/policies/independent-validation-policy.md | ab022a5f6fa019f0e6631f3244e65c38a07ff110a90a391300267cff645e7bff |
| docs/policies/dev-board-integration.md | af36991dc3ae53977aeb347db84a35aed307a58882394319ee49aec3931f5289 |
| docs/resources/evolution/skill-library-import/README.md | b827a4ff05d123363f56c3c997c970f76534e353ba780ca6f536d83a66497c1a |
| docs/resources/evolution/skill-library-import/review-readiness.md | 45453af97d4da667c9221dd1e47fdf3987e716f0ac906c7de9f5297ee41c89c7 |
| docs/methodology/guides/skill-execution-contract.md | ea5381d2c26dcb4f6a7902a97200a3a95132c444b12ad34e9ebb6bea4fd5f901 |
| docs/methodology/dev-skills/council/SKILL.md | 62165c4229ec96977e53cf57eaece58635b85e57fb1e9d8511f6b267caeee157 |
