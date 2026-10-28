#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Render known scaffold tokens literally; callers own overwrite decisions."""
from pathlib import Path
import re
import sys


def main() -> None:
    source, destination, project, slug, date, phase = sys.argv[1:]
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
    # One pass prevents tokens in a user-supplied project name from being
    # interpreted as scaffold instructions during a later substitution.
    pattern = re.compile("|".join(re.escape(key) for key in replacements))
    text = pattern.sub(lambda match: replacements[match.group()], text)
    text = re.sub(r"^Date:$", lambda _: f"Date: {date}", text, flags=re.MULTILINE)
    text = re.sub(r"^Owner:$", "Owner: TBD", text, flags=re.MULTILINE)
    Path(destination).write_text(text)


if __name__ == "__main__":
    main()
