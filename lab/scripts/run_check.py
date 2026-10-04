#!/usr/bin/env python3
"""Run a non-interactive lab verifier with durable, timestamped output capture."""

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys
import uuid


def timestamp():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def save_metadata(path, record):
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--log-dir", required=True)
    parser.add_argument("--cwd", default=str(Path.cwd()))
    parser.add_argument("--actor", choices=("learner", "agent"), default="learner")
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command
    if command and command[0] == "--":
        command = command[1:]
    if not command:
        parser.error("provide a check command after --")

    started = timestamp()
    run_name = started.replace(":", "-") + "-" + uuid.uuid4().hex
    run_dir = Path(args.log_dir).resolve() / run_name
    record = {
        "started_at": started,
        "finished_at": None,
        "actor": args.actor,
        "command": command,
        "cwd": str(Path(args.cwd).resolve()),
        "status": "running",
        "exit_code": None,
    }
    output = None
    try:
        run_dir.mkdir(parents=True, exist_ok=False)
        output = (run_dir / "output.log").open("xb")
        save_metadata(run_dir / "run.json", record)
    except OSError as error:
        if output is not None:
            output.close()
        print(f"Check logging failed before execution: {error}", file=sys.stderr)
        return 74

    process = None
    terminal_open = True

    def emit(data):
        nonlocal terminal_open
        output.write(data)
        output.flush()
        if terminal_open:
            try:
                sys.stdout.buffer.write(data)
                sys.stdout.buffer.flush()
            except BrokenPipeError:
                terminal_open = False

    try:
        with output:
            try:
                process = subprocess.Popen(
                    command,
                    cwd=record["cwd"],
                    stdin=subprocess.DEVNULL,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                )
            except OSError as error:
                emit(f"Unable to start check: {error}\n".encode("utf-8"))
                record.update(status="launch-error", exit_code=127)
            else:
                try:
                    while True:
                        data = process.stdout.read1(65536)
                        if not data:
                            break
                        emit(data)
                    code = process.wait()
                    record.update(
                        status="interrupted" if code < 0 else "finished",
                        exit_code=128 - code if code < 0 else code,
                    )
                except KeyboardInterrupt:
                    process.terminate()
                    try:
                        remaining, _ = process.communicate(timeout=5)
                    except subprocess.TimeoutExpired:
                        process.kill()
                        remaining, _ = process.communicate()
                    if remaining:
                        emit(remaining)
                    record.update(status="interrupted", exit_code=130)
                finally:
                    process.stdout.close()
        record["finished_at"] = timestamp()
        save_metadata(run_dir / "run.json", record)
    except OSError as error:
        if process is not None and process.poll() is None:
            process.kill()
            process.wait()
        print(f"Check logging failed; capture may be incomplete: {error}", file=sys.stderr)
        return 74

    print(f"\nCheck log: {run_dir}", file=sys.stderr)
    return record["exit_code"]


if __name__ == "__main__":
    sys.exit(main())
