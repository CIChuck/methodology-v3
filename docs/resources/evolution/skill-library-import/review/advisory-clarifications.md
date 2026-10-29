# Approved workflow clarifications

Owner/authorizer: Chuck Russell
Status: Authorized; local edits, checks, frozen candidate, one focused fresh council round
Task: skill-library-import
Branch: fix/skills-council-follow-up
Starting HEAD / PR #2 head: 8abacf4b4b4a6d005cba3bdb92a68c9ce5d81376
Prior instruction candidate: 5e2ab4047a69c82fc883735134c23527197b3c1e
Unchanged runtime reference: aa25aa89762974012c0243e6134e9785f5db970d
Produced by: Codex in T3 Code, 2026-10-29 UTC

Chuck agreed with the advisory clarifications, discussed the five-document
proposal, then said “proceed”. This authorizes that proposed slice, including
the disputed merge-gate clarification. It does not declare an earlier reviewer
wrong or accept a candidate. Prior council reports remain historical unchanged.
Constitution and local engineering/lifecycle/independent-validation policies govern.

## Acceptance

AC-01 / R3C-02: babysit-pr permits declining only optional preferences or verified
false positives with a documented reason/evidence. Actual mandatory findings,
including rare paths, retain required remediation or scope/risk disposition.
AC-02 / R3C-03: file-pr carries the selected target explicitly into CLI creation
(--base <selected-target>) and the equivalent API base field. Existing PRs retain
their actual base; no silent retargeting. Review diff against that same target.
AC-03 / R3C-04: sol-loop uses the caller's selected target before a PR exists;
resolve and record the intended target if absent, with default only when it is
appropriate to the intended work. Named-base/no-remote fallback remains explicit.
AC-04 / R3C-05: full-send creates a task branch when on default OR selected target;
full-stop forbids direct pushes to both, preserving its existing no-merge rules.
AC-05 / R3C-01: full-send's gate explicitly blocks readiness on unresolved
mandatory findings; written dismissals are only for optional preferences or
verified false positives. Out-of-scope mandatory findings need human disposition,
which cannot silently waive governing criteria or fabricate VERIFIED. full-stop
inherits the corrected readiness and retains its ban on merging.

## Checks, records and limits

Only these five SKILL.md files, adapted digests and necessary review/task records.
No runtime/helper/UI/dependency/installer/test, original project/source-skill,
recovery/frozen-ref, product authority, release or website changes. Preserve all
raw council reports and receipts. Confirm runtime diff from aa25aa8 remains empty.
Run doctor, methodology/docs coherence, board validate/next/show, metadata/source/
support/link/manifest checks, exact 23-file guide mirror and original verifier.
Use static rare-path, optional/false-positive, release-base, stacked-base, ordinary
new-PR and changed-base examples; check all nine instructions for interactions.
Use existing cached tooling; no live imported workflow/PR creation/rebase tests.
No fresh 409/17/48 runtime suite claim for unchanged runtime in this docs cycle.

Freeze locally, then one fresh three-provider high-reasoning council pass focused
on AC-01–05 and cross-skill consistency. Pinned authority/diff, no builder transcript
or sibling conclusions, reviewers read-only with external scratch outputs; no
nested agents. Further mandatory findings return to Chuck before another cycle.
After that pass, update the existing authorized PR #2 branch and description with
accurate results, preserving unresolved findings. No merge, acceptance or release.

## Anti-drift

YAGNI: only the five approved clarifications and required records.
KISS: direct wording, no new execution framework.
DRY: reuse selected-target and shared-authority rules across the existing skills.
SRP: each skill retains its own workflow responsibility.
LA: selected-target and mandatory-finding treatment must be clear at each action.
NAA: no undeclared authority-bearing abstraction or expansion of product behavior,
shared contracts, data, architecture or security; private checks stay proportionate.
