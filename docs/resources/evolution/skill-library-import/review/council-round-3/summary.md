# Council round 3 — instruction review consolidation

Status: Review complete; classification disputed, returned to Chuck
Operational candidate: 5e2ab4047a69c82fc883735134c23527197b3c1e
Branch: fix/skills-council-follow-up
Scope: full nine-skill instruction consistency plus two-wording delta conformance
Runtime reference: aa25aa89762974012c0243e6134e9785f5db970d (unchanged)
Produced by: Codex controller in T3 Code, 2026-10-29 UTC

| Member | Round 1 | Round 2 | Round 3 | Round 3 outcome |
| --- | --- | --- | --- | --- |
| GPT-6.1 Sol, high | 9/10 | 8/10 | 9.5/10 | VERIFIED |
| Claude Opus 5.5, high | 7/10 | 8/10 | 7/10 | CHANGES_REQUESTED |
| Gemini 4 Argon High | 9.5/10 | 10/10 | 9.7/10 | VERIFIED |

Raw reports and scores are preserved unchanged. Scores do not decide conformance.
There is no unanimous result. No controller-issued aggregate VERIFIED, acceptance,
completion, release or delivery is recorded. Both VERIFIED results apply only to
the named instruction/delta scope at 5e2ab40, not the whole v3 methodology.

## Confirmed results

All focused commands pass in all three contexts. All reviewers confirm the two
specific edits: babysit-pr now preserves mandatory rare-path findings, and full-send
retains/selects the correct PR target. Metadata, 14 source/import hashes/modes,
five unchanged support files, 24 discovery entries, relative resources and exact
23-file guide mirror pass. Original-input verifier actually exits 0. Runtime paths
and frozen migration manifest/approval are identical to aa25aa8; the 409/17/48
runtime suites are NOT newly rerun or claimed for round 3. Real rg worked in every
provider. No network/live workflows/product gates or Linux/hosted CI proven.

## Disputed R3C-01 and controller recommendation

Claude classifies full-send/SKILL.md:89-90 (each bot finding fixed or dismissed with
a written reason) as a medium mandatory contradiction. Its reproduction uses a
repository without an initialized GenDev product so the applicable-GenDev gate
may be empty, then dismisses a rare-path permission bypass and treats the bot
gate as satisfied. Full-stop inherits that gate. Claude requests an explicit
mandatory-versus-optional split in the gate bullet.

Sol and Gemini read that bullet together with full-send's required babysit-pr
workflow and shared contract. Both independently conclude the explicit current
prohibition controls which dismissals are permitted. The controller agrees with
that interpretation based on the text, not on vote counts:

- full-send:8-9 binds the shared contract, and step 5 (:51-52) requires babysit-pr.
- babysit-pr:103-110 classifies mandatory security/contract/permission/data-loss
  findings on every path, requires scope/risk disposition for out-of-scope ones,
  and expressly says: “A written dismissal does not satisfy required remediation
  or authorize merging.” Only optional preferences may be declined.
- shared contract:43-47 independently prohibits waiving governing criteria and
  retains mandatory contract/security findings even outside the happy path.
- Those prohibitions apply to the skill workflow itself; the lack of initialized
  product documents does not remove them. Claude's path requires disregarding
  those explicit rules, not merely satisfying the more general bot bullet.
- full-send's gate requires ALL conditions, and a written reason is not an
  exception to its governing instructions. Full-stop inherits the same boundaries.

Controller recommendation: treat the proposed gate-bullet edit as an optional
clarity improvement, not a demonstrated authorization bypass; retain the candidate.
However the builder/controller is not silently converting Claude's raw verdict
or marking the disputed requirement resolved. Chuck must decide whether to accept
this classification or request the explicit wording clarification. No fourth
review or further remediation is started under the exhausted round-3 scope.
A human decision does not rewrite any independent report or expand its scope.

## Other advisory observations

Claude R3C-02: earlier babysit-pr “not worth addressing” wording is broad, but
Claude itself notes the explicit mandatory-finding rule controls it.
Claude R3C-03 / Gemini GEM-R3-NIT-01: illustrative usual-main language and lack
of an explicit gh --base example in file-pr; selected target and final identity
check govern. No live CLI filing behavior was exercised. Optional clarity only.
Claude R3C-04: sol-loop's no-PR local diff defaults to repository default rather
than explicitly receiving a selected stacked target. Advisory scope improvement.
Claude R3C-05: default-branch wording around branch creation/push prohibition;
existing grants limit effects to the task/PR's own branch. Advisory only.
These remain recorded, not automatically added to the implementation scope.

## Evidence and provenance

Request, authority pins, member reports and durable scripts/logs copied after
all members finished. No fixture/cache trees or private reasoning copied. Large
raw skills.diff/wording.diff remain in external scratch and are exactly reproducible
from Git using request.md. evidence-index.json hashes the durable copied subset.
Claude disclosed and cleaned a reviewer-created ignored py_compile artifact;
its incident log is retained. No governed candidate file was changed during
review. Only evidence/tracking additions occur afterward. Original projects,
frozen refs, source skills and recovery are retained. No push or merge occurred.
