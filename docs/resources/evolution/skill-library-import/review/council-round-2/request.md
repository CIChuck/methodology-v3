# Independent skills council — Round 2
Created: 2026-10-28T23:48:48.413954+00:00
Project: methodology-v3 reusable baseline (no active product docs/project required)
Task: skill-library-import
Role/mode: fresh read-only FULL skills conformance plus bounded remediation review
Repository: /Users/chuckrussell/Dev/gendev/methodology-v3
Branch: fix/skills-council-follow-up
Base: ee82653ed6cacb9e1157cd791f12d0fb774f12af
Prior candidate (remediation comparison only): d41e0ebfdc587ecc6d8c3ab336afc530ce90654f
Frozen candidate: aa25aa89762974012c0243e6134e9785f5db970d
Selected full diff: selected.diff, SHA256 d34f9b633a639eebe2e9b6bb31cc50ce941b777c3a59cba1c18d1363a88ba0ca
Reproduce: git diff --binary ee82653ed6cacb9e1157cd791f12d0fb774f12af aa25aa89762974012c0243e6134e9785f5db970d -- .agents/skills docs/methodology/dev-skills docs/methodology/guides/skill-execution-contract.md scripts/create-dry-run.py scripts/verify-migration-inputs.py tests/migration AGENTS.md README.md docs/resources/releases/v3-adoption.md docs/resources/practitioner-guide docs/resources/practitioner-guide-html/content docs/planning
Remediation diff: git diff d41e0ebfdc587ecc6d8c3ab336afc530ce90654f aa25aa89762974012c0243e6134e9785f5db970d, excluding historical raw council evidence/validation logs from code audit. These remain available as historical provenance, not proof.
Authority: authority-manifest.json (hashes/revisions pinned). Read all pinned authority. Primary scope and acceptance: skill-import README plus review/bounded-follow-up.md BF-01 through BF-05. Relevant source digests: source-inventory.json and import-manifest.json there. Read original source skills only as needed, never edit them.

Chuck authorized the described bounded fixes, local commit/freeze, and exactly ONE fresh three-provider council pass. This is that pass. All review is read-only. Do not remediate, send external messages, dispatch agents, reuse another context, or initiate another round. Return mandatory findings for human disposition. No builder session/private reasoning or sibling reports are supplied as proof; do not read sibling outputs or round-1 conclusions. The pinned findings ledger states reproduction targets, not proof of resolution.

Mandatory criteria:
SK-01 All nine imports preserve intended capabilities and valid metadata/UI/relative resources, exact source traceability and unchanged helper/UI support bytes/modes; all 24 skills discoverable in source/fresh install/dry-run.
SK-02 Instructions retain gates, actual human scope/approvals, explicit invocation, stop semantics, external-effect bounds, fresh contexts, review budgets and formal-outcome distinction. Rare security/contract/permission/data-loss violations cannot become optional by labeling them nits. Inspect all nine SKILL.md and shared contract end-to-end, including review briefs and merge/stop conditions.
SK-03 Delegation and watches follow active harness contracts with no provider substitution/nested agents/fallback polling in T3. Review these statically; live provider/watcher workflows remain untested and unauthorized.
SK-04 Packaging retains selection-before-traversal, owned-source safety, full bundles, empty board/G1 pending/provenance, excluded live/runtime/unowned sources. Nested reference Markdown (including nested example SKILL.md) must be copied as support WITHOUT a discovery entry. Flat root Markdown and direct bundle SKILL.md remain discoverable. Inspect changed tests and surrounding distribution library; use counterexamples.
SK-05 Required checks pass; unchanged originals/frozen refs/skills/recovery; accurate records/guide mirror and honest limits. Verifier must allow only approved same-tree T3 checkpoint additions, now including new contexts anchored ONLY to frozen inventory (not added refs). Existing contexts retain increasing ordinals. Different trees, non-T3 refs, incorrect metadata/noncommits, rewritten/deleted frozen refs and lack of approved frozen anchor must still fail. Frozen manifest and approval record unchanged. No Linux/hosted CI/product UAT/release/acceptance inferred.

Authority reconciliation: The pinned historical approval permits only additional T3-managed refs with the frozen tree. Its prose does not expressly limit context namespace, but old verifier/tests did. The subsequent pinned BF-03 explicitly authorizes reconciling the checker for new contexts while preserving all frozen refs/content/inventory/state. Review that requirement and behavior; do not delete any original ref, rewrite inventory or waive a failed required check. Council dispatch itself may append legitimate new T3 checkpoint streams to T3_Code_Sample; the revised command must actually pass, not be excused as out of scope.

