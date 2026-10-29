# Round 3 independent instruction review

Formal outcome: **VERIFIED**

Advisory score: **9.5/10**. The score is judgment, not acceptance or the formal result.

No unresolved mandatory findings in the declared scope. This result covers one full nine-skill instruction-consistency pass and conformance of the two authorized wording corrections. It does not verify the whole v3 methodology, repeat its runtime audit, accept the work, authorize delivery, release or deployment, or advance a product gate.

## Provenance and pins

- Reviewer: GPT-6.1 Sol (`gpt-6.1-sol`), high reasoning, Codex harness in T3 Code, external evidence provider `codex`.
- Produced by: independent review context for this assignment; produced with local read-only Git/Python/uv/shell tools. Agent identity: `/root`, acting solely as assigned reviewer. No agents or workflows invoked.
- Produced on: 2026-10-29 UTC. Exact evidence and exit timestamps are in `audit.json` and `exit-state.json`; first captured command evidence time is the creation time of `doctor.log`.
- Derived from: complete pinned request `../request.md`, SHA256 `d990829215135206149c76788d4d03536a5574b9696f3b8bdcb08a012cdd394f`; candidate `5e2ab4047a69c82fc883735134c23527197b3c1e`, branch `fix/skills-council-follow-up`.
- Full instruction base: `ee82653ed6cacb9e1157cd791f12d0fb774f12af`.
- Wording delta base: `f6de7a2e121a2bf26c0d306f7451568854c5d2d5`.
- Unchanged runtime reference: `aa25aa89762974012c0243e6134e9785f5db970d`.
- Reproduced full scoped binary diff: `skills.diff`, SHA256 `c39031a5c45b63fb344bd12c71a9e20f195fe2616590155529b93e51c89db0c9`.
- Reproduced wording diff: `wording.diff`, SHA256 `a87b5c759d315026f296dca18fa52cb871ee4aad7ba4d6e1f238ab796aa09423`.
- Authority manifest: `authority-manifest.json`, SHA256 `5745339f6d33bfe9d0d94e81a68da6409cbba9b464a361346fa4f8495c3f31f5`. Every listed authority was read and every byte hash and revision independently verified. Individual hashes are preserved there and in `audit.json`.

Freshness: no builder transcript, private reasoning, sibling report body, prior council conclusion document, historical validation result or builder check was read as evidence. The board's required `show` output includes historical status/link labels; those labels were not used to establish conformance. Repository AGENTS, pinned primary authority and current source were read. Shared context consists of the assignment and harness/repository instructions, not an implementation session. No external network, credential use, PR effect, installation or persistent configuration change occurred.

## Criteria to evidence

| Criterion | Independent evidence and result |
| --- | --- |
| W-01 mandatory finding classification | Complete reading of babysit-pr, sol-loop, full-send and shared contract. Babysit-pr lines 102–110 explicitly preserve rare security/contract/permission/data-loss requirements, restrict optional declines, require out-of-scope disposition and forbid written-dismissal substitution. Static scenarios below pass. |
| W-02 actual target base | Full-send lines 34–39, 48–50 and 92–94 retain existing targets, explicitly select new targets, use the target for rebase/readiness and reconcile changes before merge. Full-stop lines 11–18, 22–38 inherit readiness and prohibit merge/auto-merge/queue. Static scenarios below pass. |
| W-03 whole instruction consistency and packaging | Read all nine complete SKILL.md files plus shared contract, not keyword-only checks. `audit.py`, `audit.log`, `audit.json`: all 14 source/destination digests and file modes; exact source file inventory; 24 valid name/description metadata entries; nine whole-folder symlinks; Markdown relative resources from canonical and discovery paths; bundled helper path; four parsed UI files with matching prompts. Five support files byte/mode-identical to source and runtime reference. All 30 pre-import skill tree entries (15 existing discovery entries and 15 canonical files) match the full instruction base. Seven other imported instruction files match runtime reference. |
| W-04 unchanged runtime and preservation | `runtime.diff` is empty for scripts, tests, .github, requirements-devboard.txt, pyproject.toml and uv.lock against aa25aa8. Frozen input manifest and checkpoint approval bytes identical to aa25aa8. Original-input verifier actually exits 0 at entry checks and exit: methodology-v2 284 files/links and T3_Code_Sample 208 files/links, inventories, bytes, symlinks, modes, working state and frozen refs protected. Only approved frozen-tree/expected-metadata additive T3 checkpoints are accepted. |
| Focused current checks | Doctor, methodology, coherence, board validate/next/show and original verifier all exit 0; helper AST syntax and --help exit 0; exact 23 filenames and Markdown bytes match HTML content and runtime reference. |
| Candidate stability | Entry clean status and exact HEAD; repeated checks in audit and final `exit-state.json` show clean worktree/index, same HEAD and branch. Authority file bytes also match frozen candidate blobs. |

