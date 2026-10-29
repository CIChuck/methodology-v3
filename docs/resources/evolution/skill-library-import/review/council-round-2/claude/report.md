# Skills council round 2 — Claude Opus 5.5 report

**Formal outcome: CHANGES_REQUESTED**
**Advisory score: 8/10** (advisory only; not acceptance)

## Identities and provenance

| Item | Value |
| --- | --- |
| Member | Claude Opus 5.5 (`claude-opus-5-5`), Claude Code harness in T3 Code |
| Context | Fresh, single pass. No builder transcript, sibling reports or round-1 reports/conclusions read. Findings ledger read only as reproduction targets. |
| Request | `request.md` SHA256 `d3982d502fe00042f9e274ec66ee9809e2b2a10668fc9fe127f84fdb729477ba` (verified at start and end) |
| Repository | `/Users/chuckrussell/Dev/gendev/methodology-v3` |
| Branch | `fix/skills-council-follow-up` |
| Frozen candidate | `aa25aa89762974012c0243e6134e9785f5db970d` (HEAD at start and end, 0 dirty entries) |
| Base | `ee82653ed6cacb9e1157cd791f12d0fb774f12af` |
| Prior candidate (remediation comparison) | `d41e0ebfdc587ecc6d8c3ab336afc530ce90654f` |
| Selected diff | `selected.diff` SHA256 `d34f9b633a639eebe2e9b6bb31cc50ce941b777c3a59cba1c18d1363a88ba0ca`. I regenerated it with the request's exact `git diff --binary` command and got the same hash. |
| Authority | All 12 `authority-manifest.json` entries match at the candidate commit and in the working tree, at start and end (`logs/final-drift.log`) |
| Source skills | `/Users/chuckrussell/Dev/gendev/tstack/skills` at `1085050f3baed1ac724caa4a8166145fb2ac88af` (matches `source_commit`), clean |

Environment, sourced before every shell batch (`env.sh`): any `rg` shell function/alias unset; the real
bundled rg dir `/opt/homebrew/lib/node_modules/@openai/codex/node_modules/@openai/codex-darwin-arm64/vendor/aarch64-apple-darwin/codex-path`
prepended to PATH (ripgrep 15.2.0); `UV_OFFLINE=1`, `PYTHONDONTWRITEBYTECODE=1`, `TMPDIR=<this folder>/tmp/`; cwd set to the absolute repo path.
Doctor ran before every batch and always exited 0, with `Prerequisite rg: present`. No stubs, installs or downloads.

## Required commands

| Command | Result | Log |
| --- | --- | --- |
| `./scripts/gendev-doctor.sh` | exit 0; all prerequisites present; authority context; project not initialized | `logs/gendev-doctor.log` |
| `./scripts/check-methodology.sh` | exit 0, 0 warnings | `logs/check-methodology.log` |
| `./scripts/check-doc-coherence.sh` | exit 0, clean | `logs/check-doc-coherence.log` |
| `uv run --frozen --group devboard python scripts/devboard.py validate` | exit 0, 3 tasks | `logs/devboard-validate.log` |
| `… devboard.py next` | exit 0; selects `v3-baseline-migration` (priority 1; owner-controlled, as the request anticipated) | `logs/devboard-next.log` |
| `… devboard.py show skill-library-import` | exit 0; `started`, `granted`, branch `fix/skills-council-follow-up`, delivery `local` | `logs/devboard-show.log` |
| `./scripts/test-methodology.sh` | exit 0; 13 suites including `migration`; 409 checks pass, 0 fail (checker 31, lifecycle 236, the other 11 suites 142) | `logs/test-methodology.log` |
| `python -m unittest discover -s tests/devboard -v` | 17 tests OK | `logs/unittest-devboard.log` |
| `python -m unittest discover -s tests/migration -v` | 48 tests OK | `logs/unittest-migration.log` |
| `python scripts/exercise-v3-toolkit.py <this folder>/exercise-output.json` | PASS, 4 isolated scenarios, explicit external output | `logs/exercise.log`, `exercise-output.json` |
| `python3 scripts/verify-migration-inputs.py` | exit 0. At the start, 34 approved T3 additions, including 9 refs in 6 new contexts, each anchored to frozen `…ZjhjNz…/ordinal/36`. At the end, exit 0 again with 36 additions, because live T3 checkpoint streams kept growing during the review. | `logs/verify-migration-inputs.log`, `logs/final-drift.log` |

## Additional evidence

