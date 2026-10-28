# Human Disposition: VAL-005 Residual

Status: Bounded follow-up authorized by Chuck Russell, 2026-10-28
Owner: Chuck Russell
Task: v3-baseline-migration
Reviewed candidate: 6ca2ad10f7eb0c71b9a316d458a20ad667c21c4b
Independent outcome: CHANGES_REQUESTED, one mandatory medium finding
Report: report.md
Remediation cycles used: 3, including the expressly approved additional cycle

## Result of the approved cycle

Ordinary complete fresh construction works from source and initialized installed
products. Fixture integrity/provenance, empty board, canonical policy/skill seeds,
live input preservation and the explicit inherited attester condition are checked.
Independent review passed all 13 inherited suites (409 checks), 17 board tests,
37 migration tests, four scenarios and six signal rollback probes. Both original
projects remain preserved under the approved additive-checkpoint exception.
No acceptance, step 8 refresh, external publication or remote action occurred.

## Remaining VAL-005 boundary

The new helper filters project-owned and agent entries after calling the shared
distribution reader, which first traverses and validates those excluded paths.
Thus a valid installed product with an external private skill link, or absent
live AGENTS/policies/discovery surfaces, cannot create a fresh exercise. This is
a defect in the new helper's selection boundary; it is not a reason to alter
live project configuration or weaken normal installer symlink protections.

## Proposed narrowly bounded follow-up

If explicitly authorized:

1. Add an explicit selection option at the distribution reader boundary so the
   dry-run caller excludes project/agent groups and unowned paths before any
   existence checks, traversal, symlink validation or content reads. Preserve
   the default installer's complete selection and existing protections.
2. Use canonical owned seeds for all fresh project-owned fixture surfaces.
3. Add end-to-end initialized installed-source regressions for an external
   discovery link, independently absent AGENTS/skills/policies, and unowned
   additions. Require complete fresh setup, doctor/board checks, 15 canonical
   links, empty board, expected sole unset-attester error, no planted contents,
   and exact preservation of each source. Retain unsafe/changed-owned refusals.
4. Run focused and appropriate inherited checks; freeze a new local candidate
   and obtain one fresh independent review. Return any mandatory findings to
   Chuck again; do not extend automatically.

Owned files: scripts/create-dry-run.py, the source-selection interface in
scripts/lib/distribution.py, tests/migration/test_v3_toolkit.py and essential
contract documentation/evidence. No broad installer rewrite, dependency change,
product implementation, new gate approval, step 8 refresh or remote effect.

Alternative: defer this issue and keep step 7 blocked without VERIFIED or
acceptance. Deferral does not waive the mandatory criterion.

The task-specific one-cycle extension is exhausted. The independent validation
policy's two-cycle escalation rule was honored before that extension and the
approved round-3 directive requires further mandatory findings to return to
Chuck. This packet proposes a follow-up; it grants no authority to implement it.

## Recorded authorization

Chuck Russell instructed: "lets fix it and test it" in response to the proposed bounded fix, regression checks and fresh independent review. This authorizes that follow-up within the stated local scope; it grants no acceptance, publication or additional automatic cycle.
