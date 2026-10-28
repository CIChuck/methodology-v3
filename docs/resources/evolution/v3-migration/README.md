# Methodology-v3 Migration: Execution Authority and Evidence

Status: Authorized execution, steps 1–6; independent review and acceptance pending
Owner and requesting human: Chuck Russell
Source baseline: methodology-v2, commit 54f0de27f2b59fdcc54e4f57bb9f73dc92843f4a
Integration branch: integration/v3-migration
Candidate identity: methodology-v3, unreleased

## Authorization and boundaries

Chuck Russell authorized: "Let's begin, execute steps 1 through 6." The
eight-step plan was reviewed in the T3_Code_Sample conversation. All changes
and local checkpoint commits belong exclusively to this new repository.
The methodology-v2 and T3_Code_Sample inputs must retain their contents,
Git refs, and working state. External publication, a new release, and human
acceptance are outside this authorization. No delegation is authorized.

This is baseline engineering, not implementation of the T3 sample product.
The baseline deliberately has no initialized docs/project. Its controlling
authority is the GenDev constitution plus this bounded migration plan.
Installing the method into a product still requires that product's own
manifest, gate approvals, phase plans, directives, and verification authority.

## Steps and checkpoints

1. Preserve both inputs. Record nonignored files, symlinks, modes, hashes,
   Git status and refs; retain a full v2 Git bundle and file archives in the
   sibling methodology-v3-recovery directory. The committed input manifest
   identifies the sources and archive digests. No test may require the
   original source directories to remain available.
2. Bootstrap v3 from v2, preserving all reachable local history and tags.
   Retain original refs under refs/archive/v2 and source local branches.
   Use independent Git objects and no configured remote. Run the inherited
   full test suite before integration. Preserve its log here.
3. Generalize the T3 engineering policies, code-generation start contract,
   independent validation, handoff skills, board CLI/schema/templates/tests,
   and discovery links. Install an empty project board, not migration tasks.
   Keep optional T3 actions separate from core provider-neutral instructions.
   Do not inherit the sample app, its Python version, approver assignments,
   project authority, accepted history, machine settings, or measured debt.
4. Promote all four recorded local amendments: NAA implementation choices,
   architecture amendment impact, rolling-wave drafting, and architecture
   wording alignment. Preserve their origin as historical decisions without
   transferring project approval to a new product. Reconcile active copies
   of the affected guidance; historical release evidence remains historical.
5. Resolve audit issues in this repository: safe upgrade ownership and
   conflict handling; canonical initializer directives; dry-run instructions
   for initialized and uninitialized contexts; archived-board schema/runtime
   agreement. Include focused behavioral regression tests. Also reconcile
   the generic review skill's edit wording with formal read-only review.
6. Run the combined checks and isolated installation, upgrade, and development
   exercises. Test failed upgrades for zero target mutations, preservation of
   project authority/approvals/custom skills/policies, idempotent installation,
   candidate provenance, and actual board lifecycle constraints. Compare both
   original inputs with their manifests after all work. Record exact commands,
   outcomes, limitations, candidate revisions, and any failures/remediation.
7. Deferred: freeze a reviewed candidate, obtain independent validation and
   Chuck's acceptance. Self-checks in step 6 do not produce VERIFIED.
8. Deferred: final documentation refresh, including practitioner/HTML guides,
   examples and release/adoption material, against the accepted candidate.
   Essential operating instructions changed by steps 1–6 must still be usable.

## Implementation contract

The new toolkit owns shipped baseline code, templates, schema and tests.
Projects own their manifest, gate log, board, task indexes, policy adaptations,
local skills, product metadata and runtime state. Upgrade preflight must
recognize prior installation ownership; detect edits, removals, symlinks and
collisions before writing; preserve extra local files and approval history;
and refuse conflicts with actionable paths. Automatic semantic merging is
out of scope. Legacy targets without ownership records may only adopt files
that match the incoming source; ambiguous replacements must stop.

Installation must not digest arbitrary target-owned additions as baseline
content. Installation provenance must retain previous records and local
amendments, including those already absorbed into the incoming baseline.
Failure rollback must cover replaced files, newly created files, managed
agent instructions, ignore-file changes and installation metadata.

The board is part of the standard toolkit. Its Python/PyYAML requirements are
tooling requirements; installation must not overwrite a product pyproject or
lockfile. Projects may use the supplied standalone requirements file with
uv or an isolated Python environment. JSON Schema validation is required in
the regression suite; the runtime's semantic checks remain additional rules.

The lifecycle contract remains based on 1.0.2. A separate candidate identity
must clearly mark this distribution unreleased in doctor and installation
records; inherited 1.0.2 release/tag evidence is not v3 publication evidence.
Release numbering and publication are deferred to human disposition.

## Stop conditions and exclusions

Stop affected work for an original-source mismatch, missing prerequisite,
unrecoverable fixture failure, undocumented ownership choice, expanded product
scope, needed external mutation, or a security/approval weakening. Record the
condition and preserve evidence. Routine implementation choices within this
contract may proceed with written rationale. Existing 1.0.3/1.1 concepts are
retained at their original status and are not implemented by this migration.

## Validation plan

- Full inherited `./scripts/test-methodology.sh --suite all` before and after.
- `./scripts/gendev-doctor.sh`, `./scripts/check-methodology.sh`, staged/range
  guards at applicable checkpoints.
- Board runtime and JSON Schema regressions, skill metadata/link checks.
- Disposable fresh install, clean upgrade, edited baseline, custom skill,
  local-amendment, target-policy, agent-integration and failure-rollback cases.
- Initializer and later-phase directive consistency, initialized-copy dry run,
  and an isolated C1 development exercise with real executed code/tests.
- Source preservation verification using input-manifest.json.

The development exercise uses fixture authority and fixture human identities,
clearly labeled synthetic; it grants no acceptance or gate approval to a real
project. Remote CI, Linux execution, actual fresh-context agent behavior and
formal independent review are separate evidence classes, not inferred from
local deterministic checks.

## Evidence

- input-manifest.json: frozen source inventory, refs and recovery digests.
- v2-copy-tests.log: all 13 inherited suites passed before integration.
- Subsequent execution and test records will be added here in step 6.
