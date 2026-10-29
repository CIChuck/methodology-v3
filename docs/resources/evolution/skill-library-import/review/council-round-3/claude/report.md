# Skills council round 3: Claude member report

**Formal outcome: CHANGES_REQUESTED** (declared instruction/delta scope only)
**Advisory score: 7/10.** The score is advisory only. It is not acceptance, formal VERIFIED status or merge authority.

## Provenance

- Reviewer: Claude Opus 5.5 (`claude-opus-5-5`), Claude Code harness inside T3 Code, one council member.
- Context: fresh and read-only. I read no builder transcript, sibling report (`../codex/` not opened) or prior council conclusions (`review/council-round-*` not opened). I used no nested agents.
- Time: 2026-10-29T00:13:00Z to about 00:18Z (UTC).
- Request: `request.md` SHA256 `d990829215135206149c76788d4d03536a5574b9696f3b8bdcb08a012cdd394f` (verified).
- Repository: `/Users/chuckrussell/Dev/gendev/methodology-v3`, branch `fix/skills-council-follow-up`. HEAD was `5e2ab4047a69c82fc883735134c23527197b3c1e` at entry and at exit.
- Bases:
  - Full instruction base: `ee82653ed6cacb9e1157cd791f12d0fb774f12af`
  - Wording delta base: `f6de7a2e121a2bf26c0d306f7451568854c5d2d5`
  - Unchanged runtime reference: `aa25aa89762974012c0243e6134e9785f5db970d`
  - Both `aa25` and `f6de` are ancestors of the candidate.
- Diffs: I regenerated both with the stated commands, and both match byte for byte.
  - `skills.diff`: `c39031a5c45b63fb344bd12c71a9e20f195fe2616590155529b93e51c89db0c9`
  - `wording.diff`: `a87b5c759d315026f296dca18fa52cb871ee4aad7ba4d6e1f238ab796aa09423`
- Authority pins: all 10 entries in `authority-manifest.json` match at both `5e2ab40:<path>` and in the working tree. This includes `wording-follow-up.md` `1df6d6bc…`, the shared contract `ea5381d2…` and `checkpoint-exception-approval.json` `37c9fa3d…`.
- Tooling: the real `rg` 15.2.0 was first on PATH (the codex vendor path), with no alias or function shadowing it. Settings were `UV_OFFLINE=1`, `PYTHONDONTWRITEBYTECODE=1` and an external `TMPDIR`. No network was used.

## Commands and results

All logs are in `logs/`.

| Check | Result |
|---|---|
| `./scripts/gendev-doctor.sh` | exit 0; bash/git/python3/rg present |
| `./scripts/check-methodology.sh` | exit 0, "passed: 0 warning(s)" |
| `./scripts/check-doc-coherence.sh` | exit 0, "clean" |
| devboard `validate` / `next` / `show skill-library-import` (3 separate calls, uv `--frozen`, offline) | all exit 0; 3 tasks; task `started`, `implementation_authority: granted`, branch matches |
| `python3 scripts/verify-migration-inputs.py` | **exit 0**; methodology-v2 284 and T3_Code_Sample 208 files/links; 44 approved identical-tree T3 checkpoint additions; PASS |
| Frozen input manifest and checkpoint approval vs `aa25` | `git diff aa25 C -- docs/resources/evolution/v3-migration` is empty (0 bytes) |
| `git diff aa25 C -- scripts tests .github requirements-devboard.txt pyproject.toml uv.lock` | **empty (0 bytes)**, so there is no runtime drift |
| Import manifest (14 entries) vs source and destination bytes | all source and destination SHA256 values match; the `changed` flags are correct; modes are 0644, and `pr-wait` is 0755 (git 100755) |
| `source-inventory.json` (14) vs `tstack/skills` | all match; `tstack` HEAD is `1085050f…`, matching the recorded `source_commit`; the `tstack` tree is clean |
| Source/destination completeness | no unlisted source files and no unlisted destination files |
| Five support files (`pr-wait` + four `agents/openai.yaml`) | byte-identical to source, to `aa25` and to `f6de` |
| Changes since `aa25` and `f6de` within skills and contract | only `babysit-pr/SKILL.md` and `full-send/SKILL.md` |
| The other 15 skills since `ee82` | unchanged |
| Nine discovery links | whole-folder relative symlinks `../../docs/methodology/dev-skills/<n>`; all resolve |
| Metadata for all 24 `.agents/skills` entries | frontmatter present; `name` equals the folder; descriptions 40–366 chars; every relative markdown link resolves |
| New digests | referenced only in `import-manifest.json`; the old digests (`4fa88385…`, `90f0e537…`) are not referenced anywhere |
| `pr-wait` | `ast.parse` OK; `--help` exit 0 run under `env -i` with a disposable HOME; no live watcher was started |
| Practitioner Guide mirror | 23/23 filenames equal; 0 byte mismatches against `practitioner-guide-html/content`; both directories unchanged since `aa25` |
| Governed tree at entry and exit | `git status --porcelain --untracked-files=all` empty; `git diff --quiet 5e2ab40` passes |

