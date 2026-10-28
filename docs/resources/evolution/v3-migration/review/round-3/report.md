CHANGES_REQUESTED

## Candidate and review identity

- Repository: `/Users/chuckrussell/Dev/gendev/methodology-v3`
- Task: `v3-baseline-migration`
- Review: full conformance review of migration steps 1–6 after remediation cycle 2
- Branch: `integration/v3-migration`
- Base: `54f0de27f2b59fdcc54e4f57bb9f73dc92843f4a`
- Candidate: `e69320fa2128f549162d633f14cd24463b743566`
- Frozen ref: `refs/review/v3/round-3`
- Exact diff: `git diff 54f0de27f2b59fdcc54e4f57bb9f73dc92843f4a e69320fa2128f549162d633f14cd24463b743566`
- Evidence directory: `/tmp/v3-round3-review.DruBam/`

The candidate and frozen ref matched throughout review. The checkout remained clean. No candidate artifacts, original projects, board records, or permanent refs were edited.

## Authority and independence

I read the round-3 request and adjacent authority manifest first, then the pinned AGENTS, constitution, four operating policies, migration directive, RV-01–RV-10 review scope, independent-code-validator skill, subagent protocol, checkpoint exception approval, and cycle-2 remediation directive. All 12 authority hashes matched the manifest and working files at the beginning and end.

Reviewer: Codex, separate fresh-context agent `/root/v3_review_round_3`; GPT-6 family as identified by the session instructions, with no more specific runtime model identifier available.

Review began at `2026-10-28T03:51:21Z`; final preservation checks completed at `2026-10-28T03:56:34Z`. The initial environment contained unrelated T3 repository instructions; these were not used as methodology-v3 authority. No builder transcript or private reasoning was supplied. Builder reports, historical logs, and prior pass claims were not used as proof. No additional agents were created.

I applied the repository’s independent-code-validator skill. Verification used existing dependencies with offline uv execution. No package downloads, network calls, publication, acceptance, or remediation occurred.

## Mandatory finding

### VAL-005 — Medium: documented dry-run copy omits required toolkit assets

**Locations**

- `docs/methodology/guides/orchestration-validation.md:20–36`, especially the copy command at line 25
- `tests/migration/test_v3_toolkit.py:343–351`

**Violated requirements**

- RV-07: the documented fresh dry run must work from an initialized project without replacing its authority.
- RV-03: distributed tooling and operating instructions must remain coherent.
- RV-09: checks must prove the relevant behavior.
- Migration steps 5 and 8: repair initialized/uninitialized dry-run instructions and keep essential changed instructions usable.

**Evidence**

The changed guide copies only:

```sh
tar -cf - AGENTS.md docs/methodology docs/project-template scripts tests
```

I installed the candidate into a disposable product, initialized it, and executed the guide’s exact setup commands from that initialized product.

Initialization returned 0 and preserved the original product’s authority. However, the resulting dry-run fixture omitted:

- `.github/workflows/methodology.yml`
- `docs/planning/board.schema.json`
- `requirements-devboard.txt`
- `docs/planning/board.yaml`
- `docs/policies/`
- `.agents/skills/`
- root `README.md`

Actual subsequent results:

| Command in copied fixture | Result |
|---|---|
| `./scripts/gendev-doctor.sh` | Exit 5: three missing baseline-owned files |
| `./scripts/check-methodology.sh` | Exit 1: missing README/workflow, plus the inherited unset-attester error |
| `python scripts/devboard.py validate` | Exit 1: missing board |

The doctor explicitly reported missing `.github/workflows/methodology.yml`, `docs/planning/board.schema.json`, and `requirements-devboard.txt`.

Reproducible evidence:

```sh
UV_OFFLINE=1 uv run --frozen --group devboard python \
  /tmp/v3-round3-review.DruBam/dryrun-installed-counterexample.py
```

See `dryrun-installed-counterexample.log`. A separate reproduction directly from the source repository is in `dryrun-counterexample.py` and `.log`.

**Problem and risk**

The guide directs the practitioner to start an agent in an incomplete governed environment. Its required orientation and board commands cannot succeed. The regression test currently proves initialization and preservation of live authority, but never checks the resulting fixture’s integrity, policies, board, or checker results.

**Classification**

Migration regression in the revised selective-copy procedure. The inherited procedure copied the repository’s supporting assets. The unset `required_attester` checker error is independently confirmed at the base revision and is not attributed to this regression.

**Required mitigation**

Provide an isolated setup that includes the required baseline assets, project-owned policy/discovery seeds, and usable empty board while excluding live product authority, migration task history, Git metadata, credentials, and runtime state. Preserve valid installation provenance when copying from an installed product.

Extend the behavioral regression to exercise doctor, checker, and board commands inside the resulting fixture, allowing only explicitly identified pre-approval conditions.

**Required verification and documentation impact**

Run the documented procedure from both source and initialized installed contexts. Confirm fixture integrity, required policy/discovery assets, empty-board operation, and unchanged live authority. Update the essential guide and focused regression together.

No remediation was performed.

## Requirement-to-evidence assessment

