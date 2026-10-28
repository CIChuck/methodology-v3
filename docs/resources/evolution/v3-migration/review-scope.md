# Independent Review Scope: Methodology-v3 Migration

Status: Review authorized by Chuck Russell; acceptance pending
Authority: migration README.md, including the quoted step 7 authorization
Task: v3-baseline-migration
Mode: full conformance review of steps 1–6, with fresh full review after fixes
Reviewer count: one fresh context per round, sequential only

## Controlling authority and applicability

Follow AGENTS.md, the GenDev constitution, repository-engineering-policy.md,
development-task-lifecycle.md, independent-validation-policy.md, and
dev-board-integration.md. Apply the independent-code-validator skill.
The migration README's implementation contract is the bounded construction
directive for this baseline engineering task. This is a methodology source
repository, not an initialized product: no product PRD/architecture or G1
approval is fabricated for the migration. Product gate protections still apply
to projects created by the toolkit. Review the request's pinned revisions/hashes.

The approved scope is preservation, generalization of the T3 integration,
promotion of the four clarifications, the specified audit fixes, and isolated
validation. Final step 8 documentation refresh, future 1.0.3/1.1 proposals,
release numbering/publication, real product implementation and deployment are
not implemented or accepted by this review. Essential current commands,
authority boundaries and changed operating instructions must nevertheless work.

## Acceptance criteria

- RV-01: both original projects retain their frozen file bytes, symlinks,
  modes, Git refs and working state. V3 preserves all inventoried v2 history,
  branches/tags including local-only history, uses independent Git storage,
  and has no configured remote or shared object alternate.
  Apply only Chuck's separately recorded narrow additive-checkpoint exception
  in the migration README and review/round-1/checkpoint-exception-approval.json.
  It permits matching-tree, higher-ordinal T3 checkpoints in an already frozen
  context; no frozen ref, file or state may change, and every allowed addition
  must be reported. The original inventory remains unchanged.
- RV-02: the copied baseline and its historical/draft/concept material remain
  identifiable. No historical acceptance or proposal is promoted into new
  product authority. Candidate identity is explicitly unreleased and separate
  from the inherited 1.0.2 lifecycle/release evidence.
- RV-03: reusable engineering/lifecycle/validation rules, board tooling,
  schema, templates/tests and discoverable skills are coherent and portable.
  Product metadata, named approvers, sample application paths, measured debt,
  task/approval history and machine settings are not seeded into new products.
  Board requirements remain separate from product runtime dependencies.
- RV-04: all four approved clarifications are incorporated consistently in
  active canonical guidance. Private implementation choices are proportionate;
  product/contract/data/architecture/security changes remain controlled;
  amendment impact determines regression; advance drafts do not authorize
  execution. Origin records remain historical evidence rather than new approvals.
- RV-05: baseline ownership and project-owned seeds are explicit. Upgrade
  preflight refuses changed/missing owned files, unsafe symlinks, unowned
  collisions, malformed ownership data and unresolved local amendments before
  writes. Force does not authorize loss of local customizations. Ordinary clean
  recorded baseline updates remain possible, and derived dashboard refresh
  preserves task state.
- RV-06: upgrades preserve local extra files/skills, project-owned policies,
  board/task state, canonical project authority and approval history. Integrity
  ownership excludes arbitrary local additions; previous installation and local
  amendment records survive. Failed operations roll back replaced and new files,
  directory creation, managed agent includes, ignore changes and metadata under
  the documented failure/interrupt contract. Filesystem-wide power-loss/SIGKILL
  atomicity and automatic semantic merging are excluded, as documented.
- RV-07: initial/later directives use the canonical complete anti-drift
  contract, correct phase references and literal user-input rendering. The
  documented fresh dry run works from an initialized project without replacing
  its authority. Accepted/archive and completed/planning backing packet records
  agree between JSON Schema and runtime checks, including negative cases.
- RV-08: security, essential runtime invariants, meaningful typing, component
  contracts, YAGNI/KISS/DRY/SRP/least astonishment and NAA satisfy governing
  rules for the changed scope. A violated mandatory requirement is a finding;
  stylistic preferences without a concrete violation are advisory.
- RV-09: required checks are reproducible and actually prove the relevant
  behavior, failure paths and preservation claims. Test results are not inferred
  from builder conclusions or matched prose. Report known baseline failures,
  omissions and evidentiary limits. The synthetic helper is not a real product
  gate traversal, fresh-context behavioral exercise, human approval or deployment.
- RV-10: reviewer independence, exact candidate identity, authority pins and
  outcomes are recorded. The board remains started during review/remediation;
  independent verification, task completion, human acceptance and delivery remain
  distinct. No effect outside the authorized local scope has occurred.

## Review inputs and evidence discipline

Review the complete baseline-to-candidate diff and relevant surrounding modules,
not only changed lines. Test implementation and negative controls as appropriate
to these criteria. Frozen raw input inventories/archives and primary source/test
files are evidence inputs. Builder-created reports, conclusions and historical
test logs in the candidate are artifacts to audit, not proof of conformance.
Do not receive the builder transcript/private reasoning or rely on its summary.

## Required commands and permitted effects

Run the doctor, methodology checker, board validate/next/show, full inherited
suite, board/schema tests, migration tests, and isolated experiment harness as
applicable. Inspect skill metadata/links, candidate identity/provenance and
ownership behavior. Verify preservation and archived refs, and Git connectivity.
Use existing local tools/dependencies, e.g. `UV_OFFLINE=1 uv run --frozen
--group devboard python ...`; package/network access is not authorized.

Tests may create disposable fixtures, .tmp scratch, caches and local fixture
Git repositories. Capture output outside governed candidate files. The experiment
harness accepts an output path: supply a disposable path rather than overwriting
its checked-in experiments.json. Source preservation checks are read-only against
both originals. No source, test, policy, authority, board, candidate commit/ref,
remote or original-project mutation is permitted to the reviewer. Do not install
packages, change credentials, push, merge, publish, release or create delegates.
Record unavailable checks as limitations/blockers according to their requirement;
do not manufacture Linux/hosted CI results or formal acceptance.

## Output and stopping conditions

Return exactly one outcome: VERIFIED, CHANGES_REQUESTED or BLOCKED, followed
by pinned candidate/diff identity, independence provenance, criteria-to-evidence
mapping, reproducible commands/results, numbered findings with severity/location/
requirement/risk/mitigation/tests, baseline-versus-regression classification,
omitted checks/limits and residual risk. Return report text to the lead; the lead
records it at the declared report path. No reviewer edits or self-remediation.

Budget: one thorough full pass, including the required local suites and targeted
counterexamples; report a concrete blocker if necessary verification cannot be
performed. Stop for critical security risk, missing/conflicting authority, scope
expansion, needed external effects or candidate drift. The lead may remediate
in-scope findings and request a new fresh-context review; after two unsuccessful
remediation cycles, return remaining findings to Chuck.

## Task-specific cycle extension

Chuck approved exactly one additional VAL-005 remediation/review cycle after
the two-cycle stop. See review/round-3/human-disposition.md and
review/round-3/remediation-directive.md. This review remains full RV-01–RV-10;
further mandatory findings return to the human without automatic remediation.

## Authorized VAL-005 boundary follow-up

Chuck Russell instructed on 2026-10-28: "lets fix it and test it" after the
round-4 bounded follow-up proposal and explanation of fresh review. Apply
review/round-4/remediation-directive.md for this one fix/test/review cycle.
Further mandatory findings return to Chuck; acceptance remains pending.
