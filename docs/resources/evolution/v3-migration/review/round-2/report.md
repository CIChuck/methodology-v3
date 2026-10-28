CHANGES_REQUESTED

Candidate: `30aa3c7d68451c9b2ed892d30f349e20c0b14c3f`  
Base: `54f0de27f2b59fdcc54e4f57bb9f73dc92843f4a`  
Branch: `integration/v3-migration`  
Frozen ref: `refs/review/v3/round-2`  
Exact diff:

```sh
git diff 54f0de27f2b59fdcc54e4f57bb9f73dc92843f4a 30aa3c7d68451c9b2ed892d30f349e20c0b14c3f
```

Review mode: full conformance review of migration steps 1–6 against RV-01–RV-10, including prior mandatory findings. All 12 authority-manifest hashes matched the pinned revision and checkout.

Reviewer: independent agent `/root/v3_review_round_2`, Codex; exact model/version unavailable. This was a fresh review context without the builder’s conversation, private reasoning or conclusions. Initial environment instructions referenced T3_Code_Sample; they were not used as methodology-v3 authority. Prior reports were inspected to identify mandatory findings, then independently reassessed. No delegation occurred.

First captured state: `2026-10-28T03:31:37.475047+00:00`. Final state check: `2026-10-28T03:37:30.097337+00:00`. HEAD, frozen ref and authority hashes remained unchanged; the checkout remained clean.

Evidence and disposable reproducers are outside the governed tree:

```text
/var/folders/dh/wfnmsgpn1yl83xlbmc109sf40000gn/T/methodology-v3-review-round-2.d0n6s6r3
```

The selected diff is saved there as `complete.diff`. No report, remediation or state change was written into the candidate.

1. **VAL-004 — Medium, mandatory: project-name substitution does not safely serialize the YAML manifest.**

   **Location:** `scripts/lib/render_template.py:12–29`, called by `scripts/init-project.sh:88–91`; affected output is `docs/project/project.yaml`, whose template places the substituted name inside a double-quoted YAML scalar.

   **Requirement:** RV-07 requires literal user-input rendering. RV-08 requires sound component contracts and essential runtime invariants in the changed scope. The renderer is now the shared boundary between initializer arguments and generated authority artifacts.

   **Evidence:** Independent disposable installations produced:

   ```text
   input: Widget "QA"
   initializer exit: 0
   generated manifest: name: "Widget "QA""
   YAML parsing: fails
   ```

   A name containing two literal backslashes was parsed as containing one backslash. A bracket-token/slash/ampersand control case remained literal.

   The initializer reports success despite generating invalid YAML or changing the parsed identity. `project-state.sh` also returned success for the quoted-name fixture; its output therefore does not establish that the manifest is valid YAML.

   Reproduce using the retained script:

   ```sh
   UV_OFFLINE=1 uv run --frozen --group devboard python \
     /var/folders/dh/wfnmsgpn1yl83xlbmc109sf40000gn/T/methodology-v3-review-round-2.d0n6s6r3/counterexamples.py
   ```

   Evidence: `counterexamples.py`, `counterexamples.log`.

   **Risk:** An otherwise accepted initializer argument can leave the canonical manifest invalid or give YAML consumers a different project name from the supplied value. Literal Markdown insertion and YAML scalar serialization require different treatment.

   **Required mitigation:** Serialize project-name data safely for its YAML context while retaining literal rendering in Markdown. Alternatively, define and validate unsupported input before creating project artifacts. Preserve the existing protection against recursively interpreting user-supplied placeholder tokens.

   **Required verification:** Add round-trip cases for quotes and backslashes: initialize a disposable product, parse its manifest with a YAML parser, and assert that the parsed name equals the supplied name. Retain the existing directive, slash, ampersand and bracket-token cases. If inputs are rejected, verify clear failure before project creation.

   **Documentation/configuration impact:** Reconcile any declared project-name restrictions and initializer/rendering tests. No product approval or architecture change is needed.

   **Classification:** Inherited weakness remaining within the materially changed rendering path and current explicit rendering contract. An isolated archive of the exact base reproduces the quoted-name failure. This is not claimed as a newly introduced regression. Evidence: `base-rendering.py`, `base-rendering.log`.

