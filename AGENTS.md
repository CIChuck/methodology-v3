# Repository Guidelines

## Repository Role

This repository is a reusable baseline for AI-assisted product development. It is intended to be
cloned, initialized for a specific project, and evolved toward documented goals with a human team
member and AI coding agents.

Do not treat chat history as build authority when methodology or project authority documents apply.

Project-local discovery entries in `.agents/skills/` link to canonical sources
under `docs/methodology/dev-skills/`. The engineering, task lifecycle and
independent validation policies under `docs/policies/` supplement GenDev.
Read `docs/policies/dev-board-integration.md` for the task/gate boundary.
The board is tooling; task state never substitutes for product gate approval.

In this methodology source repository, baseline engineering follows the
explicitly authorized evolution plan under `docs/resources/evolution/`.
The active v3 migration is recorded in
`docs/resources/evolution/v3-migration/README.md`. Do not initialize a product
merely to modify this reusable baseline. When installed into a product,
`docs/project/` remains required before product implementation.

## Methodology Authority

Follow `docs/methodology/constitution/gendev.md` for documentation-first development,
traceability, phase boundaries, test planning, review, remediation, and as-built close-out.

Use reusable templates from `docs/methodology/templates/` when creating project artifacts.

Use dev-skill guidance from `docs/methodology/dev-skills/` when creating or revising methodology
artifacts, including:

- `vision-framing.md`
- `prd-author.md`
- `architecture-spec-author.md`
- `governance-security-spec.md`
- `phase-build-planner.md`
- `tactical-implementation-planner.md`
- `ai-construction-directive-builder.md`
- `code-conformance-reviewer.md`
- `remediation-closeout.md`
- `traceability-matrix.md`

Use operating guides from `docs/methodology/guides/`:

- `agentic-development-workflow.md`
- `gates.md`
- `collaboration-modes.md`
- `human-agent-collaboration-loop.md`
- `start-and-next-step-protocol.md`
- `gate-transition-protocol.md`
- `amendment-and-regression-protocol.md`
- `enforcement-contract.md`
- `human-approval-protocol.md`
- `subagent-coordination-protocol.md`
- `artifact-collaboration-protocol.md`
- `production-operations-protocol.md`
- `orchestration-validation.md`

Use role playbooks from `docs/methodology/agents/roles/` when a task maps to a specific lifecycle
role.

## Orchestration Behavior

## Agent Start Contract

At the start of a task, the lead agent must establish repository state before
editing methodology or project artifacts:

```bash
./scripts/gendev-doctor.sh
```

The doctor's prerequisite report is contract, not decoration: GenDev requires
bash 4+, git, python3, and ripgrep (rg). If the doctor reports a missing
prerequisite (exit code 3), stop and have it installed before any methodology
work; do not substitute another tool or emulate the missing one.

If the project is initialized, also run:

```bash
./scripts/project-state.sh
```

Use the output to report the current gate, next artifact, required approver, and
recommended validation. If `docs/project/` is missing, initialize the project
before product implementation. If current state is unclear or authority is
missing, stop and ask for human disposition rather than inferring approval.

For canonical late-lifecycle artifacts, prefer the generator over ad hoc files:

```bash
./scripts/new-artifact.sh --kind deployment-readiness
```

The human may set the collaboration mode in plain language, such as:

```text
Lead proactively.
Use approval-gated mode.
Stay advisory.
Proceed execution-focused.
```

The lead agent must follow the selected mode while preserving required human approvals. Proactive
mode does not bypass gate approvals, security approvals, or production approval.

For short prompts such as `Let's begin`, `What's next?`, `Continue`, `Proceed`, `Pause`, and
`Resume`, follow `docs/methodology/guides/start-and-next-step-protocol.md`.

When coordinating sub-agents, follow `docs/methodology/guides/subagent-coordination-protocol.md`.
Sub-agent output is advisory until accepted into active project documents or approval records.

When accepted authority must change, follow
`docs/methodology/guides/amendment-and-regression-protocol.md`. Do not keep moving forward with
stale authority, and do not regress gates unless the amendment invalidates gate entry conditions.

When enforcement class, gate protection, or implementation-path controls matter, follow
`docs/methodology/guides/enforcement-contract.md`. Attested enforcement is valid at baseline, but
the active project must declare its class in `docs/project/project.yaml`.

When project scale, gate combination, or GenDev Lite matters, follow
`docs/methodology/guides/gates.md`. The active project must declare `scaling.blast_radius_class`
as `C1`, `C2`, or `C3` in `docs/project/project.yaml`. Enforcement class and blast-radius class are
different controls.

Use `docs/project/project.yaml` as the active project control-plane summary and
`docs/project/approvals/gate-log.md` as the durable approval history. Do not treat a gate as
approved unless the required approver, approval date, evidence, and risk disposition are recorded.

## Active Project Paths

For an initialized product, active authority belongs under `docs/project/`. Because
artifact names are canonical and project-independent (constitution Rule 14), these
pointers name the actual authority files, not just their directories:

```text
docs/project/vision/vision.md
docs/project/prd/prd.md
docs/project/architecture/architecture.md
docs/project/security-governance/governance-security-spec.md
docs/project/decisions/0001-technology-stack.md
docs/project/build-plan/phase-plan.md
docs/project/traceability/traceability-matrix.md
docs/project/approvals/gate-log.md
docs/project/project.yaml
```

