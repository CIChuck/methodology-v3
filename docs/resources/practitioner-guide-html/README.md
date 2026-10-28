# Methodology-v3 Practitioner Guide HTML

This is the static presentation of the canonical Markdown under
`../practitioner-guide/`. The guide home and chapter catalog describe the
unreleased v3 distribution and separate reviewed/pending-review features.
It does not publish a release, accept a product or deploy this website.

- content/ contains exact copies of all canonical Markdown files.
- index.html and the chapter catalog carry the v3 edition title/navigation.
- Existing rendering, styles, pinned Marked/Mermaid bundles and notices remain.
- Mermaid fences are supported; content is still authored as canonical Markdown.

## Synchronize From The Repository Root

After editing canonical guide files:

```bash
cp docs/resources/practitioner-guide/*.md docs/resources/practitioner-guide-html/content/
```

Verify exact file sets and bytes, not only dates or displayed titles:

```bash
python3 - <<'PYCHECK'
from pathlib import Path
source = Path("docs/resources/practitioner-guide")
mirror = Path("docs/resources/practitioner-guide-html/content")
expected = {p.name: p.read_bytes() for p in source.glob("*.md")}
actual = {p.name: p.read_bytes() for p in mirror.glob("*.md")}
assert expected == actual, "Guide mirror has missing, stale or changed Markdown"
print(f"Guide mirror synchronized: {len(expected)} Markdown files")
PYCHECK
```

If a canonical chapter is retired, explicitly remove only its stale generated
Markdown counterpart before rechecking. A new/renamed chapter also needs its
corresponding ID/file/title entry in assets/app.js. Verify the catalog's file
set matches the canonical set; keep existing IDs stable for saved links.

## Serving And Publication

The client fetches mirrored Markdown with ?raw=1; an ordinary static HTTP host
serves the same file for that query. Browser file:// security prevents this fetch
from working by directly opening index.html. Use an approved static host or your
normal local documentation preview environment. Preparing these files is not
publication to an existing external site; that requires an explicit target and
publishing authorization under docs/methodology/guides/publishing.md.

No vendor bundle, renderer logic or stylesheet update is needed for a content
refresh. Record content/catalog checks separately from visual browser UAT and
external deployment; do not claim those checks if they were not run.