The prior mandatory findings were independently reassessed:

| Prior finding | Current disposition | Independent evidence |
|---|---|---|
| VAL-001: original-source ref discrepancy | Satisfied under the explicit approved exception; exact ref-set equality is not claimed | Initial/final preservation runs, original-ref metadata inspection, preservation tests and additional counterexamples |
| VAL-002: permission-only upgrade loss | Addressed | Migration tests plus independent `0700`/`0644` zero-write conflict checks; malformed mode checks; clean upstream-mode update coverage |
| VAL-003: sample identity in task seeds | Addressed | Both templates use `[project-slug]`; fresh-install portability test passes |

The preservation exception permits exactly these observed additions under:

```text
refs/t3/orchestration-v2/checkpoints/ZjhjNzIxNWU0NTJkYzY2OTVlOGEwY2E3YTc3YTIwMDM/ordinal/
```

| Ordinal | Commit |
|---|---|
| 37 | `fcf10939b9b10f07b0eadf4a4668617c726f79da` |
| 38 | `0da4ddc97a0eb29a69f1573f8e30f61914fae562` |

Both independently inspected commits have tree `79f1f35afd2bef7fb6427129af0e05669391e243`, matching frozen checkpoint 36, with the required T3 Code author/email and exact ref-specific subject. All frozen refs remain unchanged. The original inventory was introduced once and has not been revised.

The criteria mapping is:

| Criterion | Assessment | Evidence |
|---|---|---|
| RV-01 | Satisfied under the approved exception | Both originals’ inventories/state pass; 284 v2 and 208 T3 entries checked. All 21 frozen v2 refs retain exact archive mappings; all 131 reachable commits remain reachable. Archive/bundle hashes and Git connectivity pass. No remote, alternate, object-directory symlink or original-shared object inode found. |
| RV-02 | Satisfied within scope | README, candidate metadata, doctor and installation provenance distinguish unreleased v3 from the inherited 1.0.2 lifecycle. Historical/draft material remains identifiable; no product was initialized in the source. |
| RV-03 | Satisfied within scope | Fresh-install checks confirm an empty board, reusable task identity, 15 valid internal skill discovery links, no copied product authority or migration task, and preserved product dependency files. |
| RV-04 | Satisfied within scope | Inspected canonical changes preserve controlled authority changes, impact-based regression and draft-versus-execution boundaries. All six promoted-file hashes match the four historical amendment records. |
| RV-05 | Satisfied within scope | Byte, permission, missing-file, symlink, collision, malformed/duplicate-record and amendment-conflict controls pass; clean recorded upstream changes remain possible. |
| RV-06 | Satisfied within scope | Preservation/history and failure-rollback tests pass. Independent SIGTERM injection after 100 actual replacements restored exact disposable file/mode/link/directory state. |
| RV-07 | **Not fully satisfied** | VAL-004. Canonical directive, phase-reference, initialized-project dry-run and archive/planning schema/runtime cases otherwise pass. |
| RV-08 | **Not fully satisfied** | VAL-004 concerns serialization at the changed input boundary. No additional mandatory six-principle, typing, ownership, security or scope violation identified. |
| RV-09 | **Not fully satisfied** | Required suites pass, but VAL-004 demonstrates missing rendering-edge coverage. Harness claims remain correctly limited to deterministic synthetic exercises. |
| RV-10 | Satisfied for this review | Pinned clean candidate; fresh context; board remains started; no reviewer edits, downloads, delegates, original mutations or external effects. Acceptance and delivery remain separate. |

Commands ran from `/Users/chuckrussell/Dev/gendev/methodology-v3`, using existing dependencies and `UV_OFFLINE=1`. Git preservation inspections used `GIT_OPTIONAL_LOCKS=0`.

