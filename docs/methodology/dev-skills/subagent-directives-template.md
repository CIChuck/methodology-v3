---
name: subagent-directives-template
description: Prepare bounded builder and independent validator handoffs for authorized GenDev implementation and review. Capture phase authority, candidate identity, verification, permitted effects, and human acceptance boundaries.
---

# Builder and Independent Validator Handoff Template

Use when delegated implementation or review is authorized. Replace bracketed
values before dispatch. The template itself does not grant delegation,
implementation, commit, or delivery authority.

Read `AGENTS.md`, the policies in `docs/policies/`, the project manifest at
`docs/project/project.yaml`, and the current phase authority. AGENTS.md defines
precedence. Follow `docs/methodology/guides/subagent-coordination-protocol.md`
and the active provider orchestration rules. For a board-tracked task, read its entry
in `docs/planning/board.yaml` and tracking index; task-scoped permission does
not satisfy GenDev's product implementation prerequisites.

## Controller preparation

- Project and phase: `[PROJECT AND PHASE-ID]`
- Work unit or tactical task IDs: `[TASK-IDS]`
- Current gate and phase checkpoint: `[ACTUAL MANIFEST STATE]`
- Accepted phase and tactical plans: `[PATHS AND REVISIONS]`
- Approved construction directive: `[PATH AND REVISION]`
- Acceptance criteria: `[CRITERION-IDS]`
- Source authority manifest: `[PATHS, REVISIONS, AND HASHES]`
- Branch, checkout ownership, and base commit: `[EXACT IDENTITY]`
- Owned files and non-goals: `[BOUNDED SCOPE]`
- Verification and permitted test outputs: `[COMMANDS AND EXPECTATIONS]`
- Authorized external effects, credentials, and costs: `[NONE OR EXACT AUTHORITY]`
- Delegation and commit authority: `[RECORDED HUMAN DIRECTION]`
- Effort limit and stop conditions: `[BOUNDARIES]`

Confirm that GenDev permits implementation at the recorded checkpoint and that
required artifact approvals exist. Preserve unrelated work. The repository
needs an initial commit before isolated worktrees or a frozen candidate review.

## Builder dispatch

Use the active session's authorized delegation mechanism and checkout rules.
Provide only the assignment's required authority, inputs and permitted effects.
For T3-specific examples see docs/methodology/guides/t3-code-integration.md.

Provide the bounded assignment and instruct the builder to:

1. read the pinned authority and implement only the approved directive;
2. stop on scope, authority, security, or checkout conflicts;
3. add and run the required meaningful verification;
4. update the required phase evidence and documentation;
5. record omitted checks and baseline failures;
6. commit only when authorized, excluding unrelated files; and
7. return the candidate identity, exact diff, and requirement-to-evidence report.

The builder may not approve or independently verify its own candidate, widen
scope, push, merge, release, deploy, or create external effects without the
applicable authority.

## Candidate freeze and review request

After checking candidate stability and scope, prepare a validation request at
`[EXACT REQUEST PATH]`. Use the canonical phase code-review artifact referenced
by the manifest, phase-local supporting evidence, or aggregate review support
under `docs/project/review/` as appropriate.

Record phase/task IDs, base and candidate commits, diff range, authority pins,
directive, acceptance criteria, full/delta/aggregate mode, required commands,
known failures/exclusions, permitted outputs/effects, and exact report and
evidence locations. Do not dispatch formal validation of uncommitted work.

## Validator dispatch

Assign a fresh-context validator using
`.agents/skills/independent-code-validator/SKILL.md`. Give it only the frozen
request and named repository inputs, not the builder conversation or its
conclusions. Ensure the chosen review mechanism starts a fresh context. A
human independent reviewer may fulfill the same policy gate.

The validator is read-only. It returns exactly VERIFIED, CHANGES_REQUESTED, or
BLOCKED, with cited evidence and context provenance. It may not repair the
candidate, update project state, accept work, commit, push, merge, release,
deploy, or disclose credentials.

## Controller disposition

Store the request, report, and evidence at their declared paths and reconcile
them with the canonical phase/aggregate review and traceability artifacts.

- VERIFIED permits a proposal for the next authorized human decision; it does
  not close a gate or establish acceptance.
- CHANGES_REQUESTED requires a bounded remediation directive covering each
  numbered finding, authorized fixes, a new candidate, and a fresh review.
- BLOCKED requires the exact missing authority/evidence and the condition that
  would allow review to resume.

After two unsuccessful remediation cycles, return unresolved findings to the
human. Record actual gate or phase decisions through the installed GenDev
transition commands only after the required human approval and evidence exist.
