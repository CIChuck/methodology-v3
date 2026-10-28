CHANGES_REQUESTED

Candidate: `b869f0cd8df3521666aee51f9b7531631681b2c3`  
Base: `54f0de27f2b59fdcc54e4f57bb9f73dc92843f4a`  
Diff: `git diff 54f0de27f2b59fdcc54e4f57bb9f73dc92843f4a b869f0cd8df3521666aee51f9b7531631681b2c3`  
Branch: `integration/v3-migration`  
Frozen ref: `refs/review/v3/round-1`

Review mode: full conformance review of migration steps 1–6 against RV-01 through RV-10. All ten authority-manifest hashes matched the pinned candidate and checkout. The candidate and frozen ref matched throughout; the working tree remained clean.

Reviewer: independent agent `/root/v3_review_round_1`, Codex; exact model/version was not exposed. This fresh review context began approximately 2026-10-28 03:05–03:06 UTC; its first captured timestamp was `2026-10-28T03:06:50.587503Z`. Exact platform context-creation time was unavailable. Final state recheck: `2026-10-28T03:15:25.503799Z`.

The reviewer received the request, manifest and repository inputs, without the builder’s transcript or private reasoning. Parent messages subsequently supplied raw observations concerning the source-ref mismatch. The added refs were independently confirmed through instrumentation of the authorized preservation verifier; the supplied author/tree metadata is explicitly distinguished below. Unrelated T3 repository instructions were present in the initial environment context and were not used as methodology-v3 build authority. No delegation occurred.

All review logs and disposable reproducers are under:

`/tmp/methodology-v3-review-round-1.6t7cpb`

The complete selected diff is retained as `complete.diff`. No report or remediation was written into the candidate.

1. **VAL-001 — High: original-source ref preservation does not satisfy RV-01.**

   **Location:** `docs/resources/evolution/v3-migration/input-manifest.json`, the corresponding T3 original repository, and preservation evidence.

   **Requirement:** RV-01 requires both originals to retain their frozen Git refs and working state. The migration directive requires source-preservation verification and identifies an original-source mismatch as a stop condition.

   **Evidence:** Independently running `python3 scripts/verify-migration-inputs.py` returned **1**, reporting `T3_Code_Sample: Git refs changed`. Instrumenting that verifier’s existing read-only ref comparison established:

   - Every frozen T3 ref/OID remains unchanged.
   - No frozen refs were removed.
   - Two refs were added under `refs/t3/orchestration-v2/checkpoints/ZjhjNzIxNWU0NTJkYzY2OTVlOGEwY2E3YTc3YTIwMDM/ordinal/`:
     - `37` → `fcf10939b9b10f07b0eadf4a4668617c726f79da`
     - `38` → `0da4ddc97a0eb29a69f1573f8e30f61914fae562`

   The verifier found no inventoried source-file, symlink, mode, inventory or status mismatch. Methodology-v2 passed its comparison. Logs: `preservation.log`, `preservation-ref-observations.json`, and `counterexamples.log`.

   The parent-supplied raw metadata at `methodology-v3-recovery/review/round-1/t3-checkpoint-observation.json` identifies both additions as T3 Code checkpoints with the same tree as frozen checkpoint 36. I inspected that artifact but did not independently execute additional Git operations against the original to establish author/tree provenance. It supports an explanation involving checkpoint tooling; it does not waive strict ref equality.

   **Risk:** The mandatory preservation criterion and final verification command currently fail. This is an operational acceptance-condition discrepancy, not evidence that migration code changed source contents.

   **Required disposition:** Preserve the evidence and obtain explicit human disposition under the governing preservation requirement. Do not delete these refs or silently replace the frozen inventory to make validation pass. Record any authorized exception or revised preservation contract before fresh review.

   **Required verification:** Re-run the preservation verifier against the governing inventory and document its exact result and any approved exception. Retain the original frozen evidence.

   **Documentation impact:** Preservation results, limitations and review authority must reflect the discrepancy. This cannot be represented as an unconditional preservation PASS.

