# Development Board Integration

Status: Reusable operating policy
Authority: docs/methodology/constitution/gendev.md and AGENTS.md

The board owns work-item priority, dependencies, scope authorization and
recorded delivery state. The product manifest and gate log own product and
phase approvals. Task approval cannot bypass GenDev checkpoints. Canonical
product authority stays under docs/project when tracking indexes are archived.

A methodology source repository without docs/project uses its recorded,
human-authorized baseline evolution plan as authority for baseline tooling
work. This does not permit product implementation or invent product approvals.
Keep such tasks started through independent review and human acceptance.

The CLI, schema, requirements file, templates and tests are baseline assets.
The board, generated dashboard, tracking indexes, project policy adaptations,
and additional skills are project-owned. New installations receive an empty
board. Upgrades preserve its work items, events, task packets and approvals.

The board requires Python 3.11+ and PyYAML; its regression suite also uses
JSON Schema validation. From the repository root:

```sh
uv run --no-project --with-requirements requirements-devboard.txt python scripts/devboard.py validate
uv run --no-project --with-requirements requirements-devboard.txt python scripts/devboard.py next
```

Alternatively install requirements-devboard.txt into a separate Python 3.11+
environment and run python scripts/devboard.py. Product dependencies and
lockfiles do not need to change. The CLI does not create/move task directories.
Use docs/planning/task-template.md to prepare tracking indexes.

Role flags are declarations, not authentication. Validation checks structure
and semantic constraints; it does not prove actual human authorization,
independent VERIFIED evidence, remote delivery, or gate acceptance. Verify
those records before corresponding transitions. Formal review requires a
frozen candidate and an independent context under the validation policy.
