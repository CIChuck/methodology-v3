# 10. Review, Remediation, And Close-Out

## Review Is Conformance

Review compares actual implementation with accepted scope and authority: the
construction directive, tactical and phase plans, PRD, architecture, governance,
verification plan and traceability. It checks the six constitutional principles
as well as behavior, boundaries, security, failure paths and evidence. A green
test suite does not prove those concerns or replace human acceptance.

## Freeze The Candidate And Pin The Request

Formal validation requires a stable commit and exact base/candidate diff. The
request identifies project/phase/task, branch/checkout, pinned authority revisions
or digests, directive, acceptance criteria, required commands, known baseline
failures, exclusions, permitted effects and report/evidence locations. Uncommitted
work can receive advisory review, not formal VERIFIED.

Use a new fresh context for every conformance review or changed candidate. Supply
only the needed authority, diff, surrounding code, verification evidence and
questions. Exclude the builder transcript, private reasoning and conclusions as
proof. The reviewer remains read-only, creates only permitted disposable test
outputs, and cannot start nested reviewers, remediate, change state or deliver.
A different model is optional; independent context is mandatory.

## Context Provenance

Record reviewer identity/model when available, context creation time, inputs,
authority pins, exact candidate/diff, whether implementer context was shared and
any justified exception. Preserve commands, actual results, skipped checks and
limits. A changed candidate or authority makes the previous result stale; retain
it as a historical result for its own revision, then obtain fresh review.

Use canonical phase review/evidence paths under `docs/project/` for products.
The board tracking packet links to those records; it does not move them into a
tracking archive. Baseline evolution uses its explicitly authorized equivalent.

## The Six Principles And NAA

Review whether work is requested (YAGNI), proportionate (KISS), reuses existing
logic (DRY), separates responsibilities (SRP), behaves as intended (least
astonishment), and respects declared authority (NAA). Private helpers, adapters,
values and fixtures may implement approved scope without individual architecture
entries if they add no new domain concept, persisted/shared state, public or
cross-component contract, component/ownership/trust/security/lifecycle boundary,
or unapproved behavior. A new private symbol alone is not a NAA finding.

Architectural or security boundary changes need amendment and impact assessment;
they do not automatically regress the project to G3. Identify the actual
requirement violation and reconcile the affected authority before deciding whether
prior gate conditions are invalidated. Preferences without a violated requirement
remain advisory; a mandatory violation remains mandatory even if rare.

## Outcomes And Findings

The independent validator returns exactly one outcome:

| Outcome | Meaning |
| --- | --- |
| VERIFIED | Required conformance/evidence established for the exact candidate; no unmet mandatory requirement |
| CHANGES_REQUESTED | A mandatory requirement needs remediation, regardless of its severity label |
| BLOCKED | Authority, candidate stability or required evidence is insufficient for a defensible conclusion |

Each finding needs a stable ID, severity, exact location, governing requirement,
reproducible evidence, risk, required mitigation and verification. Explain whether
it is inherited or a regression. Severity conventions may vary by report, but
minor/low does not mean optional when a mandatory requirement was violated.
Advisory APPROVE, bot scores, successful commands and branch status are separate
evidence classes and never rewrite these formal outcomes.

Human risk acceptance does not change CHANGES_REQUESTED to VERIFIED. A governing
exception or amendment must be handled through the actual authority process;
review the resulting candidate/authority as required. Missing identity, approval
or evidence cannot be filled by a role flag or a report label.

## Bounded Remediation

Translate findings into a directive with exact scope, tests, non-goals and stop
conditions. Fix within the approved migration/phase/task boundary, rerun relevant
checks and freeze the revised candidate. Request fresh independent review; do not
have the builder self-attest or reuse a reviewer conversation for a new candidate.
After two unsuccessful remediation cycles, return unresolved findings and options
to the human instead of continuing automatically. A round budget or workflow
skill never extends that limit without human disposition.

If the defect is in accepted authority, record and classify an amendment, assess
the affected subtree, reconcile it and determine whether a gate must regress.
Do not silently rewrite source requirements to match implementation.

## Board, Verification, Acceptance And Delivery

Work remains under execution through required review/remediation. Propose
completed only with the applicable independent VERIFIED evidence; only the human
records accepted. Baseline evolution may explicitly remain started through human
acceptance. Keep branch, task state, candidate and evidence consistent.

A commit, push, merge, release or deployment is an observed delivery event,
recorded separately from verification and acceptance. A pushed feature branch
can still be unreviewed. A VERIFIED candidate can still await human acceptance.
Record both facts accurately; do not use delivery to imply gate approval.

## As-Built Close-Out

Record actual implemented behavior and deviations; test/UAT and security/migration
evidence; review/remediation status; accepted risks and deferred work; current
traceability and source provenance; amended authority; operational limits and
next actions. Report unavailable verification with its reason. Reconcile the
approved documents and the actual result rather than presenting plans as built.

A useful prompt is:

```text
Perform Phase 1 as-built close-out from the reviewed candidate and actual test,
UAT, remediation and traceability evidence. Identify gaps, stale authority and
residual risks. Propose acceptance; do not record a human decision for me.
```

## Phase Review Versus Aggregate Acceptance

Per-phase review occurs inside the G5-to-G6 loop against that phase's accepted
artifacts. G6 is aggregate readiness for review after all declared live phases
exit; G7 is final implementation acceptance after aggregate review/remediation;
G9 is terminal project close-out. A phase review is not G6 or final acceptance.
Use the canonical phase and aggregate records required by the manifest, including
final review/test reports, remediation disposition and project-level as-built/value
records. Close-out documentation never supplies deployment or gate approval.

The policies under `docs/policies/` and the constitution control this workflow.
Documentation-only maintenance has its bounded direct-authorization route and
checks; it is not a new formal independent VERIFIED result.
