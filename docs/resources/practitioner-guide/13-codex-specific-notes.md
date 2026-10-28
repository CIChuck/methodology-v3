# 13. Codex-Specific Notes

## Scope And Sources

Last reviewed: 2026-10-28
Review scope: v3 repository instructions, skill discovery and separation of
provider permissions from GenDev authority. Exact CLI flags, subscription access
and model defaults are outside this guide; consult the installed harness.

Codex reads AGENTS.md as repository instructions, with layered project guidance.
Start from the intended product root so the right files govern the task.
[Official instruction guidance](https://learn.chatgpt.com/docs/agent-configuration/agents-md).

Codex discovers repository skills under `.agents/skills/`; skill metadata routes
discovery while full instructions/resources load when used. Preserve whole skill
bundles when they contain supporting files.
[Official skill guidance](https://learn.chatgpt.com/docs/build-skills).

## V3 Entry Contract

The toolkit's AGENTS.md points to the constitution, policies and canonical skills.
An installed product's authority lives under docs/project; baseline maintenance
instead follows its authorized evolution directive. Begin with:

```bash
./scripts/gendev-doctor.sh
./scripts/project-state.sh
uv run --no-project --with-requirements requirements-devboard.txt python scripts/devboard.py validate
uv run --no-project --with-requirements requirements-devboard.txt python scripts/devboard.py next
```

Run project-state for an initialized product. Inspect the selected task and the
actual branch/authority before code generation. A good initial prompt asks for
the current gate, required approver, active artifact and next permitted action.

## Settings And Permissions

Choose provider model, reasoning and access settings in the active Codex/T3
configuration. They are machine/account settings, not baseline product authority.
A tool-level approval or permissive sandbox does not approve a GenDev gate,
accept risk, authorize product scope or supply human attestation. Follow the
current harness's tools and permissions rather than copying flags from an old
session or assuming a model/subscription is available.

## Independent Review And T3

Use only authorized delegation. Every formal review uses a frozen candidate,
pinned authority and a fresh context with no builder transcript or conclusions
as proof. The validator is read-only; advisory scores are not formal VERIFIED.
Follow active dispatch/worktree and watch/unwatch rules when Codex runs through
T3. Worktree setup validates existing authority and must not reinitialize it.
Optional actions are documented in `docs/methodology/guides/t3-code-integration.md`.

Keep product commands and durable facts in the appropriate project artifacts,
not just chat or memory. Run the methodology checker and applicable guard; report
failures and reconcile actual authority instead of bypassing a hook or inventing
approval. Chapter 21 lists skill availability and pending-review follow-ups.
