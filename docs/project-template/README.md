# Project Template

This directory defines the canonical `docs/project/` structure for an initialized product.

Run:

```bash
./scripts/init-project.sh "Project Name"
```

The script creates `docs/project/`, copies starter documents from `docs/methodology/templates/`,
and writes a project manifest.

The template is intentionally documentation-first. Product source code, package configuration,
tests, CI, deployment files, and runtime commands should be added only after the active project
authority documents define the stack and implementation plan.

## Manifest

`project.yaml` is the active project's control-plane manifest. It records:

- project identity and current gate;
- human owner and approval fields;
- collaboration mode and lead-agent fields;
- blast-radius class, classification reason, and any combined-gate decisions;
- authority document paths;
- current phase paths;
- current approval summary, including gate status, approver, evidence, risk acceptance, and next
  handoff;
- active amendment count and amendment protocol path;
- enforcement class, attestation cadence, binding paths, and override policy;
- measurement command, metrics snapshot cadence, and value review path;
- example/non-authority notes.

The manifest is a map and state summary, not a replacement for the documents it references.

## Scaling Block

The `scaling` block declares how much methodology ceremony the project needs:

- `C1` for contained, low-risk, reversible internal work;
- `C2` for ordinary product work;
- `C3` for critical work involving regulated data, irreversible actions, external integrations,
  agentic runtime behavior, or high operational impact.

If the project combines gates, record each combination under `scaling.combined_gates` with the
affected gates, justification, approver, date, and evidence path. Gate combination changes form,
not required content.

## Approval Log

`approvals/gate-log.md` is the durable approval history for the active project. The manifest should
summarize the latest approval state; the log should preserve who approved what, what evidence was
reviewed, what risks were accepted, and what gate or role comes next.

## Orchestration

The active project uses the orchestration guides under `docs/methodology/guides/` to coordinate the
human team member, lead agent, and any sub-agents.

Key guides:

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

## Validation

After initialization, run:

```bash
./scripts/check-methodology.sh
```

The checker validates the active project structure, manifest paths, approval-state invariants,
enforcement block presence, phase-plan sections, and basic traceability evidence signals.

Project metrics can be generated on demand:

```bash
./scripts/methodology-metrics.sh docs/project
```

Use the report as a phase close-out snapshot when the phase reaches G9 or production value is
reviewed.

## Optional Local Hook

The template also includes an optional Git pre-commit hook installer:

```bash
./scripts/install-hooks.sh
```

The hook runs the methodology guard against staged changes. It is a convenience binding, not a
substitute for CI or human gate approval.

## V3 Installation Seeds

The installer, not product initialization alone, seeds the empty board/dashboard,
tracking lanes, project-owned policy copies and discovery entries. The planning
and dry-run policy subdirectories here are source seeds; init-project renders
the canonical docs/project manifest/artifacts rather than cloning source tasks.

A new product is G1 pending with an empty owner-controlled board. Name the actual
required attester; the fresh TBD value causes the explicit inherited
GENDEV-MANIFEST-ENFORCEMENT-002 error until resolved, without granting approval.
Board tooling stays separate from the product environment. Current startup and
upgrade guidance is docs/resources/releases/v3-adoption.md and Practitioner
Chapters 4 and 20–22. The 1.0.2 manifest lifecycle version is intentional while
methodology-v3 remains an unreleased distribution.
