# Skills council — Round 2 consolidation

Status: CHANGES_REQUESTED; one authorized fresh round completed
Reviewed candidate: aa25aa89762974012c0243e6134e9785f5db970d
Branch: fix/skills-council-follow-up
Base: ee82653ed6cacb9e1157cd791f12d0fb774f12af
Remediation comparison: d41e0ebfdc587ecc6d8c3ab336afc530ce90654f
Produced by: Codex controller in T3 Code, 2026-10-29 UTC

| Member | Round 1 | Round 2 | Round 2 formal outcome |
| --- | --- | --- | --- |
| GPT-6.1 Sol, high | 9/10 | 8/10 | CHANGES_REQUESTED |
| Claude Opus 5.5, high | 7/10 | 8/10 | CHANGES_REQUESTED |
| Gemini 4 Argon High | 9.5/10 | 10/10 | VERIFIED |

Raw reports are retained unchanged. Scores are advisory, not a majority vote.
Gemini's approval does not establish aggregate conformance in the presence of
reproducible mandatory instruction contradictions reported by the other members.
The controller accepts the two residual instruction findings for disposition.

## Findings and disagreement

R2-01 (Claude F-01, medium, mandatory): babysit-pr/SKILL.md:102-107 still says
to fix intended-case bugs and decline the rest. That can classify rare security,
contract, permission or data-loss violations as optional, contrary to the shared
contract and corrected sol-loop. Full-send invokes this review handling and
permits dismissing findings with reasons, so this remains material. Proposed
correction: keep mandatory requirement-based classification on all paths;
report out-of-scope mandatory findings for disposition; decline only optional
preferences. No behavior/code/test change beyond these instructions is needed.

R2-02 (Sol COD-R2-001, major/mandatory; Claude F-02, low/advisory): full-send
step 4 and merge gate require the default branch, but existing release or stacked
PRs can have another actual target. full-stop inherits the workflow/readiness.
The controller agrees with Sol that the conflicting imperative violates the
actual-base requirement and should be corrected before conformance. Proposed
correction: resolve and retain the actual target of an existing PR; explicitly
select the intended target for a new PR (default only when appropriate). Rebase
and assess readiness against that target consistently. Verify release-base,
stacked-base and normal new-default-base examples; update adapted skill digest.
No live PR/rebase/merge is needed for these static counterexamples.

Claude F-03 is informational: highest-ordinal frozen anchor is correct for the
pinned single-context inventory. No speculative multi-context redesign is added.

## Confirmed results

All three reviewers report actual passing required commands, including 409
inherited checks across all 13 suites, 17 board tests, 48 migration tests and
four isolated replay scenarios. BF-02 nested support discovery and BF-03 new T3
checkpoint context handling have independent before/after counterexamples and
negative probes. Original contents/modes/status/frozen refs are preserved; the
required verifier exits 0, including growing same-tree T3 checkpoint additions.
Real rg prerequisites now work for all three providers. Metadata, 24-skill
source/fresh/dry-run discovery, unchanged support files/source skills and exact
23-file guide mirror pass. No remaining runtime defect was reported.

The reviewed candidate stayed clean/pinned during all reviewers' runs. The lead
adds only reports/tracking afterward; aa25aa8 remains the reviewed operational
candidate. No further remediation, new delegates, remote push/merge, acceptance,
release, real product gates, live workflow effects or source-project resync.
No Linux/hosted CI/live watcher/provider behavior is proven.

## Scope and next decision

The authorized directive explicitly says: “If that round has unresolved mandatory
findings, return them to Chuck before another cycle.” That boundary has been
reached. Proposed next slice: two wording corrections above, adapted manifest
hashes and corresponding record updates, static counterexamples plus relevant
metadata/methodology checks, local candidate freeze and a fresh council pass.
This is a proposal, not execution authority. Original projects, recovery and all
frozen refs remain protected; no remote effects proposed. Human acceptance is
pending. The original migration VERIFIED remains solely at 98f8bec.

## Evidence locations

Request, authority pins, reports and durable root/log/script outputs are copied
here; no runtime fixture/cache trees are copied. Absolute paths inside raw
reports retain their historical external-scratch meaning. Large raw selected.diff
and authority-read.txt remain in external scratch and are reproducible from Git
and pinned authority. evidence-index.json hashes this durable subset. For original
external hashes and detailed reproduction commands see each member report.
