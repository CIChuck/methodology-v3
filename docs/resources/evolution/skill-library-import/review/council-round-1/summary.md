# Skills council review — Round 1 consolidation

Controller disposition: BLOCKED. Mandatory instruction correction also required.
Reviewed candidate: d41e0ebfdc587ecc6d8c3ab336afc530ce90654f
Base: ee82653ed6cacb9e1157cd791f12d0fb774f12af
Selected diff SHA256: 6818fab01b30764ed63cee1b214fd63b3fceed8f6a5062fcdcf450ccd4100b1c
Task: skill-library-import. One fresh-context three-provider read-only round.
No remediation, repository edits, board changes, commits, pushes, PR changes or further rounds were performed by the controller.

| Member | Outcome as returned | Advisory score |
| --- | --- | --- |
| GPT-6.1 Sol (high) | BLOCKED | 9/10 |
| Claude Opus 5.5 (high) | BLOCKED | 7/10 |
| Gemini 4 Argon High | VERIFIED | 9.5/10 |

These outcomes are retained verbatim in the adjacent reports. They are not a vote. Gemini's verdict is not adopted as aggregate conformance: it treats a required failed preservation command as nonblocking despite request SK-05 and the validation policy. The other two correctly retain an evidence blocker. The controller also agrees with Claude's mandatory sol-loop text conflict; Sol and Gemini did not flag it. Agreement or scores do not waive this requirement.

## Controller assessment and proposed bounded remediation

1. Mandatory medium instruction conflict (SKL-C-01): sol-loop/SKILL.md:77-80 categorizes rare/other paths as nits, while :25 permits stopping on nits and :95 declining them. :88-89 and the shared contract correctly retain mandatory security/contract violations. Remove the contradictory brief taxonomy; all mandatory contract, security, permission and data-loss findings retain their requirement-based severity regardless of frequency. Reconcile early-stop and decline conditions after controller classification. Fresh review required after changes.
2. Preservation evidence blocker (COD-SK-001 / SKL-B-02 / OBS-OUT-001): required verify-migration-inputs.py exits 1 on three T3-created new-context ordinal/0 checkpoint refs. All reviewers independently identify matching frozen tree, T3 author/subject, unchanged original content/modes/status/frozen refs. Current verifier and negative test restrict allowed additions to an existing frozen namespace. The approval's prose permits same-tree T3-managed additions without expressly naming a namespace restriction. Reconcile that prose/mechanical boundary explicitly rather than deleting refs, changing frozen inventory, or silently calling the command passed. Proposed mechanical scope: cross-context additions only in the precise T3 namespace with expected metadata and frozen-tree equality; preserve every original ref and keep all different-tree, non-T3, rewritten/deleted ref negative checks. This is a proposed follow-up, not a scope waiver or implemented fix.
3. Reviewer environment blocker (SKL-B-01): Claude could not find a real rg executable and its dynamic results are incomplete. This is not evidence of a repository regression. Sol and Gemini completed the dynamic checks; Gemini exposed a real bundled rg on PATH. Controller separately confirmed a real rg executable in its own environment. A future Claude round must expose a real existing rg binary to its shell and pass the doctor before running checks; no emulation or new dependency is needed if the bundled binary is accessible. Claude's doctor-stubbed probes are explicitly non-substitute evidence, not full dynamic proof.
4. Low-priority wording corrections: council trigger requires explicit invocation; PR-description publication must be within scope; babysit-pr should use actual PR base/repository review requirements while preserving an accurate description of the unchanged fallback helper; full-send can state applicable GenDev validation/approval prerequisites directly; modernize subject/verb typo can be fixed when otherwise touched.
5. Latent packaging issue (SKL-L-05): the discovery loop scans any selected nested Markdown with name frontmatter and can promote a bundled reference into an extra skill. Claude supplied a 25-versus-24 counterexample. Restrict discovery to legitimate flat top-level entries and direct bundle SKILL.md entrypoints, with a focused regression and complete-bundle preservation. Lower severity than the mandatory instruction conflict; a proposed bounded improvement.
6. Tracking closeout remains separate: merge/delivery and this council result have not yet been reconciled into board/readiness/current-availability artifacts. The original migration VERIFIED result remains pinned to 98f8bec, not this integration. No human acceptance or v3 release is inferred.

## Evidence and limits

All three reports confirm candidate/authority pins, unchanged bundled helper/UI files, source inventory and discoverability. Sol and Gemini report passing 12 non-migration inherited suites, 17 board tests, 42 migration tests and four explicit-output isolated replay scenarios. Claude's missing-rg failures remain recorded as environment-limited, not green. All three required preservation runs exited 1. No Linux/hosted CI, live watcher/provider workflows, real product gates or production behavior were proven.

Request correction: there are 13 inherited suite files total, and the explicit exclusion of test-migration.sh left 12 required suites. The count error did not cause a suite to be silently omitted beyond the named exclusion. Future requests should list the exact suite set correctly.

Read individual reports and logs for exact reproduction commands, criteria mapping, hashes and limitations. Reports remain unmodified. Any follow-up should be separately scoped, freeze a revised candidate and obtain fresh contexts. No second council round has been dispatched.
