#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Render known scaffold tokens literally; callers own overwrite decisions."""
from pathlib import Path
import json
import re
import sys
import unicodedata


def validate_project_name(project: str) -> None:
    if not project.strip() or any(unicodedata.category(character) in {"Cc", "Cs", "Zl", "Zp"} for character in project):
        raise ValueError("Project name must be nonempty single-line text without control characters.")


def main() -> int:
    if len(sys.argv) == 3 and sys.argv[1] == "--validate-project-name":
        validate_project_name(sys.argv[2])
        return 0
    if len(sys.argv) != 7:
        raise ValueError("Usage: render_template.py SOURCE DESTINATION PROJECT SLUG DATE PHASE")
    source, destination, project, slug, date, phase = sys.argv[1:]
    validate_project_name(project)
    text = Path(source).read_text()
    replacements = {
        "[Project Name]": project,
        "[project name]": project,
        "[project-slug]": slug,
        "[YYYY-MM-DD]": date,
        "[phase-id]": phase,
        "[id]": phase,
        "[Phase Name]": f"Phase {phase}",
        "[phase-build-plan]": f"phase-{phase}-build-plan",
        "[phase-tactical-plan]": f"phase-{phase}-tactical-implementation-plan",
    }
    if Path(source).suffix in {".yaml", ".yml"}:
        # The known scaffold uses a whole-scalar project-name token. Match its
        # quotes too so quotes/backslashes in input remain data, not YAML syntax.
        encoded = json.dumps(project, ensure_ascii=False)
        for token in ("[Project Name]", "[project name]"):
            replacements[token] = encoded
            replacements['"' + token + '"'] = encoded
            replacements["'" + token + "'"] = encoded
    # One pass prevents tokens in a user-supplied project name from being
    # interpreted as scaffold instructions during a later substitution.
    pattern = re.compile("|".join(re.escape(key) for key in replacements))
    text = pattern.sub(lambda match: replacements[match.group()], text)
    text = re.sub(r"^Date:$", lambda _: f"Date: {date}", text, flags=re.MULTILINE)
    text = re.sub(r"^Owner:$", "Owner: TBD", text, flags=re.MULTILINE)
    Path(destination).write_text(text)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValueError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(2)
