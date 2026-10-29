# Skills council round 4 — Claude member report

## Outcome

**VERIFIED** for the declared delta/interaction scope only: AC-01 to AC-05 on the
five clarified skill instructions, and how they interact with the other four
imported skills and the shared execution contract.

Advisory score: **9/10**

This is not a VERIFIED result for the whole v3 baseline, and it does not record
acceptance, delivery or release. It covers no runtime fidelity, hosted CI or live
PR behaviour.

## Provenance

| Field | Value |
| --- | --- |
| Reviewer | Claude Opus 5.5 (`claude-opus-5-5`), Claude Code harness inside T3 Code |
| Context | Fresh, read-only. Given the pinned request only. No builder transcript, sibling outputs or prior council conclusions were used as proof. No agents were spawned. |
| Review window | 2026-10-29 00:35:52Z – 00:39:17Z (command phase), followed by static analysis and report |
| Repository | /Users/chuckrussell/Dev/gendev/methodology-v3 |
| Branch | fix/skills-council-follow-up |
| Candidate | 464cdec246996ebf5bc769174b22a4c62f82305e (HEAD at entry and at exit) |
| Delta base | 8abacf4b4b4a6d005cba3bdb92a68c9ce5d81376 (ancestor confirmed) |
| Runtime reference | aa25aa89762974012c0243e6134e9785f5db970d (ancestor confirmed) |
| Request | request.md, SHA256 45ea6546…5472 (matches) |
| Clarification diff | Reproduced with the git command in the request. SHA256 996a382e…0731 matches the clarifications.diff file. |
| Authority pins | All 10 entries in authority-manifest.json match at the candidate revision and in the worktree. |
| Controlling directive | review/advisory-clarifications.md (pinned, 2490148e…) |

## Commands and results

All logs are in `logs/`. Every shell batch sourced `env.sh`, which:
- puts the real ripgrep 15.2.0 binary first on PATH (Mach-O arm64, the codex-path vendor `rg`);
- sets `UV_OFFLINE=1` and `PYTHONDONTWRITEBYTECODE=1`;
- sets an external `TMPDIR`;
- uses the repository as the working directory.

The doctor ran first.

| # | Command | Exit | Result |
| --- | --- | --- | --- |
| 01 | `./scripts/gendev-doctor.sh` | 0 | All prerequisites present (bash, git, python3, rg) |
| 02 | `./scripts/check-methodology.sh` | 0 | Passed, 0 warnings |
| 03 | `./scripts/check-doc-coherence.sh` | 0 | Clean |
| 04 | `uv run --frozen --group devboard python scripts/devboard.py validate` | 0 | Passed, 3 tasks |
| 05 | `… devboard.py next` | 0 | Selects `v3-baseline-migration` (owner priority; not changed) |
| 06 | `… devboard.py show skill-library-import` | 0 | `started`, `implementation_authority: granted`, branch matches, next gate is round 4, acceptance pending |
| 07 | `python3 scripts/verify-migration-inputs.py` | 0 | PASS. Originals and frozen refs preserved. Only approved additive identical-tree T3 checkpoint refs (ordinals 70–72) |
| 08 | `git diff aa25aa8 464cdec -- scripts tests .github requirements-devboard.txt pyproject.toml uv.lock` | 0 | **Empty** |
| 09 | `python3 -I -B scripts/integrity.py` (external script) | 0 | 200 PASS, 0 FAIL (detail below) |
| 10 | `pr-wait --help` (python3 -I -B, scratch HOME); YAML `safe_load` of 4 UI files via the devboard uv env | 0 / 0 | Help printed; 4 dicts with an `interface` key |
| 11 | `gh pr create --help` (local only) | 0 | Without `--base`, gh uses `gh-merge-base` config, otherwise the repository default branch. This confirms why an explicit `--base` is needed. |
| 12 | Exit state | — | HEAD and branch unchanged. Porcelain status empty (no tracked or untracked drift). |

`integrity.py` checked:
- **Import manifest (14 entries):** source digests, candidate-tree and worktree destination digests, `changed` flags, and git/worktree modes all match. The source tree holds exactly these 14 files.
- **Support files:** all 5 unchanged support files (`pr-wait` and 4 `openai.yaml`) are byte-identical across source, aa25aa8, 8abacf4 and the candidate, with modes unchanged.
- **Discovery links:** all 9 are committed symlinks (mode 120000) to `../../docs/methodology/dev-skills/<name>` and resolve.
- **Skill entries:** all 24 have frontmatter, a `name` that matches the directory, a non-empty description, and every relative Markdown link resolves.
- **pr-wait:** `ast.parse` and `compile` ran in memory only.
- **Practitioner Guide:** the canonical guide and its HTML `content/` mirror match exactly (23 files), and neither has changed since aa25aa8.
- **Frozen records:** the frozen input manifest and the checkpoint-exception approval are unchanged since aa25aa8.
- **Delta scope:** since 8abacf4, the only changes under methodology, scripts, tests, `.agents`, `.github` or tooling are the five SKILL.md files. The remaining 20 changed paths are under `docs/planning/` or `docs/resources/evolution/skill-library-import/`: digest, tracking and evidence records.

