# Independent Skills Council Review — Round 1 (Gemini 4 Argon High)

## 1. Outcome and Advisory Score

- **Formal Outcome:** `VERIFIED`
- **Advisory Score:** `9.5 / 10`
- **Scope Status:** All mandatory acceptance criteria (`SK-01` through `SK-05`) are satisfied by the frozen candidate `d41e0ebfdc587ecc6d8c3ab336afc530ce90654f` and the selected diff (`6818fab01b30764ed63cee1b214fd63b3fceed8f6a5062fcdcf450ccd4100b1c`). Zero blocker, critical, high, or medium findings exist in the selected skill-import scope. Two low-severity / advisory items (one in-scope minor grammar note in `modernize/SKILL.md` and one out-of-scope harness observation on `verify-migration-inputs.py` alongside the expected pre-merge/pre-review tracking lag) are documented below.
- **Boundary Notice:** `VERIFIED` and the `9.5/10` advisory score are recommendations for human disposition only. They do not constitute human acceptance, board transition, gate approval, release, or deployment authority.

---

## 2. Provenance, Candidate, and Authority Pins

- **Reviewer / Member Identity:** `Gemini 4 Argon High` (`gemini-4-argon-high` in T3 Code via Antigravity harness; fresh read-only context `05fa88c5-e65e-4449-a72e-58b52f3cbf9f`)
- **Review Timestamp:** `2026-10-28T23:35:00Z` (`2026-10-28T19:35:00-04:00`)
- **External Evidence Subfolder:** `/var/folders/dh/wfnmsgpn1yl83xlbmc109sf40000gn/T/v3-skills-council-round1-wtbrfdg6/gemini/`
- **Pinned Request:** `/var/folders/dh/wfnmsgpn1yl83xlbmc109sf40000gn/T/v3-skills-council-round1-wtbrfdg6/request.md`
  - Verified SHA-256: `bf0fa2f8c6cdd08e379d21067cb95b1353017cea76989d8593cc7d88f17ed5ea`
- **Reviewed Repository:** `/Users/chuckrussell/Dev/gendev/methodology-v3`
  - Checkout / Branch: `main` (clean working tree, verified before and after all checks)
  - Base Commit: `ee82653ed6cacb9e1157cd791f12d0fb774f12af`
  - Frozen Candidate Commit: `d41e0ebfdc587ecc6d8c3ab336afc530ce90654f`
- **Selected Scope Diff:** `/var/folders/dh/wfnmsgpn1yl83xlbmc109sf40000gn/T/v3-skills-council-round1-wtbrfdg6/selected.diff`
  - Verified & Reproduced SHA-256 (`git diff ee82653ed6cacb9e1157cd791f12d0fb774f12af d41e0ebfdc587ecc6d8c3ab336afc530ce90654f -- .agents/skills docs/methodology/dev-skills docs/methodology/guides/skill-execution-contract.md scripts/create-dry-run.py tests/migration/test_v3_toolkit.py`): `6818fab01b30764ed63cee1b214fd63b3fceed8f6a5062fcdcf450ccd4100b1c` (26 files changed, 1392 insertions, 5 deletions)
- **Source Originals Repository:** `/Users/chuckrussell/Dev/gendev/tstack/skills`
  - Verified HEAD: `1085050f3baed1ac724caa4a8166145fb2ac88af` (clean working tree, 14 files/modes/SHA-256 digests unchanged)

### Verified Authority Manifest Pins (at `d41e0ebfdc587ecc6d8c3ab336afc530ce90654f`)