2. **VAL-002 — Medium: upgrade preflight overlooks permission-only customizations and silently replaces them.**

   **Location:** `scripts/lib/distribution.py:157–164`, `:185–195`, and its ownership-record generation and file application.

   **Requirements:** RV-05 requires changed owned files to be refused before writes and states that force does not authorize losing local customizations. RV-06 requires preservation. The distribution guide promises conflict-aware upgrades.

   **Evidence:** `fingerprint()` captures file mode, but ownership preflight compares only file kind and byte digest. Ownership metadata records byte digests alone. The independently created `counterexamples.py` performed:

   ```text
   fresh installation
   chmod scripts/check-methodology.sh 0700
   --force upgrade
   ```

   Result:

   ```text
   mode-only customization: 0o700 -> 0o755 installer exit 0
   mode-only preflight rejected? False
   ```

   Logs/reproducer: `counterexamples.log`, `counterexamples.py`.

   **Risk:** A local permission restriction is silently discarded, including added group/other read permission in this example. Successful byte-integrity checks do not establish preservation of that customization.

   **Required mitigation:** Preserve customized permissions or validate expected modes with an explicit, backward-compatible reconciliation policy. A conflicting permission change must not silently disappear during force upgrades.

   **Required tests:** Add permission-only conflict cases, including restrictive permissions and executable-bit changes. Verify refusal occurs before target mutations, alongside successful clean upgrades and exact rollback.

   **Documentation/configuration impact:** Reconcile ownership metadata and integrity consumers if its contract changes. Document treatment of legacy records that do not contain modes.

   **Classification:** The old baseline also lacked permission-preservation protection: an isolated base-version reproduction changed `0700` to `0711` and exited 0 (`baseline-mode-check.log`). The candidate additionally resets it to `0755`. This is an inherited safety weakness left unresolved within the migration’s explicit new preservation contract, with a broader reset in the changed implementation.

3. **VAL-003 — Low, mandatory: distributed task templates retain sample-product identity.**

   **Location:** `docs/planning/task-template.md:35` and `docs/project-template/planning/task-template.md:35`.

   **Requirement:** RV-03 and migration step 3 prohibit seeding sample-product metadata into new products.

   **Evidence:** Both templates contain:

   ```text
   Project: t3-code-sample
   ```

   An independent fresh installation reproduced that exact line in the installed `docs/planning/task-template.md`. See `counterexamples.log`.

   **Risk:** New task indexes copied according to the template identify the wrong project.

   **Required mitigation:** Replace the fixed product value with an explicit project placeholder or an appropriately rendered project identity in both templates.

   **Required verification:** Fresh-install checks must reject the sample identity in distributed project-owned seeds and confirm that the template remains usable for another project.

   **Documentation impact:** Both reusable template copies require reconciliation. No product authority or acceptance change is needed.

The criteria mapping is:

| Criterion | Assessment | Independent evidence |
|---|---|---|
| RV-01 | **Not satisfied** | VAL-001. Inventoried contents/state otherwise matched. All 21 inventoried v2 refs/OIDs exist under `refs/archive/v2/`; bundle coverage and connectivity passed. No remote, alternates, symlinked object directory or multiply linked object files found. |
| RV-02 | Satisfied within scope | Candidate identity in README, `candidate.json`, doctor output and fresh installation is explicitly unreleased; lifecycle remains 1.0.2. Historical refs/material remain identifiable; no product project was initialized. |
| RV-03 | **Not satisfied** | VAL-003. Otherwise, fresh-install tests confirmed empty board, no migration task/product authority, preserved product dependency files and 15 working skill discovery links. Board requirements are separate. |
| RV-04 | Satisfied within scope | Inspected canonical amendment changes and governing constitution. All six promoted-file hashes match `promoted-amendments.json`. Guidance preserves controlled authority changes, impact-based regression and draft-versus-execution boundaries. Origin records remain historical. |
| RV-05 | **Not satisfied** | VAL-002. Existing negative tests passed for byte edits, missing files, symlinks, collisions, malformed/duplicate records and amendment conflicts; permission changes remain undetected. |
| RV-06 | **Not fully satisfied** | VAL-002. Positive preservation/history tests and both rollback suites passed. An additional real SIGTERM injection restored the exact disposable inventory, including files, modes, links and directories. |
| RV-07 | Satisfied within scope | Initial/later canonical directive tests, initialized-project dry run, archive/planning schema/runtime cases and tamper rejection passed. Additional literal bracket-token, slash and ampersand inputs remained literal in both directives. |
| RV-08 | **Not fully satisfied** | Permission preservation gap in VAL-002. Inspected changed component boundaries, input validation, typed records, failure handling and six-principle conformance; no additional mandatory violation identified. |
| RV-09 | **Not fully satisfied** | Required executable suites passed independently, but source-preservation verification failed and the added counterexample exposes a regression-coverage gap. Synthetic exercise limitations are correctly bounded. |
| RV-10 | Review-process portion satisfied; overall preservation claim unresolved | All authority pins and candidate identities matched; board stayed started; no reviewer edits, delegation, downloads, publication or original-repository mutations. VAL-001 prevents asserting that every original-state constraint is met. |

