# Independent Skills Council Review — Round 1 — Claude member

**Formal outcome: BLOCKED**
**Advisory score: 7/10** (this rates the skill content and packaging only. It is not a validation result, and it does not offset the blocked evidence.)

Even if the evidence blocks were cleared, finding SKL-C-01 is a mandatory SK-02 defect. On the evidence obtained so far, the outcome would then be no better than CHANGES_REQUESTED.

## Provenance

- Reviewer: Claude Opus 5.5 (`claude-opus-5-5`) in the Claude Code harness inside T3 Code. This was one fresh context with no builder transcript, no prior verdicts and no sibling outputs read. I started no additional agents.
- Review window: 2026-10-28T23:26Z to about 23:45Z.
- Request: `request.md`, sha256 `bf0fa2f8…ed5ea` (verified).
- Repository: `/Users/chuckrussell/Dev/gendev/methodology-v3`, branch `main`, HEAD `d41e0ebfdc587ecc6d8c3ab336afc530ce90654f`. HEAD was unchanged at the start and at the end. The governed tree was clean apart from ignored files.
- Base: `ee82653ed6cacb9e1157cd791f12d0fb774f12af`.
- Selected diff: I reproduced it with the request's command. Its sha256 is `6818fab01b30764ed63cee1b214fd63b3fceed8f6a5062fcdcf450ccd4100b1c`, which matches `selected.diff` and the request.
- Authority pins: all 10 entries in `authority-manifest.json` match, both as `git show d41e0eb:<path>` and as the working-tree bytes.
- Source originals: `/Users/chuckrussell/Dev/gendev/tstack/skills` at `1085050f3baed1ac724caa4a8166145fb2ac88af`. The skills tree is clean. I only read it.
- Logs and scripts: `claude/logs/` and `claude/scripts/`. Disposable fixtures are in `claude/tmp/`.

## Commands, results, skips and limits

| Check | Result |
|---|---|
| `./scripts/gendev-doctor.sh` | **exit 3**: prerequisite `rg` is MISSING. This host has only a Claude Code shell function named `rg`, with no ripgrep binary on PATH. Under AGENTS.md I did not substitute or emulate it. |
| `./scripts/check-methodology.sh` | exit 0 (0 warnings) |
| `./scripts/check-doc-coherence.sh` | **exit 3** (requires rg); not run |
| devboard `validate` / `next` / `show skill-library-import` | 0 / 0 / 0. `next` points to `v3-baseline-migration`. `show`: state started, authority granted, delivery pushed, next_gate cites the old candidate `1516712` (tracking lag, see OOS-01). |
| 12 `tests/methodology/test-*.sh` (all except `test-migration.sh`) | Only `test-lifecycle-coherence` passed (236/0). `test-checker` exited 1 because `init-project.sh` refused to continue on the missing rg. The other 10 exited 3 on the rg preflight. **Not evidence.** The request says "13 … EXCEPT test-migration"; only 12 such files exist at d41e0eb (OOS-03). |
| `unittest discover -s tests/devboard` | 17 tests OK |
| `unittest discover -s tests/migration` | 42 run: **32 failures, 10 passes**. All 32 failures I checked trace to doctor/init refusing on the missing rg (31 "missing prerequisite" hits). The 10 passes cover preservation refs, refusal and rollback paths. |
| `exercise-v3-toolkit.py <claude/exercise-output.json>` | **exit 1**: `init-project.sh` refused on rg. No output was written, and the default governed evidence path was not touched. |
| `verify-migration-inputs.py` (default manifest, approval file present and valid) | **exit 1**. File contents and modes are preserved (methodology-v2: 284, T3_Code_Sample: 208). The failure comes from three unapproved added refs in new T3 checkpoint namespaces (SKL-B-02). |
| Source/destination digests and modes (14 manifest entries) | All match. The 5 support files are byte- and mode-identical (`pr-wait` 0755). Every source file is listed in the manifest and present in the destination. |
| Offline nine-skill metadata, UI and link checks (`scripts/skill_checks.py`) | Frontmatter parses. Each name equals its directory, descriptions are non-empty and under 1024 characters, and only allowed keys appear. Each discovery link is exactly `../../docs/methodology/dev-skills/<n>`. The contract link resolves both from source and through discovery. The four `openai.yaml` files parse, their fields are non-empty, and each `$skill` refers to itself. The two "unknown skill ref" hits are regex false positives on `` `--admin` `` and `` `--force-with-lease` ``. |
| `pr-wait` syntax and `--help`, offline | `compile()` OK. `--help` exits 0 with HOME pointing at scratch, a stripped PATH and no token. No state directory was created. |
| Fresh-install selection probe (`install_probe.py`, Python 3.14 and 3.13) | 24 `.agents/skills` entries. The 9 new ones are internal directory links. `pr-wait` is owned with mode 0755, and all 4 yaml files are present. |
| Dry-run probe (`dryrun_probe.py`) | Calls the real `build()` with **only** the doctor subprocess stubbed. This is labelled as non-substitute evidence. Result: 24 skills, `pr-wait` executable and byte-identical, yaml present, contract resolves for all 9, board `tasks: []`, no `docs/project` or `docs/resources`, `source_commit=d41e0eb`, `source_worktree_dirty: true`, no `.agents` in owned records. |
| Counterexample (local clone fixture plus one commit) | Reproduces SKL-L-05. |