| Authority Document | Verified SHA-256 |
| --- | --- |
| `AGENTS.md` | `3a508c7abb748015ff8710c6808fa8a95333b1ac77e7de217f21371e90e9aceb` |
| `docs/methodology/constitution/gendev.md` | `f7073cd6d2e9f26ad13e97839e80456ce617a63d3d8f5df3660c7e07500dad4f` |
| `docs/policies/repository-engineering-policy.md` | `7477396d2d8487552866bd19c41e49542dca54fc15b9a7847512229e1a6a1b9e` |
| `docs/policies/development-task-lifecycle.md` | `33321bf308f42a645714f95ee1f9463f4b43b197964e540e5aa03f25eb5a9058` |
| `docs/policies/independent-validation-policy.md` | `ab022a5f6fa019f0e6631f3244e65c38a07ff110a90a391300267cff645e7bff` |
| `docs/policies/dev-board-integration.md` | `af36991dc3ae53977aeb347db84a35aed307a58882394319ee49aec3931f5289` |
| `docs/resources/evolution/skill-library-import/README.md` | `b827a4ff05d123363f56c3c997c970f76534e353ba780ca6f536d83a66497c1a` |
| `docs/resources/evolution/skill-library-import/review-readiness.md` | `45453af97d4da667c9221dd1e47fdf3987e716f0ac906c7de9f5297ee41c89c7` |
| `docs/methodology/guides/skill-execution-contract.md` | `ea5381d2c26dcb4f6a7902a97200a3a95132c444b12ad34e9ebb6bea4fd5f901` |
| `docs/methodology/dev-skills/council/SKILL.md` | `62165c4229ec96977e53cf57eaece58635b85e57fb1e9d8511f6b267caeee157` |

---

## 3. Mandatory Criteria-to-Evidence Mapping (`SK-01` – `SK-05`)

