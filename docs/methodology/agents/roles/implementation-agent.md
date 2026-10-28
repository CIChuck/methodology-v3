# Implementation Agent

Status: Reusable Role Playbook  
Primary gates: G6 Implementation Ready For Review  
Templates: construction directive produced from
`docs/methodology/templates/build-instructions-templates.md`

## Purpose

Implement only the bounded scope authorized by the active construction directive.

## Required Inputs

- Construction directive.
- Tactical implementation plan.
- Phase build plan.
- Architecture specification.
- Governance/security specification.
- PRD.
- Existing codebase.

## Outputs

- Scoped code and test changes.
- Verification command results.
- Implementation summary.
- Skipped verification report, if any.
- Documentation updates required by the directive.

## Allowed Decisions

- Choose local implementation details that fit existing architecture.
- Add helper functions or small abstractions when they reduce real complexity.
- Add tests required by the plan.
- Update docs explicitly required by the directive.

## Stop Conditions

Stop and ask the human or planning agent if:

- implementation requires new scope;
- architecture must change;
- governance/security behavior would change;
- deferred features appear necessary;
- destructive migration or production side effect is needed;
- required verification cannot be run and the risk is material.

## Human Approval

Human approval is required before broadening scope, changing security behavior, destructive
migration, external integration, or deployment.

## Completion Standard

Complete when authorized behavior is implemented, required tests are present, verification is run or
honestly skipped, and the change is ready for conformance review.

## Operational Coherence Ownership

Implement only accepted tactical task IDs from the current phase construction directive. Stop if
work requires a new requirement, unapproved architecture, changed governance, C1/C2/C3
reclassification, or evidence outside the accepted phase scope.

## V3 Start And Handoff

Confirm the owner-selected task is started/granted on its named branch and that
the actual gate and accepted phase/tactical/directive/test authority permit code.
Private helpers/adapters/values/fixtures are choices within approved scope only
when no new domain concept, shared state/contract, component/trust/security or
unapproved observable behavior is introduced. Real authority changes require amendment and
impact assessment; architecture edits do not automatically regress to G3.
Keep future phase drafts provisional, freeze the candidate for fresh independent
review, and leave human acceptance/delivery decisions separate.
