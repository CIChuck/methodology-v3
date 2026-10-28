# Independent Validation Policy

Status: Reusable operating policy
Authority: AGENTS.md and docs/methodology/constitution/gendev.md
Derived from: the active project integration; provenance is recorded in the v3 migration inventory.

## Purpose and authority

This policy defines independent conformance review for the active project. It
supplements [AGENTS.md](../../AGENTS.md), the
[engineering policy](repository-engineering-policy.md), and the
[task lifecycle policy](development-task-lifecycle.md). GenDev authority and
the accepted project specifications control; this policy cannot waive them.

Independent review answers whether a stable candidate conforms to its named
authority. It does not accept the project, approve a gate, authorize delivery,
or establish deployment readiness.

## Applicability and documentation maintenance

Product code, behavioral tests, dependency/environment changes, runtime
configuration, migrations, and public contract changes require independent
review proportionate to their scope before being proposed as complete.
GenDev's independent-context rule applies even when deterministic checks pass.

A bounded documentation-only maintenance request may use a direct user
authorization record, scope description, accuracy pass, link checks, and
methodology checks. It does not automatically require a new construction
directive or a formal frozen-candidate report. Record who requested the work,
the scope, checks, and limitations in the relevant artifact or task evidence.

This maintenance route does not approve product specifications, waive a
mandatory review in accepted authority, or cover runtime, dependency,
enforcement-code, or security-behavior changes. If the task crosses those
boundaries, stop and obtain the required authority. Rewriting policy documents
must not be reported as formal independent VERIFIED evidence.

## Roles and independence

The human approver owns scope, risk, required artifact acceptance, and gate
approval. The controller owns bounded dispatch and evidence reconciliation.
The builder implements authorized work. A validator reviews the frozen
candidate read-only. A remediator changes only the authorized findings.

The builder may also be the controller, but may not validate its own candidate
or remediation. An independent human reviewer or a separate fresh-context
agent may perform the validation. A different model is optional; independent
context is mandatory. A skill or enabled capability is not authorization to
start additional agents.

A reviewer receives pinned authority, the selected candidate diff and relevant
surrounding code, requirements, and permitted verification evidence. Do not
supply the builder's session transcript, private reasoning, or conclusions as
proof. A justified context exception must be recorded with its limits.

## Candidate and required request

Formal validation needs a stable candidate commit and an exact base/candidate
diff. Uncommitted work can receive advisory review but not formal VERIFIED.
The repository must have an initial commit before this process is available.

Before dispatch, prepare a request containing:

- project and phase identity, work-unit or tactical task IDs, and review mode;
- base commit, candidate commit, branch or checkout identity, and exact diff;
- controlling authority paths with revisions or hashes and artifact status;
- the approved construction directive and acceptance criteria;
- relevant architecture rules, including the accepted domain model;
- required commands and expected behavioral, design, and implementation evidence;
- known baseline failures, exclusions, and explicitly approved exceptions;
- permitted external effects, credential use, and costs, if any; and
- exact repository locations for the request, report, and evidence.

For board-tracked work, include its task ID and link the same canonical phase
authority and evidence from its tracking index. Use tactical identifiers from
the actual approved plan; a board label does not approve that plan. Missing,
stale, contradictory, or unapproved authority blocks formal validation.

## Evidence locations and provenance

Use the canonical phase code-review report referenced by the manifest for
phase review. Store detailed phase requests and evidence beside their phase
artifacts, and aggregate review support under `docs/project/review/`.
Reference these records from the canonical review report, traceability, and
as-built closeout as appropriate. Choose exact paths in the request rather
than inventing a separate planning packet or board schema.

Record project identity, reviewer identity/model where known, review-context
creation time, review mode, candidate/diff identity, authority revisions,
shared-context exceptions, commands, results, skipped checks, and residual
risk. Include the GenDev provenance fields on authority and evidence artifacts.

## Read-only review procedure

1. Read AGENTS.md, these local policies, and every authority named in the request.
2. Confirm candidate stability, checkout ownership, authority pins, and diff bounds.
3. Map every acceptance criterion and directive task to implementation and evidence.
4. Inspect the complete selected diff and relevant surrounding code for drift,
   undeclared abstractions, duplication, contract violations, and deferred scope.
5. Evaluate GenDev's six code-quality principles and the required behavioral,
   design, security, failure-path, migration, and implementation checks.
6. Run authorized commands and separate pre-existing failures from regressions.
7. Reconcile documentation, configuration, traceability, and closeout obligations.
8. Return exactly one outcome with reproducible evidence and stated limits.

Do not edit or remediate the candidate, change project state, commit, push,
merge, release, deploy, or send external messages. Read-only review may create
ordinary disposable test outputs only when the request permits them; it must
not mutate governed files or persistent application state. Never print or
persist credentials. If a required command needs an unauthorized effect or
cannot respect those boundaries, omit it and report the resulting blocker.

## Review modes and outcomes

A full review covers the complete selected work-unit scope. A delta review
checks specified remediation and regressions against the new candidate. An
aggregate review covers the complete integration or phase scope before its
required closeout; delta review alone does not establish integration conformance.

Return VERIFIED only when all mandatory criteria and checks have cited
evidence, any permitted exception is explicitly recorded, no mandatory
requirement is violated, no blocker/critical/high finding remains, and the
required closeout evidence is reconciled. Advisory suggestions may remain;
an uncited assertion cannot support VERIFIED.

Return CHANGES_REQUESTED when the candidate violates authority or needs
remediation. Every finding identifies its stable ID, severity, location,
violated requirement, evidence, risk, fix, required verification, and
configuration/documentation impact.

Return BLOCKED when authority, candidate stability, acceptance criteria,
infrastructure, or permitted evidence is insufficient. Identify checks already
performed, the exact blocker, and what would resolve it. BLOCKED is not a code
failure or a formal verification result.

A human may separately accept a documented risk within their authority. That
decision does not rewrite a validator's result or turn unmet mandatory review
conditions into VERIFIED. Resolve governing exceptions through GenDev's
approval/amendment process and review the resulting candidate as required.

## Remediation and stale candidates

The controller converts each numbered finding into a bounded remediation
directive with tests, documentation, acceptance criteria, and non-goals. The
original builder may perform authorized mechanical fixes. Use independent
expertise when the risk or accepted plan requires it; do not start extra agents
without the applicable delegation authority.

Commit the corrected candidate when authorized, retain the old report as
historical/superseded evidence, and obtain a fresh review of the new revision.
After two unsuccessful remediation cycles, return unresolved findings and
options to the human instead of continuing automatically.

A change to reviewed code, tests, runtime configuration, governing authority,
or the candidate revision makes a running review stale. Stabilize and request
a new independent review; do not reuse the old conclusion. Evidence-only
closeout additions may be reviewed as such, but do not excuse changes to the
governed candidate.

## Acceptance boundary

VERIFIED permits a recommendation for human acceptance or the next authorized
checkpoint. It is not acceptance, phase exit, deployment approval, or a gate
transition. Record those decisions through the GenDev gate-log and manifest
process only when the named human has actually made them.
