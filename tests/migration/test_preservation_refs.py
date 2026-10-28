from __future__ import annotations

import importlib.util
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("migration_preservation", ROOT / "scripts/verify-migration-inputs.py")
if spec is None or spec.loader is None:
    raise RuntimeError("Cannot load preservation verifier")
preservation = importlib.util.module_from_spec(spec)
spec.loader.exec_module(preservation)


class PreservationRefTests(unittest.TestCase):
    def setUp(self) -> None:
        temp = tempfile.TemporaryDirectory(prefix="preservation-refs-")
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.git("init", "-q")
        (self.root / "source.txt").write_text("Frozen source\n")
        self.git("add", "source.txt")
        self.tree = self.git("write-tree")
        self.prefix = "refs/t3/orchestration-v2/checkpoints/fixture_context/ordinal/"
        self.original = self.checkpoint("0")
        self.expected = self.refs()

    def git(self, *args: str, data: str | None = None, author: str = "T3 Code") -> str:
        result = subprocess.run(["git", *args], cwd=self.root, input=data,
                                capture_output=True, text=True, check=True,
                                env={**os.environ, "GIT_AUTHOR_NAME": author,
                                     "GIT_AUTHOR_EMAIL": "t3code@users.noreply.github.com",
                                     "GIT_COMMITTER_NAME": author,
                                     "GIT_COMMITTER_EMAIL": "t3code@users.noreply.github.com"})
        return result.stdout.strip()

    def checkpoint(self, ordinal: str, *, tree: str | None = None, author: str = "T3 Code") -> str:
        ref = self.prefix + ordinal
        oid = self.git("commit-tree", tree or self.tree, data="t3 checkpoint ref=" + ref + "\n", author=author)
        self.git("update-ref", ref, oid)
        return oid

    def refs(self) -> str:
        return self.git("for-each-ref", "--format=%(refname) %(objectname)")

    def compare(self, approved: bool = True) -> tuple[list[str], list[dict[str, str]]]:
        return preservation.compare_refs(self.root, self.expected, self.refs(), allow_identical_t3_checkpoints=approved)

    def test_only_approved_identical_tree_addition_passes(self) -> None:
        self.checkpoint("1")
        errors, allowed = self.compare()
        self.assertEqual(errors, [])
        self.assertEqual([entry["ref"] for entry in allowed], [self.prefix + "1"])
        self.assertEqual(allowed[0]["tree"], self.tree)
        self.assertEqual(allowed[0]["frozen_anchor"], self.prefix + "0")

    def test_no_exception_applies_without_explicit_approval(self) -> None:
        self.checkpoint("1")
        self.assertTrue(self.compare(approved=False)[0])
        self.assertEqual(self.compare(approved=False)[1], [])

    def test_changed_frozen_ref_fails_even_with_identical_tree(self) -> None:
        other = self.checkpoint("1")
        self.git("update-ref", self.prefix + "0", other)
        self.assertTrue(any("changed or removed" in error for error in self.compare()[0]))

    def test_removed_frozen_ref_fails(self) -> None:
        self.git("update-ref", "-d", self.prefix + "0")
        self.assertTrue(any("changed or removed" in error for error in self.compare()[0]))

    def test_other_added_branch_fails(self) -> None:
        self.git("update-ref", "refs/heads/other", self.original)
        self.assertTrue(any("unapproved added ref" in error for error in self.compare()[0]))

    def test_added_checkpoint_with_different_tree_fails(self) -> None:
        (self.root / "source.txt").write_text("Different source\n")
        self.git("add", "source.txt")
        self.checkpoint("1", tree=self.git("write-tree"))
        self.assertTrue(self.compare()[0])

    def test_added_checkpoint_with_other_author_fails(self) -> None:
        self.checkpoint("1", author="Other Author")
        self.assertTrue(self.compare()[0])

    def test_new_context_uses_frozen_tree_anchor(self) -> None:
        self.prefix = "refs/t3/orchestration-v2/checkpoints/other_context/ordinal/"
        self.checkpoint("0")
        errors, allowed = self.compare()
        self.assertEqual(errors, [])
        self.assertEqual(allowed[0]["tree"], self.tree)
        self.assertEqual(allowed[0]["frozen_anchor"], "refs/t3/orchestration-v2/checkpoints/fixture_context/ordinal/0")

    def test_new_context_different_tree_fails(self) -> None:
        self.prefix = "refs/t3/orchestration-v2/checkpoints/other_context/ordinal/"
        (self.root / "source.txt").write_text("Changed new context\n")
        self.git("add", "source.txt")
        self.checkpoint("0", tree=self.git("write-tree"))
        self.assertTrue(self.compare()[0])

    def test_new_context_without_any_frozen_checkpoint_fails(self) -> None:
        self.expected = ""
        self.assertTrue(self.compare()[0])

    def test_checkpoint_with_wrong_subject_fails(self) -> None:
        ref = self.prefix + "1"
        oid = self.git("commit-tree", self.tree, data="Wrong subject\n")
        self.git("update-ref", ref, oid)
        self.assertTrue(self.compare()[0])

    def test_checkpoint_ref_to_noncommit_fails(self) -> None:
        self.git("update-ref", self.prefix + "1", self.tree)
        self.assertTrue(self.compare()[0])

    def test_existing_context_nonincreasing_ordinal_fails(self) -> None:
        self.checkpoint("00")
        self.assertTrue(self.compare()[0])


if __name__ == "__main__":
    unittest.main()