| Criterion | Assessment and primary evidence |
|---|---|
| RV-01 | **PASS with approved exception.** Preservation verifier passed before and after. Recovery archives matched frozen inventories and digests; bundle verification succeeded. All 21 frozen v2 refs were preserved under `refs/archive/v2/`, local branches/tags retained, base ancestry present, and Git storage independent with no remotes or alternate object store. |
| RV-02 | **PASS.** README, doctor, installation records, and `candidate.json` identify an unreleased methodology-v3 candidate separately from inherited 1.0.2 lifecycle evidence. Historical release evidence and constitution were unchanged. |
| RV-03 | **Finding VAL-005.** Normal fresh installations passed portability, empty-board, policy preservation, dependency separation, and skill checks. The documented dry-run construction omits those required surfaces. |
| RV-04 | **PASS.** Inspected the six promoted canonical guidance files and four origin records. All recorded promoted-file digests matched. Private implementation allowances remain bounded; amendment impact controls regression; advance drafts confer no checkpoint or execution authority. |
| RV-05 | **PASS.** Installer preflight code and executed regressions cover modified/missing owned files, permission changes, unsafe symlinks, collisions, malformed/duplicate metadata, local amendments, and clean upstream updates. Independent malformed permission metadata control refused with zero writes. |
| RV-06 | **PASS.** Upgrade and rollback regressions plus four experiments passed. Independent SIGINT, SIGTERM, and SIGHUP controls at the final metadata replacement restored the complete target inventory, including directories, modes, managed instructions, ignore file, and metadata. |
| RV-07 | **Finding VAL-005.** Canonical initial/later directives, phase references, literal rendering, YAML name round trips, and board archive/planning positive and negative tests passed. The documented dry-run fixture remains incomplete. |
| RV-08 | **PASS within changed scope.** Inspected installer, rendering, preservation, board validation, surrounding callers, schemas, and tests. Essential checks use runtime validation; changed boundaries have explicit contracts; no blanket suppressions or concrete unauthorized scope expansion found. |
| RV-09 | **Finding VAL-005.** Required suites and experiments actually ran and passed, but the targeted counterexample demonstrates a gap in the dry-run regression. Baseline and platform limits are stated below. |
| RV-10 | **PASS for review process.** Exact pins verified; clean candidate retained; board remains `started`, local, and awaiting review/human disposition. No acceptance or delivery authority was exercised. |

The approved T3 additions observed at both preservation checks were:

- Context `ZjhjNzIxNWU0NTJkYzY2OTVlOGEwY2E3YTc3YTIwMDM`, ordinal **37**: `fcf10939b9b10f07b0eadf4a4668617c726f79da`
- Same context, ordinal **38**: `0da4ddc97a0eb29a69f1573f8e30f61914fae562`

Both satisfy the approved metadata and identical-tree conditions against frozen ordinal 36. Every frozen ref remains protected; exact ref-set equality is not claimed.

## Commands and results

Commands ran from methodology-v3 unless stated otherwise. Logs are in the external evidence directory.

| Command/check | Result |
|---|---|
| Authority SHA-256 and working-file verification | All 12 pins matched |
| `./scripts/gendev-doctor.sh` | Exit 0; prerequisites present; unreleased baseline context |
| `./scripts/check-methodology.sh` | Exit 0; zero warnings |
| `UV_OFFLINE=1 uv run --frozen --group devboard python scripts/devboard.py validate` | Exit 0 |
| Same invocation with `next` | Exit 0; migration remains in progress |
| Same invocation with `show v3-baseline-migration` | Exit 0; started/granted/local, correct branch |
| Documented standalone requirements invocation of board validation | Exit 0 |
| `./scripts/test-methodology.sh --suite all` | Exit 0; all 13 inherited suites completed successfully |
| Offline unittest discovery in `tests/devboard` | Exit 0; 17 tests passed |
| Offline unittest discovery in `tests/migration` | Exit 0; 33 tests passed |
| Offline `scripts/exercise-v3-toolkit.py /tmp/v3-round3-review.DruBam/experiments.json` | Exit 0; four isolated scenarios passed |
| `python3 scripts/verify-migration-inputs.py` | Exit 0 before and after; 284 v2 and 208 T3 files/links preserved |
| `git fsck --full --no-reflogs` | Exit 0 |
| Recovery archive/bundle digest and inventory checks; `git bundle verify` | Passed; complete bundle history |
| Skill discovery/metadata and promoted-amendment checks | All 15 links valid; six promoted digests matched |
| Range guard over exact base/candidate | Exit 0 |
| Staged guard | Exit 0 |
| `counterexamples.py` under offline uv | Passed interrupt rollback, combined literal name rendering, invalid forced-name refusal, malformed permission metadata refusal |
| Dry-run counterexamples | Reproduced VAL-005 |
| `git diff --check BASE CANDIDATE` | Nonzero: whitespace in retained raw review evidence, Markdown hard breaks, and a historical log ending; no executable failure inferred |

The first history-check script used an incorrect assumed archive namespace (`refs/archive/v2/refs/...`). I corrected the observer to the actual namespace (`refs/archive/v2/...`) and reran successfully. This was a reviewer command correction, not a candidate defect.

## Baseline distinctions, omissions, and residual risk

A freshly initialized base-revision fixture independently produced the existing `GENDEV-MANIFEST-ENFORCEMENT-002` error for an unset named attester. That condition requires actual project disposition; no human identity or approval was fabricated. VAL-005 concerns the additional missing assets introduced by the changed copy instructions.

The latest YAML project-name remediation passed both its focused suite and independent combined quote/backslash/Unicode/token controls. Permission preservation and narrow checkpoint handling also passed current primary-code and behavioral checks.

No Linux or hosted CI execution, real product gate traversal, deployment, or fresh-context practitioner behavior exercise is claimed. The synthetic experiment remains a local tooling exercise. Power-loss/SIGKILL atomicity and semantic merging remain documented exclusions. No exhaustive redesign audit of unchanged historical material was attempted.

Whitespace findings in retained raw evidence are advisory and do not require rewriting historical evidence.

## Recommended next gate

Return **VAL-005** and its reproduction to Chuck Russell for disposition. Two remediation cycles have been used; do not begin another automatic cycle. Keep the task started and preserve this candidate and all review refs. Human acceptance, step-8 refresh, publication, and delivery remain pending.