**Incident (disclosed).** My `python3 -m py_compile` syntax probe wrote an ignored `docs/methodology/dev-skills/babysit-pr/scripts/__pycache__/pr-waitcpython-314.pyc` at 20:15 local time. `py_compile` ignores PYTHONDONTWRITEBYTECODE. I removed exactly that file and directory right away; tracked content was not affected. See `logs/incident-pycache.txt`. Other `__pycache__` files in the tree predate this review (Oct 27 23:32, Oct 28 18:24 and 19:56) and were left untouched.

**Skips and limits.**
- The static counterexamples are reading-based and are not live workflow tests.
- I did not rerun runtime suites (409/17/48). Runtime evidence stays pinned to `aa25`, which I proved unchanged; I make no fresh runtime claim.
- No Linux, hosted CI, product-gate or live GitHub claims.
- The HTML mirror check compares the content directory only. I did not inspect any rendered HTML.

## Criteria-to-evidence map

- **W-01: not satisfied, because of an interaction (R3C-01).**
  - The new wording in `babysit-pr/SKILL.md:103-110` is correct on its own terms and agrees with `sol-loop/SKILL.md:81-85,93-102` and the contract (`skill-execution-contract.md:43-47`).
  - The full-send merge gate it feeds into still accepts written dismissals.
  - Counterexample results:
    - Optional style: PASS (`babysit-pr:109-110`).
    - Usual intended-case defect: PASS (`:86` "Fix real findings" and `:109` "Decline only optional preferences").
    - Rare permission bypass: FAIL in full-send and full-stop (R3C-01).
    - Out-of-scope data loss: FAIL for the same reason. The gate never forces a human disposition before merge.
- **W-02: satisfied.**
  - Existing `release/1.x` PR with `main` as default: full-send `:36,48-49,92-94` retain it; `babysit-pr:114`, `modernize:18-19,37` and `sol-loop:42-44` use the actual base; `full-stop:36` fetches the target. PASS.
  - Stacked new PR: `full-send:37-39` select the target explicitly, and the gate at `:92-94` detects a mismatch. PASS, with the advisory R3C-03 and R3C-04.
  - Ordinary new `main` PR: PASS.
  - Base changes after resolution: `full-send:93-94`, `babysit-pr:124-125` and contract `:66-67` require a recheck and reconciliation, and full-stop treats the mismatch as Blocked. PASS.
  - Full-stop's ban on merging is intact (`full-stop:11-12,22-28`).
- **W-03: satisfied for metadata, support files, sources and preservation (see the table).**
  - Cross-skill consistency of scope, gates, stop semantics, external effects, fresh contexts, bounded remediation, actual base and formal outcomes holds, except for R3C-01.
  - Reading the skills invoked nothing. Scores are described as advisory in `council:58` and contract `:38-39`.
- **W-04: satisfied.** The runtime diff is empty, the migration verifier exits 0, and the manifest and approval are identical to `aa25`.

## Findings

### R3C-01: Medium, mandatory, in scope of W-01

**Where:** `docs/methodology/dev-skills/full-send/SKILL.md:89-90`. The readiness check that inherits it is at `docs/methodology/dev-skills/full-stop/SKILL.md:32,40`.