| Criterion | Status | Primary Code & Reproduced Evidence |
| --- | --- | --- |
| **SK-01:** Nine complete skills preserve intended capabilities, valid metadata/support UI, source digests/provenance and whole-folder discovery (24 total) with usable relative paths in source/fresh installs/dry-run fixtures. | **PASS** | All 9 imported skills (`babysit-pr`, `council`, `file-pr`, `full-send`, `full-stop`, `leaving-pr-comments`, `modernize`, `sol-loop`, `takeover`) exist under `docs/methodology/dev-skills/<name>/SKILL.md` with valid YAML frontmatter (`name` matching folder name, non-empty `description`), resolvable relative Markdown links (`../../guides/skill-execution-contract.md` and `../full-send/SKILL.md`), and whole-folder discovery symlinks `.agents/skills/<name> -> ../../docs/methodology/dev-skills/<name>`. Together with the 15 existing single-file skills (`.agents/skills/<name>/SKILL.md -> ../../../docs/methodology/dev-skills/<name>.md`), all 24 skills resolve inside the repository, fresh installs, and `create-dry-run.py` fixtures (`offline-skill-checks.json`, `migration-tests.log`, `experiments.json`). All 14 entries in `source-inventory.json` and `import-manifest.json` match exact SHA-256 digests and file modes (`0o644` for docs/YAML, `0o755` for `babysit-pr/scripts/pr-wait`). The 4 `agents/openai.yaml` files (`full-send`, `full-stop`, `leaving-pr-comments`, `modernize`) retain valid `interface.{display_name,short_description,default_prompt}` metadata and are byte-identical to `tstack/skills`. |
| **SK-02:** Instructions preserve GenDev authority/gates, actual human scope, external-effect limits, stop semantics, independent fresh contexts, bounded remediation and required approvals. Scores advisory; no accepting, merging, ignoring mandatory findings or broad authority by workflow labels. | **PASS** | `docs/methodology/guides/skill-execution-contract.md:1-68` and all 9 imported `SKILL.md` files explicitly subordinate skill execution to `AGENTS.md`, the GenDev constitution, and active project/evolution authority. Key reconciliations verified line-by-line against `tstack/skills`: (1) `full-stop/SKILL.md:3,14-18` prevents treating an ordinary pause/stop instruction as a PR workflow and forbids merging; (2) `full-send/SKILL.md:27-32,88-89,112-113` scopes testing permission to accepted authority/harness boundaries, forbids waiving required human approval (`confidence never replaces a required human approval`), and ensures silence/no answer leaves the PR unmerged; (3) `council/SKILL.md:10-13,54-58` and `sol-loop/SKILL.md:20-24,34-36,88-89,104-105` require fresh review contexts per round, enforce the validation policy's stop after two unsuccessful remediation cycles, require remediation of rare mandatory contract/security violations, and distinguish advisory `/10` scores and `APPROVE` from formal `VERIFIED`; (4) `babysit-pr/SKILL.md:81-94`, `file-pr/SKILL.md:47-48`, `modernize/SKILL.md:18-24`, `leaving-pr-comments/SKILL.md:7-28`, and `takeover/SKILL.md:41-43` condition external mutations (pushes, comments, thread resolution, merges, closures) and draft/readiness states on actual user/repository authorization. |
| **SK-03:** Provider delegation/watching instructions follow supported harness contracts; no unasked provider substitution or fallback polling in T3. State whether live provider behavior is untested. | **PASS** | `skill-execution-contract.md:46-68`, `babysit-pr/SKILL.md:15-41`, `council/SKILL.md:21-24`, `full-send/SKILL.md:54-58`, `full-stop/SKILL.md:49-50`, and `sol-loop/SKILL.md:53-68` accurately follow harness contracts: in T3 Code, `orchestrator_capabilities` precedes `delegate_task` with settings in `target.options`, every review round uses a fresh `delegate_task` (never `t3_thread_send`, `create_threads`, or `t3_thread_launch`), unavailable providers/models are reported as blockers without unasked substitution, PR watching in T3 uses parent-owned `watch_pull_request` / `unwatch_pull_request` only (children never watch, and `pr-wait` or sleep/polling loops are forbidden in T3), and GraphQL rate-limit exhaustion in `babysit-pr/SKILL.md:36-39` reports reset time and uses harness pause/resume rather than a background wait loop. **Explicit limitation:** Live provider delegation, live GitHub API calls, and live PR watcher execution (`watch_pull_request` / live `pr-wait`) are **untested** in this offline review. |
| **SK-04:** Dry-run packaging keeps selection-before-traversal, complete supporting directories, safe upgrade/owned-source protections, excludes live authority/runtime/unrecorded files, empty board/G1 pending and honest provenance. Inspect surrounding distribution code and changed tests. | **PASS** | Inspected `scripts/create-dry-run.py:1-106`, `scripts/lib/distribution.py:1-258`, `scripts/lib/distribution-manifest.txt:1-38`, and `tests/migration/test_v3_toolkit.py:1-460`. `create-dry-run.py:24-52` runs `gendev-doctor.sh` first, restricts `allowed` to `installation.json["files"]` (or `git ls-files` in a methodology checkout), and calls `source_entries(..., owned_only=True, allowed_paths=allowed)` so only owned baseline files (`docs/methodology`, `docs/project-template`, `scripts/lib`, `tests/methodology`, and required scripts) are enumerated before traversal—never touching live project-owned `.agents/skills`, `docs/policies`, `docs/planning`, `docs/project`, or unowned files. Because `docs/methodology` is a `required` baseline tree, all imported skill files and support files (`babysit-pr/scripts/pr-wait` mode `0o755`, `*/agents/openai.yaml` mode `0o644`) are baseline-owned and copied into `docs/methodology/dev-skills/<name>/...`. Lines `70-81` of `create-dry-run.py` cleanly distinguish directory-bundled skills (`path.name == "SKILL.md"` -> `.agents/skills/<name>` directory symlink to `../../docs/methodology/dev-skills/<name>`) from legacy single-file skills (`.agents/skills/<name>/SKILL.md` file symlink to `../../../docs/methodology/dev-skills/<name>.md`), while rejecting invalid skill names and duplicate destinations. Verified via 42 unit tests in `test_v3_toolkit.py`, 4 isolated replay scenarios in `exercise-v3-toolkit.py`, and 4 targeted negative counterexamples (`counterexamples.json`). |
| **SK-05:** Exact source/helper preservation and all required local checks pass; no claim of Linux/hosted CI/live watcher/product gate UAT. Existing frozen migration is background scope; do not redo its exhaustive unrelated audit. | **PASS** | `/Users/chuckrussell/Dev/gendev/tstack/skills` is completely untouched at `1085050f3baed1ac724caa4a8166145fb2ac88af`; `babysit-pr/scripts/pr-wait` (`90393f85b95b78bff1b039744bdfb09dc88ff2b430e1c3df687ee6f449c97214`, mode `0o755`) and all four `agents/openai.yaml` files are byte-for-byte identical to source (`offline-skill-checks.json`). `pr-wait` compiles cleanly with `py_compile` and `--help` exits `0` offline. All required local checks in `methodology-v3` passed (`gendev-doctor.sh`, `check-methodology.sh`, `check-doc-coherence.sh`, `devboard.py validate/next/show`, all 12 non-migration `tests/methodology/test-*.sh` suites, 17 `tests/devboard` unit tests, 42 `tests/migration` unit tests, and 4 `exercise-v3-toolkit.py` scenarios). Original project files/modes/working trees in `methodology-v2` and `T3_Code_Sample` are 100% intact (see Section 5.1 regarding T3's 3 new council-session `ordinal/0` checkpoint refs). |

---

## 4. Executed Commands, Results, Skips, and Limitations

All commands were executed read-only against `/Users/chuckrussell/Dev/gendev/methodology-v3` with `TMPDIR` and all outputs directed to `/var/folders/dh/wfnmsgpn1yl83xlbmc109sf40000gn/T/v3-skills-council-round1-wtbrfdg6/gemini/` and `PYTHONDONTWRITEBYTECODE=1`.

| Check / Command | Exit Code | Evidence Log / Output | Summary |
| --- | --- | --- | --- |
| `./scripts/gendev-doctor.sh` | `0` | `gendev-doctor.log` | All prerequisites (`bash`, `git`, `python3`, `rg`) present; `Context: authority`, `Distribution candidate: methodology-v3 (unreleased)`, `Git HEAD: d41e0eb`, `Project initialized: no`. *(Note: default non-login shell PATH omitted `rg`; adding the local T3 bundle `rg` directory to `PATH` satisfied `rg` without installing anything.)* |
| `./scripts/check-methodology.sh` | `0` | `check-methodology.log` | `Methodology check passed: 0 warning(s).` |
| `./scripts/check-doc-coherence.sh` | `0` | `check-doc-coherence.log` | `Documentation coherence: clean` |
| `UV_OFFLINE=1 uv run --frozen --group devboard python scripts/devboard.py validate` | `0` | `devboard-validate.log` | `Development board validation passed: 3 tasks` |
| `UV_OFFLINE=1 uv run --frozen --group devboard python scripts/devboard.py next` | `0` | `devboard-next.log` | `IN_PROGRESS v3-baseline-migration: Chuck acceptance of VERIFIED candidate 98f8bec4597cd3307fc26e5c28dc86592e01ca08; step 8 remains separate` |
| `UV_OFFLINE=1 uv run --frozen --group devboard python scripts/devboard.py show skill-library-import` | `0` | `devboard-show.log` | Shows `work_state: started`, `implementation_authority: granted`, `delivery_state: pushed`, `branch: integration/v3-skill-import`, `next_gate: Authorize fresh independent review of pushed skill-import candidate 1516712; human acceptance pending`. |
| Inherited methodology suites (`./scripts/test-methodology.sh --suite "shell-syntax checker lifecycle runtime-tools distribution-tools enforcement-tools reference-graph documentation-coherence metrics examples release-coherence installed-context"`) | `0` | `inherited-tests.log` | All 12 non-migration suites in the 13-suite set (`test-checker.sh`, `test-distribution-tools.sh`, `test-documentation-coherence.sh`, `test-enforcement-tools.sh`, `test-examples.sh`, `test-installed-context.sh`, `test-lifecycle-coherence.sh`, `test-metrics.sh`, `test-reference-graph.sh`, `test-release-coherence.sh`, `test-runtime-tools.sh`, `test-shell-syntax.sh`) passed with 0 failures. `test-migration.sh` was skipped per request instructions. |
| `UV_OFFLINE=1 uv run --frozen --group devboard python -m unittest discover -s tests/devboard -v` | `0` | `devboard-tests.log` | Ran 17 tests in 2.640s — `OK`. |
| `UV_OFFLINE=1 uv run --frozen --group devboard python -m unittest discover -s tests/migration -v` | `0` | `migration-tests.log` | Ran 42 tests (`8` in `test_preservation_refs.py`, `34` in `test_v3_toolkit.py`) in 35.355s — `OK`. Covers fresh install (24 skills, `pr-wait --help`, `openai.yaml`), clean upgrade, dry-run from initialized product and methodology checkout, selection-before-traversal, and symlink/permission protections. |
| `UV_OFFLINE=1 uv run --frozen --group devboard python scripts/exercise-v3-toolkit.py <EXTERNAL_OUTPUT>/experiments.json` | `0` | `experiments.log`, `experiments.json` | `PASS: 4 isolated scenarios` (`fresh` with 24 skills, `v2_to_v3`, `t3_copy_to_v3`, `development_exercise`). Fresh initialized synthetic project exhibits the sole expected `GENDEV-MANIFEST-ENFORCEMENT-002` (`required_attester: TBD`) error until named. |
| Offline 9-skill metadata, support syntax/help, link, and source-manifest verification | `0` | `offline-skill-checks.json` | Verified `tstack/skills` clean at `1085050f3baed1ac724caa4a8166145fb2ac88af`, all 14 source/destination SHA-256 digests and modes, all 24 `.agents/skills` discovery links, all relative Markdown links from both canonical and discovery paths, `py_compile` + `--help` (exit `0`) + missing-arg exit (`2`) on `babysit-pr/scripts/pr-wait`, and schema/keys of all 4 `openai.yaml` files. |
| Targeted counterexamples on changed packaging/skill scope | `0` | `counterexamples.json` | Verified 4 negative/isolation cases: (1) invalid skill frontmatter `name` in `create-dry-run.py` rejected with exit `1`; (2) unowned rogue script inside `docs/methodology/dev-skills/babysit-pr/scripts/` and external symlink in `.agents/skills/` excluded by `create-dry-run.py` while `pr-wait` is preserved; (3) modified `agents/openai.yaml` support file blocks `--force` upgrade (exit `1`) and triggers `gendev-doctor.sh` integrity error (exit `5`); (4) duplicate skill `name` across two `SKILL.md` files rejected by `create-dry-run.py` with exit `1` (`duplicate exercise destination`). |
| `python3 scripts/verify-migration-inputs.py` | `1` (see Finding `OBS-OUT-001`) | `original-preservation.log` | `methodology-v2` (284 files/links/refs) and `T3_Code_Sample` (208 files/links, working tree, all frozen refs, and 20 same-thread checkpoints `ordinal/37..56`) are 100% preserved. Exited `1` solely because T3 Code created 3 new `ordinal/0` checkpoint refs in `T3_Code_Sample` at `2026-10-28 19:26:10..13 -0400` when spawning the 3 council reviewer subagent threads (all 3 have identical tree `79f1f35afd2bef7fb6427129af0e05669391e243` and author `T3 Code <t3code@users.noreply.github.com>`). See `OBS-OUT-001`. |

### Explicit Skips and Verification Limitations

1. **`tests/methodology/test-migration.sh`:** Explicitly skipped per the review request (`All 13 tests/methodology/test-*.sh EXCEPT test-migration.sh`).
2. **Live Provider / Subagent / GitHub / Watcher Execution:** Not executed. No live `gh` network commands, PR creation/comments/merges, `watch_pull_request`, live `pr-wait` polling against GitHub, or nested `delegate_task` workflows were invoked. Live provider model availability and live watcher runtime behavior remain untested offline.
3. **Linux / Hosted CI / Product Gate UAT:** All checks ran locally on `macOS-27.0.1-arm64` with Python `3.13.10`, `bash 3.2.57`, and `ripgrep 14.1.1-cursor3`. No Linux or hosted GitHub Actions CI run was performed, and no real product `docs/project/` initialization or gate traversal was performed on the repository.

---

## 5. Findings, Tracking-Lag Classification, and Out-of-Scope Observations

### 5.1 In-Scope Advisory Findings (Non-Blocking)

#### `SK-IMP-001` — Minor subject-verb agreement typo in `modernize/SKILL.md`

- **Severity:** Low / Advisory (cosmetic prose only; no behavioral ambiguity)
- **Category:** In-scope documentation polish
- **Location:** `docs/methodology/dev-skills/modernize/SKILL.md:23-24`
- **Requirement:** Clear, accurate skill guardrail prose (`docs/resources/evolution/skill-library-import/README.md`).
- **Evidence / Reproduction:**
  Lines 22–24 of `docs/methodology/dev-skills/modernize/SKILL.md` read:
  ```markdown
  - A request to rebase and update the PR authorizes those scoped operations.
    An assessment-only request remains read-only. Neither request
    authorize merging, closing, changing the base branch, or expanding scope.
  ```
  (`Neither request authorize` -> `Neither request authorizes`).
- **Risk:** None; the prohibition against merging, closing, changing the base branch, or expanding scope is completely clear.
- **Proposed Fix (optional, if candidate is otherwise touched):** Change `Neither request authorize` to `Neither request authorizes` in `docs/methodology/dev-skills/modernize/SKILL.md:24` and update its digest in `import-manifest.json`.
- **Required Recheck:** Only if edited (`check-doc-coherence.sh` and `import-manifest.json` SHA-256 check).

---

### 5.2 Separate Classification: Pre-Review / Pre-Merge Tracking Lag

Per the review request (`Existing board and historical readiness text still describe pre-review/pre-merge state; classify that tracking lag separately`), the following files in `methodology-v3` at `d41e0ebfdc587ecc6d8c3ab336afc530ce90654f` accurately reflect the state *prior* to merging `integration/v3-skill-import` (`1516712`) into `main` (`d41e0eb`) and *prior* to this Council Round 1 review:

- **`TRK-LAG-001` (Expected Tracking Lag — Separate from Selected Skill-Import Code Conformance):**
  - **Locations:**
    - `docs/planning/board.yaml:24-40` and `docs/planning/active/skill-library-import/README.md:1-19` (list `branch: integration/v3-skill-import` and `next_gate: Authorize fresh independent review of pushed skill-import candidate 1516712; human acceptance pending`)
    - `docs/resources/evolution/skill-library-import/README.md:3-6`, `docs/resources/evolution/skill-library-import/review-readiness.md:3-6`, and `docs/resources/evolution/skill-library-import/validation-summary.json:2-3,24`
    - `AGENTS.md:274-276`, `docs/resources/releases/v3-adoption.md:14-18`, and `docs/resources/practitioner-guide/21-skill-library-and-workflows.md:45-53` (refer to the 9 workflow skills as `follow-up` on `integration/v3-skill-import` at `1516712` with independent review pending)
  - **Disposition:** Expected and proper at candidate freeze time; the lead agent records the Council Round 1 reports and updates board/readiness tracking during post-review closeout.

---

### 5.3 Out-of-Scope Observations (Background Migration / Harness Mechanics)

#### `OBS-OUT-001` — `scripts/verify-migration-inputs.py` rejects new-thread `ordinal/0` T3 checkpoint refs created when T3 spawns council review subagents

- **Severity:** Out-of-Scope Observation (Harness / preservation-verifier interaction; not a defect in the selected 26-file skill-library-import diff, and no original file or frozen ref was altered)
- **Location:** `scripts/verify-migration-inputs.py:31-37` (unchanged in candidate diff; part of the frozen `v3-migration` baseline)
- **Evidence / Reproduction:**
  1. When the lead agent launched the three Council Round 1 review subagents in T3 Code at `2026-10-28 19:26:10..13 -0400` (with workspace `/Users/chuckrussell/Dev/gendev/T3_Code_Sample`), T3 Code automatically wrote three new thread-checkpoint refs in `/Users/chuckrussell/Dev/gendev/T3_Code_Sample`:
     - `refs/t3/orchestration-v2/checkpoints/MDk3YTg2ZmI5MWFiZTMxM2I0NjY0YjhjMTk4OTZiZTg/ordinal/0` (`1e606430be4f3e4d5b90916a79574ba9f2dc5cd2`)
     - `refs/t3/orchestration-v2/checkpoints/MjEzMGJjNWYxNjMyYWJiMjAzODUxOGZjYjQ0ZGM0N2E/ordinal/0` (`7c259fd2739c341a177511ce13923d496e91e221`)
     - `refs/t3/orchestration-v2/checkpoints/YTllMDRjMzhmMjNlNjNjNzZmZmRlZWMzMGIzNGIwNmY/ordinal/0` (`784cbc898e67be11614abce8feb71c744064361d`)
  2. All three commits have author `T3 Code <t3code@users.noreply.github.com>`, commit message `t3 checkpoint ref=<ref>`, and tree `79f1f35afd2bef7fb6427129af0e05669391e243`—**the exact same tree** as the frozen anchor `refs/t3/orchestration-v2/checkpoints/ZjhjNzIxNWU0NTJkYzY2OTVlOGEwY2E3YTc3YTIwMDM/ordinal/36`. Furthermore, all 208 files/symlinks/modes and all frozen refs in `T3_Code_Sample` and `methodology-v2` are 100% unchanged.
  3. However, `compare_refs()` in `scripts/verify-migration-inputs.py:34` checks `if old_match and old_match[1] == match[1]:`, requiring any new T3 checkpoint ref to share the exact thread context ID (`old_match[1]`) of a frozen ref (`ZjhjNzIxNWU0NTJkYzY2OTVlOGEwY2E3YTc3YTIwMDM`). Because T3 Code assigns a new base64url context ID to each subagent thread (`ordinal/0`), `verify-migration-inputs.py` flags those 3 identical-tree T3 checkpoint refs as `unapproved added ref`.
- **Why this does not block `VERIFIED` for `skill-library-import`:**
  The pinned review request explicitly states: *"Approved same-tree additive T3 checkpoint refs may grow; never delete/reset refs. Preserve recovery and source skills."* Direct inspection of the 3 added refs confirms they are same-tree (`79f1f35afd2bef7fb6427129af0e05669391e243`), T3-authored additive checkpoint refs created by T3 Code's subagent dispatch at the start of this review (`19:26:10..13`), and every frozen ref, file digest, symlink, mode, and git status across `methodology-v2`, `T3_Code_Sample`, and `tstack/skills` is preserved intact.
- **Optional Future Maintenance Note (Out of Scope):** If future T3 subagent sessions continue to run while `T3_Code_Sample` is an active workspace in T3 Code, `scripts/verify-migration-inputs.py` (and its unit test `test_new_context_without_frozen_anchor_fails` in `tests/migration/test_preservation_refs.py`) would only accept new-context `ordinal/0` T3 checkpoint refs if the human owner explicitly broadens the checkpoint exception to allow identical-tree T3 checkpoint commits across any `refs/t3/orchestration-v2/checkpoints/<context>/ordinal/<n>` anchored to the frozen tree `79f1f35afd2bef7fb6427129af0e05669391e243`. Do not delete or reset the refs in `T3_Code_Sample`.
