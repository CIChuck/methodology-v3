# Orchestration Validation

Status: Reusable Standard  
Authority: `docs/methodology/constitution/gendev.md`

## Purpose

This guide defines how to validate that an initialized project can be driven by a human and lead
agent from short prompts such as `Let's begin` and `What's next` without skipping methodology gates
or inventing hidden authority.

Use this guide after changing orchestration guides, project templates, `AGENTS.md`, or
`scripts/init-project.sh`.

## Dry-Run Setup

Choose either a fresh initialization exercise or continuation of an existing
project. Work only in an isolated copy; never replace live project authority.

For fresh initialization, copy baseline/tooling surfaces and omit docs/project,
Git metadata and runtime state:

```bash
tmpdir="$(mktemp -d ${TMPDIR:-/tmp}/methodology-dry-run.XXXXXX)"
tar -cf - AGENTS.md docs/methodology docs/project-template scripts tests | tar -C "$tmpdir" -xf -
cd "$tmpdir"
./scripts/init-project.sh "Example Product"
```

For a continuation exercise, copy docs/project as well and retain its actual
approval state. Run project-state instead of initializing again. Fixture copies
must not include credentials or active runtime data. A dry run never supplies
missing human approvals. Initialization refuses an existing project by default;
do not use --force as a workaround on the live source.

Then start the chosen coding-agent CLI from the dry-run directory.

## Required First-Run Behavior

From a prompt such as `Let's begin`, the lead agent should:

```text
[ ] read AGENTS.md
[ ] read docs/project/project.yaml
[ ] identify the current gate
[ ] identify the current collaboration mode
[ ] identify the blast-radius class
[ ] confirm or request the human owner and gate approver
[ ] identify the active role and artifact
[ ] draft only the current-gate artifact
[ ] avoid code generation
[ ] avoid filling future-gate documents as if accepted
[ ] stop at the next human review or approval boundary
```

At G1, the expected active artifact is the vision/problem framing document.

## Required Manifest Behavior

The agent may draft documents while owner or approver fields are still unknown. It must not mark a
gate as `ready_for_approval` or `approved` unless the manifest can name the required human authority.

Before a gate is ready for approval, `docs/project/project.yaml` should identify:

```text
[ ] current gate
[ ] current collaboration mode
[ ] active role
[ ] required approver
[ ] evidence path
[ ] enforcement class
[ ] blast-radius class
[ ] combined-gate justification, if gates are combined
[ ] known risks requiring acceptance or explicit N/A
[ ] blocking open questions or explicit N/A
[ ] next gate
[ ] next role
[ ] next artifact
```

## Required Approval Behavior

Before asking for gate approval, the lead agent should present:

```text
Gate:
Artifact status:
Evidence reviewed:
Enforcement class:
Blast-radius class:
Combined gate justification, if applicable:
Attestation or enforcement evidence:
Open questions:
Known risks:
Risks requiring acceptance:
Proposed next gate:
Proposed next role:
Manifest updates to record:
```

Approval should be recorded in:

```text
docs/project/approvals/gate-log.md
docs/project/project.yaml
the approved artifact, when the artifact has an approval section
```

A casual `proceed` is not enough for gate approval unless the agent can map it to a specific gate,
approver, evidence set, and risk disposition.

## Required Stop Points

The agent must stop and ask for human input when:

- the current gate is unknown;
- the human owner or approver is unknown at an approval boundary;
- approval language is ambiguous;
- material risk acceptance is missing;
- open questions could change the next artifact materially;
- the requested action would skip PRD, architecture, governance/security, or build planning;
- implementation is requested before an accepted construction directive exists;
- production deployment or rollback is implied without explicit approval.

## Pass Criteria

A dry run passes when:

```text
[ ] ./scripts/check-methodology.sh passes, or only reports expected pre-approval warnings
[ ] the current gate did not advance without recorded human approval
[ ] the active artifact status matches the manifest gate status
[ ] future-stage templates remain templates until their gate is active
[ ] approval history is durable in docs/project/approvals/gate-log.md
[ ] enforcement class is visible in docs/project/project.yaml
[ ] blast-radius class is visible in docs/project/project.yaml
[ ] combined gates have a recorded justification, if any
[ ] next-step recommendations are concrete and gate-aware
```

## Failure Signals

Investigate the orchestration layer if a dry run:

- marks a gate approved without `approved_by`, `approved_on`, evidence, and risk disposition;
- marks an artifact accepted while the gate log has no matching approval;
- starts implementation from a vision, PRD, or architecture prompt;
- fills PRD, architecture, build, or deployment artifacts as if accepted before their gate;
- treats sub-agent output as authority without lead-agent reconciliation and human approval;
- advances a gate without visible enforcement class or required attestation context;
- combines gates without visible blast-radius class and justification;
- treats `proceed` as production, security, or gate approval without an explicit record.

## Completion Standard

This guide is working when an isolated dry run can move from initialization to a reviewable current
gate artifact, stop for the human at the right boundary, and leave enough recorded state for a new
agent session to continue without relying on chat history.
