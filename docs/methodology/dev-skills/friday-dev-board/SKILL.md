---
name: friday-dev-board
description: Operate this repository's work-item board alongside GenDev. Use for selecting, queuing, resuming, tracking, or handing off a board task; task approval never substitutes for GenDev gate authority or authorizes external effects.
---

# Development Task Board

The skill retains its imported name for discovery. Follow `AGENTS.md`,
`docs/policies/development-task-lifecycle.md`, and
`docs/policies/dev-board-integration.md`.

For an initialized product, read `docs/project/project.yaml` and the gate log;
for baseline engineering, read the explicitly authorized evolution plan. Then read
`docs/planning/board.yaml` and the selected tracking index for task state. For
implementation, also read the local engineering/validation policies and all
accepted canonical phase authority. Board task approval cannot bypass GenDev.

## Commands and task selection

From the repository root, run:

```sh
uv run --no-project --with-requirements requirements-devboard.txt python scripts/devboard.py validate
uv run --no-project --with-requirements requirements-devboard.txt python scripts/devboard.py next
```

Use `list` and `show <id>` for details. If there are no open tasks, report that
fact; do not invent work or grant approval. Add a genuinely requested task
using `docs/planning/task-template.md`, initially queued with no implementation
authority, then render and validate the board.

The registry owns task state, priority, dependencies, and recorded delivery.
Its generated README is a view. GenDev's manifest/gate log retain all project
and phase approval authority. The task's free-text next action is not a GenDev
gate transition.

## Authorized execution

Before generating product code, confirm the task is started, task-scoped
authority is granted, and the feature branch matches. Approved permits
execution preparation only. Read the actual human scope direction and accepted
GenDev prerequisites, construction directive, and required verification.
Preserve unrelated changes. Use the active orchestration instructions for
separately authorized delegation; this skill does not request subagents.

Keep canonical authority under `docs/project/`. Planning lanes and accepted
archives contain tracking indexes and bounded task evidence linked to that
authority. The CLI does not move those directories: prepare and repair their
locations/links as part of the authorized transition.

Only a human may approve or accept task scope. Do not impersonate that person
by supplying a maintainer role flag without their actual recorded direction.
A role flag is a declaration, not authentication. Do not use a queued task,
a tool's success result, silence, or historical acceptance as build authority.

Keep work started during implementation, independent review, and remediation.
Record completion only after the applicable evidence and independent review
exist, then present the actual decision to the human. Formal VERIFIED requires
a frozen candidate and independent context, as defined by the local policy.

## Handoff and limitations

Validate the board/dashboard and run GenDev checks before handing off tracked
work. Report task state, project gate/checkpoint, authority, evidence, omitted
checks, blockers, and the exact next authorized action.

Structural board validation does not prove human approval, formal independent
verification, or remote Git/hosting delivery. Check the underlying records
before recording those facts. Task acceptance does not approve a GenDev gate,
and no board action grants push, merge, release, or deployment authority.
