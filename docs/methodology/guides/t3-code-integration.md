# Optional T3 Code Integration

GenDev's core policies are provider-neutral. The example action definitions in
`docs/methodology/integrations/t3/t3.json` provide health, state, validation and
board commands. Adopt them into the project's t3.json when requested. Worktree
setup validates an existing project; it must not reinitialize authority.

Follow the active T3 session's orchestration rules for authorized subagents,
provider/model selection, worktree isolation and review. A skill or action
never grants delegation, product implementation, acceptance or external effects.
Machine model defaults, account identities, credentials and full-access settings
are not part of the distributed baseline.