- **Offline skill checks** (`scripts/offline_checks.py`, `logs/offline-checks.log`; `scripts/frontmatter.py`, `logs/frontmatter.log`):
  - All 14 source-inventory digests and modes match the live source, and the inventory covers every file in the nine source folders.
  - All import-manifest destination digests match.
  - All 5 unchanged support files (`pr-wait`, 4 × `agents/openai.yaml`) are byte- and mode-identical to the source; `pr-wait` is 755.
  - 24 discovery entries; every `.agents/skills/*/SKILL.md` resolves.
  - YAML frontmatter is valid and `name` matches the entry for all 24.
  - UI metadata parses.
  - All relative Markdown links inside the bundles resolve.
  - The source tree has no nested non-entry SKILL.md files.
  - My first frontmatter regex was too strict and gave false FAILs on folded/`metadata` frontmatter. Those lines remain in `offline-checks.log`, and the YAML parse replaces that check.
- **pr-wait** (`logs/mirror-prwait-preservation.log`): AST parse OK. `--help` exits 0 with no GH token, a fake HOME and no state dir created. No live watch was run.
- **Guide mirror**: 23 canonical files and 23 HTML content files; filenames identical and `diff -r` clean.
- **BF-03 counterexamples** (`scripts/bf03_probe.py`, `logs/bf03-candidate.log`, `logs/bf03-prior.log`):
  - Candidate: 22/22 cases behave as expected.
  - Passes: existing-context next ordinal, and new contexts (ordinal 0 or any ordinal) with the frozen tree.
  - Fails, as required: new context with a different tree or with only an older non-latest frozen tree; no frozen T3 anchor at all; new contexts that chain only to each other; wrong subject, author or email; subject naming another ref; ref to a tree, blob or annotated tag; rewritten or deleted frozen ref; same-ordinal rewrite; non-increasing `01`; non-T3 ref; other `refs/t3` namespace; approval absent; context name outside the regex.
  - Prior verifier: 20/22. It wrongly rejects both valid new-context cases, which reproduces COD-SK-001.
- **BF-02 / SK-04 counterexamples** (`scripts/bf02_and_install_probe.sh`, `logs/bf02-install-probe.log`):
  - Setup: a disposable clone at the candidate plus a probe commit adding nested files: `council/references/notes.md`, `council/references/example/SKILL.md`, `council/extra.md`, `council/examples/deep/x/SKILL.md`, a flat `flat-probe.md` and a direct bundle `probebundle/SKILL.md`, all with valid `name:` frontmatter.
  - Candidate dry-run: 26 entries. All 4 nested files are copied byte-for-byte and none is discovered. The flat and bundle probes are discovered and resolve. `pr-wait` is 755. Board has 0 task rows; no `docs/project` (G1 pending).
  - Prior dry-run: 30 entries; all 4 nested files were wrongly discovered.
  - Fresh install (`install-methodology.sh`) from the probe clone: 24 entries, all resolving. Nested files are copied and not discovered. Installed doctor exits 0.
- **Regressions fail before the fix** (`logs/regressions-against-prior.log`): the candidate's two new tests, run against the d41e0eb scripts, both FAIL (`unapproved added ref…` and `unsafe target parent: .agents/skills/example-note`).
- **Frozen inventory and approval**: `git diff ee82653 aa25aa8` on `input-manifest.json` and `checkpoint-exception-approval.json` is empty, so both are unchanged.

## Criterion mapping

- **SK-01 (met):**
  - Nine imports: babysit-pr, council, file-pr, full-send, full-stop, leaving-pr-comments, modernize, sol-loop, takeover.
  - Metadata, UI and links are valid.
  - Source digests are exact; helper/UI bytes and modes are unchanged.
  - 24 skills are discoverable in the source, a fresh install and the dry-run.
  - Evidence: offline/frontmatter logs, bf02-install-probe, exercise.
- **SK-02 (not met; F-01):**
  - All nine SKILL.md files and the shared contract were read end to end.
  - BF-01 is resolved in sol-loop (lines 25–28, 81–85, 93–102).
  - council requires explicit invocation and limits PR edits to authorized scope (lines 3, 51–53).
  - full-send's merge gate now requires GenDev validation and approvals (lines 79–81).
  - The modernize typo is fixed (line 24).
  - babysit-pr distinguishes its helper modes from required reviews (lines 54–60).
  - One residual instance of the SKL-C-01 defect class remains in babysit-pr (F-01).
- **SK-03 (met, static review only):**
  - council and sol-loop use `orchestrator_capabilities` before `delegate_task`, with settings in `target.options`.
  - Each recheck is a fresh delegate; no provider substitution; Sol starts no subagents.
  - babysit-pr: only the owning thread watches; delegated children never watch; unwatch at handoff; never both watchers; no polling or sleep loop in T3.
  - Contract lines 49–68 agree with these rules.
  - Live provider and watcher workflows were not tested.
- **SK-04 (met):**
  - Selection happens before traversal (`allowed_paths`, owned_only).
  - Full bundles, empty board, G1 pending and provenance in the dry-run record are present.
  - Live AGENTS.md, policies and board history are not copied (create-dry-run.py:59–74).
  - Nested reference Markdown is copied without discovery; flat-root and direct-bundle entries are still discovered (probe above).