Commands ran from `/Users/chuckrussell/Dev/gendev/methodology-v3`. Check execution used `UV_OFFLINE=1`, existing local dependencies, `PYTHONDONTWRITEBYTECODE=1` and read-only Git options where applicable.

| Command/check | Exact result | Log |
|---|---|---|
| `./scripts/gendev-doctor.sh` | Exit 0; prerequisites present; unreleased v3 candidate; review/acceptance pending; no initialized product | `doctor.log` |
| `./scripts/check-methodology.sh` | Exit 0; zero warnings | `checker.log` |
| `uv run --frozen --group devboard python scripts/devboard.py validate` | Exit 0; 1 task valid | `board-validate.log` |
| Same board invocation with `next` | Exit 0; `IN_PROGRESS v3-baseline-migration` | `board-next.log` |
| Same board invocation with `show v3-baseline-migration` | Exit 0; started, granted, matching branch | `board-show.log` |
| `./scripts/test-methodology.sh --suite all` | Exit 0; all 13 inherited suites successful | `full-suite.log` |
| `uv run --frozen --group devboard python -B -m unittest discover -s tests/devboard -v` | Exit 0; 17 tests, OK | `board-tests.log` |
| Corresponding discovery under `tests/migration` | Exit 0; 17 tests, OK | `migration-tests.log` |
| `uv run --frozen --group devboard python -B scripts/exercise-v3-toolkit.py /tmp/methodology-v3-review-round-1.6t7cpb/experiments.json` | Exit 0; 4 isolated scenarios | `experiments.log`, `experiments.json` |
| `python3 scripts/verify-migration-inputs.py` | **Exit 1**; T3 refs changed | `preservation.log` |
| `./scripts/methodology-guard.sh --range BASE CANDIDATE` using the full pinned SHAs | Exit 0; zero methodology warnings | `range-guard.log` |
| `git fsck --full` | Exit 0 | `pins-and-git.log` |
| Recovery archive hashes/inventories; bundle hash, `git bundle verify` and frozen ref coverage | Passed; 284 v2 and 208 T3 inventoried files/links checked | `archive-and-amendment-check.log` |
| Skill links/front matter | All 15 passed | `skill-check.log` |
| `python3 -B /tmp/methodology-v3-review-round-1.6t7cpb/counterexamples.py` | Exit 0; confirmed VAL-002/003; literal-input checks passed; records preservation failure | `counterexamples.log` |
| `python3 -B /tmp/methodology-v3-review-round-1.6t7cpb/signal-rollback.py` | Exit 0; injected SIGTERM caused installer exit 1 and exact restoration | `signal-rollback.log` |
| `git diff --check BASE CANDIDATE` | Exit 2; one extra blank line at EOF in historical `validation/experiments-first.log:16` | `pins-and-git.log` |
| Final candidate/ref/status/pin comparison | Passed; candidate and every repository ref/OID unchanged; clean checkout | `final-state.log` |

The `diff --check` issue is an advisory formatting observation in retained historical evidence, not a separate conformance finding.

No hosted CI, Linux execution, real product gate traversal, deployment, release or publication was performed. The deterministic helper exercise does not prove fresh-agent behavior or human approval. Filesystem-wide power-loss/SIGKILL atomicity remains excluded by the documented contract. Exact permissions/ACL/xattr preservation beyond the tested Unix modes was not established. Source author/tree attribution for the two added checkpoint refs rests on the inspected parent-supplied raw observation artifact; their actual addition and unchanged frozen ref/OIDs were independently confirmed.

No inherited-suite failure was observed on this host. VAL-002 has the inherited precursor described above. VAL-003 entered through the generalized templates. VAL-001 is a post-freeze operational discrepancy whose cause is not established by the candidate code review.

Keep the task **started**. Prepare bounded remediation for VAL-002 and VAL-003, obtain human disposition for VAL-001 without modifying the originals to conceal the mismatch, then freeze a new candidate and request a fresh full review. This report grants no acceptance, gate transition or delivery authority.
