---
name: subagents-worktrees-template
description: Prepare an isolated worktree delegation plan when parallel subagent work is authorized. Define independent task ownership, GenDev authority, permitted effects, effort limits, and integration verification.
---

# Worktree Delegation Template

Prepare a plan for `[AUTHORIZED GOAL]` only when the user has authorized
parallel or isolated subagent work. A project setting or this template alone
does not request delegation.

Read `AGENTS.md`, `docs/project/project.yaml`, the applicable local policies,
and `docs/methodology/guides/subagent-coordination-protocol.md`. Establish the
current gate/checkpoint and accepted phase authority before assigning product
implementation. Worktrees require an initial commit.

## Assignment record

For each independent task, specify:

- phase and tactical task IDs;
- objective and approved construction directive;
- pinned authority paths and acceptance criteria;
- non-overlapping owned files and explicit non-goals;
- base revision and intended branch;
- required tests, evidence, and report paths;
- permitted external effects and commit/delivery authority;
- provider/model settings only when requested or inherited;
- effort limit, dependencies, integration order, and stop conditions.

If tasks overlap or required authority is missing, resolve ownership or return
the decision to the human before dispatch. Do not invent product architecture
to make a parallel split possible.

## Provider-specific execution

Follow the active session's worktree and orchestration rules for explicitly
authorized dispatch. T3 integration examples are documented separately in
`docs/methodology/guides/t3-code-integration.md`. The plan does not authorize
additional agents, external effects, commits, integration or publication.