Limits:
- Nothing was run on Linux or in hosted CI.
- No live GitHub, watcher, merge, comment or delegation behaviour was invoked. **Live provider and harness behaviour (T3 `delegate_task`/`watch_pull_request`, Claude Monitor, Codex) is untested.** SK-03 is assessed from text only.
- No product gate UAT was run.
- The checkout was shared with concurrent sibling reviewer processes. An untracked `.tmp/methodology-runtime-tools-*` directory appeared and then disappeared during my run (created 19:30:11 EDT by PID 61106, not by my commands; my runtime-tools run exited in 0s). I did not touch it.

## Criteria-to-evidence mapping

- **SK-01: met on static evidence. Full dynamic proof is blocked.** All nine bundles are complete, digests match, metadata and UI are valid, 24 skills are discoverable, and relative paths work from source, the fresh-install selection and the dry-run probe. The full regression that proves this (`test_fresh_install…`, `test_documented_fresh_dry_run…`) could not run (SKL-B-01).
- **SK-02: one mandatory defect (SKL-C-01) plus Low items.** The shared contract and the adaptations preserve gates, scope, stop semantics, fresh contexts, the two-cycle limit, human approvals and advisory scores. full-stop's narrowed trigger works well.
- **SK-03: met in text. Live behaviour is untested.** council and sol-loop resolve models at runtime and report rather than substitute. T3 rules are followed: `orchestrator_capabilities` before `delegate_task`, a new task per recheck, no thread messages or top-level threads, parent-owned `watch_pull_request`/`unwatch`, and no polling or Monitor in T3 (babysit-pr:16-39, contract:55-61).
- **SK-04: met on code inspection and the probe. The regressions are blocked.**
  - Selection still runs before traversal. The new branch only transforms already-selected entries (create-dry-run.py:75-87).
  - Supporting directories are complete because they come from the owned `docs/methodology` tree.
  - Owned-symlink and parent protections are unchanged. Discovery links are not owned (the `False` flag).
  - Live authority, runtime and unrecorded files are excluded, the board is empty, and provenance is honest.
  - Latent issue: SKL-L-05.
- **SK-05: source and helper preservation is met. "All required local checks pass" is NOT established** (SKL-B-01, SKL-B-02).

## Findings

### SKL-B-01: required evidence unobtainable (missing ripgrep). Severity: Blocker (evidence/environment)
- **Requirement:** SK-05 and the request's required checks. AGENTS.md says to stop when the doctor exits 3 and not to substitute.
- **Reproduction:** `./scripts/gendev-doctor.sh` prints "Prerequisite rg: MISSING", exit 3. `command -v rg` finds no binary; only the shell function exists. The consequences are listed in the table above.
- **Risk:** VERIFIED cannot be supported for SK-01, SK-04 or SK-05 dynamic behaviour.
- **Fix:** a human installs ripgrep on the review host, or assigns the checks to an equipped reviewer.
- **Recheck:** the full required command set.

### SKL-B-02: original-input verifier fails on new T3 checkpoint namespaces. Severity: Blocker (needs human disposition)
- **Requirement:** SK-05, the preserved originals, and the approved exception in `checkpoint-exception-approval.json`.
- **Reproduction:** `python3 scripts/verify-migration-inputs.py` exits 1 with these three refs reported as unapproved:
  - `refs/t3/orchestration-v2/checkpoints/{MDk3YTg2…,MjEzMGJj…,YTllMDRj…}/ordinal/0`
- **Read-only inspection of those refs:**
  - All three have tree `79f1f35afd2b…`, which is identical to the frozen anchor `…ZjhjNzIx…/ordinal/36`.
  - None has a parent commit. Each was authored by T3 Code at 19:26:10–13 EDT.
  - That time is the council dispatch, and this reviewer's workspace is T3_Code_Sample.
  - The verifier allows identical-tree additions only inside the anchored namespace, by design (`test_new_context_without_frozen_anchor_fails`).
- **Risk:** the preservation evidence now fails. The cause is probably environmental (the council launch) and not the candidate. Contents are intact.
- **Fix:** human disposition: either extend the approved exception to identical-tree initial checkpoints in new thread namespaces, or launch future reviewers outside the originals. Do not delete refs.
- **Recheck:** rerun the verifier.

