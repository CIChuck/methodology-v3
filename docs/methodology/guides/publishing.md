# Repository And Documentation Publishing

Status: Reusable operating guidance
Authority: accepted project/release authority and actual human publishing instruction

GitHub hosting, a PR, a methodology release and deployment of a documentation site
are different effects. Confirm the requested target, revision, visibility and
scope before each. Repository availability does not imply accepted methodology,
passed CI or a production release. Keep an unreleased candidate labeled that way.

For toolkit hosting, preserve source/history and push only intended branches;
verify destination ownership, visibility, default branch and exact remote OIDs.
Keep review-pending work separate from the reviewed baseline and record observed
delivery independently of verification/acceptance. Do not mirror hidden/tool refs,
publish inherited release tags as a new release, or merge by implication.

For a Practitioner site, update canonical Markdown first, synchronize every HTML
content file, verify navigation/links and validate the chosen revision. The source
Markdown is authority for content; deployment does not make it project authority.
Use the active provider's supported publishing workflow only when site publication
is actually requested. Resolve current capabilities, destination and credentials
there; do not copy personal domains, API endpoints or machine settings from old
notes. Secrets stay outside Git and rendered content.

Creating/updating a remote or preparing local HTML does not deploy the site.
Record actual URL/revision/visibility, successful delivery and any remaining
limits only after they are observed. Methodology release numbering, tags, branch
protection, independent review, human acceptance and production controls remain
separate decisions under their applicable plans. Never fabricate them from a
successful upload or a workflow skill's name.
