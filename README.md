# GenDev Methodology-v3 — Unreleased Development Toolkit

GenDev combines documented product authority and human gate decisions with
bounded AI code generation, a work-item board, reusable skills, independent
candidate validation and evidence-based close-out. This repository is hosted at
https://github.com/CIChuck/methodology-v3 and is still an unreleased distribution.

## Current Status

| Component | Availability and evidence |
| --- | --- |
| Inherited lifecycle | GenDev 1.0.2; gate numbering and release identity remain unchanged |
| Migration baseline | Candidate 98f8bec independently VERIFIED; human acceptance pending |
| Default GitHub main | Migration plus review/hosting records; 15 baseline skills |
| Expanded skills | Nine more on integration/v3-skill-import; 24 total on that branch and this docs branch; local checks passed, independent review pending |
| Documentation | V3 Practitioner Guide and matching HTML content; describes status without granting acceptance |

A GitHub push is delivery, not verification, acceptance or a methodology release.
Use an exact source revision and its own evidence. Earlier VERIFIED results do
not cover subsequent imports or documentation changes. Historical release and
review records remain preserved at their original revisions.

Current methodology version: `1.0.2`

That value identifies the inherited normative lifecycle. The separate unreleased
v3 distribution identity lives in `docs/methodology/schema/candidate.json`.
Historical 1.0.2 publication evidence belongs to the inherited baseline, not a
new v3 release. See `docs/resources/releases/README.md` and
`docs/resources/evolution/v3-migration/review/round-5/report.md`.

## Start Here

Read `AGENTS.md`, `docs/methodology/constitution/gendev.md` and the
[Practitioner Guide](docs/resources/practitioner-guide/README.md).
Current adoption instructions are in [V3 Adoption](docs/resources/releases/v3-adoption.md).
The HTML guide source is under `docs/resources/practitioner-guide-html/`.

## What Changed In V3

- The owner-controlled task board tracks scope, priorities and delivery alongside
  GenDev; the manifest and gate log retain product/phase approval authority.
- Product code starts from a started/granted task on its named branch and the
  accepted phase, tactical, directive and verification artifacts.
- Private implementation details may be proportionate choices within approved
  scope; changes to domain/shared contracts/architecture/security stay controlled.
- Amendment impact and reconciliation determine whether regression is needed;
  an architecture edit does not automatically send the product back to G3.
- Phase build-plan drafts can be prepared ahead without acceptance; detailed
  tactical plans and directives are finalized just in time.
- Formal review freezes an exact candidate and uses fresh read-only context.
  Mandatory findings drive bounded remediation; human acceptance stays separate.
- Ownership-aware installation/upgrades preserve project data and local extensions,
  refuse conflicts before writes and support documented rollback.
- Canonical skill content is discoverable through linked entries; complete bundles
  retain scripts, references and UI metadata. Provider-specific actions are optional.

## Repository Model

| Location | Role |
| --- | --- |
| docs/methodology | Constitution, operating guides, templates, canonical skills, schema and optional integrations |
| docs/project-template | Product manifest plus planning and fresh-exercise seeds |
| docs/project | Active product authority, created in a product destination by initialization |
| docs/policies | Project-owned engineering, lifecycle, validation and board policies |
| docs/planning | Owner-selected tasks, indexes and generated dashboard |
| .agents/skills | Discovery links to canonical skills |
| docs/resources | Practitioner editions, adoption guides, examples and historical evidence |

This methodology source is not an initialized product. Its own engineering tasks
follow explicitly authorized evolution plans under `docs/resources/evolution/`.
Install into a separate destination for a product; do not inherit source migration
tasks, project approvals or machine/account settings.

## Prerequisites

GenDev requires **bash 4+, git, python3 and ripgrep (rg)**. Run the doctor first;
a missing prerequisite is blocking. Install rg using the package manager for
your platform. Board tooling requires Python 3.11+ and `requirements-devboard.txt`;
uv is convenient, or use a separate tooling environment. Product runtime
requirements and lockfiles remain the product's responsibility.

## Install And Initialize A Product

From the chosen toolkit checkout, into an existing destination directory:

```bash
./scripts/gendev-doctor.sh
./scripts/install-methodology.sh --dry-run /path/to/product
./scripts/install-methodology.sh /path/to/product
```

Add --with-resources to include examples and the Practitioner Guide. An existing
AGENTS.md is preserved unless an authorized managed include is requested through
--integrate-agents. In the destination, preserve its existing README.md or create a short product
README first; the installer does not copy the toolkit README. Then run:

```bash
./scripts/gendev-doctor.sh
./scripts/init-project.sh "My Product Name"
./scripts/project-state.sh
./scripts/check-methodology.sh
```

Initialization creates canonical authority and starts **G1 pending**, while the
installed board is **empty**. The owner selects its tasks and priorities. The
fresh manifest's required_attester is TBD: checker exit 1 with
GENDEV-MANIFEST-ENFORCEMENT-002 is expected until a real human is named. Do not
invent identity or approval; investigate other errors separately.

An existing docs/project means resume its actual state. Installer --force updates
owned baseline paths subject to conflict checks; initializer --force replaces
project authority and is not an upgrade. Snapshot the destination and follow
`docs/methodology/guides/distribution-ownership.md` before any upgrade.

## Work With The Board And Agent

```bash
uv run --no-project --with-requirements requirements-devboard.txt python scripts/devboard.py validate
uv run --no-project --with-requirements requirements-devboard.txt python scripts/devboard.py next
```

Use show with the selected task ID. Task labels and role flags cannot supply
missing authority. Keep canonical project artifacts under docs/project even when
tracking packets move or are archived. Read the applicable skill and the actual
user request before workflow execution; discovery is not invocation.

## Validation And Close-Out

Run `./scripts/check-methodology.sh` before implementation/handoff. Use the
applicable product verification plan and `./scripts/methodology-guard.sh --staged`
for diff-aware checks. Source-only contributors also use documentation, lifecycle,
reference and regression suites; installed products use their product bindings.
The optional `./scripts/install-hooks.sh` supplies local staged checks, not human
approval or branch protection. Metrics come from
`./scripts/methodology-metrics.sh docs/project`.

The source Actions workflow currently runs for PRs and pushes to master. A main
or feature-branch upload alone is not hosted CI evidence. No v3 release or
production deployment is implied by successful local checks or repository hosting.

Record actual tests/UAT, independent review/remediation, traceability, as-built
state, deferred work and human decisions. The project uses the same G0–G9 gates
and G5 phase checkpoints; the board and workflow skills support that process.

## Reference Paths

- Operating workflow: `docs/methodology/guides/agentic-development-workflow.md`
- Phase loop: `docs/methodology/guides/phase-loop.md`
- Board boundary: `docs/policies/dev-board-integration.md`
- Validation: `docs/policies/independent-validation-policy.md`
- Skill workflow contract: `docs/methodology/guides/skill-execution-contract.md` on the expanded branch
- Optional T3 integration: `docs/methodology/guides/t3-code-integration.md`
- Safe dry runs: `docs/methodology/guides/orchestration-validation.md`
- Current examples: `docs/resources/examples/current/` (non-authoritative)

## License

Documentation uses CC-BY-4.0; scripts/source use MIT. See `LICENSE`,
`LICENSE-CC-BY-4.0` and `LICENSE-MIT`. Third-party browser bundles retain their
own notices. Source and archived evidence are retained for provenance.
