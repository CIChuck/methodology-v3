# 22. Installation And Upgrades

## Source Toolkit Versus Product

Use a pinned methodology checkout as the toolkit source and a separate product
repository as its destination. A source checkout may contain evolution tasks and
historical examples; those are not the new product. Directly cloning the source
for a product leaves source board/history to reconcile. Installation supplies
project seeds and an empty board instead.

Choose the source revision based on its actual review and acceptance record.
The v3 repository is hosted privately on GitHub and remains unreleased. GenDev
1.0.2 is the inherited lifecycle contract, not evidence that every v3 change is a
published release. Chapter 21 distinguishes the expanded skill branch.

## Fresh Installation

From the toolkit root, into an existing destination directory:

```bash
./scripts/install-methodology.sh --dry-run /path/to/product
./scripts/install-methodology.sh /path/to/product
```

Use --with-resources when the product should receive reference material, which
can include historical evolution/review evidence. Those copied references do not
populate its live board or make source approvals active product authority. An
existing AGENTS.md is preserved; --integrate-agents adds a managed include when
authorized. Set the intended --protected-branch explicitly when needed. Then
create a product README when none exists, then initialize in the destination
and follow Chapter 4. Do not initialize again if
it already has active authority.

## Ownership Boundary

| Baseline-owned | Project-owned |
| --- | --- |
| Constitution, guides, templates, schema and shipped scripts/tests | Product manifest, canonical authority and approval history |
| Canonical shipped skill content | Task board, tracking packets and delivery history |
| Standalone board requirements and rendered baseline workflow | Local policy adaptations, extra skills and agent instructions |
| Hash/mode provenance for managed files | Product dependency files, code and runtime settings |

`docs/methodology/schema/installation.json` records managed file hashes, Unix
modes, source revision/worktree state, candidate identity and installation history.
Project seeds copy only missing files. Extra local files are not silently claimed
as baseline-owned. The doctor checks recorded integrity; it does not supply
product acceptance, approval or a complete security audit.

## Controlled Upgrade

Snapshot or commit the destination first. Inspect without writing:

```bash
./scripts/install-methodology.sh --force --dry-run /path/to/product
```

Reconcile every conflict against actual local authority, then apply:

```bash
./scripts/install-methodology.sh --force /path/to/product
```

Installer --force permits an owned baseline update; it does not authorize data
loss. Preflight rejects edited, missing or chmod-changed owned files, unsafe
symlinks/parents, unowned collisions, malformed ownership and unresolved local
amendments before writes. Explicitly decide whether an upstream equivalent absorbs
a local amendment, whether to keep the local extension under another path, or
whether to defer the upgrade. Never change integrity hashes just to hide an edit.

Previous installation/amendment records and retired owned files are retained.
Legacy records without mode evidence can adopt incoming owned files only when
the current mode matches; otherwise they stop for reconciliation. Ordinary clean
owned upgrades work, while arbitrary project-owned data survives.

Caught failures and SIGINT/SIGTERM/SIGHUP roll back replaced/new files, created
directories, managed includes, ignore changes and installation metadata. This is
file-level atomic replacement with bounded rollback, not a guarantee against
power loss, SIGKILL or concurrent hostile filesystem changes. Keep the snapshot.

After upgrading, run the doctor, project-state and methodology checker. If the
board renderer changed, explicitly regenerate its derived dashboard, then validate
and inspect next; rendering must preserve board.yaml work items/events. Review
policy/discovery seeds separately because an upgrade preserves local adaptations.

## Safe Fresh Exercise

From a tracked toolkit checkout or integrity-valid installed product:

```bash
tmpdir="$(python3 scripts/create-dry-run.py)"
cd "$tmpdir"
./scripts/init-project.sh "Example Product"
./scripts/gendev-doctor.sh
uv run --no-project --with-requirements requirements-devboard.txt python scripts/devboard.py validate
uv run --no-project --with-requirements requirements-devboard.txt python scripts/devboard.py next
./scripts/check-methodology.sh
```

The final checker returns the explicit unset-attester error until a real person
is named; expect no other errors. The board is empty and G1 remains pending.
TMPDIR must be outside the source repository. Untracked toolkit additions are
excluded; commit or otherwise track an approved toolkit change before expecting
it in a source-based exercise.

Selection occurs before inspecting excluded surfaces. Missing live policies,
AGENTS/discovery folders, external private skill links and unrecorded additions
do not contaminate or block the fresh fixture. Selected unsafe/changed/missing
owned assets still fail. The fixture gets new marked provenance, canonical
policies/skills and an empty board, with no live authority, task history,
credentials, Git metadata or runtime data. A continuation exercise instead uses a
human-reviewed sanitized authority snapshot and preserves its real approval state.

## Reusing T3_Code_Sample

The sample was an integration/test input, not a required product dependency of
v3. Its actual upgrade was not performed. Disposable copied-input upgrades were
exercised with explicit reconciliation while preserving authority, policies and
amendments. A live resync requires its own snapshot, dry run and authorized local
reconciliation. Keep both original projects and recovery data until their owner
explicitly chooses disposal; publishing v3 is not that decision.
