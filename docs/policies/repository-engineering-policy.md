# Repository Engineering Policy

Status: Reusable operating policy
Authority: AGENTS.md and docs/methodology/constitution/gendev.md
Derived from: the active project integration; provenance is recorded in the v3 migration inventory.

## Purpose and authority

This policy governs engineering work in the active project. It supplements
[AGENTS.md](../../AGENTS.md) and the
[GenDev constitution](../methodology/constitution/gendev.md). Use the authority
precedence defined in AGENTS.md; this document introduces no competing order.
Accepted project governance, architecture, requirements, and approved phase
authority remain controlling for their scope. Stop and surface a conflict
rather than silently choosing a lower-level rule.

The [task lifecycle policy](development-task-lifecycle.md) governs execution and
handoff. The [independent validation policy](independent-validation-policy.md)
governs conformance review. Confirmed pre-existing findings belong in the
[policy debt register](legacy-policy-debt.md).

These are repository operating rules. Their adaptation does not accept the
project's draft specifications, grant product implementation authority, or
advance a GenDev gate.

## Scope and current layout

Apply this policy to product source, product tests, dependency declarations,
lockfiles, runtime configuration, and documents that define product contracts.

Product source layout, language/toolchain, tests, runtime configuration, and
implementation paths are defined by the active project's accepted architecture,
stack decision, phase plan, and manifest. No sample application's paths or
Python version are inherited by this policy.

In an installed project, the installation record identifies baseline-owned
files. Local policies, board/task state and additional skills are project-owned.
Use the distribution's conflict-aware upgrade path; never update integrity
hashes merely to hide an unapproved change. In the methodology source repository,
baseline engineering follows its explicitly authorized migration/evolution plan
and remains separate from any initialized product's gates.

## Before implementation

Run the GenDev doctor and project-state command. Read the manifest, active
artifact, approval record, and governing directive. Report the current gate,
approval state, and next authorized work.

Product implementation requires the accepted upstream authority and phase
checkpoints specified by GenDev. The initialized draft scaffold is not build
authority. At G1, framing and authorized environment or policy maintenance may
proceed; product code generation awaits the required authority.

Preserve unrelated changes. Inspect branch and checkout ownership before
editing, committing, or integrating. Stage only files belonging to the
current task when a commit is authorized.

## Design and interface rules

Apply GenDev's six principles: YAGNI, KISS, DRY, SRP, least astonishment, and no
undeclared authority-bearing abstractions. Use existing logic and keep each
unit responsible for one coherent task.

When components or public interfaces exist, use documented contracts rather
than internal reach-through or incidental side effects. A contract change
must identify affected consumers, migration needs, tests, and documentation.
Do not introduce packages, interfaces, schemas, or dependencies merely to
satisfy a hypothetical future need.

Structured data crossing a persistent, external, or component boundary must
have an explicit contract. Use the simplest suitable representation. A typed
dataclass, typed dictionary, or validation library may be appropriate; this
policy does not select or install a new library.

## Typing and runtime invariants

For new or materially changed Python product code:

- annotate public functions and boundary methods, including return types;
- make exchanged values and failure behavior explicit;
- justify `Any` at dynamic boundaries rather than propagating it;
- prefer validation and stronger contracts over repeated casts; and
- avoid blanket source suppressions or weakening type-checker configuration.

Tests may use narrow, justified relaxations for dynamic fixtures and doubles.
Test ergonomics do not justify hiding source defects. Pre-existing exceptions
must be recorded as debt rather than silently treated as compliant.

Use explicit exceptions or validation for external inputs, configuration,
authorization, persistence, and essential lifecycle requirements. Use `assert`
only for internal programmer checks whose removal cannot weaken required
runtime behavior. A cast needs an already-established invariant and must
narrow to the actual contract; it cannot substitute for validation.

## Verification and available tooling

Define verification before product implementation in the phase build plan,
tactical plan, construction directive, and test/UAT plan. Cover the meaningful
positive, negative, regression, boundary, and failure cases for that scope.
Do not add tests that merely repeat implementation wording.

The available repository checks are:

```sh
./scripts/gendev-doctor.sh
./scripts/project-state.sh
./scripts/check-methodology.sh
./scripts/test-methodology.sh --suite shell-syntax
```

The first three orient and validate the installed project. The shell suite is
appropriate when shell tooling or its integration changes. These checks do
not establish product correctness, independent verification, or acceptance.

No product linter, product test runner, or type checker is currently declared
in `pyproject.toml`. Select and configure any such tools through the accepted
stack and implementation plan. Do not report Ruff, pytest, or mypy as existing
repository gates or install them just to satisfy this imported policy.

PyYAML is declared separately in the `devboard` tooling dependency group.
For board changes and task selection, run board validation. For board code or
schema changes, also run the focused standard-library test suite:

```sh
uv run --no-project --with-requirements requirements-devboard.txt python scripts/devboard.py validate
uv run --no-project --with-requirements requirements-devboard.txt python -m unittest discover -s tests/devboard -v
```

These checks cover task-tracking behavior, not product tests, independent
conformance, authenticated approval, or remotely reconciled delivery.

Source and installed-product workflows run their context-appropriate checks
when hosted and enabled. Its presence is not evidence that a hosted run, branch protection,
or local hook is active. Enforcement remains as declared in the project
manifest; full filesystem access does not grant project approval.

## Review, exceptions, and closeout

Applicable implementation must receive independent conformance review under
the validation policy before it is proposed as complete. Passing commands or
a builder's report do not substitute for that review or human acceptance.

A policy exception identifies the named human, date, scope, requirement,
reason, risk, validation, and expiry or follow-up. It cannot silently override
the constitution, accepted security requirements, or a required gate. Use the
GenDev amendment or override protocol when those controls are affected.

Update test/UAT evidence, review findings, remediation disposition, as-built
records, and traceability as applicable. Report omitted checks and known
limits. Keep verification, human acceptance, delivery, and deployment distinct.
