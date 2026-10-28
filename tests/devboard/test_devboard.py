from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

REPOSITORY = Path(__file__).resolve().parents[2]
SCRIPT = REPOSITORY / "scripts" / "devboard.py"


class DevelopmentBoardTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="devboard-test-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.planning = self.root / "docs" / "planning"
        for lane in ("active", "queued", "review", "blocked", "deferred", "backlog"):
            (self.planning / lane).mkdir(parents=True)
        shutil.copyfile(
            REPOSITORY / "docs/planning/board.schema.json",
            self.planning / "board.schema.json",
        )
        self.board: dict[str, object] = {
            "version": 1,
            "updated": "2026-10-27",
            "tasks": [],
            "events": [],
        }
        self.write_board()
        self.succeed("render")

    def run_cli(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--root", str(self.root), *arguments],
            capture_output=True,
            text=True,
            check=False,
        )

    def succeed(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        result = self.run_cli(*arguments)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return result

    def write_board(self) -> None:
        (self.planning / "board.yaml").write_text(
            yaml.safe_dump(self.board, sort_keys=False), encoding="utf-8"
        )

    def snapshots(self) -> tuple[bytes, bytes]:
        return (
            (self.planning / "board.yaml").read_bytes(),
            (self.planning / "README.md").read_bytes(),
        )

    def queue_task(self) -> None:
        packet = self.planning / "queued" / "example-task"
        packet.mkdir()
        (packet / "README.md").write_text("# Fixture tracking index\n")
        self.board["tasks"] = [
            {
                "id": "example-task",
                "title": "Fixture task",
                "priority": 1,
                "work_state": "queued",
                "condition": "normal",
                "implementation_authority": "not_granted",
                "packet": "docs/planning/queued/example-task/",
                "next_gate": "Fixture maintainer approval",
                "delivery_state": "not_started",
                "branch": None,
                "depends_on": [],
                "validation": [],
            }
        ]
        self.write_board()
        self.succeed("render")

    def approve_task(self) -> None:
        self.succeed(
            "transition", "example-task", "approved",
            "--actor", "Fixture Maintainer", "--actor-role", "maintainer",
            "--note", "Fixture scope approval", "--next-gate", "Prepare execution",
        )

    def start_task(self) -> None:
        self.queue_task()
        self.approve_task()
        (self.planning / "queued/example-task").rename(
            self.planning / "active/example-task"
        )
        self.succeed(
            "transition", "example-task", "started",
            "--packet", "docs/planning/active/example-task/",
            "--branch", "feature/fixture", "--actor", "Fixture Agent",
            "--actor-role", "agent", "--note", "Fixture start",
            "--next-gate", "Fixture verification",
        )

    def assert_rejected_without_writes(self, message: str, *arguments: str) -> None:
        before = self.snapshots()
        result = self.run_cli(*arguments)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn(message, result.stderr)
        self.assertEqual(self.snapshots(), before)

    def test_empty_board_and_compatibility_entrypoint(self) -> None:
        self.assertIn("0 tasks", self.succeed("validate").stdout)
        self.assertEqual(self.succeed("next").stdout.strip(), "NO_OPEN_TASK")
        result = subprocess.run(
            [sys.executable, str(REPOSITORY / "scripts/friday-dev-board.py"),
             "--root", str(self.root), "next"],
            capture_output=True, text=True, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "NO_OPEN_TASK")

    def test_agent_cannot_approve(self) -> None:
        self.queue_task()
        self.assert_rejected_without_writes(
            "only a maintainer", "transition", "example-task", "approved",
            "--actor", "Fixture Agent", "--actor-role", "agent",
            "--note", "Attempted self-approval", "--next-gate", "Start",
        )

    def test_board_approval_preserves_gendev_state(self) -> None:
        self.queue_task()
        project = self.root / "docs/project"
        (project / "approvals").mkdir(parents=True)
        manifest = project / "project.yaml"
        gate_log = project / "approvals/gate-log.md"
        manifest.write_text("project:\n  current_gate: G1\n")
        gate_log.write_text("# No gate approvals\n")
        before = (manifest.read_bytes(), gate_log.read_bytes())
        self.approve_task()
        self.assertEqual((manifest.read_bytes(), gate_log.read_bytes()), before)
        task = yaml.safe_load((self.planning / "board.yaml").read_text())["tasks"][0]
        self.assertEqual(task["work_state"], "approved")
        self.assertEqual(task["implementation_authority"], "granted")

    def test_start_requires_a_branch(self) -> None:
        self.queue_task()
        self.approve_task()
        self.assert_rejected_without_writes(
            "started work requires", "transition", "example-task", "started",
            "--actor", "Fixture Agent", "--actor-role", "agent",
            "--note", "Missing branch", "--next-gate", "Verification",
        )

    def test_completion_requires_evidence(self) -> None:
        self.start_task()
        self.assert_rejected_without_writes(
            "requires at least one --evidence", "transition", "example-task", "completed",
            "--actor", "Fixture Agent", "--actor-role", "agent",
            "--note", "Missing evidence", "--next-gate", "Acceptance",
        )

    def test_agent_cannot_accept_completed_work(self) -> None:
        self.start_task()
        (self.planning / "active/example-task").rename(
            self.planning / "review/example-task"
        )
        self.succeed(
            "transition", "example-task", "completed",
            "--packet", "docs/planning/review/example-task/",
            "--evidence", "Fixture verification only",
            "--actor", "Fixture Agent", "--actor-role", "agent",
            "--note", "Fixture evidence", "--next-gate", "Human acceptance",
        )
        self.assert_rejected_without_writes(
            "only a maintainer", "transition", "example-task", "accepted",
            "--actor", "Fixture Agent", "--actor-role", "agent",
            "--note", "Attempted self-acceptance", "--next-gate", "None",
        )

    def test_queued_work_cannot_skip_to_started(self) -> None:
        self.queue_task()
        self.assert_rejected_without_writes(
            "transition not allowed", "transition", "example-task", "started",
            "--branch", "feature/fixture", "--actor", "Fixture Agent",
            "--actor-role", "agent", "--note", "Skipped approval",
            "--next-gate", "Verification",
        )

    def test_unknown_dependency_is_rejected(self) -> None:
        self.queue_task()
        board = yaml.safe_load((self.planning / "board.yaml").read_text())
        board["tasks"][0]["depends_on"] = ["missing-task"]
        self.board = board
        self.write_board()
        self.assert_rejected_without_writes("depends on unknown task", "validate")

    def test_stale_dashboard_check_is_read_only(self) -> None:
        (self.planning / "README.md").write_text("stale\n")
        self.assert_rejected_without_writes("dashboard is stale", "validate")
        self.assert_rejected_without_writes("dashboard is stale", "render", "--check")
        self.succeed("render")
        self.succeed("validate")

    def test_started_task_requires_accepted_dependencies(self) -> None:
        self.queue_task()
        board = yaml.safe_load((self.planning / "board.yaml").read_text())
        dependent = dict(board["tasks"][0])
        dependent.update(
            id="dependent-task", title="Dependent fixture", priority=2,
            work_state="started", implementation_authority="granted",
            packet="docs/planning/active/dependent-task/", branch="feature/dependent",
            depends_on=["example-task"], approved_by="Fixture Maintainer",
            approved_at="2026-10-27",
        )
        packet = self.planning / "active/dependent-task"
        packet.mkdir()
        (packet / "README.md").write_text("# Dependent tracking fixture\n")
        board["tasks"].append(dependent)
        self.board = board
        self.write_board()
        self.assert_rejected_without_writes("unaccepted dependency", "validate")

    def test_schema_disagreement_is_rejected(self) -> None:
        import json

        path = self.planning / "board.schema.json"
        schema = json.loads(path.read_text())
        schema["$defs"]["task"]["properties"]["work_state"]["enum"] = ["queued"]
        path.write_text(json.dumps(schema))
        self.assert_rejected_without_writes("schema work states disagree", "validate")

    def test_delivery_cannot_move_backward(self) -> None:
        self.start_task()
        self.succeed(
            "set-delivery", "example-task", "pushed",
            "--actor", "Fixture Agent", "--actor-role", "agent",
            "--note", "Fixture push record",
        )
        self.assert_rejected_without_writes(
            "cannot move backward", "set-delivery", "example-task", "local",
            "--actor", "Fixture Agent", "--actor-role", "agent",
            "--note", "Invalid backward delivery",
        )

    def test_merge_record_requires_evidence(self) -> None:
        self.start_task()
        self.assert_rejected_without_writes(
            "merged delivery requires --evidence", "set-delivery", "example-task", "merged",
            "--actor", "Fixture Agent", "--actor-role", "agent",
            "--note", "Missing merge evidence",
        )


if __name__ == "__main__":
    unittest.main()