Skipped, with reasons:
- **409/17/48 suites not rerun.** The runtime is unchanged (check 08 is empty) and the request scopes this as a wording-only cycle. No fresh suite result is claimed.
- **No live `pr-wait` watch, PR creation, rebase or GitHub call.** These are forbidden by the request.
- **No `py_compile` on candidate paths.**

## AC-to-primary-evidence map

Line numbers refer to the candidate (464cdec).

### AC-01 — babysit-pr

`docs/methodology/dev-skills/babysit-pr/SKILL.md`, read as a whole:
- **84–88:** verify each bot finding against the source; fix real findings; explain dismissed false positives with reproducible evidence.
- **93–94:** never bypass a required check or review.
- **96–101 (changed):** only an optional preference or a verified false positive may be declined, and only after documenting the reason and evidence. Reply/resolve needs authorization. Actual mandatory findings keep their required remediation or scope/risk disposition "regardless of rarity".
- **105–114:**
  - Security, contract, permission and data-loss violations stay mandatory on rare paths.
  - In-scope mandatory findings are fixed; out-of-scope ones are reported for disposition rather than silently implemented or waived.
  - A written dismissal does not satisfy remediation or authorize merging.
  - The declining rule (now including verified false positives) needs documented reason and evidence.

The relaxation in the base text ("feedback you believe is not worth addressing") has been removed. The readiness paragraph (125–131) and the `pr-wait` qualifiers (54–60: "not the repository's complete review requirements … neither mode supplies merge authority") add no relaxation: merging over an undisposed mandatory finding would be the silent waiver that 108–111 forbid. **Satisfied.**

### AC-02 — file-pr

`docs/methodology/dev-skills/file-pr/SKILL.md`:
- **11–15:**
  - an existing PR keeps its actual base;
  - a new PR uses the caller's selected target, or the intended target is resolved and recorded first;
  - the default is used only when appropriate;
  - the review diff is taken against that target;
  - no silent retargeting.
- **49–52:** pass `gh pr create --base <selected-target>` or the API `base` field, never rely on a CLI or configuration default, and verify the returned base and head.
- **55:** the REST fallback carries `-f base=...`.

Cases checked before any PR exists:

| Case | Selected target | Creation | Review diff |
| --- | --- | --- | --- |
| Release | release/1.x in a main-default repo | `--base release/1.x` | against release/1.x |
| Stacked | feature/parent | `--base feature/parent` | against feature/parent |
| Usual | main | explicit `--base main` | against main |

In all three cases the post-create base/head check catches drift from the `gh-merge-base` default. **Satisfied.**

### AC-03 — sol-loop

`docs/methodology/dev-skills/sol-loop/SKILL.md`:
- **42–44:** an existing PR uses `baseRefName`.
- **45–49:** before a PR exists, use `merge-base HEAD origin/<selected-target>`. If no target is recorded, resolve and record it first, using the default only when appropriate. Never silently review a stacked or release change against another branch.
- **49–51:** with no remote, use a named base commit, or `HEAD` for uncommitted changes only. Missing formal-review authority blocks formal validation instead of supplying an inferred base. This is consistent with lines 36–38 and validation policy 58–59 and 77.

**Satisfied.**

### AC-04 — full-send and full-stop

- **full-send 45–46:** a separate task branch is created when the checkout is on the default branch **or** the selected target, and task work stays off both.
- **full-send 22:** the force-push grant is limited to the PR's own branch.
- **full-send 118–120:** force-pushing any other branch requires asking.
- **full-stop 22–25:**
  - commit, push and force-with-lease are allowed only on this task's branch;
  - never merge, auto-merge, use a merge queue, push directly to the default or selected target, bypass protection, or delegate those actions;
  - work only on a separate task branch.
- **full-stop 27–29:** disable auto-merge and remove the PR from the queue.

Cases:
- **Checkout on release/1.x, target release/1.x, main-default repo:** a task branch is created. full-stop may not push to release/1.x or main.
- **Checkout on feature/parent, stacked target feature/parent:** same outcome.

**Satisfied.**

### AC-05 — full-send merge gate and full-stop inheritance

**full-send 83–98:** "all of these are true".
- **Bullet 3:** applicable independent validation and human approvals must be recorded; Sol APPROVE is not VERIFIED.
- **Bullet 4 (changed):**
  - unresolved mandatory findings block readiness and need human disposition;
  - dismissal cannot satisfy remediation or authorize merging;
  - only optional preferences or verified false positives may be dismissed, with reason and evidence;
  - human risk decisions follow governing authority and do not fabricate VERIFIED.
