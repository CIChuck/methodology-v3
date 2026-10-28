#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage:
  scripts/init-project.sh [--force] "Project Name"

Creates docs/project/ from the methodology templates.

Options:
  --force   Replace an existing docs/project directory.
USAGE
}

force=0

if [ "${1:-}" = "--help" ] || [ "${1:-}" = "-h" ]; then
  usage
  exit 0
fi

if [ "${1:-}" = "--force" ]; then
  force=1
  shift
fi

if [ "$#" -ne 1 ]; then
  usage
  exit 2
fi

project_name="$1"
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "$script_dir/.." && pwd)"

# Prerequisite preflight: initialization is the front door, so a missing tool
# fails here rather than surfacing later as a confusing checker failure. There
# is deliberately no skip flag; an environment without the prerequisites is not
# an environment the methodology supports.
. "$script_dir/lib/gendev-common.sh"
gendev_require_prereqs "init-project.sh" || exit 3
python3 "$script_dir/lib/render_template.py" --validate-project-name "$project_name"
target="$repo_root/docs/project"
template_root="$repo_root/docs/methodology/templates"
project_template="$repo_root/docs/project-template"

slug="$(
  printf '%s' "$project_name" |
    tr '[:upper:]' '[:lower:]' |
    sed -E 's/[^a-z0-9]+/-/g; s/^-+//; s/-+$//'
)"

if [ -z "$slug" ]; then
  echo "Project name must contain at least one alphanumeric character." >&2
  exit 2
fi

if [ -e "$target" ]; then
  if [ "$force" -ne 1 ]; then
    echo "docs/project already exists. Re-run with --force to replace it." >&2
    exit 1
  fi
  rm -rf "$target"
fi

today="$(date +%F)"

mkdir -p \
  "$target/approvals" \
  "$target/vision" \
  "$target/prd" \
  "$target/architecture" \
  "$target/design" \
  "$target/security-governance" \
  "$target/decisions" \
  "$target/build-plan/phases" \
  "$target/review" \
  "$target/deployment" \
  "$target/testing" \
  "$target/traceability" \
  "$target/as-built"

render_template() {
  src="$1"
  dest="$2"

  python3 "$script_dir/lib/render_template.py" "$src" "$dest" "$project_name" "$slug" "$today" "1"
}

render_template "$project_template/project.yaml" "$target/project.yaml"
render_template "$template_root/gate-log-template.md" "$target/approvals/gate-log.md"
render_template "$template_root/vision-template.md" "$target/vision/vision.md"
render_template "$template_root/prd-template.md" "$target/prd/prd.md"
render_template "$template_root/architecture-template.md" "$target/architecture/architecture.md"
render_template "$template_root/governance-security-template.md" "$target/security-governance/governance-security-spec.md"
render_template "$template_root/traceability-matrix-template.md" "$target/traceability/traceability-matrix.md"
render_template "$template_root/0001-technology-stack-template.md" "$target/decisions/0001-technology-stack.md"
render_template "$template_root/phase-build-plan-template.md" "$target/build-plan/phases/phase-1-build-plan.md"
render_template "$template_root/tactical-implementation-template.md" "$target/build-plan/phases/phase-1-tactical-implementation-plan.md"
render_template "$template_root/test-uat-plan-template.md" "$target/testing/phase-1-test-uat-plan.md"
render_template "$template_root/code-review-report-template.md" "$target/build-plan/phases/phase-1-code-review.md"
render_template "$template_root/as-built-closeout-template.md" "$target/as-built/phase-1-as-built-closeout.md"
render_template "$template_root/value-review-template.md" "$target/as-built/phase-1-value-review.md"

render_template "$template_root/phase-plan-template.md" "$target/build-plan/phase-plan.md"

render_template "$template_root/phase-construction-directive-template.md" "$target/build-plan/phases/phase-1-construction-directive.md"

cat > "$target/README.md" <<EOF
# $project_name

This is the active project authority directory for $project_name.

Start with the vision document, then move through PRD, architecture, governance/security,
phase planning, tactical implementation planning, construction directives, implementation,
review, remediation, and as-built close-out.

Controlling methodology:

\`\`\`text
docs/methodology/constitution/gendev.md
\`\`\`

Project manifest:

\`\`\`text
docs/project/project.yaml
\`\`\`

Current gate:

\`\`\`text
G1 Vision Ready
\`\`\`
EOF

cat > "$target/build-plan/README.md" <<EOF
# Build Plan

Use this directory for build planning: the phase plan and phase-specific plans.

Phase plans live under:

\`\`\`text
docs/project/build-plan/phases/
\`\`\`
EOF

echo "Initialized docs/project for $project_name"
echo "Project slug: $slug"
echo "Next document: docs/project/vision/vision.md"
