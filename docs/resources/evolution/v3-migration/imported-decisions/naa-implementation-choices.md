# NAA Implementation Choices: Approved Local Amendment

Status: Approved local methodology clarification
project: t3-code-sample
Date: 2026-10-27
Owner: Chuck Russell
Authority: docs/methodology/constitution/gendev.md, First Principles of Code Quality
Produced by: Codex under Chuck Russell's approved request
Produced on: 2026-10-27
Produced with: human-agent collaboration
Agent identity: GPT-6.1 Sol via T3 Code
Derived from: installed GenDev 1.0.2 constitution and the approved NAA recommendation

## Decision and scope

Chuck Russell approved the recommendation to relax implementation-detail
constraints with "approved, make that change" on 2026-10-27.

Align the construction-directive template and the reviewer checklist with the
constitution's existing permission for proportionate implementation-local
detail. Builders may choose private helpers, internal types/classes, adapters,
fixtures, fakes, mocks, and framework-generated types within approved work.
Those details do not each need an architecture inventory entry or approval.

Unapproved product behavior, public/cross-component contracts, persisted/shared
data, component ownership, security/trust boundaries, acceptance criteria, and
phase scope remain controlled. An authority-bearing change still needs approved
upstream authority or an amendment before implementation. Significant internal
choices belong in the implementation report.

## Installation provenance

### Architecture wording reconciliation

On 2026-10-27, Chuck Russell authorized the consistency audit's issue 1 fix
with "fix issue 1". The architecture template and the project's Draft
architecture still required every class, field, and interface to be inventoried.
Both now use the constitution's authority-bearing boundary and all conditions
on implementation-local detail described above. The project architecture
remains Draft; this maintenance does not accept its contents.

The installation record adds a separate `naa-architecture-alignment-2026-10-27`
entry, preserving the earlier amendments and the architecture template's
original source hash. Its synchronized project artifact is
`docs/project/architecture/architecture.md`.

Validation: the GenDev doctor verifies all 137 effective baseline file hashes;
the methodology checker passes with no warnings. A scoped accuracy check
confirms identical NAA wording in the template and project draft, removal of
the stale inventory requirement from both, unchanged prior amendment entries,
and unchanged project manifest and gate log. Referenced local files exist.
These are documentation-maintenance checks, not formal independent VERIFIED
evidence.

### Baseline identity

This is a local amendment to the installed 1.0.2 baseline, not a new upstream
release. The constitution and upstream source repository are unchanged.

`docs/methodology/schema/installation.json` retains the original source commit.
Its `local_amendments` entry records the approval, affected files, original
source hashes, and amended hashes. Its effective file hashes reflect this
approved local content so installation integrity checks remain meaningful.
The additional metadata documents the amendment; it does not modify checker
behavior. Reconcile or reapply this clarification on a later baseline upgrade.

The scope is limited to NAA guidance and its documentation/provenance. It does
not change the architecture-amendment or rolling-wave guidance, authorize
product implementation, or advance the pending G1 gate.
