# Round 1 Bounded Remediation Directive

Status: Authorized in-scope remediation; VAL-001 narrow exception approved
Task: v3-baseline-migration
Reviewed candidate: b869f0cd8df3521666aee51f9b7531631681b2c3
Base: 54f0de27f2b59fdcc54e4f57bb9f73dc92843f4a
Authority: migration README.md step 7 authorization and review-scope.md RV-01–RV-10
Independent outcome: CHANGES_REQUESTED

Chuck authorized addressing findings within the migration scope and obtaining
fresh independent review after fixes. Preserve both originals and all original
frozen evidence. Work remains local, on integration/v3-migration, and started.

## VAL-002: Permission-only upgrade conflicts

Record expected Unix permission modes for owned files alongside byte hashes.
Validate modes before any target write. Mode-only local changes, including
restrictive and executable-bit changes, must cause a conflict rather than being
silently overwritten. A clean recorded upstream mode update must still work.

Use a documented conservative policy for legacy records that have no mode map:
an incoming owned file may only be adopted when its current mode already agrees
with the incoming mode; ambiguous permission replacement requires reconciliation.
Retired files retained without writes may keep their actual mode with adoption
provenance. Preserve prior records rather than inventing historical mode evidence.
Update the integrity doctor and ownership guide consistently. Add regressions
for mode-only conflicts with zero writes, legacy records, actual upstream mode
changes, malformed mode data and doctor detection. Retain rollback coverage.

Owned scope: distribution.py, gendev-doctor.sh, migration tests and the ownership
guide. No product behavior, ACL/xattr implementation, external effects or changes
to either original repository are authorized.

## VAL-003: Sample identity in task seeds

Replace the fixed sample-project identity in both task-template.md copies with
an explicit reusable project placeholder. Extend fresh-install checks to reject
the fixed sample identity in project seed data and verify that the template is
usable for another project. Do not change project authority or accepted task data.

Owned scope: docs/planning/task-template.md, its project-template seed copy,
and the fresh-install regression test.

## VAL-001: Preservation discrepancy

The original T3 refs are retained unchanged, but T3 created two additional
checkpoint refs with the same tree as frozen checkpoint 36. The original exact
ref-set verifier fails. Preserve the observed refs and original inventory.
Chuck explicitly answered "Approve the narrow checkpoint exception." The
approval record and original observations are retained beside this directive.
Implement a narrowly scoped classifier that preserves every frozen ref and
allows only higher-ordinal T3 checkpoints in an already frozen context, with
the expected author/subject metadata and an identical tree to the latest frozen
checkpoint. Report additions explicitly. Reject missing/rewritten refs, other
additions, different trees, malformed objects or mismatched metadata. The frozen
inventory must not change, and no original ref may be removed or rewritten.
Add real temporary-Git tests for both the allowed case and negative cases.

## Verification and next action

Run the focused migration/board tests, doctor/coherence and appropriate inherited
checks. Record failure/remediation evidence, a new clean candidate and its exact
diff. After all required authority is resolved, obtain a new fresh-context full
review with one reviewer. A previous review result is stale for a changed
candidate. Stop after two unsuccessful remediation cycles or a material scope,
security or authority conflict. Human acceptance and step 8 remain pending.