| Command/check | Result | Evidence |
|---|---|---|
| `./scripts/gendev-doctor.sh` | Exit 0; prerequisites present; unreleased candidate; review/acceptance pending | `doctor.log` |
| `./scripts/check-methodology.sh` | Exit 0; zero warnings | `checker.log` |
| `uv run --frozen --group devboard python scripts/devboard.py validate` | Exit 0; one valid task | `board-validate.log` |
| Same invocation with `next` | Exit 0; `IN_PROGRESS v3-baseline-migration` | `board-next.log` |
| Same invocation with `show v3-baseline-migration` | Exit 0; started, granted, matching branch | `board-show.log` |
| `./scripts/test-methodology.sh --suite all` | Exit 0; all 13 inherited suites successful | `full-suite.log` |
| `uv run --frozen --group devboard python -m unittest discover -s tests/devboard -v` | Exit 0; 17 tests, OK | `board-tests.log` |
| Corresponding discovery under `tests/migration` | Exit 0; 31 tests, OK | `migration-tests.log` |
| `uv run --frozen --group devboard python scripts/exercise-v3-toolkit.py <external-log-directory>/experiments.json` | Exit 0; four scenarios; synthetic helper executes three tests and remains started | `experiments.log`, `experiments.json` |
| `python3 scripts/verify-migration-inputs.py` | Exit 0 initially and finally; approved additions explicitly reported | `preservation.log`, `final-preservation.log` |
| Exact range guard in a disposable independent clone | Exit 0; zero warnings | `range-guard.log` |
| Empty staged guard in that clone | Exit 0; zero warnings | `staged-guard.log` |
| Frozen-ref/history/archive/bundle checks; `git fsck --connectivity-only --no-dangling` | Passed; connectivity exit 0 | `history-archive-check.log` |
| Skill links/front matter and promoted amendment hashes | All 15 links and six hashes pass | `skill-amendment-check.log` |
| Independent permission/malformed-mode counterexamples | Conflicts rejected with exact zero writes | `counterexamples.log` |
| `python3 -B <external-log-directory>/ref-counterexamples.py` | Exit 0; higher ordinal allowed; lower/equal ordinals, wrong subject/email and non-commit rejected | `ref-counterexamples.log` |
| `python3 -B <external-log-directory>/signal-rollback.py` | Exit 0; genuine SIGTERM produces installer exit 1 and exact restoration | `signal-rollback.log` |
| `git diff --check BASE CANDIDATE` | Exit 2; whitespace in retained evidence/report artifacts | `diff-check.log` |
| Final candidate/ref/hash/status/preservation check | Passed | `final-state.log` |

The initial additional signal-test wrapper addressed the wrong argument and never invoked installation. Its output is retained as `signal-rollback-initial-invalid-harness.log` and is excluded from conformance evidence. The corrected wrapper additionally requires the expected signal-specific error before asserting restoration.

Advisory A-001: `git diff --check` flags retained raw diff/log whitespace and Markdown hard-break spaces. These are evidence-formatting observations, not an additional mandatory finding; preserve raw historical evidence rather than silently rewriting it.

No inherited-suite failure was observed on this host. VAL-004’s inherited origin was reproduced against the exact base. The prior permission weakness and sample-template finding are addressed in this candidate.

Validation ran locally on macOS with harness Python `3.13.10`. No Linux or hosted CI run, real product gate traversal, actual fresh-agent behavioral exercise, deployment, release or publication was performed. The deterministic development exercise does not establish human approval or acceptance. Power-loss/SIGKILL atomicity and automatic semantic merging remain explicitly excluded; ACL/xattr preservation was not established.

Keep the migration task **started**. Prepare bounded remediation for VAL-004, freeze the corrected candidate and obtain fresh independent review. This report does not grant acceptance, gate movement, completion or delivery authority.