**What's wrong:** the merge gate condition reads "Review bots have finished, and each finding is fixed or dismissed with a written reason." A written dismissal of *any* finding satisfies this merge-authorizing bullet, which contradicts W-01: "A written dismissal cannot satisfy mandatory remediation or authorize merge." It also contradicts `babysit-pr/SKILL.md:107-108` and the anti-drift rule "LA: … mandatory finding treatment must be unambiguous" in `wording-follow-up.md`. The text predates the delta (it is in the source original and at `f6de:82`), but W-01 explicitly makes its interaction with this gate part of the review scope.

**Static reproduction:**
1. A full-send runs on a repo with no initialized GenDev product, so the GenDev bullet at `:86-88` has no recorded prerequisites to check.
2. A bot flags a permission bypass on a rare path.
3. The agent posts a written dismissal ("rare path, outside the requested change").
4. Every bullet in `:84-94` now reads as true, so step 6 (`:53`) merges unattended.
5. Under full-stop, `:40` reports "Ready to merge."
6. `full-send:113` ("ask when the merge gate cannot pass") never fires.

**Risk:** an unattended merge with an unresolved security, permission or data-loss violation, while the two skills give conflicting instructions.

**Minimal fix:** replace the bullet with: "Review bots have finished. Each mandatory finding (security, contract, permission, data-loss or other approved-requirement violation, including rare paths) is fixed, or is out of scope with a recorded human scope/risk disposition. Only optional preferences or verified false positives are declined or dismissed with a written reason."

**Recheck:**
- Run the four W-01 counterexamples against full-send and full-stop.
- Update the full-send `destination_sha256` in `import-manifest.json`.
- Run the metadata, link and digest checks again.

### R3C-02: Low, advisory, related to W-01

**Where:** `babysit-pr/SKILL.md:96`.

**What's wrong:** "feedback you believe is not worth addressing … reply with a written reason and resolve the comment" is not limited to optional preferences or verified false positives. Lines 103-110 of the same file take precedence, but this line invites the failure mode W-01 removed: judging a rare-path finding "not worth addressing."

**Fix:** begin the line with "If feedback is an optional preference or a verified false positive, …"

### R3C-03: Low, advisory, related to W-02

**Where:** `file-pr/SKILL.md:12,47-50`.

**What's wrong:** line 12 says the diff is reviewed against "the base branch (usually `origin/main`)", and the `gh pr create` path gives no explicit `--base`. Without `--base`, `gh pr create` targets the repository default, so full-send's explicitly selected stacked or release target is not carried into PR creation. Only the REST fallback has a `base=` field.

**Mitigation:** the gate at `full-send:92-94` detects the mismatch and blocks. Correcting it then requires retargeting, which `:39` sends back to the user.

**Fix:** "Use the caller's selected target (`--base <target>`), or the existing PR's actual base."

### R3C-04: Low, advisory, related to W-02

**Where:** `sol-loop/SKILL.md:45`.

**What's wrong:** before a PR exists (full-send step 3), the local base is `origin/<default-branch>`. For a stacked or release target, the reviewed diff then includes the parent branch's commits, so review scope drifts from the selected target.

**Fix:** "Local: merge-base with the caller's selected target, else the default branch."

### R3C-05: Low, advisory, related to W-02

**Where:** `full-send/SKILL.md:45` and `full-stop/SKILL.md:24`.

**What's wrong:** both lines name only the default branch. Line 45 says "If you are on the default branch, create a branch first", so an agent already on a `release/1.x` target is not told to branch. Line 24 forbids pushing to "the default branch", not to the selected target.

**Mitigation:** the grants already limit pushes to the PR's own branch or the task branch.

**Fix:** use "default or selected target branch" in both places.

Only R3C-01 is mandatory; R3C-02 through R3C-05 are optional and left to human disposition. These findings go back to Chuck. I made no remediation and did not start another round.

## Boundaries

- I made no edits to the candidate, refs, branch, board, originals or `review/council-round-3/`.
- No workflows were invoked, and there were no network, PR or watcher effects.
- The only outputs are under this `claude/` folder (`report.md`, `logs/`, `scripts/`, and the empty `tmp/`).
- This report does not verify all of v3 and does not grant acceptance, release or delivery.
