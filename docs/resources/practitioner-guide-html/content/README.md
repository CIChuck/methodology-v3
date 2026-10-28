# GenDev Methodology-v3 Practitioner Guide

Status: Unreleased v3 distribution guidance; 1.0.2 lifecycle contract
Documentation review date: 2026-10-28
Audience: Product owners, developers, architects, technical leads and AI-agent operators.

## Purpose

This is the field manual for using methodology-v3 from first orientation through
product definition, bounded code generation, independent review and production
close-out. The constitution and accepted project authority control the work;
this guide explains how to use them with the board, skills and current tools.

## What V3 Adds

V3 combines GenDev's documentation and gate discipline with a portable task board,
engineering policies, independent builder/validator handoffs and a standard skill
library. It permits proportionate private implementation details, uses amendment
impact to decide gate regression, and supports advance phase-plan drafts while
keeping tactical plans and construction directives just in time.

New products start at **G1, pending approval**, with an **empty task board**.
The repository owner chooses board tasks, scope and priorities. The manifest and
gate log own product approvals; board state never replaces them.

Installation records baseline ownership, file hashes and modes. Upgrades preserve
project authority, board/task history, policies and local extensions, and stop on
conflicts. A fresh isolated dry run uses canonical seeds instead of live state.

## Availability And Release Status

| Surface | Current status |
| --- | --- |
| Normative lifecycle and inherited release | GenDev 1.0.2; the version has not been renamed to 3.0 |
| V3 distribution | Unreleased; GitHub hosting is not a new methodology release |
| Migration implementation | Candidate `98f8bec` independently VERIFIED; human acceptance pending |
| Default GitHub `main` | Migration baseline plus hosting/delivery records; 15 baseline skills |
| Nine additional workflow skills | Present on `integration/v3-skill-import` and this documentation branch; local checks passed; independent review pending |
| This documentation refresh | Describes the combined v3 approach; it does not accept or release either candidate |

Use an exact approved revision when adopting the toolkit. A branch name or current
HEAD is not proof that every subsequent change received the earlier review.
The full 24-skill catalog and its status are in Chapter 21.

## Reading Path

Read Chapters 1–7 for foundations. Use Chapters 8–11 during delivery and operations.
Chapters 12–18 supply examples, provider notes, prompts, checklists and terminology.
Chapter 19 covers existing product documents. Chapters 20–22 explain the v3 board,
skills, distribution and upgrades.

1. [Orientation](01-orientation.md)
2. [Core Mental Model](02-core-mental-model.md)
3. [Repository Map](03-repository-map.md)
4. [Starting A New Project](04-starting-a-new-project.md)
5. [Working With The Agent](05-working-with-the-agent.md)
6. [Gates And Artifacts](06-gates-and-artifacts.md)
7. [Approvals And Risk](07-approvals-and-risk.md)
8. [Subagents And Delegation](08-subagents-and-delegation.md)
9. [Build Planning And Implementation](09-build-planning-and-implementation.md)
10. [Review, Remediation, And Close-Out](10-review-remediation-and-closeout.md)
11. [Production Operations](11-production-operations.md)
12. [Vendor Contract Tracker Walkthrough](12-vendor-contract-tracker-walkthrough.md)
13. [Codex-Specific Notes](13-codex-specific-notes.md)
14. [Claude Code-Specific Notes](14-claude-code-specific-notes.md)
15. [Prompt Library](15-prompt-library.md)
16. [Checklists](16-checklists.md)
17. [Common Failure Modes](17-common-failure-modes.md)
18. [Glossary](18-glossary.md)
19. [Starting Mid-Stream](19-starting-mid-stream.md)
20. [Work-Item Board](20-work-item-board.md)
21. [Skill Library And Workflows](21-skill-library-and-workflows.md)
22. [Installation And Upgrades](22-installation-and-upgrades.md)

## How To Use This Guide

Follow the current gate and actual authority revision. Drafting, local checks,
independent VERIFIED, completion, human acceptance, GitHub delivery and a release
are separate events. Read the applicable chapter before invoking a workflow;
installing or discussing a skill never runs it or supplies approval.

Current adoption guidance: `docs/resources/releases/v3-adoption.md`.
Inherited 1.0.2 guidance remains at `docs/resources/releases/1.0.2-adoption.md`;
use the v3 guide for the changed distribution and operating approach.

Primary authority is `AGENTS.md`, the GenDev constitution, operating guides and
local policies, plus `docs/project/project.yaml` and its canonical artifacts after
product initialization. A methodology source repository instead uses its explicit
baseline evolution directive; do not initialize a fake product to maintain it.

## Canonical And HTML Editions

These Markdown files are canonical. The HTML edition's `content/` directory must
contain exactly the same files and bytes. Its chapter catalog must include each
chapter. Recopy and verify the mirror after any edit; an updated website title
alone does not synchronize content. See the HTML edition's README for commands.
Historical decision records and review evidence remain historical rather than
being rewritten to match current guidance.
