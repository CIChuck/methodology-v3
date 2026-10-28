#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
# Shell entry point shared by distribution callers; the planner performs all
# preflight, ownership, provenance and transactional rollback in one process.
gendev_dist_install() {
  python3 "$1/scripts/lib/distribution.py" "$@"
}

gendev_dist_print_report() {
  # The transactional installer emits its report before returning.
  :
}
