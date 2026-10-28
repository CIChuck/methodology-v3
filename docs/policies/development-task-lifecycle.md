# Development Task Lifecycle Policy

Status: Reusable operating policy
Authority: AGENTS.md and docs/methodology/constitution/gendev.md
Derived from: the active project integration; provenance is recorded in the v3 migration inventory.

## Purpose and authoritative state

This policy applies GenDev to development tasks in the active project. It
supplements [AGENTS.md](../../AGENTS.md), the
[engineering policy](repository-engineering-policy.md), and the
[independent validation policy](independent-validation-policy.md).

The authoritative project summary is
[project.yaml](../project/project.yaml). The durable approval and transition
history is the [gate log](../project/approvals/gate-log.md). Follow the installed
[gate definitions](../methodology/guides/gates.md),
[phase loop](../methodology/guides/phase-loop.md), and
[human approval protocol](../methodology/guides/human-approval-protocol.md).

The work-item tracker is [board.yaml](../planning/board.yaml), rendered as the
[planning dashboard](../planning/README.md). It owns task state, priority,
dependencies, task-scoped authority, and recorded delivery state. GenDev's
manifest and gate log continue to own project and phase gates. If task scope,
project state, approval history, and evidence disagree, reconcile them before
execution. Never infer approval from a thread status or a board label.

The [integration record](dev-board-integration.md) defines this boundary and
the setup's validation limits.

## Orientation and authorization

Begin with the doctor and project-state commands. Inspect branch/checkout
ownership, unrelated changes, the current gate, active artifact, required
approver, and documented next action.

The current major gate and approval state use the values defined by GenDev.
Artifact status and gate approval status have different meanings; a Draft,
Complete, or VERIFIED report is not an approved gate.

Task authorization must identify scope, permitted effects, expected artifact,
and verification. A direct request to maintain repository documentation or
configuration authorizes that bounded work. It does not accept future product
specifications, grant product implementation authority, or bypass a gate.

For product implementation, the accepted phase plan, phase build plan,
tactical plan, construction directive, and test/UAT authority must satisfy the
applicable GenDev checkpoints. A pre-created template is not approval.

## Task progress and blockers

Track each work item as `queued`, `approved`, `started`, `completed`, or
`accepted`. Only explicit human direction permits approval or acceptance.
Queued work has no implementation authority. Starting requires a named branch
and satisfied dependencies. Completion requires the applicable verification
evidence and independent review; acceptance remains a separate human decision.

The board's `implementation_authority` records task-scoped permission. It does
not satisfy GenDev's upstream artifact approvals or phase checkpoints. A task
can be approved for design or environment work at G1 without authorizing
product implementation. The board's free-text `next_gate` describes its next
task action; it is not a GenDev gate value.

Use `normal`, `blocked`, `deferred`, or `backlog` as task conditions. Preserve
their reason and exit condition in the tracking index and next action.
Keep implementation, review, and remediation evidence in the appropriate
canonical phase artifacts and link it from the board's tracking index.

A task remains under execution while required review or remediation is
unfinished. When blocked, record the missing decision or evidence, owner, and
exit condition in its relevant artifact. Deferred work stays in the plan's
explicit deferred scope. A blocker or deferral grants no implementation
permission and does not by itself regress or advance a gate.

## Canonical artifact locations

Use the fixed GenDev artifacts and the paths recorded in the manifest:

- `docs/project/vision/vision.md` and `docs/project/prd/prd.md` for framing and
  requirements;
- `docs/project/architecture/architecture.md`,
  `docs/project/security-governance/governance-security-spec.md`, and
  `docs/project/decisions/0001-technology-stack.md` for design and governance;
- `docs/project/build-plan/phase-plan.md` for the ordered build partition;
- `docs/project/build-plan/phases/` for phase build plans, tactical plans,
  construction directives, implementation evidence, reviews, and remediation;
- `docs/project/testing/` for test/UAT plans and execution evidence;
- `docs/project/review/` for aggregate reviews and their bounded supporting
  request, evidence, and remediation records;
