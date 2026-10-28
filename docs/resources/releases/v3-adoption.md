# Methodology-v3 Adoption And Upgrade Guide

Status: Unreleased distribution guidance; human acceptance/release pending
Lifecycle contract: GenDev 1.0.2

Use the Practitioner Guide, especially Chapters 4 and 20–22, for the full workflow.
This guide concerns v3's distribution and operating changes. The inherited
1.0.2 adoption and release records are historical baseline references, not proof
that the v3 repository or expanded skills are released.

## Choose A Source Revision

The private source is https://github.com/CIChuck/methodology-v3. The reviewed
migration is pinned to 98f8bec. GitHub main carries it with later evidence/hosting
records; human acceptance remains pending. The nine workflow additions are on
integration/v3-skill-import at operational candidate 1516712 with local checks and
pending independent review. This documentation branch describes the combined
library; it does not merge, accept or release it. Use a source revision appropriate
to the adopting owner's decision and retain its provenance.

## New Product

Create a product destination with its own README, install from the chosen toolkit checkout,
then initialize in the destination. Use the installer's dry run before applying.
Request --with-resources if the product should receive the guide/examples and
other historical references; these do not seed active task or approval history.
Preserve existing AGENTS.md or explicitly authorize its managed integration.
Declare the actual protected branch for the rendered product workflow.

The product begins G1 pending with an empty owner-controlled board. Assign the
real owner, gate approver and required attester, plus collaboration, scaling and
enforcement controls. A fresh unset attester causes the explicit
GENDEV-MANIFEST-ENFORCEMENT-002 checker error until named; naming is not approval.
Validate doctor, project-state, methodology and board state before proceeding.

## Existing GenDev Installation

Snapshot the target. Run `scripts/install-methodology.sh --force --dry-run TARGET`
from the source and reconcile reported paths before applying the same command
without --dry-run. --force does not bypass changed/missing/mode-modified owned
files, unsafe symlinks, unowned collisions or unresolved local amendments.
Preserve authority/approvals, board/tasks, local policies/skills and runtime data.
Do not reset integrity hashes to make a conflict disappear.

Installation history and amendment records survive. Retained project-owned seeds
may need an explicit owner-reviewed semantic update; they are not silently
replaced. After application, check integrity, current project state, methodology,
board validate/next and dashboard freshness. Record changes and evidence.

## Existing Product Documents Without GenDev

Use the declared-source backfill route and Chapter 19. Preserve originals,
conform actual vision/PRD/architecture content, surface gaps and earn acceptance
at the real gates. Imported documents, prior team habits and a board task are
not automatically accepted authority.

## Changed Operating Habits

Use started/granted task scope plus accepted phase/directive/verification authority
before product generation. Allow private implementation-local choices that stay
inside that authority. Assess amendment impact before regression. Draft future
phase build plans without implying acceptance; finalize tactical/directive detail
just in time. Freeze exact candidates for fresh read-only validation and bounded
remediation. Record human acceptance and actual delivery separately.

Skills package those techniques. Preserve full folders and relative resources;
provider model/access settings and T3 actions are optional integrations, not
project approvals or portable account defaults. The full catalog is Chapter 21.

## Methodology Development And Product Installation

The source repo uses its authorized evolution records and may have no docs/project.
An installed product uses canonical project authority and its own generated board.
Do not copy source tasks or reinitialize a live project to test the method. Use
create-dry-run.py for a fresh isolated exercise with owned assets, canonical
seeds and no live authority/task history. Follow the full contract and rollback
limits in `docs/methodology/guides/distribution-ownership.md`.

No live T3_Code_Sample resync, release or deployment has been performed by this
documentation refresh. Preserve both originals and recovery until their owner
explicitly decides otherwise.