## Static requirement counterexamples

These are instruction analysis, not GitHub, rebase, merge or workflow executions.

1. **Rare permission bypass:** suppose a bot identifies a bypass reachable only through an unintended request. Before the correction, babysit-pr's intended-case wording could decline it as an irrelevant edge guard. Current lines 104–108 classify it as mandatory regardless of rarity. Sol-loop lines 81–85 and 93–102 agree. Full-send's written-dismissal bullet cannot waive this explicit prohibition or the shared contract's mandatory-security rule and formal review requirements. Result: remediate within authority or stop for disposition; no merge by written dismissal.
2. **Out-of-scope data loss:** a valid finding lies outside the authorized files or goal. Current babysit-pr lines 105–108 require scope/risk disposition without silently fixing or waiving it. Sol-loop lines 101–102 likewise deny approval to ship. Shared contract lines 40–45 preserve budget/escalation and mandatory requirements. Result: return unresolved mandatory finding to human; no autonomous scope expansion.
3. **Optional style preference:** no approved requirement or real defect is violated. Babysit-pr lines 109–110 and sol-loop lines 25–28, 82 and 100 allow decline with reason/follow-up. This does not dilute mandatory categories.
4. **Usual intended-case defect:** approved behavior fails on the ordinary path. Babysit-pr lines 84–88 and 103–110 require verification and the smallest authorized correction. Full-send requires proof for fixes, final independent validation and required approvals. Scope limits still apply.
5. **Existing release PR targeting release/1.x while default is main:** the old full-send step directed rebase onto default and readiness against default. Current target section resolves and retains release/1.x, step 4 rebases onto that selected target, and the gate checks its actual base. File-pr lines 11–13 refer to the base, with origin/main only described as usual, not a command to override the recorded target. Babysit-pr lines 114–127 also follow actual base. No retarget is authorized.
6. **Stacked feature PR targeting feature/parent:** the same explicit retention rule selects feature/parent. A default-main rebase would violate full-send lines 36–39 and 48–50. Modernize lines 18–26 and 37–40 independently preserve actual-base and no-retarget boundaries; takeover lines 19–22 honor explicitly stacked continuation.
7. **Ordinary new PR intended for main:** select and record main explicitly when appropriate, rebase against it and verify readiness. Default branch remains a permissible target, not a universal assumption.
8. **Base or head changes after initial resolution:** full-send lines 92–94 require actual-base/head recheck and target reconciliation. Shared contract final paragraph requires identity recheck before external mutations; its independent-review section and validation policy make changed candidates stale. Babysit-pr requires current checks after rebase; full-stop requires final proof/review and a live base/head/checks/reviews check. A prior green run or old review cannot establish readiness of the changed candidate. No live mutation was performed to exercise this case.

## Complete nine-skill consistency pass

- **babysit-pr:** supported single watcher, T3 parent ownership, unwatch at handoff, scoped replies, actual-base readiness, explicit merge permission and mandatory findings agree with the shared contract. Helper ready mode explicitly does not represent all repository requirements.
- **council:** requested read-only scope stays read-only, provider availability cannot silently substitute, every round has fresh context, budget/escalation binds, scores remain advisory and PR description edits require scope. Reading this council skill did not invoke it.
- **file-pr:** existing-PR detection, goal/base review, model identity, draft/readiness choice, privacy checks and scoped comments do not override selected-base or formal approval requirements.
- **full-send:** explicit invocation controls effects; proof and final gate preserve GenDev approvals, current independent validation and branch protection. Narrow-change wording is bounded by explicit mandatory-security/contract rules and cannot waive them.
- **full-stop:** explicit PR workflow only; ordinary stop/pause stops work. Inherits target/readiness but removes merge rights, auto-merge, queue, default-branch pushes and delegation of those actions. Automatic merging must be prevented before work continues.
- **leaving-pr-comments:** attribution uses verified identities, privacy/format checks and successful posting precedes resolving a thread. This format instruction creates no posting permission; shared contract remains controlling.
- **modernize:** actual base/head, dirty-work preservation, explicit assessment versus update scope, separate REWORK/CLOSE decisions, observed-head lease and no merge preserve scope and effects.
- **sol-loop:** one reviewer, independent fresh rounds, exact formal versus advisory distinction, mandatory-category treatment, no automatic extra rounds, bounded remediation and escalation agree with contract and policies. Advisory APPROVE alone does not supply formal VERIFIED.
- **takeover:** original work/credit retained, current code independently inspected, stacked/in-place intent honored, intended base retained, no merge/close/comment grant from PR creation. Inherited workflows remain inside actual requested effects.

