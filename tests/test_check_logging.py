"""Behaviour checks for automatic lab verification logs."""

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import json
from pathlib import Path
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import unittest


PROJECT = Path(__file__).resolve().parents[1]
RUNNER = PROJECT / "lab/scripts/run_check.py"


class CheckLoggingTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="lab-check-tests-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.logs = self.root / "logs/checks"

    def run_check(self, code, *arguments, actor="learner", cwd=None, log_dir=None):
        return subprocess.run(
            [
                sys.executable, str(RUNNER),
                "--log-dir", str(log_dir or self.logs),
                "--cwd", str(cwd or self.root),
                "--actor", actor, "--",
                sys.executable, "-u", "-c", code, *arguments,
            ],
            capture_output=True,
            timeout=15,
        )

    def records(self):
        return [
            (folder, json.loads((folder / "run.json").read_text()))
            for folder in sorted(self.logs.iterdir())
        ]

    def test_stdout_stderr_and_utc_timestamps(self):
        result = self.run_check(
            'import sys; print("PASS spaces"); print("FAIL hidden files", file=sys.stderr)'
        )
        self.assertEqual(result.returncode, 0)
        folder, record = self.records()[0]
        expected = b"PASS spaces\nFAIL hidden files\n"
        self.assertEqual((folder / "output.log").read_bytes(), expected)
        self.assertEqual(result.stdout, expected)
        self.assertEqual(record["status"], "finished")
        self.assertEqual(record["exit_code"], 0)
        self.assertEqual(record["actor"], "learner")
        times = [datetime.fromisoformat(record[key].replace("Z", "+00:00"))
                 for key in ("started_at", "finished_at")]
        self.assertTrue(all(time.utcoffset().total_seconds() == 0 for time in times))
        self.assertLessEqual(times[0], times[1])

    def test_failed_check_keeps_output_and_exit_code(self):
        result = self.run_check('import sys; print("FAIL empty input"); sys.exit(7)')
        self.assertEqual(result.returncode, 7)
        folder, record = self.records()[0]
        self.assertEqual(record["exit_code"], 7)
        self.assertEqual(record["status"], "finished")
        self.assertEqual((folder / "output.log").read_bytes(), b"FAIL empty input\n")

    def test_silent_check_is_still_logged(self):
        result = self.run_check("pass")
        self.assertEqual(result.returncode, 0)
        folder, record = self.records()[0]
        self.assertEqual((folder / "output.log").read_bytes(), b"")
        self.assertIsNotNone(record["finished_at"])

    def test_agent_label_arguments_and_working_directory(self):
        cwd = self.root / "workspace with spaces"
        cwd.mkdir()
        result = self.run_check(
            'import os,sys; print(os.getcwd()); print(sys.argv[1])',
            "argument with spaces", actor="agent", cwd=cwd,
        )
        self.assertEqual(result.returncode, 0)
        folder, record = self.records()[0]
        self.assertEqual(record["actor"], "agent")
        self.assertEqual(record["cwd"], str(cwd))
        self.assertEqual(record["command"][-1], "argument with spaces")
        self.assertEqual((folder / "output.log").read_text(),
                         f"{cwd}\nargument with spaces\n")

    def test_concurrent_retries_preserve_separate_histories(self):
        with ThreadPoolExecutor(max_workers=3) as pool:
            results = list(pool.map(
                lambda number: self.run_check(f'print("attempt {number}")'), range(3)
            ))
        self.assertTrue(all(result.returncode == 0 for result in results))
        records = self.records()
        self.assertEqual(len(records), 3)
        self.assertEqual(
            {(folder / "output.log").read_text() for folder, _ in records},
            {f"attempt {number}\n" for number in range(3)},
        )

    def test_launch_error_is_logged(self):
        result = subprocess.run(
            [sys.executable, str(RUNNER), "--log-dir", str(self.logs),
             "--", str(self.root / "missing-check")],
            capture_output=True, timeout=15,
        )
        self.assertEqual(result.returncode, 127)
        folder, record = self.records()[0]
        self.assertEqual(record["status"], "launch-error")
        self.assertIn(b"Unable to start check", (folder / "output.log").read_bytes())

    def test_logging_setup_failure_prevents_execution(self):
        blocker = self.root / "not-a-directory"
        blocker.write_text("keep")
        sentinel = self.root / "should-not-exist"
        result = self.run_check(
            'from pathlib import Path; import sys; Path(sys.argv[1]).touch()',
            str(sentinel), log_dir=blocker / "checks",
        )
        self.assertEqual(result.returncode, 74)
        self.assertFalse(sentinel.exists())
        self.assertIn(b"logging failed before execution", result.stderr)

    def test_large_binary_output_is_preserved(self):
        expected = bytes(range(256)) * 1000
        result = self.run_check('import sys; sys.stdout.buffer.write(bytes(range(256))*1000)')
        self.assertEqual(result.returncode, 0)
        folder, _ = self.records()[0]
        self.assertEqual((folder / "output.log").read_bytes(), expected)
        self.assertEqual(result.stdout, expected)

    @unittest.skipIf(sys.platform == "win32", "POSIX signal exit status")
    def test_signal_failure_keeps_partial_output(self):
        result = self.run_check(
            'import os,signal; print("before signal"); os.kill(os.getpid(), signal.SIGTERM)'
        )
        self.assertEqual(result.returncode, 128 + signal.SIGTERM)
        folder, record = self.records()[0]
        self.assertEqual(record["status"], "interrupted")
        self.assertEqual((folder / "output.log").read_bytes(), b"before signal\n")

    @unittest.skipUnless(shutil.which("bash"), "Bash example launcher")
    def test_documented_launcher_logs_direct_terminal_runs(self):
        lab = self.root / "lab with spaces"
        checks = lab / "checks"
        checks.mkdir(parents=True)
        shutil.copyfile(RUNNER, checks / "run_check.py")
        (checks / "verify.sh").write_text(
            'printf "criterion output\\n"; printf "diagnostic\\n" >&2; exit "${1:-0}"\n'
        )
        reference = (PROJECT / "lab/references/check-logging.md").read_text()
        launcher = re.search(r"```bash\n(.*?)\n```", reference, re.S).group(1)
        (lab / "check.sh").write_text(launcher + "\n")
        result = subprocess.run(
            ["bash", str(lab / "check.sh"), "3"], cwd=self.root,
            capture_output=True, timeout=15,
        )
        self.assertEqual(result.returncode, 3)
        folder = next((lab / "logs/checks").iterdir())
        record = json.loads((folder / "run.json").read_text())
        self.assertEqual(record["cwd"], str(lab))
        self.assertEqual(record["exit_code"], 3)
        self.assertEqual((folder / "output.log").read_bytes(),
                         b"criterion output\ndiagnostic\n")


if __name__ == "__main__":
    unittest.main()
