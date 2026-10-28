import hashlib,importlib.util,json,os,pathlib,re,subprocess,sys
from datetime import datetime,timezone
from run import ROOT,OUT
assert json.loads((OUT/'initial-state.json').read_text())==json.loads((OUT/'final-state.json').read_text())
manifest=json.loads((ROOT/'docs/resources/evolution/v3-migration/input-manifest.json').read_text())
spec=importlib.util.spec_from_file_location('preservation',ROOT/'scripts/verify-migration-inputs.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
s=manifest['sources']['T3_Code_Sample']; current=subprocess.check_output(['git','for-each-ref','--format=%(refname) %(objectname)'],cwd=s['path'],text=True)
errors,allowed=m.compare_refs(pathlib.Path(s['path']),s['refs'],current,allow_identical_t3_checkpoints=True);assert not errors
(OUT/'preservation-observations.json').write_text(json.dumps(allowed,indent=2)+'\n')
authority=json.loads((OUT/'authority-check.json').read_text())
authority_rows='\n'.join('| `'+p+'` | `'+r['sha256']+'` |' for p,r in authority.items())
ref_rows='\n'.join('| '+a['ref'].rsplit('/',1)[-1]+' | `'+a['oid']+'` |' for a in allowed)
start=datetime.fromtimestamp((OUT/'run.py').stat().st_birthtime,timezone.utc).isoformat();finish=datetime.now(timezone.utc).isoformat()
request=ROOT.parent/'methodology-v3-recovery/review/round-5';request_sha=hashlib.sha256((request/'request.md').read_bytes()).hexdigest();manifest_sha=hashlib.sha256((request/'authority-manifest.json').read_bytes()).hexdigest()
diff=json.loads((OUT/'diff-audit.json').read_text())
report=f'''VERIFIED

Candidate and diff identity

- Project/task: methodology-v3 / v3-baseline-migration; full independent conformance review of steps 1–6 and RV-01–RV-10 after the authorized VAL-005 follow-up.
- Repository: /Users/chuckrussell/Dev/gendev/methodology-v3.
- Branch: integration/v3-migration; clean frozen candidate: 98f8bec4597cd3307fc26e5c28dc86592e01ca08; refs/review/v3/round-5 resolves to that exact commit.
- Base: 54f0de27f2b59fdcc54e4f57bb9f73dc92843f4a.
- Full diff: git diff 54f0de27f2b59fdcc54e4f57bb9f73dc92843f4a 98f8bec4597cd3307fc26e5c28dc86592e01ca08. The --binary --no-ext-diff rendering hashes to {diff['full_binary_diff_sha256']}; 286 changed paths are inventoried in diff-audit.json. Raw full-diff bytes are not retained in this evidence directory.
- Latest remediation boundary: 6ca2ad10f7eb0c71b9a316d458a20ad667c21c4b..98f8bec4597cd3307fc26e5c28dc86592e01ca08. This review covers the full migration, not only that delta.
- Tracked file/link bytes, modes, full candidate ref set, branch, HEAD and clean status match between initial-state.json and final-state.json. No candidate or original was edited.

Authority and review mode

The controlling request is {request}/request.md (SHA256 {request_sha}); its adjacent authority-manifest.json hashes to {manifest_sha}. pins.py independently checked every manifest digest against both the pinned Git blob and the working file. Every authority below is pinned at candidate 98f8bec4597cd3307fc26e5c28dc86592e01ca08; authority-check.json preserves the exact records.

| Authority path | SHA256 |
| --- | --- |
{authority_rows}

The migration README is the bounded construction directive for this uninitialized methodology source. Its steps 1–6, review-scope RV-01–RV-10, the narrow additive-checkpoint approval, round-2 rendering directive, round-3 human extension and controlling round-4 VAL-005 follow-up were applied. The user's recorded “lets fix it and test it” authorizes this bounded cycle. No product G1 approval was inferred or fabricated. Further mandatory findings would return to Chuck; none were identified in this pass.

Independence and context provenance

Reviewer: Codex independent agent /root/v3_review_round_5, GPT-6 family as identified by the runtime. The exact serving model revision and precise agent-creation timestamp are not separately exposed. A new dedicated review context was dispatched for round 5; first durable reviewer script creation: {start}; report prepared: {finish}. Provider/model/effort settings were inherited without override. No additional agents were created.

The reviewer received the bounded assignment and pinned request/authority, then independently inspected primary source, tests and selected changes. No builder transcript, private reasoning or builder conclusions were supplied or used as conformance proof. Prior report references in dispositions/tracking are historical context; their verdicts and stored test logs were not substituted for this run's evidence. The inherited top-level conversation contains repository/environment instructions for T3, not a builder implementation session; all review operations explicitly targeted methodology-v3 and preserved T3. No independence exception affecting the conclusion was used.

Findings

No mandatory conformance finding remains. No blocker, critical or high finding was identified. VAL-005 is resolved at the required selection boundary: source_entries selects owned groups and allowed destination paths before touching excluded source surfaces; the helper reuses selected canonical agent/policy/planning seeds. The default installer retains full selection and external-link rejection. Current code and independently executed checks also evidence the prior ownership, archived-packet and project-name rendering areas; prior verdicts are not the basis of this conclusion.

Requirement-to-evidence mapping

All evidence paths below are relative to /tmp/v3-independent-round5.x5446H. Source paths are relative to the reviewed repository.

| Criterion | Result and primary evidence |
| --- | --- |
| RV-01 | PASS. preservation.log and final-preservation.log check 284 v2 and 208 T3 files/links, hashes, modes, inventories, Git status and frozen refs. pins.py/history-and-skills.json verify all 21 inventoried v2 refs under refs/archive/v2, retained local heads/tags and reachable objects, recovery archive/bundle digests, independent Git storage, and no remotes/alternates. fsck.log exits 0. Approved additions are individually listed below. |
| RV-02 | PASS. README.md, schema/candidate.json, doctor and installation provenance keep methodology-v3 unreleased and the inherited lifecycle at 1.0.2. Historical refs and drafts remain identifiable. The full changed-path inventory shows no implementation of deferred 1.0.3/1.1 concepts or real product authority. doctor.log, history-and-skills.json and experiments.json corroborate. |
| RV-03 | PASS. AGENTS.md, reusable policies, portable handoff/validation skills, board/schema/templates, optional T3 guide/actions and standalone requirements were inspected. All 15 discovery links resolve internally with usable metadata. Migration fresh-install and upgrade tests prove empty board, no migration tasks/product metadata, preservation of product pyproject/lockfile, local skills/policies and separate tooling dependencies. board-tests.log, migration-tests.log, history-and-skills.json and additional-commands.json cover the standalone offline command. |
| RV-04 | PASS. Canonical architecture/directive/build-plan templates, phase-build-planner, phase-loop and subagent-coordination guidance consistently preserve proportional private implementation choices, controlled authority boundaries, impact-based regression and draft-only advance planning. pins.py verifies all six promoted canonical hashes against promoted-amendments.json. Imported approvals remain explicitly historical; no new product approval is seeded. |
| RV-05 | PASS. distribution.py plan/relative/check_parents/fingerprint/json_record preflight validates ownership, modes, symlinks, collisions, local amendments and metadata before writes. migration-tests.log exercises edits/removals, permissions, malformed/duplicate ownership, unsafe parents, collisions, matching legacy adoption and actual upstream byte/mode updates. experiments.json additionally records refusal with zero T3-copy mutations, explicit fixture-only reconciliation, and board render preserving task bytes. |
| RV-06 | PASS. distribution.py preserves target extras, policy seeds, project authority, task state, local amendments and installation history. Its apply rollback includes replaced/new files, created directories, managed AGENTS include, ignore changes and record. Existing failure injection tests pass; additional-results.json records six independent SIGINT/SIGTERM/SIGHUP probes after the final metadata replacement, on both fresh installation and real upstream upgrade, with exact pre/post target inventory equality. |
| RV-07 | PASS. init-project/init-phase use the same canonical directive and one-pass render_template.py; YAML names round-trip as data, Markdown retains literal tokens, invalid names fail before creation/replacement. Board/schema tests cover completed/planning and accepted/archive backing records, cross-state negatives and tampering. Fresh setup passes from tracked source and initialized installation; boundaries-results.json covers independently absent AGENTS, discovery and policies plus planted unowned regular files/links/directories. Each fresh fixture has verified integrity/provenance, canonical policies, 15 links, empty board, G1 pending and the sole inherited unset-attester error. |
| RV-08 | PASS for the bounded changes. Primary code exposes explicit ownership/path/runtime checks, typed Entry and AuthorityBacking boundaries, and contextual JSON/YAML validation. Essential replay invariants use explicit exceptions. The selector extends the shared reader rather than duplicating distribution traversal; seed duplication has a focused equality regression. No undeclared product/data/security boundary, blanket suppression or unnecessary runtime dependency was introduced. Instrumented probes verify excluded paths receive no metadata, traversal, resolution or content calls; unsafe selected sources are refused. |
| RV-09 | PASS. Full inherited, board/schema, migration, replay, preservation, guards and direct counterexamples were independently executed and logged. Positive/negative/failure/integration checks exercise actual behavior and entire fixture-input preservation. The four replay scenarios remain synthetic local tooling evidence, not real product gate traversal, human approval or deployment. Commands and limitations follow. |
| RV-10 | PASS. Exact authority/candidate pins and context provenance are recorded here and in authority-check.json and state snapshots. board-next.log/show retain started/granted on the current branch with human acceptance pending. No candidate/ref/board/original edits, network/package download, credential use, external publication or delegates occurred. Verification, completion proposal, human acceptance and delivery remain separate. |

Executed commands and results

Unless stated otherwise, commands ran in /Users/chuckrussell/Dev/gendev/methodology-v3 with UV_OFFLINE=1, GIT_OPTIONAL_LOCKS=0, PYTHONDONTWRITEBYTECODE=1 and an external disposable TMPDIR under the evidence directory. Existing cached dependencies were used; no packages were downloaded. *.result.json files preserve exact argv, cwd, return code and elapsed time. Probe command JSON preserves individual fixture commands and their actual outputs.

| Command | Exact result | Evidence |
| --- | --- | --- |
| ./scripts/gendev-doctor.sh | exit 0; prerequisites present; authority context; unreleased v3, inherited 1.0.2; no initialized product | doctor.log/result.json |
| ./scripts/check-methodology.sh | exit 0, 0 warnings | checker.log/result.json |
| UV_OFFLINE=1 uv run --frozen --group devboard python -B scripts/devboard.py validate | exit 0; one task | board-validate.log/result.json |
| same prefix, scripts/devboard.py next | exit 0; IN_PROGRESS v3-baseline-migration, fresh review/human acceptance pending | board-next.log/result.json |
| same prefix, scripts/devboard.py show v3-baseline-migration | exit 0; started, granted, integration/v3-migration | board-show.log/result.json |
| ./scripts/test-methodology.sh --suite all | exit 0; all 13 suites, 409 checks, 0 failures | full-suite.log/result.json |
| same uv prefix, -m unittest discover -s tests/devboard -v | exit 0; 17 tests, OK | board-tests.log/result.json |
| same uv prefix, -m unittest discover -s tests/migration -v | exit 0; 42 tests, OK | migration-tests.log/result.json |
| same uv prefix, scripts/exercise-v3-toolkit.py /tmp/v3-independent-round5.x5446H/experiments.json | exit 0; all four isolated scenarios PASS, three synthetic helper tests executed | replay.log/result.json; experiments.json |
| python3 -B scripts/verify-migration-inputs.py | initial and final exit 0; original contents/state and frozen refs preserved with only approved additions | preservation.log/result.json; final-preservation.log/result.json |
| git fsck --full --connectivity-only | exit 0; three dangling blobs, no connectivity/corruption error | fsck.log/result.json |
| ./scripts/methodology-guard.sh --staged | exit 0 | staged-guard.log/result.json |
| ./scripts/methodology-guard.sh --range BASE CANDIDATE (exact pins above) | exit 0 | range-guard.log/result.json |
| python3 -B /tmp/v3-independent-round5.x5446H/pins.py initial; same command final | exit 0 both; authority, history/archive, no-remote, skills, candidate snapshots verified | pins.py; authority-check.json; history-and-skills.json; initial-state.json; final-state.json |
| UV_OFFLINE=1 uv run --frozen --group devboard python -B /tmp/v3-independent-round5.x5446H/boundaries.py | exit 0; 11 independent boundary probes PASS | boundaries.py/log; boundaries-results.json; boundaries-commands.json |
| same uv prefix, /tmp/v3-independent-round5.x5446H/additional.py | exit 0; metadata/read/traversal guards, six rollback probes and documented cached standalone command PASS | additional.py/log; signal-child.py; additional-results.json; additional-commands.json |
| python3 -B /tmp/v3-independent-round5.x5446H/diff-audit.py | exit 0; complete path inventory/diff digest, exact initial/final equality, original v2 HEAD and final preservation checked | diff-audit.py/json; diff-check.log |
| git diff --check BASE CANDIDATE | exit 2; whitespace only in historical review/evidence or validation logs, no active source/guidance whitespace finding | diff-check.log; diff-audit.json |

Inherited suite totals are shell-syntax 40, checker 31, lifecycle 236, runtime-tools 23, distribution-tools 12, enforcement-tools 22, reference-graph 3, documentation-coherence 7, metrics 3, examples 7, migration 6, release-coherence 11 and installed-context 8: 409 passed, 0 failed. Host: macOS 27.0.1 arm64; uv tooling Python 3.13.10. No Linux or hosted CI execution is claimed.

The independent boundary tests use only synthetic marker contents. They compare complete input inventories, including modes/directories/links, before and after operations. Planted regular files, external file/directory links and nested directories under required source trees and both canonical seed trees do not leak to output. Guarded source_entries calls forbid rglob, stat/lstat, exists, is_dir/is_file/is_symlink, resolve, open/read_bytes/read_text on excluded paths. Missing, changed, leaf-symlinked and parent-symlinked owned sources refuse before fixture output, while the normal installer continues to reject external source discovery links. Source-checkout and initialized-installed end-to-end cases also run in the required migration suite.

Original preservation exception observations

Frozen T3 context: refs/t3/orchestration-v2/checkpoints/ZjhjNzIxNWU0NTJkYzY2OTVlOGEwY2E3YTc3YTIwMDM/ordinal/. Every frozen ref remains unchanged. The following additional checkpoints each meet the human-approved higher-ordinal, expected author/subject and identical-tree conditions, anchored to frozen ordinal 36. All share tree {allowed[0]['tree']}. This is not exact ref-set equality and does not authenticate who created a checkpoint. Full refs/OIDs/trees/anchors are recorded in preservation-observations.json.

| Added ordinal | OID |
| --- | --- |
{ref_rows}

Skipped checks, baseline conditions and residual risk

- No required local suite or boundary check was skipped. Formal real-product gate traversal, human UAT/approval, Linux, hosted CI, remote delivery and actual production deployment are outside this request and are not inferred from passing local tests.
- A fresh initialized fixture deliberately returns checker exit 1 with exactly GENDEV-MANIFEST-ENFORCEMENT-002 for its unset required_attester. This inherited pre-approval condition remains explicit; the independent fresh probes leave it unset and G1 pending. No real human attestation was fabricated. Existing regression/replay fixtures label any synthetic identity as fixture data.
- git diff --check reports retained historical raw-evidence/report whitespace; it does not indicate a behavior regression. The first reviewer classification script underclassified two historical report paths and raised a harness assertion; the corrected classification and unchanged raw diagnostic are retained in diff-audit.initial.py and diff-audit.initial-result.json. No candidate change was made to obtain passing results.
- fsck's three dangling blobs are unreachable-object notices, not connectivity failure. The full tracked inventory and refs are unchanged across this review.
- File-level atomic writes and caught-exception/interrupt rollback are evidenced. Power loss, SIGKILL, concurrent hostile filesystem mutation and automatic semantic merging remain outside the declared transaction contract. Keep the documented pre-upgrade snapshot.
- Board role flags remain declarations, not authentication. Structural/JSON Schema checks do not prove actual human scope approval, independent review or remote delivery; the reusable policies preserve those distinctions.
- This was one bounded full pass of the changed migration scope. Historical proposals and old self-check reports were retained/audited as artifacts, not exhaustively re-evaluated or used as current proof. Step 8's final refresh remains deferred. No mandatory candidate regression was found.

Recommended next gate and durable handoff

The lead may record this VERIFIED report/evidence for candidate 98f8bec4597cd3307fc26e5c28dc86592e01ca08 and present the exact reviewed candidate and residual risks to Chuck Russell for human acceptance. This report does not accept work, complete the task, advance a product gate, authorize step 8, or authorize publication/delivery. The board remains started and acceptance pending.

An identical report is saved as /tmp/v3-independent-round5.x5446H/report.md. evidence-index.json lists SHA256/size for durable top-level reviewer scripts, logs, results and report; it excludes fixture trees, caches, lockfiles and raw full diffs. The index does not index itself. The lead's declared destination remains docs/resources/evolution/v3-migration/review/round-5/report.md and its evidence/ directory; the reviewer did not write governed candidate paths.
'''
(OUT/'report.md').write_text(report)
index={p.name:{'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size} for p in sorted(OUT.iterdir()) if p.is_file() and p.name!='evidence-index.json' and p.suffix not in {'.lock','.diff'} and p.name not in {'uv.lock'}}
(OUT/'evidence-index.json').write_text(json.dumps(index,indent=2)+'\n')
print('VERIFIED report saved',OUT/'report.md');print('report SHA256',index['report.md']['sha256']);print('indexed durable files',len(index));print('index SHA256',hashlib.sha256((OUT/'evidence-index.json').read_bytes()).hexdigest())