No new mandatory finding was established in this single bounded pass. No remediation or second review pass was performed.

## Commands, reproducibility and results

Every shell batch used repository cwd `/Users/chuckrussell/Dev/gendev/methodology-v3` and prepended the parent directory of the real existing rg binary:

```sh
export PATH=/opt/homebrew/lib/node_modules/@openai/codex/node_modules/@openai/codex-darwin-arm64/vendor/aarch64-apple-darwin/codex-path:$PATH
export PYTHONDONTWRITEBYTECODE=1 UV_OFFLINE=1
export TMPDIR=/var/folders/dh/wfnmsgpn1yl83xlbmc109sf40000gn/T/v3-skills-council-round3-k749snd7/codex/tmp
```

Initial batch removed any shadowing rg function/alias; real doctor ran first. No replacement binary, install or emulation was used. Doctor found bash, git, python3 and rg; initialized product: no; baseline acceptance: pending. No product initialization was attempted.

| Command | Exit | Evidence |
| --- | --- | --- |
| ./scripts/gendev-doctor.sh | 0 | doctor.log |
| ./scripts/check-methodology.sh | 0 | methodology.log; zero warnings |
| ./scripts/check-doc-coherence.sh | 0 | coherence.log |
| uv run --frozen --group devboard python scripts/devboard.py validate | 0 | board-validate.log; 3 tasks |
| uv run --frozen --group devboard python scripts/devboard.py next | 0 | board-next.log; v3-baseline-migration awaits human acceptance |
| uv run --frozen --group devboard python scripts/devboard.py show skill-library-import | 0 | board-show.log; started, granted, correct branch; round 3 next, acceptance pending |
| python3 scripts/verify-migration-inputs.py | 0, twice | originals.log and originals-exit.log |
| uv run --frozen --group devboard python /…/codex/audit.py | 0 | audit.py, audit.log, audit.json; replace /… with this external report's parent directory |
| Python ast.parse(helper source); absolute-helper-path --help | 0 | helper.log; syntax PASS, argparse help returned |
| git diff aa25aa8 5e2ab40 -- scripts tests .github requirements-devboard.txt pyproject.toml uv.lock | 0, empty | runtime.diff; exact full SHAs in pins above |
| git status --porcelain=v1 --untracked-files=all; git diff --exit-code; git diff --cached --exit-code; rev-parse HEAD; branch --show-current | 0 | exit-state.json |

`commands.json` records the seven main command invocations. `audit.py` reproduces exact diff hashes, authority hashes, original-manifest/approval equality, import metadata/hashes/modes, support identity, preexisting skill preservation, relative links/UI and guide mirror checks. External scripts use assertions as review checks only; no runtime code or essential application invariant was changed.

## Limits and disposition

Whole-library runtime tests, the historical 409/17/48 suites, replay/install scenarios, hosted/Linux CI, live providers, live watcher readiness, GitHub checks, real merges, rebases and remote branch protection were deliberately not rerun or claimed. No runtime drift exists in the specified paths, so this remains the authorized wording/instruction scope with runtime evidence pinned to aa25aa8. Syntax/help checks alone do not prove live watcher behavior. Static instruction conformance cannot guarantee future agent execution fidelity.

All output is external disposable evidence under this report directory. No candidate, board, branch, ref, source skill, recovery input or original project was edited. The validator result permits a recommendation for human disposition only; Chuck's acceptance remains separate.
