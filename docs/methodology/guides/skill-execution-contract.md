# Skill Execution Contract

Status: Reusable operating guidance for workflow skills
Authority: AGENTS.md, the GenDev constitution and applicable project authority

Skills supply techniques within an authorized task. Discovery, installation,
mentioning a skill while discussing it, and reviewing its text do not invoke its
workflow or grant approval. Apply the user's actual requested scope and selected
collaboration mode. A request to pause or stop is a stop instruction; do not turn
ordinary wording into a PR workflow.

## Authority and effects

Before implementation, read the manifest and gate log for an initialized product,
or the explicitly authorized evolution directive for baseline toolkit work.
Follow the task lifecycle and independent validation policies. Workflow labels,
review scores, tool readiness, bot verdicts and a green PR do not approve GenDev
gates, accept work, supply attestation or authorize production.

Explicit workflow invocation may grant its stated task-scoped execution effects
when compatible with the user's instruction and accepted authority. Confirm the
actual scope before commits, pushes, comments, rebases, force-with-lease, merges
or live tests; retain separate evidence for each. A material authority change
requires amendment before implementation. Never bypass branch protection or
required human approval. When an explicitly invoked skill authorizes messages
to others, name and link that skill in the final report. Reviewer advice to obtain human review cannot be
silently discarded when a governing approval requirement applies.

No new dependency, provider/account, credential, remote, deployment or unrelated
mutation is authorized merely because a skill could use it. Use the active
harness's credential and tool mechanisms. Do not print credentials. A scoped
review is read-only unless explicitly assigned remediation as separate work.

## Review and remediation

Use the independent validation policy for formal conformance: freeze an exact
candidate, pin authority, supply acceptance criteria and receive VERIFIED,
CHANGES_REQUESTED or BLOCKED. Advisory APPROVE, confidence scores and bot checks
do not replace that result. Every review/recheck gets a fresh context without the
builder transcript or private reasoning; an earlier result does not cover a
changed candidate. No reviewer edits, nested delegation or external effects.

Apply the declared round budget and the policy's stop after two unsuccessful
remediation cycles. Return unresolved mandatory findings and options to the human;
extra rounds require human disposition. A mandatory contract or security violation
remains mandatory even when rare or outside the happy path. Report out-of-scope
findings separately; do not silently implement them or waive governing criteria.

## Provider integration and monitoring

Follow the active provider's orchestration rules. Availability does not authorize
delegation. Resolve requested provider/model/settings at runtime; unavailable
choices are blockers, never grounds for an unasked substitution. In T3, use its
capability/delegation tools where required, fresh review tasks, bounded budgets
and parent-owned PR watches. Do not make top-level threads for delegates.

Use one supported watcher per PR and the provider's wait/resume semantics. In T3,
use watch_pull_request and unwatch at handoff; never run the bundled fallback or
an additional polling/sleep loop there. Outside T3, use the bundled pr-wait only
when that harness permits it. It requires Unix, Python 3.11+ and an authenticated
gh CLI, reads GitHub and stores local state under ~/.local/state/pr-wait/. It
reports events, not permission to merge. If the supported watcher is unavailable,
report the limitation; do not invent a background workaround.

Use verified repository review/check requirements, not assumed bot brands or a
hard-coded default branch. Resolve the actual PR base/head and recheck their
identity before external mutations. Link, watch and stop tasks using the active
harness's rules. Capability documentation governs tool parameters.