### SKL-C-01: sol-loop reviewer brief downgrades rare-path mandatory violations to "nit". Severity: Medium (mandatory under SK-02)
- **Location:** `docs/methodology/dev-skills/sol-loop/SKILL.md:77-80`, together with :25 and :95.
- **Requirement:** SK-02 forbids ignoring mandatory findings. Contract :45-46 says "A mandatory contract or security violation remains mandatory even when rare or outside the happy path".
- **Reproduction:** read the round-1 brief. It says "Other paths, rare cases, small perf, extra compat: nits. … nit = rest." The budget rule at :25 says "Stop early if a round returns only nits", and :95 says "Out of scope or nit: decline in one line".
  - So an authorization bypass on a non-intended path is, by the brief's own taxonomy, a nit. The loop may then stop early and decline it.
  - The adapted controller sentence at :88-89 contradicts the brief, but the brief and stop rule were left unadapted.
- **Risk:** security or contract violations get labelled away. The result also feeds full-send's merge gate (full-send:40, :79-80).
- **Fix:** amend the brief so that mandatory contract, security, permission or data-loss violations are classified blocker or should regardless of path rarity. Make the early stop depend on the controller's own re-classification, not the reviewer's labels.
- **Recheck:** read sol-loop end-to-end for consistency, and get a fresh review of the changed candidate.

### SKL-L-01: council auto-trigger on the bare word "council". Severity: Low
- **Location:** `council/SKILL.md:3`, which reads "Trigger this if the user says 'council'".
- **Requirement:** SK-02 and contract :6-9 (mentioning a skill is not invoking it). full-stop's description was narrowed for exactly this reason, but council's was not. Unlike full-send (:16-17), council has no explicit-request guard in its body.
- **Risk:** incidental use of the word could start costly three-provider delegation. The contract header mitigates this.
- **Fix:** change the description to require an explicit council review request.
- **Recheck:** metadata validation.

### SKL-L-02: council publishes to the PR description without an authorization condition. Severity: Low
- **Location:** `council/SKILL.md:35, 51`, which read "If the PR is open, edit the description".
- **Requirement:** external-effect limits and contract :19-21.
- **Risk:** a read-only council review could edit a live PR.
- **Fix:** add "when PR edits are within the authorized scope; otherwise the final reply only."

### SKL-L-03: babysit-pr assumes `main` and specific bot brands. Severity: Low
- **Location:** `babysit-pr/SKILL.md:108` ("changes to `main`") and :54-57 (`ready` requires Greptile or Macroscope).
- **Requirement:** contract :65-66 says "not assumed bot brands or a hard-coded default branch".
- **Fix:** say "the PR's base branch". Choose `--until` from the verified repository requirements. The helper itself stays unchanged.

### SKL-L-04: full-send merge gate omits GenDev validation and lifecycle preconditions. Severity: Low/advisory
- **Location:** `full-send/SKILL.md:73-89`, :40 and :23.
- **What it does:** the gate relies on sol-loop's advisory APPROVE.
- **Why this is not mandatory:** the authority does not explicitly forbid a merge before VERIFIED, because merge is recorded as separate delivery evidence. It is covered only by the contract's reference to the lifecycle and validation policies.
- **Second point:** "without asking first" at :23 conflicts with project ask-first rules that the adapted text now says remain in force.
- **Fix:** add a gate bullet: "any GenDev-required independent validation and human approval for this work is recorded". Reword :23 to "within accepted authority and harness permissions".

### SKL-L-05: dry-run promotes bundle support Markdown with frontmatter into separate skills. Severity: Low (latent)
- **Location:** `scripts/create-dry-run.py:76-87`.
- **Reproduction:**
  1. In a local-clone fixture at d41e0eb, add `docs/methodology/dev-skills/council/references/notes.md` beginning with `---\nname: notes`.
  2. Commit it.
  3. Run `build()` with the doctor stubbed.
  4. Result: 25 skills, including `.agents/skills/notes/SKILL.md` linked to the reference file (log `counterexample-support-frontmatter.log`).
- **Why it matters:** fresh install and source discovery would not show this skill, so the dry-run diverges from them. A support file becomes discoverable.
- **Fix:** only derive discovery entries from `<bundle>/SKILL.md` or from flat files directly under `dev-skills/`. Add a regression test.
- **Recheck:** the migration tests.

### SKL-I-01: friday-dev-board discovery shape differs in dry-runs. Severity: Info
- Source and fresh install use a directory containing a `SKILL.md` link. The dry-run now uses a directory link.
- This works, and the test accepts both shapes. The adaptation note only talks about "flat-file skills", so this side effect is not documented.

## Out of scope (not counted toward the outcome)

- **OOS-01:** tracking lag, as anticipated. The board `next_gate` cites `1516712`, and README/readiness still say branch `integration/v3-skill-import` and "review pending" while the candidate has been merged as `d41e0eb`.
- **OOS-02:** shared-checkout concurrency between council members (the `.tmp/` above, T3 refs) makes runs interfere with each other. Isolate reviewer fixtures.
- **OOS-03:** the request's suite count. 12 non-migration suites exist, not 13; the builder's "13" includes migration.
- **OOS-04:** the dry-run record reports `methodology_version: 1.0.2` while the candidate is unreleased v3. This is pre-existing provenance semantics, outside the selected diff.

No repository files, refs, board, branch or originals were changed by this review.
