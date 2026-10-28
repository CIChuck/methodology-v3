# Distribution Ownership and Upgrade Contract

This v3 distribution is an unreleased candidate built on the 1.0.2 lifecycle
contract. Candidate identity is separate from historical release evidence.

Use the methodology repository as the source toolkit. For a new product,
create its destination directory and install into it:

```bash
./scripts/install-methodology.sh --dry-run /path/to/product
./scripts/install-methodology.sh /path/to/product
```

Then run init-project in the destination. Existing project authority is never
copied from the source toolkit. The source's migration tasks are not product
scaffolding; installed products receive an empty board and project-owned seeds.

Initializer project names are nonempty single-line text without control
characters and must produce a nonempty alphanumeric slug. Quotes, apostrophes,
backslashes, Unicode, slashes, ampersands and literal bracket tokens remain data.
The shared renderer serializes whole-scalar name tokens safely in YAML and keeps
literal text in Markdown. Invalid names are rejected before creating or replacing
project authority; later-phase setup applies the same input validation.

The distribution manifest identifies baseline-owned assets and `project`
seeds. Project seeds copy only missing files. Baseline-owned files are pinned
in installation.json; target-owned policies, board state, task indexes, agent
instructions, extra skills, product pyproject/lockfiles, and runtime state are
outside baseline ownership. Standard discovery links are seeded without
replacing local entries. Optional resources install only when requested.

Before an upgrade, commit or snapshot the destination and inspect the report:

```bash
./scripts/install-methodology.sh --force --dry-run /path/to/product
./scripts/install-methodology.sh --force /path/to/product
```

`--force` permits updates to recorded baseline files; it does not bypass
conflicts. Preflight refuses changed/missing owned files, permission-only
customizations, unsafe symlinks,
unowned collisions, malformed ownership data, and local amendments whose
effective contents differ from the incoming baseline. Inspect each reported
path against the accepted project authority. Reconcile by moving a local
extension to a distinct project-owned path, adopting an upstream equivalent,
or retaining the amendment and deferring the upgrade. Record the decision and
required checks. Do not edit integrity hashes merely to conceal an edit.

Upgrades merge managed source files into their owned directories while
preserving additional local files. Retired baseline files are retained and
remain tracked in ownership until an explicit migration disposes of them.
History retains prior installation metadata and local amendment records,
including amendments whose contents are now supplied upstream. Effective
hashes cover only managed files, not arbitrary local additions. The record
also identifies an unreleased distribution candidate and source worktree state.

Expected Unix permission modes are recorded in `file_modes` alongside byte
hashes and checked by both upgrade preflight and doctor. A local chmod requires
explicit reconciliation, while a clean recorded upstream mode update may proceed.
Legacy records contain no historical mode evidence: an incoming owned file can
be adopted only when its current mode already equals the incoming mode. Otherwise
preflight refuses the ambiguous replacement. Retired files retained without
writes keep their actual mode. `legacy_mode_adoptions` records this first mode
observation; prior history is retained rather than inventing past evidence.

Target file changes are staged atomically per file and rolled back on a caught
failure or interrupt, including new files/directories, managed agent includes,
ignore entries, and installation metadata. This is not a filesystem-wide
transaction against power loss or SIGKILL; keep the pre-upgrade snapshot.
The installer does not execute target hooks or change a product's dependencies.

An existing AGENTS.md is preserved by default. `--integrate-agents` adds a
managed include only when requested and refuses collisions in that include.
Project gate approvals, formal review and human acceptance retain their
independent meaning; successful installation supplies none of them.

After an upgrade that changes the board renderer, regenerate its derived
dashboard with the documented board `render` command, then run `validate` and
`next`. Rendering updates the view and must leave board.yaml task state and
events unchanged. The installer preserves the existing view until that explicit
refresh; a stale-dashboard report is not permission to change task approvals.
