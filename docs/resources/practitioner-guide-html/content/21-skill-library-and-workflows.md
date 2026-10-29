# 21. Skill Library And Workflows

## Skills Package Techniques

Skills provide reusable instructions and sometimes scripts, templates or provider
UI metadata. They do not replace project authority or grant permissions simply
by being installed, discovered, read or discussed. Use them within the user's
actual request and accepted GenDev scope. The shared execution contract is
`docs/methodology/guides/skill-execution-contract.md` in the current library.

Canonical sources live under `docs/methodology/dev-skills/`; discovery entries
under `.agents/skills/` link to them. Legacy single-file sources have a linked
SKILL.md. Packaged skills link their entire folder so sibling resources remain
usable. Do not copy only SKILL.md when a bundle has scripts, references or UI
metadata. Providers with different discovery conventions can read the canonical
source directly or use an explicitly adopted adapter (Chapters 13–14).

## Catalog And Availability

The independently reviewed migration candidate `98f8bec` contains the first 15
skills. The nine additional PR/coordination skills and this guide were merged
through PR #1 at `d41e0eb`, bringing GitHub main to 24 skills. Council round 1
returned two BLOCKED outcomes and one VERIFIED outcome; the controller retained
BLOCKED because required preservation evidence failed and a mandatory instruction
conflict remained. Bounded remediation is local on `fix/skills-council-follow-up`,
with one fresh council round authorized. Human acceptance and v3 release remain
pending. No earlier verdict automatically covers the revised candidate.

| Skill | Use |
| --- | --- |
| vision-framing | Frame the problem, users, outcomes and non-goals |
| prd-author | Author testable requirements and acceptance criteria |
| architecture-spec-author | Define architecture and verification contracts |
| governance-security-spec | Define security/governance authority |
| phase-build-planner | Plan bounded phases and their tests |
| tactical-implementation-planner | Turn accepted scope into exact tasks |
| ai-construction-directive-builder | Prepare controlling code-generation instructions |
| code-conformance-reviewer | Review the six principles and approved scope |
| remediation-closeout | Reconcile findings and close-out evidence |
| traceability-matrix | Maintain requirement-to-evidence links |
| migration-refactor-analyst | Analyze a bounded migration/refactor |
| subagent-directives-template | Package bounded agent assignments |
| subagents-worktrees-template | Package authorized isolation/coordination guidance |
| independent-code-validator | Fresh read-only formal candidate validation |
| friday-dev-board | Operate the task board alongside GenDev |
| babysit-pr — follow-up | Monitor authorized PR work with the supported watcher |
| council — follow-up | Obtain an explicitly requested multi-provider advisory review |
| file-pr — follow-up | Prepare an authorized PR with accurate scope and evidence |
| full-send — follow-up | Execute an explicitly requested end-to-end PR workflow within authority |
| full-stop — follow-up | Prepare an explicitly requested PR workflow for human merge |
| leaving-pr-comments — follow-up | Attribute authorized agent-written GitHub comments |
| modernize — follow-up | Reassess/rebase an existing PR within requested scope |
| sol-loop — follow-up | Run a bounded requested Sol review workflow |
| takeover — follow-up | Continue inherited work while preserving intent and credit |

Read the actual skill before use. Availability of a named model/provider/tool is
resolved at runtime; a catalog entry does not promise account access, a particular
subscription, machine defaults, or permission to delegate.

## Governance Across Workflows

A workflow invocation can grant its stated task-scoped effects when compatible
with the actual request and accepted authority. It cannot approve GenDev gates,
supply human attestation, bypass branch protection or silently waive a required
human review. Ordinary requests to stop or pause mean stop; discussing full-stop
is not permission to begin PR preparation.

Conformance review needs an exact frozen candidate, pinned authority and a fresh
context. Advisory scores/APPROVE and bot results are not formal VERIFIED. A changed
candidate needs fresh review. Apply the declared budget and return unresolved
mandatory findings after two unsuccessful remediation cycles unless the human
explicitly authorizes an extension. No reviewer self-remediation or nested
reviewer delegation is inferred.

Use the active provider's orchestration, worktree and credential rules. In T3,
keep PR watches parent-owned, use its watch/unwatch lifecycle, and never substitute
a polling loop. The bundled Unix/Python/gh pr-wait fallback is for other harnesses
that permit it, reads GitHub and keeps local watcher state. It is not a merge gate
or a tool to run merely because the library was imported.

## Adding Or Updating Skills

Inspect the source bundle, metadata, references and scripts; record provenance
and permitted scope. Reconcile policy conflicts in the imported copy while
preserving the source. Add canonical content and discovery links, update inventory
checks, then verify fresh install and dry-run resource paths. Test script entry
points without starting an unrequested live workflow. Keep new executable or
behavioral changes on a follow-up candidate with the applicable independent review;
an earlier VERIFIED checkpoint does not cover them automatically.
