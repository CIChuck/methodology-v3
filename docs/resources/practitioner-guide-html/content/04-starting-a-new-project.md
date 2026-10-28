# 04. Starting A New Project

## Choose A Toolkit Revision And Destination

Keep the methodology source repository as a reusable toolkit. Create or select a
separate product directory, and install the chosen v3 revision into it. Pin the
source commit and inspect its review/acceptance status first. The expanded
24-skill branch is not the same reviewed candidate as the 15-skill migration.

From the toolkit checkout:

```bash
mkdir -p /path/to/product
./scripts/gendev-doctor.sh
./scripts/install-methodology.sh --dry-run /path/to/product
./scripts/install-methodology.sh /path/to/product
```

Replace `/path/to/product` with the intended destination. An existing AGENTS.md
is preserved; use `--integrate-agents` only when authorized to add the managed
include. `--protected-branch BRANCH` selects the product CI branch.
`--with-resources` also supplies examples and this guide. Product code, runtime
settings, dependency files, source-project authority and migration tasks are not
copied into the destination. The installation does not initialize Git for you.

Current adoption: `docs/resources/releases/v3-adoption.md`.
Inherited baseline guidance: `docs/resources/releases/1.0.2-adoption.md`.
Chapter 22 explains distribution ownership and safe upgrades in detail.

## Prerequisites

GenDev requires bash 4+, git, python3 and ripgrep (`rg`). Run the doctor before
methodology work; a missing prerequisite is a stop, not permission to emulate it.
Install ripgrep with the package manager appropriate to your platform.

The task board additionally requires Python 3.11+ and the packages in
`requirements-devboard.txt`. Use uv with that standalone file or a separate
Python environment; installation must not replace the product's pyproject or lockfile.

## Initialize The Product

From the product directory, preserve its existing README.md or create one
with a short product description. The installer leaves this product-owned file
to the owner; it does not copy the toolkit README. Then run:

```bash
./scripts/gendev-doctor.sh
./scripts/init-project.sh "My Product Name"
./scripts/project-state.sh
```

Names are nonempty single-line text that yields a nonempty alphanumeric slug.
Quotes, apostrophes, backslashes, Unicode and bracket tokens remain literal data;
control characters and empty names are rejected before authority is created.

Initialization creates canonical paths such as `docs/project/vision/vision.md`,
not project-prefixed filenames. It renders the manifest and phase-1 starter
artifacts from the standard templates. Templates are not accepted plans or
implementation authority. The product begins at **G1, pending approval**. Its manifest may already name
the PRD as the next gate handoff; while G1 is pending, current work is still the
vision, not permission to skip to requirements.

If `docs/project/` already exists, resume from its actual manifest and approvals.
`init-project.sh --force` replaces that authority directory; it is not an upgrade
or routine recovery command. Use it only for an explicitly authorized reset in
an appropriate disposable or backed-up destination.

## Assign Human Authority And Scaling

Inspect `docs/project/project.yaml`. Confirm the product name/slug, current G1
state, canonical paths, collaboration mode and named human owner and approver.
Declare the enforcement class and actual attester, protected branch, binding and
implementation-path controls. Record a C1/C2/C3 blast-radius classification and
rationale. Gate combinations need the project's recorded justification.

A fresh manifest leaves `enforcement.attestation.required_attester` as `TBD`.
The checker returns exit 1 with `GENDEV-MANIFEST-ENFORCEMENT-002` until that person
is named. This is the inherited pre-approval error, not a clean pass or warning.
The agent may help draft G1 material, but cannot invent an identity, attestation
or approval. Naming the attester does not approve G1. Investigate any additional
checker errors separately.

## Orient To The Empty Board

Installation seeds `docs/planning/board.yaml` with no tasks or events. The board
has no automatic G1 task and does not set the product gate. The repository owner
chooses its initial work items, priorities and scope. A first task can cover
vision/problem framing, linked to the actual G1 authority.

```bash
uv run --no-project --with-requirements requirements-devboard.txt python scripts/devboard.py validate
uv run --no-project --with-requirements requirements-devboard.txt python scripts/devboard.py next
```

A fresh board validates and `next` returns `NO_OPEN_TASK`. For work subsequently
selected by the owner, inspect it with `show <task-id>`. Chapter 20 explains task
approval and implementation start checks.

## First Prompt

Start the chosen agent from the product root and ask:

```text
Let's begin. Read AGENTS.md, the project manifest, gate log and board. Report the
current gate, next artifact, owner/approver/attester and recommended validation.
We are at G1; draft the vision only and identify missing human decisions.
```

Expected current artifact: `docs/project/vision/vision.md`. Do not generate product
code from this prompt. Follow the active provider's instruction discovery rules;
Chapters 13 and 14 cover Codex and Claude Code, and Chapter 21 covers skill discovery.

## Validate And Pin Evidence

```bash
./scripts/check-methodology.sh
./scripts/pin-provenance.sh --help
```

Use pin-provenance with its documented arguments when preparing accepted artifacts
and evidence. Pin actual revisions/digests; do not use a passing command or a
placeholder as approval. Resolve the named-attester error and other required
controls before treating a gate as ready. The optional hook installer is
`./scripts/install-hooks.sh`; it supports local checks and does not replace
GenDev approvals, CI or branch protection.

## Existing Product Artifacts And Safe Exercises

For existing vision/PRD/architecture source material, use the declared-source
backfill route in Chapter 19. Installation and adoption do not automatically
accept imported documents. Preserve the originals and conform them through the
actual gates.

For a fresh isolated exercise, use `python3 scripts/create-dry-run.py` and the
commands in `docs/methodology/guides/orchestration-validation.md`. That helper
copies owned/tracked baseline assets, canonical policy/skill seeds and an empty
board, while excluding live authority and project-owned adaptations. Never use a
live project's `--force` initialization as a dry run.