Reviewer prerequisite: A REAL existing rg executable is available at /opt/homebrew/lib/node_modules/@openai/codex/node_modules/@openai/codex-darwin-arm64/vendor/aarch64-apple-darwin/codex-path/rg.
Before EVERY shell batch, ensure its parent directory is on PATH (or find another real installed rg), remove a shadowing rg shell function if needed, then run doctor. This is a child-shell-only PATH adjustment, no dependency installation/config change. Do not stub or emulate rg/doctor. If doctor still exits 3, STOP checks needing prerequisites and report BLOCKED rather than claiming dynamic success. All tools run against the absolute repository above, NOT the default T3_Code_Sample cwd. Set UV_OFFLINE=1, PYTHONDONTWRITEBYTECODE=1 and TMPDIR to your own external scratch. Use cached existing dependencies; no downloads.

Required commands (capture exact args/results/logs independently):
./scripts/gendev-doctor.sh
./scripts/check-methodology.sh
./scripts/check-doc-coherence.sh
UV_OFFLINE=1 uv run --frozen --group devboard python scripts/devboard.py validate; next; show skill-library-import (separate CLI invocations)
./scripts/test-methodology.sh  (all 13 suites INCLUDING test-migration.sh; 409 checks expected at baseline)
UV_OFFLINE=1 uv run --frozen --group devboard python -m unittest discover -s tests/devboard -v (17 expected)
UV_OFFLINE=1 uv run --frozen --group devboard python -m unittest discover -s tests/migration -v (48 expected)
UV_OFFLINE=1 uv run --frozen --group devboard python scripts/exercise-v3-toolkit.py <YOUR_EXTERNAL_OUTPUT.json> (four scenarios; explicit external output MANDATORY, never default)
python3 scripts/verify-migration-inputs.py (must exit 0)
Offline skill metadata/relative-link/source manifest/helper syntax+--help/support modes, exact 23-file canonical guide/HTML filename-and-byte equality. No live helper watch. Capture targeted positive/negative cases for BF-01/BF-02/BF-03. Inspect actual code; tests and builder reports do not prove conformance alone.

No product initialization in source. Synthetic disposable initialization may exhibit sole inherited GENDEV-MANIFEST-ENFORCEMENT-002 unset named attester; do not invent real approval. Inherited lifecycle 1.0.2 and v3 unreleased are distinct identities. Historical delivery files retain timestamps; current remediation is local and import delivery merged via PR #1, not acceptance. Board remains started/granted; next may still select migration at priority 1 (owner controls priorities). Do not change board to satisfy review.

Permissions: read-only candidate/originals/refs. External disposable fixtures/logs/report only; normal test caches if unavoidable. Fixture Git operations allowed. No governed edits, checkout/ref changes, real installations, credential use, network/PR actions, dependencies/global configuration, nested delegates or persistent application state changes. Prefer external TMPDIR; required runtime suite can transiently create self-cleaning .tmp directories. Other reviewers may run checks concurrently; distinguish transient fixtures from governed file/candidate drift. All HEAD/authority hashes must remain pinned.

Output: save report.md and evidence in /var/folders/dh/wfnmsgpn1yl83xlbmc109sf40000gn/T/v3-skills-council-round2-278hync6/<your-provider>/ only (codex / claude / gemini). The lead later records reports under docs/resources/evolution/skill-library-import/review/council-round-2/; YOU DO NOT WRITE THERE. Return EXACTLY one formal outcome VERIFIED / CHANGES_REQUESTED / BLOCKED, advisory score /10, candidate/base/diff/authority identities and fresh-context provenance, each criterion-to-evidence mapping, commands/results/skips/limits and findings with stable ID/severity/path:line/violated requirement/reproduction/risk/fix/recheck. VERIFIED needs ALL mandatory criteria/checks cited and no mandatory violation. Do not treat scores as acceptance. No prior verdict or sibling response is proof.

Budget: one thorough full pass of selected skills/import/authorized follow-up; no whole-methodology redesign or exhaustive historical audit. Stop for missing authority, candidate drift, external-effect need or expanded scope. Do not start a second pass/reviewer on errors. Report exactly what failed and what remains untested.
