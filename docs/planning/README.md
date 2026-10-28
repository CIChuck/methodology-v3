# Planning Dashboard

This dashboard is generated from [`board.yaml`](board.yaml), the canonical
work-item registry. Do not edit task state in this file directly.
GenDev project and phase approvals remain in the project manifest and gate log.

The governing workflow is the
[development task lifecycle policy](../policies/development-task-lifecycle.md).
Task approval and directory placement do not bypass GenDev authority.

## Queued

| Priority | Initiative | Condition | Authority | Delivery | Next gate |
| ---: | --- | --- | --- | --- | --- |
| — | _None_ | — | — | — | — |

## Approved

| Priority | Initiative | Condition | Authority | Delivery | Next gate |
| ---: | --- | --- | --- | --- | --- |
| — | _None_ | — | — | — | — |

## Started

| Priority | Initiative | Condition | Authority | Delivery | Next gate |
| ---: | --- | --- | --- | --- | --- |
| 1 | [Integrate and validate methodology-v3 steps 1–6](active/v3-baseline-migration/) | normal | granted | pushed | Chuck acceptance of VERIFIED candidate 98f8bec4597cd3307fc26e5c28dc86592e01ca08; step 8 remains separate |
| 2 | [Import and reconcile nine local workflow skills](active/skill-library-import/) | normal | granted | pushed | Authorize fresh independent review of pushed skill-import candidate 1516712; human acceptance pending |
| 3 | [Refresh v3 documentation and synchronize Practitioner Guide](active/v3-documentation-refresh/) | normal | granted | local | Owner review of checked documentation and main integration decision; no new formal VERIFIED |

## Completed

| Priority | Initiative | Condition | Authority | Delivery | Next gate |
| ---: | --- | --- | --- | --- | --- |
| — | _None_ | — | — | — | — |

## Accepted

| Priority | Initiative | Condition | Authority | Delivery | Next gate |
| ---: | --- | --- | --- | --- | --- |
| — | _None_ | — | — | — | — |

## Operating Rules

- Work progresses through `queued -> approved -> started -> completed -> accepted`.
- `blocked`, `deferred`, and `backlog` are conditions, not authorization.
- Only the maintainer may approve or accept work.
- Delivery state is tracked independently from work state.
- Each current initiative has one packet `README.md` containing its detailed gate.
- Accepted tracking history remains in [the archive](../archive/).
- Canonical GenDev authority stays under docs/project/; archive tracking records only.
- Validation checks recorded structure, not actual human approvals or remote delivery.

## Board Commands

Run `uv run --no-project --with-requirements requirements-devboard.txt python scripts/devboard.py <command>`.
Use `next`, `list`, `show`, and `validate` for read-only review. Mutation commands
record state, condition, or delivery transitions and regenerate this dashboard.
