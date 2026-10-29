import json
from pathlib import Path

REPO = Path("/Users/chuckrussell/Dev/gendev/methodology-v3")

def read_lines(rel_path: str, start: int, end: int) -> str:
    lines = (REPO / rel_path).read_text(encoding="utf-8").splitlines()
    return "\n".join(f"{i}: {lines[i-1]}" for i in range(start, end + 1))

static_evaluation = {
    "target_propagation_cases": [
        {
            "case_id": "TP-01",
            "scenario": "New PR targeting release/1.x in a main-default repository (checkout starts on release/1.x)",
            "branch_isolation": {
                "rule": "full-send Step 1 and full-stop No merging require creating a separate task branch when on default OR selected target branch (release/1.x), forbidding direct commits/pushes to release/1.x or main.",
                "citations": [
                    "docs/methodology/dev-skills/full-send/SKILL.md:36-39",
                    "docs/methodology/dev-skills/full-send/SKILL.md:45-46",
                    "docs/methodology/dev-skills/full-stop/SKILL.md:22-25",
                ],
            },
            "pre_pr_review": {
                "rule": "sol-loop uses caller's selected target (release/1.x) and computes git merge-base HEAD origin/release/1.x; forbids silently reviewing against main.",
                "citations": [
                    "docs/methodology/dev-skills/sol-loop/SKILL.md:45-49",
                ],
            },
            "pr_creation": {
                "rule": "file-pr uses caller's selected target (release/1.x), reviews diff against release/1.x, passes gh pr create --base release/1.x (or REST base=release/1.x), and verifies returned PR base and head.",
                "citations": [
                    "docs/methodology/dev-skills/file-pr/SKILL.md:11-15",
                    "docs/methodology/dev-skills/file-pr/SKILL.md:49-55",
                ],
            },
            "readiness_and_merge_gate": {
                "rule": "babysit-pr monitors actual base (release/1.x); full-send merge gate (and full-stop readiness gate) verifies PR actual base matches selected target (release/1.x), branch is up to date, and rechecks base/head before merge/handoff.",
                "citations": [
                    "docs/methodology/dev-skills/babysit-pr/SKILL.md:118-121",
                    "docs/methodology/dev-skills/full-send/SKILL.md:96-98",
                    "docs/methodology/dev-skills/full-stop/SKILL.md:33-38",
                ],
            },
        },
        {
            "case_id": "TP-02",
            "scenario": "New stacked PR targeting nondefault feature/parent in a main-default repository (checkout starts on feature/parent)",
            "branch_isolation": {
                "rule": "Creates separate task branch off feature/parent because feature/parent is the selected target; forbids direct pushes to both main and feature/parent.",
                "citations": [
                    "docs/methodology/dev-skills/full-send/SKILL.md:45-46",
                    "docs/methodology/dev-skills/full-stop/SKILL.md:22-25",
                ],
            },
            "pre_pr_review": {
                "rule": "sol-loop computes git merge-base HEAD origin/feature/parent so parent commits are excluded from the stacked review scope.",
                "citations": [
                    "docs/methodology/dev-skills/sol-loop/SKILL.md:45-49",
                ],
            },
            "pr_creation": {
                "rule": "file-pr passes --base feature/parent explicitly and verifies returned base/head match.",
                "citations": [
                    "docs/methodology/dev-skills/file-pr/SKILL.md:12-15",
                    "docs/methodology/dev-skills/file-pr/SKILL.md:49-55",
                ],
            },
            "readiness_and_merge_gate": {
                "rule": "Merge/readiness gate verifies actual base == feature/parent and up-to-date status.",
                "citations": [
                    "docs/methodology/dev-skills/full-send/SKILL.md:96-98",
                    "docs/methodology/dev-skills/full-stop/SKILL.md:33-38",
                ],
            },
        },
        {
            "case_id": "TP-03",
            "scenario": "Ordinary new PR where repository default (main) is appropriate to requested work",
            "branch_isolation": {
                "rule": "If checkout is on main, creates a separate task branch first.",
                "citations": [
                    "docs/methodology/dev-skills/full-send/SKILL.md:36-39",
                    "docs/methodology/dev-skills/full-send/SKILL.md:45-46",
                ],
            },
            "pre_pr_review": {
                "rule": "sol-loop resolves/records intended target main (since appropriate to requested work) and uses git merge-base HEAD origin/main.",
                "citations": [
                    "docs/methodology/dev-skills/sol-loop/SKILL.md:45-48",
                ],
            },
            "pr_creation": {
                "rule": "file-pr explicitly passes --base main and verifies returned PR base/head.",
                "citations": [
                    "docs/methodology/dev-skills/file-pr/SKILL.md:12-14",
                    "docs/methodology/dev-skills/file-pr/SKILL.md:49-52",
                ],
            },
            "readiness_and_merge_gate": {
                "rule": "Gate confirms actual base matches main and all conjunctive conditions pass.",
                "citations": [
                    "docs/methodology/dev-skills/full-send/SKILL.md:83-98",
                ],
            },
        },
        {
            "case_id": "TP-04",
            "scenario": "Existing PR targeting nondefault base (or PR whose base was changed externally before merge)",
            "branch_isolation": {
                "rule": "Retains existing PR actual base; forbids silent retargeting; rechecks actual base and head before external mutations or merge, requiring reconciliation if target changed.",
                "citations": [
                    "docs/methodology/guides/skill-execution-contract.md:66-67",
                    "docs/methodology/dev-skills/full-send/SKILL.md:36-39",
                    "docs/methodology/dev-skills/full-send/SKILL.md:49-50",
                    "docs/methodology/dev-skills/full-send/SKILL.md:96-98",
                    "docs/methodology/dev-skills/file-pr/SKILL.md:11-15",
                    "docs/methodology/dev-skills/sol-loop/SKILL.md:42-44",
                    "docs/methodology/dev-skills/modernize/SKILL.md:18-19",
                ],
            },
        },
        {
            "case_id": "TP-05",
            "scenario": "Local review with no remote or missing formal-review authority",
            "rule": "With no remote, sol-loop uses a user-named base commit or HEAD for uncommitted changes only (which remains advisory per lines 36-38); missing formal-review authority blocks formal validation rather than supplying an inferred base.",
            "citations": [
                "docs/methodology/dev-skills/sol-loop/SKILL.md:36-38",
                "docs/methodology/dev-skills/sol-loop/SKILL.md:49-51",
                "docs/policies/independent-validation-policy.md:58-60",
                "docs/policies/independent-validation-policy.md:77",
                "docs/policies/independent-validation-policy.md:131-134",
            ],
        },
    ],
    "finding_classification_cases": [
        {
            "case_id": "FC-01",
            "scenario": "Rare permission bypass (in-scope mandatory violation on a rare/unintended path)",
            "classification": "Mandatory (blocker/should)",
            "allowed_disposition": "Must be remediated with proof and re-verified on latest head, or if unresolved blocks readiness and requires human disposition. Written dismissal is forbidden and cannot satisfy remediation or authorize merge.",
            "full_send_outcome": "Blocked until fixed and verified (or escalated to human; never merged on written dismissal).",
            "full_stop_outcome": "Blocked (not Ready to merge); PR left open and unmerged.",
            "citations": [
                "docs/methodology/guides/skill-execution-contract.md:45-47",
                "docs/methodology/dev-skills/babysit-pr/SKILL.md:99-100",
                "docs/methodology/dev-skills/babysit-pr/SKILL.md:107-111",
                "docs/methodology/dev-skills/sol-loop/SKILL.md:88-90",
                "docs/methodology/dev-skills/sol-loop/SKILL.md:98-99",
                "docs/methodology/dev-skills/full-send/SKILL.md:90-94",
                "docs/methodology/dev-skills/full-stop/SKILL.md:33-45",
            ],
        },
        {
            "case_id": "FC-02",
            "scenario": "Out-of-scope data loss (mandatory violation outside authorized task scope)",
            "classification": "Mandatory out-of-scope",
            "allowed_disposition": "Cannot be silently implemented (scope violation) and cannot be silently waived or dismissed with a written reason. Blocks readiness and must be reported to human for scope/risk disposition under governing authority; human risk decision does not fabricate independent VERIFIED.",
            "full_send_outcome": "Blocked; asks user via harness question tool and leaves PR unmerged.",
            "full_stop_outcome": "Blocked; reports blocker and leaves PR open and unmerged.",
            "citations": [
                "docs/methodology/guides/skill-execution-contract.md:46-47",
                "docs/methodology/dev-skills/babysit-pr/SKILL.md:108-111",
                "docs/methodology/dev-skills/sol-loop/SKILL.md:106-107",
                "docs/methodology/dev-skills/full-send/SKILL.md:90-94",
                "docs/methodology/dev-skills/full-send/SKILL.md:117-128",
                "docs/policies/independent-validation-policy.md:136-139",
            ],
        },
        {
            "case_id": "FC-03",
            "scenario": "Optional style preference (no mandatory requirement violated)",
            "classification": "Optional preference (advisory nit)",
            "allowed_disposition": "May be declined/dismissed with a documented reason and supporting evidence, listed as a follow-up, and replied/resolved only when comment effects are authorized.",
            "full_send_outcome": "Does not block merge gate provided all other conjunctive merge-gate conditions pass on the latest commit.",
            "full_stop_outcome": "Ready to merge (or Waiting for required approval if human approval remains); never merged by agent.",
            "citations": [
                "docs/methodology/dev-skills/babysit-pr/SKILL.md:96-99",
                "docs/methodology/dev-skills/babysit-pr/SKILL.md:112-113",
                "docs/methodology/dev-skills/sol-loop/SKILL.md:87",
                "docs/methodology/dev-skills/sol-loop/SKILL.md:105",
                "docs/methodology/dev-skills/full-send/SKILL.md:83-98",
                "docs/methodology/dev-skills/full-stop/SKILL.md:41-43",
            ],
        },
        {
            "case_id": "FC-04",
            "scenario": "Evidence-proven false positive (bot claim disproven by source/test/reproduction evidence)",
            "classification": "Verified false positive",
            "allowed_disposition": "Verified against source/reproduction first; may be declined/dismissed with documented reason and reproducible evidence (using leaving-pr-comments when posting replies is authorized).",
            "full_send_outcome": "Does not block merge gate provided all other conjunctive merge-gate conditions pass on the latest commit.",
            "full_stop_outcome": "Ready to merge (or Waiting for required approval if human approval remains); never merged by agent.",
            "citations": [
                "docs/methodology/dev-skills/babysit-pr/SKILL.md:85-88",
                "docs/methodology/dev-skills/babysit-pr/SKILL.md:96-99",
                "docs/methodology/dev-skills/babysit-pr/SKILL.md:112-113",
                "docs/methodology/dev-skills/sol-loop/SKILL.md:104",
                "docs/methodology/dev-skills/full-send/SKILL.md:92-93",
            ],
        },
        {
            "case_id": "FC-05",
            "scenario": "Usual intended-case defect (in-scope bug or unmet requirement in requested work)",
            "classification": "Mandatory in-scope finding (blocker/should)",
            "allowed_disposition": "Must be fixed with smallest change that works, proven with direct evidence, and re-verified on the latest head. Cannot be dismissed.",
            "full_send_outcome": "Remediated, proven, and re-verified before merge gate can pass.",
            "full_stop_outcome": "Remediated, proven, and re-verified before handoff as Ready to merge.",
            "citations": [
                "docs/methodology/dev-skills/full-send/SKILL.md:43-47",
                "docs/methodology/dev-skills/full-send/SKILL.md:52-53",
                "docs/methodology/dev-skills/full-send/SKILL.md:83-98",
                "docs/methodology/dev-skills/babysit-pr/SKILL.md:86",
                "docs/methodology/dev-skills/babysit-pr/SKILL.md:108-114",
                "docs/methodology/dev-skills/sol-loop/SKILL.md:101-103",
            ],
        },
    ],
}

out_path = Path("/var/folders/dh/wfnmsgpn1yl83xlbmc109sf40000gn/T/v3-skills-council-round4-lk4zdm_d/gemini/static-counterexamples.json")
out_path.write_text(json.dumps(static_evaluation, indent=2) + "\n", encoding="utf-8")
print("Saved static counterexample evaluation:", out_path)
