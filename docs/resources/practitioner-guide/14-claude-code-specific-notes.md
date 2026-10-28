# 14. Claude Code-Specific Notes

## Scope And Sources

Last reviewed: 2026-10-28
Review scope: v3 instruction entry, skill integration and fresh-context governance.
Verify the active Claude Code version and settings; provider controls can change.

Current Claude Code supports AGENTS.md, with loading dependent on configuration
and whether CLAUDE.md files are present. Where direct loading is unavailable or
CLAUDE.md is used, an `@AGENTS.md` import remains a supported way to share the
repository instructions. Confirm what actually loaded rather than assuming either
file was read. [Official memory/instruction guidance](https://code.claude.com/docs/en/memory).

Example project-local adapter, when needed:

```markdown
@AGENTS.md

Follow the GenDev constitution and policies referenced there. Read the actual
project manifest and gate log before acting on product work.
```

## Skill Discovery

Claude Code project skills use `.claude/skills/`. GenDev's canonical skill content
is under `docs/methodology/dev-skills/`, exposed through `.agents/skills/` for
providers that discover that surface. Read canonical sources directly or adopt
an explicit project-local adapter, preserving complete folders and relative
resources. Do not assume that `.agents/skills/` alone is discovered by every
provider. [Official skill guidance](https://code.claude.com/docs/en/skills).

## V3 Operating Pattern

Start from the product root. Read the shared instructions, project manifest,
gate log and board. Run the doctor, project-state, board validate/next and inspect
the selected task before implementation. A fresh product is G1 pending with an
empty board; the owner selects tasks. Skills and provider settings do not create
product approvals or a new task scope.

Use Claude-specific settings/rules for provider behavior while keeping GenDev
policy and canonical product authority in their established files. Access settings
are not GenDev gate decisions. A plain stop request means stop, regardless of a
similarly named PR workflow. Read Chapter 21 before invoking workflow skills.

## Review And Memory

For conformance, use an authorized fresh review context with exact authority and
candidate pins, no builder transcript/private reasoning, and read-only effects.
Do not reuse the builder conversation or delegate gate acceptance. A reviewer
returns VERIFIED, CHANGES_REQUESTED or BLOCKED under the local policy; model
scores and green checks remain separate evidence.

Treat memory as supporting context. Put accepted facts, commands, approvals and
changes in the appropriate durable project records. A hook failure calls for
reconciliation, not a silent bypass. Keep declaration of actual actor authority,
independent review, human acceptance and remote delivery distinct.