- `docs/project/as-built/` for closeout and value evidence; and
- `docs/project/approvals/gate-log.md` for required human decisions and events.

Phase filenames use the phase identifier and the canonical role, never the
project name or slug. Preserve canonical authority locations as work
progresses. Do not relocate accepted authority to an unrelated archive tree.
Retain superseded evidence with explicit status and revision identity.

Board tracking indexes live under `docs/planning/queued/`, `active/`, `review/`,
`blocked/`, `deferred/`, or `backlog/` according to task state and condition.
Accepted indexes live under `docs/archive/completed/<year>/<task-id>/`.
Archive tracking metadata and task evidence only; canonical GenDev authority
remains under `docs/project/`. Repair tracking links and update the board and
generated dashboard together. Use the tracking template in
`docs/planning/task-template.md`; do not copy another project's tasks/history.

## Branches, commits, and delegation

Use an isolated branch for product implementation and record its baseline and
candidate revision. The repository needs an initial commit before Git
worktrees or a formal candidate diff can be used.

A request to edit files does not automatically authorize staging unrelated
work, making commits, pushing, merging, or changing external systems. Respect
any explicit task authorization for those actions.

Subagent capability or a skill template does not itself request delegation.
When delegation is authorized, use a bounded assignment and the installed
[subagent protocol](../methodology/guides/subagent-coordination-protocol.md).
Provide the task, controlling authority, owned files, verification, effects,
effort limit, and stop conditions.

Use the active provider's orchestration instructions for authorized dispatch.
Reviewer assignments require a fresh context without the builder transcript.
Optional T3-specific examples are in
`docs/methodology/guides/t3-code-integration.md`; provider capabilities do not
grant delegation, implementation, or external-effect authority.

## Verification, acceptance, and delivery

The independent validator returns VERIFIED, CHANGES_REQUESTED, or BLOCKED for
a frozen candidate. The controller records the evidence and handles bounded
remediation. Only the named human accepts scope, risk, artifact authority, or
phase closeout where GenDev requires human approval.

Maintain separate evidence for a local change, commit, push, merge, release,
and deployment when those events occur. None proves human acceptance or
replaces independent validation. An agent run marked completed is an execution
fact, not a project gate decision.

## Gate and phase operations

Use the installed commands after the required evidence and human decision
exist. Read each command's help and supply its required answers:

- `scripts/close-gate.sh` records a major gate transition;
- `scripts/record-phase-checkpoint.sh` records an interior phase checkpoint;
- `scripts/close-phase.sh` records a phase exit; and
- `scripts/record-deployment-approval.sh` records deployment or non-deployment
  approval without performing a production action.

A --dry-run invocation can prepare a reviewable transition. Never generate
approval answers, checked statements, dates, or risk acceptance on behalf of
a human. Keep the major gate at G5 during the G5 phase-loop checkpoints and
update the manifest and corresponding gate-log event together.

No gate movement, human attestation, or product acceptance is recorded merely
because these policies were adapted. The next product task follows the actual
manifest and active gate evidence.

## Board operations

Run from the repository root:

```sh
uv run --no-project --with-requirements requirements-devboard.txt python scripts/devboard.py validate
uv run --no-project --with-requirements requirements-devboard.txt python scripts/devboard.py next
uv run --no-project --with-requirements requirements-devboard.txt python scripts/devboard.py list
```

Use `show <id>` for task details and `render --check` to check the dashboard
without rewriting it. `render` regenerates the dashboard. `transition`,
`set-condition`, and `set-delivery` require recorded task authority, actor,
role, note, and the evidence/next action required by their command help.
The CLI does not move tracking folders; prepare their correct locations and
links as part of the authorized transition.

Role flags are declarations, not authentication or proof of a human decision.
The controller must check actual authority and independent review before
recording the corresponding task state. Board validation checks structure,
schema agreement, packet presence, and dashboard consistency; it does not
contact Git hosts, authenticate the actor, prove formal VERIFIED evidence, or
advance a GenDev gate. No board-only result substitutes for those checks.
