# Independent Skills Council Review — Round 1
Created: 2026-10-28T23:26:01.245846+00:00
Project: methodology-v3 reusable source baseline, no initialized product
Task: skill-library-import
Mode: full independent conformance of selected skills import at merged candidate
Repository: /Users/chuckrussell/Dev/gendev/methodology-v3
Checkout: main, must remain at d41e0ebfdc587ecc6d8c3ab336afc530ce90654f, clean governed tree
Base: ee82653ed6cacb9e1157cd791f12d0fb774f12af
Candidate: d41e0ebfdc587ecc6d8c3ab336afc530ce90654f
Exact selected diff: selected.diff beside this request, SHA256 6818fab01b30764ed63cee1b214fd63b3fceed8f6a5062fcdcf450ccd4100b1c
Reproduce: git diff ee82653ed6cacb9e1157cd791f12d0fb774f12af d41e0ebfdc587ecc6d8c3ab336afc530ce90654f -- .agents/skills docs/methodology/dev-skills docs/methodology/guides/skill-execution-contract.md scripts/create-dry-run.py tests/migration/test_v3_toolkit.py
Authority pins: authority-manifest.json beside this request. Read all named authority from candidate, not builder conclusions.

Chuck Russell now explicitly requests: "Let's do an independent skills review using the council". This authorizes three fresh read-only contexts, one round, high reasoning. Prior import restrictions on delegation are superseded for this review only. Prior GitHub merge is delivery evidence, not independent verification or human acceptance. Existing board and historical readiness text still describe pre-review/pre-merge state; classify that tracking lag separately. No product initialization is required or permitted for this reusable source, except disposable synthetic fixtures.

Construction authority: pinned import README plus its acceptance criteria; exact source attribution/inventory: source-inventory.json and import-manifest.json in that directory. Read source originals at /Users/chuckrussell/Dev/gendev/tstack/skills only as needed; never modify them. No builder conversation, private reasoning, prior validator verdict or self-check conclusion is proof. Inspect primary code and reproduce checks independently. Other documentation-refresh content is context only unless directly inconsistent with skills; this is not a whole methodology or historical audit.

Full selected scope: all nine skills (babysit-pr, council, file-pr, full-send, full-stop, leaving-pr-comments, modernize, sol-loop, takeover), supporting helper/UI files, nine directory discovery symlinks, shared execution contract, narrow create-dry-run packaging change, changed regression tests and relevant surrounding distribution code. Reviewing a workflow does not invoke it. Do not run imported workflows, PR helpers in live mode, nested agents, network requests or external messages.

Mandatory criteria:
SK-01 Nine complete skills preserve intended capabilities, valid metadata/support UI, source digests/provenance and whole-folder discovery (24 total) with usable relative paths in source/fresh installs/dry-run fixtures.
SK-02 Instructions preserve GenDev authority/gates, actual human scope, external-effect limits, stop semantics, independent fresh contexts, bounded remediation and required approvals. Scores advisory; no accepting, merging, ignoring mandatory findings or broad authority by workflow labels.
SK-03 Provider delegation/watching instructions follow supported harness contracts; no unasked provider substitution or fallback polling in T3. State whether live provider behavior is untested.
SK-04 Dry-run packaging keeps selection-before-traversal, complete supporting directories, safe upgrade/owned-source protections, excludes live authority/runtime/unrecorded files, empty board/G1 pending and honest provenance. Inspect surrounding distribution code and changed tests.
SK-05 Exact source/helper preservation and all required local checks pass; no claim of Linux/hosted CI/live watcher/product gate UAT. Existing frozen migration is background scope; do not redo its exhaustive unrelated audit.

Required independent checks in repository (outputs only in your own external scratch):
./scripts/gendev-doctor.sh; ./scripts/check-methodology.sh; ./scripts/check-doc-coherence.sh
UV_OFFLINE=1 uv run --frozen --group devboard python scripts/devboard.py validate (and next/show skill-library-import read-only)
All 13 tests/methodology/test-*.sh EXCEPT test-migration.sh (the inherited 13-suite set).
UV_OFFLINE=1 uv run --frozen --group devboard python -m unittest discover -s tests/devboard -v
UV_OFFLINE=1 uv run --frozen --group devboard python -m unittest discover -s tests/migration -v
UV_OFFLINE=1 uv run --frozen --group devboard python scripts/exercise-v3-toolkit.py <YOUR_EXTERNAL_OUTPUT.json> (MANDATORY explicit output path; default would overwrite governed evidence).
Offline nine-skill metadata, support syntax/help, link and source-manifest checks; use installed local validator or simple equivalent structure assertions if necessary; do not install anything. Targeted counterexamples appropriate to changed scope.
Verify original inputs using scripts/verify-migration-inputs.py and approved exception docs/resources/evolution/v3-migration/review/round-1/checkpoint-exception-approval.json; inspect CLI first for exact flags. Read-only original metadata is permitted. Approved same-tree additive T3 checkpoint refs may grow; never delete/reset refs. Preserve recovery and source skills.

Known baseline: fresh initialized synthetic project has sole required-attester GENDEV-MANIFEST-ENFORCEMENT-002 until named human attester; do not invent approval to hide it. Full v3 still unreleased. Hosted CI/release identity is outside selected scope unless directly affected. Missing required evidence => BLOCKED, mandatory violation => CHANGES_REQUESTED.

Permissions: read-only candidate/originals/refs. Create only disposable external fixtures/logs/report (scratch dirs beside this request), ordinary test caches if unavoidable. Prefer TMPDIR in external scratch and PYTHONDONTWRITEBYTECODE=1. No governed files, board, refs, checkout, commits, pushes, installation into real projects, dependencies/downloads, credentials, releases, PR actions, additional delegates or persistent application state. Test fixture Git operations allowed. Scope is review only; return findings, no remediation. Do not expand into evaluating other council members or importing their conclusions. Never read sibling reviewer outputs.

Each reviewer: save report and command logs under /var/folders/dh/wfnmsgpn1yl83xlbmc109sf40000gn/T/v3-skills-council-round1-wtbrfdg6/<your-provider>/; report.md is permitted external evidence. Lead will later record reports under docs/resources/evolution/skill-library-import/review/council-round-1/<provider>/report.md; reviewers must not write there. Return full report (or report path plus substantive summary), exact outcome VERIFIED / CHANGES_REQUESTED / BLOCKED, score out of 10 (advisory), reviewer/model/time/context provenance, candidate/base/authority pins, criteria-to-evidence mapping, commands/results/skips/limits, reproducible findings (stable ID, severity, path:line, requirement, reproduction, risk, proposed fix and required recheck). Distinguish scope findings from out-of-scope suggestions. Finish within one thorough bounded full pass. Do not remediate or start another round. Candidate drift => BLOCKED.
