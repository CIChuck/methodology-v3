# Round 2 Bounded Remediation Directive

Status: Authorized remediation cycle 2; fresh full review required
Task: v3-baseline-migration
Reviewed candidate: 30aa3c7d68451c9b2ed892d30f349e20c0b14c3f
Independent outcome: CHANGES_REQUESTED
Authority: migration README.md step 7 authorization and review-scope.md

Round 2 independently cleared VAL-001, VAL-002 and VAL-003. The remaining
mandatory VAL-004 identifies inherited unsafe project-name substitution in
the materially changed shared rendering boundary. Chuck's authorization to
address in-scope findings covers this bounded fix and fresh review.

## VAL-004: Context-safe project-name rendering

Serialize project-name data as a YAML scalar when rendering a YAML manifest.
Retain literal text in Markdown and the one-pass protection against interpreting
placeholder tokens embedded in user input. Do not add a core YAML dependency:
JSON string encoding is a valid YAML scalar encoding for the known template.
Single-line project names support quotes, apostrophes, backslashes, Unicode,
slashes, ampersands and literal bracket tokens. Reject empty/control-character
names clearly before creating or replacing project artifacts, since raw newlines
or controls cannot be preserved as a single Markdown metadata/title value.

Owned scope: render_template.py, init-project.sh/init-phase.sh validation calls,
focused migration tests and their essential input-contract documentation.
No product behavior, new gate approval, source-project changes or final step 8
refresh is authorized. Existing control-plane parsing/phase rules remain intact.

## Acceptance and verification

- A fresh product initialized with quotes/backslashes in its name exits 0,
  produces parseable YAML, and the YAML-parsed name equals the exact input.
- Markdown titles retain those literal characters, including bracket-token text.
- Existing slash/ampersand, canonical directive/phase and placeholder tests pass.
- Invalid control-character names fail before project creation and before
  replacing an existing project, including --force. Later-phase setup likewise
  rejects invalid names before creating artifacts.
- All prior review findings remain resolved under their approved scope.
- Focused tests, appropriate inherited checks and an independent fresh full
  review are required. This is remediation cycle 2; if fresh review still
  requests mandatory changes, stop and return the unresolved findings to Chuck
  under the validation policy rather than starting another automatic cycle.