Per-phase and multi-artifact authority lives in directories, one set per phase or
record:

```text
docs/project/build-plan/phases/
docs/project/testing/
docs/project/as-built/
docs/project/decisions/
```

If `docs/project/` does not exist, initialize it before product implementation:

```bash
./scripts/init-project.sh "Project Name"
```

## Authority Precedence

When documents conflict, use this precedence unless the active project explicitly defines a
different order:

1. `docs/methodology/constitution/gendev.md`
2. Active project governance/security specification
3. Active project architecture specification
4. Active project PRD
5. Active project phase build plan
6. Active project tactical implementation plan
7. Active project construction directive
8. Current user instruction, only within the documented scope above

If a user request changes scope, architecture, security behavior, acceptance criteria, or phase
boundaries, update the relevant authority document before implementation.

## Implementation Rules

### Board and Code-Generation Start Contract

Before generating or modifying product code:

1. Run the GenDev doctor and project-state commands, then
   `uv run --no-project --with-requirements requirements-devboard.txt python scripts/devboard.py validate` and `next`.
   Inspect the selected task with `show <task-id>`.
2. Confirm the board task is `started`, has `implementation_authority: granted`, and names
   the current feature branch. `approved` permits execution preparation; it does not begin
   product code generation. Check the actual human direction behind the recorded approval.
3. Read the tracking index and its links to accepted canonical GenDev authority. Confirm the
   current project gate and phase checkpoints permit that implementation scope.
4. Read the approved phase build plan, tactical plan, construction directive, and verification
   plan. Each work unit needs exact scope, non-goals, requirements, tests, and stop conditions.
   Only the documented maintenance route applies to eligible non-product maintenance.
5. Reconcile task state, branch/checkout, authority revisions, source, tests, and evidence
   before proceeding if they disagree. No directory, label, role flag, or tool result supplies
   missing authority.

The board tracks tasks through queued, approved, started, completed, and accepted. Only the human
approves or accepts task scope. Task state and recorded delivery never substitute for GenDev
approval. Preserve unrelated changes and local runtime data; do not clean or broad-stage them.

### Candidate Review and Acceptance

After authorized product generation, freeze a stable candidate commit when committing is
authorized, then obtain fresh-context, read-only conformance review. Supply pinned authority,
the directive, exact candidate/diff, acceptance criteria, and required evidence; exclude the
builder's transcript, private reasoning, and conclusions. The reviewer returns exactly
`VERIFIED`, `CHANGES_REQUESTED`, or `BLOCKED` with reproducible evidence.

Work remains `started` through required review and bounded remediation. A changed candidate or
authority makes the prior result stale and requires fresh review. Propose `completed` only
after the applicable independent `VERIFIED` result; only the human records `accepted`.
If a candidate cannot yet be frozen, report that limit rather than claiming formal verification.
Eligible documentation maintenance follows its separately recorded scope and checks.

Review does not authorize reviewer edits, automatic unbounded remediation, additional delegates,
push, merge, release, deployment, credential disclosure, or external effects. Keep board tracking
indexes and their evidence in the lanes described by the local lifecycle policy; canonical
GenDev authority stays under `docs/project/` through tracking moves and archival.


Before meaningful code generation, confirm that the active project has enough documented authority
to answer:

- what is being built;
- why it is being built;
- who it is for;
- what is in scope;
- what is out of scope;
- what architecture governs it;
- what security and governance rules apply;
- what tests or UAT checks prove it works;
- what documentation must be reconciled afterward.

Do not implement deferred features, silently widen scope, weaken security/governance behavior,
or mark planned behavior as implemented unless it is actually implemented and verified.

## Examples Are Not Active Authority

`docs/resources/examples/` contains example methodology artifacts. It is not the active project for a new
clone. Do not cite example PRDs, architecture docs, traceability matrices, implementation evidence,
source paths, tests, or UAT claims as local project authority unless the active project explicitly
adopts that material and matching local source/test files exist.

## Verification and Close-Out

When implementing product code, follow the active project verification commands. If commands are not
yet defined, create or update the relevant phase plan before proceeding.

Run the methodology checker before implementation, phase close-out, and handoff when applicable:

```bash
./scripts/check-methodology.sh
```

For each completed phase, update:

- test or UAT evidence;
- code review findings or review status;
- remediation status, if applicable;
- as-built close-out;
- traceability matrix;
- deferred item list and known limitations.

Report skipped verification honestly with the reason.

## V3 Documentation And Availability

The current Practitioner Guide is under docs/resources/practitioner-guide/; its
HTML edition mirrors that canonical Markdown exactly when resources are present.
Use docs/resources/releases/v3-adoption.md for current distribution/adoption
instructions. These are reference guides; canonical authority above still governs.
The inherited lifecycle is 1.0.2 and the v3 distribution remains unreleased.
Migration candidate 98f8bec is independently VERIFIED with human acceptance
pending. The additional nine workflow skills merged in PR #1; council round 1
is consolidated as BLOCKED. The authorized bounded follow-up is recorded at
docs/resources/evolution/skill-library-import/review/bounded-follow-up.md; its
local revised candidate needs fresh review. Read the guide's availability table
for revision-specific contents.
Do not treat a documentation refresh or GitHub upload as a new verification,
acceptance, product gate transition or methodology release.
