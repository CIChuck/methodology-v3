# Human Disposition Required: VAL-005

Status: Queued proposed remediation; additional cycle not authorized
Task: v3-baseline-migration
Reviewed candidate: e69320fa2128f549162d633f14cd24463b743566
Independent result: CHANGES_REQUESTED
Completed automatic remediation cycles: 2
Decision owner: Chuck Russell

## Remaining finding

The essential dry-run guide's selective tar copy omits baseline-owned files,
board state/schema, requirements, policies and skill discovery. The initializer
can succeed while the resulting fixture fails doctor, checker and board
orientation. The existing regression checked initialization and preservation
of live authority, but not the completeness of the resulting environment.

This is VAL-005, a mandatory medium finding in the independent round-3 report.
VAL-001–VAL-004 are addressed under the current reviewed scope and the approved
checkpoint exception. The frozen original inventory remains unchanged.

## Proposed additional bounded cycle

If Chuck explicitly authorizes one additional cycle:

1. Replace the incomplete copy recipe with an isolated fixture setup that
   carries every required baseline asset and valid installation provenance.
2. Include usable policy/discovery seeds and an empty board while excluding
   live product authority, task history, Git metadata, credentials and runtime
   state. Keep both original repositories intact.
3. Exercise the documented setup from both source and initialized installed
   contexts. Check doctor, checker, board validate/next, policy/discovery
   presence and unchanged live authority. Identify the inherited unset-attester
   pre-approval condition explicitly; do not fabricate human identity/approval.
4. Run focused regressions and appropriate inherited checks, freeze the revised
   candidate, and obtain one new fresh-context full independent review.

Exact implementation choices belong to the approved bounded directive once
authorized. Permitted owned scope would be the essential dry-run guide, focused
fixture-construction helper if needed, regression tests and their declared
distribution references. Product work, final step 8 refresh, remote operations,
publication and acceptance remain excluded.

## Options

- Recommended: authorize this one additional VAL-005 remediation/review cycle.
- Keep the current candidate and defer the fix. Step 7 stays blocked; the
  candidate has no VERIFIED result or acceptance. No exception to the mandatory
  requirement is inferred from deferral.

No VAL-005 implementation has been performed. The independent-validation
policy requires returning unresolved findings after two unsuccessful cycles,
so the task remains started and blocked pending this decision.
