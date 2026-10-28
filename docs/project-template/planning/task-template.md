# Task Tracking Index Template

Copy the index below to `docs/planning/queued/<task-id>/README.md` for a newly
requested task. Add its corresponding entry to `board.yaml` as queued, with
`implementation_authority: not_granted`. Do not copy example approvals or
another repository's tasks. Choose a unique positive priority.

Example entry to add to the board's `tasks` list:

```yaml
- id: example-task
  title: Example task
  priority: 1
  work_state: queued
  condition: normal
  implementation_authority: not_granted
  packet: docs/planning/queued/example-task/
  next_gate: Human scope approval and applicable GenDev prerequisites
  delivery_state: not_started
  branch: null
  depends_on: []
  validation: []
```

Replace the example values, render the dashboard, and validate the board. The
entry is tracking metadata; it does not authorize implementation. The board
CLI does not create or move task folders.

## Index content

```markdown
# [Task title]

Task ID: [lowercase-kebab-id]
Project: [project-slug]
Owner: [named owner]

## Objective and scope

[Bounded request, permitted effects, non-goals, and acceptance criteria.]

## GenDev authority

- Current gate/checkpoint: [actual manifest state]
- Phase and tactical task IDs: [IDs or explained N/A for environment maintenance]
- Canonical authority: [existing docs/project paths with revisions/status]
- Construction directive: [approved path or documented maintenance route]
- Human scope authorization: [decision, person, date, evidence, and limits]

## Execution and evidence

[Baseline/branch, permitted verification, results, canonical review and
traceability references, blockers, remediation, and next action.]

## Human acceptance and delivery

[Record actual decisions and observed delivery evidence only when they exist.
Task acceptance does not close a GenDev gate or authorize external actions.]
```

Canonical project authority stays under `docs/project/`. Tracking indexes link
to it rather than relocating or duplicating it during lane moves or archival.
