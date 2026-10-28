# 20. Work-Item Board

## What The Board Owns

The board at `docs/planning/board.yaml` records work-item priority, dependencies,
scoped implementation authority, condition, branch and observed delivery. Its
README dashboard is a generated view. The project manifest and gate log own
product/phase approvals. The board's free-text `next_gate` is a next task action,
not a value that changes GenDev's current gate.

A newly installed product gets an empty board. Initialization sets the product to
G1 pending; it does not populate G1 tasks. The repository owner decides which
tasks to add and their scope and priorities. Agents maintain those records within
the owner's authorization. Do not import the toolkit's migration tasks or claim
source-project approvals as product approvals.

## Orientation Commands

From the product root:

```bash
./scripts/gendev-doctor.sh
./scripts/project-state.sh
uv run --no-project --with-requirements requirements-devboard.txt python scripts/devboard.py validate
uv run --no-project --with-requirements requirements-devboard.txt python scripts/devboard.py next
uv run --no-project --with-requirements requirements-devboard.txt python scripts/devboard.py show <task-id>
```

Replace `<task-id>` with the selected item. Use `list` to see alternatives. The
standalone requirements keep Python 3.11+/PyYAML tooling separate from product
runtime dependencies. Contributor schema checks also use jsonschema.

## Task State And Authority

| State | Meaning |
| --- | --- |
| queued | Requested/planned work; implementation authority is not granted |
| approved | Human approved the bounded task; preparation may proceed |
| started | Execution has begun on its named branch after applicable prerequisites |
| completed | Applicable verification/review evidence is recorded; human acceptance remains separate |
| accepted | The human accepted the task scope/result and disposition of risk |

Product code generation requires a started task, `implementation_authority:
granted`, the correct branch, and accepted phase plan, tactical plan, directive
and verification authority permitted by the actual gate/checkpoints. Approved
alone is not the code-generation start signal. A baseline toolkit or eligible
maintenance task follows its separately documented authority route; do not create
a fictitious product to satisfy it.

Conditions such as blocked/deferred/backlog are separate from work state.
Delivery values such as local, pushed, merged and released describe observed
external state. Pushed or merged work can still await independent review or human
acceptance. Role flags and directory names are declarations, not authentication.

## Tracking Locations

Use the task template under `docs/planning/`. Tracking packets belong in its
queued, active, review, blocked, deferred or backlog lanes. Accepted packets go
under `docs/archive/completed/<year>/<task-id>/`. The CLI does not move folders;
reconcile the packet path and board together. Keep canonical project authority
under `docs/project/` throughout moves and archival.

Use `transition`, `set-condition` and `set-delivery` only for actual authorized
or observed events. Their `--help` output names required actor, note, evidence
and next-action arguments. The generated dashboard is refreshed with `render`;
`render --check` checks it without changing task state. Never edit a status just
to make validation green or interpret structural validation as acceptance.

## Working Alongside GenDev

The lifecycle and integration policies under `docs/policies/` are controlling
operating guidance. They distinguish task permission, product gates, review,
human acceptance and delivery. During required review/remediation, work remains
under execution; a new candidate makes previous conformance evidence stale.
Baseline evolution tasks may explicitly remain started through human acceptance.

At resumption, compare task scope, branch, candidate, authority revisions and
recorded delivery with reality. Resolve disagreements before continuing. Queue
new out-of-scope work for the owner instead of silently extending the task.
