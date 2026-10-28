---
name: phase-build-planner
description: Use when defining build definitions or phase build plans from accepted PRD and architecture authority. Focuses on bounded scope, phase objectives, dependencies, deferred items, sequencing, risks, test strategy, migration behavior, acceptance criteria, and documentation close-out.
metadata:
  short-description: Plan bounded build phases
---

# Phase Build Planner

Use this skill to turn product and architecture authority into a bounded build phase.

The goal is to prevent feature smuggling and create a phase that can become a tactical implementation plan.

## Governing Standard

Follow `docs/methodology/constitution/gendev.md` when available.

## Inputs

Use:

- PRD;
- architecture specification;
- governance/security specification;
- build definition;
- prior phase reports;
- deferred feature backlog;
- code review findings, if applicable.

## Output Structure

Produce a Markdown build plan with:

- title;
- status;
- date;
- source authority;
- phase objective;
- in-scope work;
- out-of-scope work;
- deferred items;
- dependencies;
- assumptions;
- workstreams;
- sequencing;
- migration/removal requirements;
- security/governance implications;
- architecture mirror check;
- test strategy;
- CLI/API/UAT strategy;
- phase exit test traced to PRD requirements and the vision;
- acceptance criteria;
- documentation close-out;
- risks;
- open decisions.

## Scope Rules

- Label every major item as included, deferred, out of scope, or blocked.
- Do not let implementation details override architecture.
- If scope is too broad, recommend subphases.
- Make migration/removal work first-class for refactors.
- Make documentation close-out part of definition of done.

## Architecture Mirror Check

Hold the accepted G3 architecture up as a mirror: confirm the phase still conforms
to it, and surface anything the phase reveals that the architecture did not
anticipate. A necessary change triggers impact assessment under
`docs/methodology/guides/amendment-and-regression-protocol.md`, not automatic
regression to G3.

Stop affected implementation, record the amendment and its rationale, identify
affected requirements/plans/tests, obtain the required human approval, and
reconcile downstream artifacts before using changed authority. Keep the current
gate when its governing conditions remain satisfied. Regress only when the change
invalidates a previously satisfied gate condition, returning to the earliest gate
whose decision must be revisited. Editorial corrections need no gate regression.

## Accuracy Pass

Before finalizing, identify:

- scope ambiguity;
- deferred items that look included;
- included items without acceptance criteria;
- a phase exit test that does not trace to PRD requirements and the vision;
- an unperformed architecture mirror check;
- an architecture change without an impact assessment and amendment disposition;
- missing test strategy;
- missing migration work;
- missing security/governance work;
- unresolved decisions that block tactical planning.

## Completion Standard

The build plan is complete when a tactical implementation planner can convert it into executable workstreams.

## Operational Coherence Requirements

The project-wide phase plan describes the whole build: phase order and scope, requirement
ownership, dependencies, the coverage contract, integration criteria, and explicit deferrals.
It does not need to pre-author the detailed implementation of every future phase.

Phase build plans may be drafted ahead to clarify boundaries, non-goals, dependencies, and
provisional verification expectations. Those advance drafts remain Draft and do not enter,
close, or advance a checkpoint or authorize code generation. Formal acceptance still requires
the applicable checkpoint prerequisites, required approval, and pinned upstream authority.

Develop and finalize detailed tactical plans and construction directives just before their
phase, incorporating the prior phase's learnings (N/A for the first phase). The next phase's
tactical plan must cite those learnings. Issue a build prompt only through the applicable
checkpoint from the accepted, pinned directive and authorized current-phase scope.

Record test/UAT execution, review outcomes, remediation disposition, traceability results, and
as-built evidence from actual work. Advance planning drafts must never present future execution
or acceptance as already completed. Follow `docs/methodology/guides/phase-loop.md` for this
rolling-wave drafting cadence and `docs/methodology/guides/gates.md` for checkpoint conditions.