- **Bullets 5–6:** no outstanding change request; actual base equals the selected target, the branch is up to date, and GitHub reports it mergeable.

Supporting rules:
- **full-send 114–117:** if the gate cannot pass, ask the user.
- **full-stop 33:** uses full-send's gate as the readiness check, and keeps the merge ban (lines 12 and 22–25).
- **Independent validation policy 136–139:** human risk acceptance does not rewrite a validator result.

Static cases:

| Case | babysit-pr / sol-loop | full-send gate | full-stop |
| --- | --- | --- | --- |
| Rare-path permission bypass, in scope | Mandatory (bp 107–108, sol 88–90, 98–99). Fix. | Blocks (bullet 4). Dismissal is ineffective. Bullet 3 still needs validation. | Not "Ready"; Blocked. Never merges. |
| Out-of-scope data loss | Report for disposition (bp 108–110, sol 106–107) | Blocks until human disposition under authority; ask (114–117). Disposition is not VERIFIED (bullet 4 + bullet 3). | Blocked or handoff with the risk reported. Never merges. |
| Optional style preference | Decline with documented reason and evidence; follow-up (bp 112–113, sol 105) | Dismissal permitted | Does not block |
| Evidence-proven false positive | Decline with reproducible evidence (bp 87–88, 96–97; sol 104) | Dismissal permitted | Does not block |
| Ordinary defect in the intended case | Real finding: fix (bp 86, full-send step 5) | Blocks until fixed and re-proved | Blocks until fixed |

No single condition is treated as sufficient: the bullets are joined by "all of these are true". **Satisfied.**

### Cross-skill target propagation (request check 8)

The selected target flows through the workflow as follows:
1. **full-send Target base (36–39):** selects and records the target.
2. **sol-loop (45–49):** uses the "caller's selected target" for the merge-base.
3. **file-pr (11–14, 49–52):** uses the same target for the review diff and `--base`, then verifies it.
4. **babysit-pr (118):** works against the PR's actual base.
5. **full-send gate (96–98):** requires actual base = selected target, with a recheck before merging.

Related skills:
- **takeover (19–21, 30, 40):** uses the intended base, an honoured stacked continuation, and file-pr.
- **modernize (18–19, 37):** uses the PR's actual base.
- **Execution contract (65–67):** forbids a hard-coded default branch.

No contradiction was found among the nine skills.

## Findings

No mandatory findings. No blocker, critical, high, medium or low severity violation was established within scope.

## Advisory suggestions (optional, out of AC scope)

None of these block VERIFIED. All are wording polish, and none violates AC-01 to AC-05.

| ID | Location | Suggestion |
| --- | --- | --- |
| R4-CL-A1 | `full-send/SKILL.md:38-39` | The recorded target is said to be used "for rebasing and readiness". It reaches review only through the sol-loop and file-pr phrase "caller's selected target". Adding "review" here would put target propagation in one place (least astonishment), but the current chain is already coherent. |
| R4-CL-A2 | `full-stop/SKILL.md:42-43` | "Waiting for required approval: only human approval remains" could be confused with a pending human *disposition* of a mandatory finding. Lines 33 and 43 ("Confirm that this is the actual blocker") already keep that case from being "Ready to merge". An explicit "an unresolved mandatory finding is Blocked" would remove any doubt. |
| R4-CL-A3 | `file-pr/SKILL.md:52` | Says to verify the returned base and head but not what to do on a mismatch. full-send 98 ("a changed target requires reconciliation") covers the composed workflow; standalone file-pr could add "stop and report". |
| R4-CL-A4 | `babysit-pr/SKILL.md:94` (unchanged) | "CodeRabbit may be advisory" refers to the bot's check status, not finding severity. Lines 106–108 already classify findings against approved requirements. Noted only so no one reads it as a relaxation. |

## Limits

- **Static instruction analysis only.** These are instructions, not executable controls. Agent compliance in practice was not tested, and no live gh, GitHub, PR or watcher actions were run.
- **Constitution reading was targeted, not exhaustive.** I read the code-quality principles, Rules 4–8 and the Review Standard. The other ~2,000 lines were not re-read for this wording-only delta.
- **Builder evidence was not used as proof.** `advisory-validation/*`, `advisory-counterexamples.json` and the prior council directories were not read.
- **Pre-existing ignored bytecode.** `docs/methodology/dev-skills/babysit-pr/scripts/__pycache__/pr-waitcpython-313.pyc` (2026-10-28 20:16:45 local) and `scripts/__pycache__/*.pyc` predate this review. They are ignored (not governed) and were not created or touched here: this review used Python 3.14 with in-memory compile and `-B`.
- **No unauthorized external effects.** The uv lock file in scratch TMPDIR is disposable. No PR #2 interaction, board change, ref change or network call was made.