- **SK-05 (met):**
  - All required checks pass.
  - Originals, frozen refs and inventory are preserved. The verifier passes on real T3_Code_Sample with new contexts, and the negative cases fail.
  - Records consistently state that PR #1 is delivery, not acceptance; the remediation is local and acceptance is pending; inherited 1.0.2 and unreleased v3 are kept distinct.
  - The guide mirror is exact.
  - Nothing here infers Linux, hosted CI, product UAT, release or acceptance.

## Findings

### F-01 — Medium, mandatory — babysit-pr still allows declining real bugs outside the intended case

- **Path:** `docs/methodology/dev-skills/babysit-pr/SKILL.md:102-107`. The text is unchanged from the source at `tstack/skills/babysit-pr/SKILL.md:96-97`.
- **Violated requirement:** SK-02. Rare security, contract, permission or data-loss violations must not become optional. Contract `skill-execution-contract.md:45-47` says such violations stay mandatory "even when rare or outside the happy path". This is the defect class BF-01 / SKL-C-01 fixed in sol-loop.
- **Reproduction:** read lines 102–107: "Fix real bugs in the intended case. Decline the rest with a written reason … guards for edge cases that do not matter …". Read literally, "the rest" includes real bugs on unintended or rare paths.
  - full-send step 5 (`full-send/SKILL.md:44-45`) delegates review handling to babysit-pr.
  - full-send's merge gate (line 82–83) accepts findings "dismissed with a written reason".
  - So an autonomous full-send run could decline a bot-reported rare-path permission or security bug and then merge.
- **Risk:** the skill text conflicts with its governing contract on a mandatory-severity rule, in the most autonomous (merge-capable) path. The contract link at line 8 and the line 93 reference to repository requirements reduce the risk but do not remove the contradiction.
- **Fix:** a small wording change at lines 102–104, matching sol-loop:
  - Fix real bugs in the intended case.
  - Security, contract, permission and data-loss findings stay mandatory even on rare paths; report out-of-scope mandatory ones for disposition.
  - Decline only optional preferences, with a written reason.
- **Recheck:** read babysit-pr lines 102–107 against contract lines 45–47 and sol-loop lines 81–85 and 100–102, then rerun check-methodology, check-doc-coherence and the skill metadata checks.

### F-02 — Low, advisory — full-send hard-codes the default branch

- **Path:** `docs/methodology/dev-skills/full-send/SKILL.md:41-42,85`
- **Requirement:** contract `skill-execution-contract.md:65-66` says to use the actual PR base, not a hard-coded default branch. This is the same topic as SKL-L-03, which was fixed in babysit-pr and modernize.
- **Reproduction:** step 4 says "Rebase onto the latest default branch first", and the merge gate says "up to date with the default branch". full-send also takes over work "from its current state", which can be an existing PR stacked on a non-default base.
- **Risk:** in that case the agent would rebase the stacked PR onto the wrong base, widening its diff. PRs that full-send files itself through file-pr usually target the default branch, so the impact is limited.
- **Fix:** say "the PR's actual base branch (usually the default branch)".
- **Recheck:** grep for "default branch" in full-send.

### F-03 — Info — verifier anchor choice

- **Path:** `scripts/verify-migration-inputs.py:51`
- A new context anchors to the highest-ordinal frozen checkpoint across all frozen contexts. With the pinned inventory (one frozen context, ordinals 0–36), that is exactly "the frozen checkpoint" named in the approval.
- If a frozen inventory ever held several contexts with different latest trees, the choice by max ordinal and then name would be arbitrary.
- The regex `[A-Za-z0-9_-]+` would also reject padded base64 context names. None have been observed.
- No action is required for the current authority.

## Untested, skipped and limits

- Not run, by design and authorization: live `pr-wait` watch, GitHub/gh calls, `watch_pull_request`, provider delegation, council/sol-loop/full-send execution, PR or network effects.
- Not tested: Linux or hosted CI, product gate UAT, release, acceptance.
- No `docs/project` initialization in the source. The synthetic initialization ran only inside the inherited installed-context suite.
- Every governed path was read-only.
- Fixture Git operations ran only in disposable clones under `tmp/`, which were deleted. The uv lock files that remain under `tmp/` are cache artifacts.
- Concurrent reviewers could add T3 refs. The verifier passed at both the start and end of the review despite that growth.
- One bounded pass; no historical audit beyond the selected and remediation diffs.

## Verdict basis

Every mandatory check passes and SK-01, SK-03, SK-04 and SK-05 are met with cited evidence. BF-02 and BF-03 are correctly implemented and protected by regressions shown to fail before the fix. BF-01 is resolved in sol-loop, but one mandatory SK-02 inconsistency of the same class remains in babysit-pr (F-01). A VERIFIED outcome requires no mandatory violation, so the outcome is CHANGES_REQUESTED for human disposition. No remediation was performed, and this report starts no further round.
