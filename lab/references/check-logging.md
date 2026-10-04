# Check-run logging

Log verification within the check entry point itself. A model cannot reliably observe a learner's separate terminal session, and a report written later cannot reconstruct missing output.

## Create a logging-enabled checker

Copy the bundled `scripts/run_check.py` from the installed skill into the generated lab's `checks/` directory. Keep the underlying verifier alongside it. Create a learner-facing entry point appropriate to the lab's language that calls the runner. All documented check commands must use this entry point, including any check that the learner runs directly. If an existing public verifier must remain callable directly, instrument that entry point too or turn it into the launcher and move its verification logic to a separate implementation.

For example, a Bash lab can have this `check.sh` at the lab root:

```bash
#!/usr/bin/env bash
set -euo pipefail
lab_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
exec python3 "$lab_dir/checks/run_check.py" \
  --log-dir "$lab_dir/logs/checks" \
  --cwd "$lab_dir" \
  --actor "${LAB_CHECK_ACTOR:-learner}" \
  -- bash "$lab_dir/checks/verify.sh" "$@"
```

The learner runs `bash check.sh`; the agent uses `LAB_CHECK_ACTOR=agent bash check.sh` for its own validation. Actor labels describe the invocation; they are not identity authentication or cheating detection. Preserve verification arguments as distinct arguments, and propagate the verifier's exit status so a failed check still reports failure.

The bundled runner requires Python 3 and is suitable for non-interactive checks. If that runtime is unavailable or the exercise needs an interactive checker, implement equivalent logging within the chosen language. Verify its success and failure behaviour before presenting it. Do not silently offer an unlogged alternative check command.

## Log contract

Each invocation gets a unique run directory under `logs/checks/`, named with a UTC timestamp and a unique suffix. It contains:

- `run.json`: `started_at` and `finished_at` in UTC ISO 8601, actor, command argument list, working directory, status, and exit code.
- `output.log`: complete combined stdout and stderr, including failures and launch errors. A silent run has an empty file.

The runner streams output to the terminal while retaining it. It writes initial metadata before launching the check and final metadata when the check ends. Ordinary completion uses status `finished`; launch failures use `launch-error`; signals and user interruption use `interrupted`. A started record left as `running` with no finish time means completion was not recorded, for example after a forced shutdown; do not interpret it as success or invent the missing output.

If a log cannot be created, report the logging error and do not start the check. If logging fails during execution, return a nonzero logging error and explain that the capture is incomplete. Keep logs outside directories cleared by fixture resets. Preserve earlier runs and do not backfill timestamps for unrecorded past attempts.

## Use the history for teaching

Read metadata and relevant output in chronological order, keeping agent runs separate. Encourage check scripts to print each tested criterion, expected behaviour, and actual result when useful, rather than only an overall failure message. Let the model choose checks suited to the capability.

In `REPORT.md`, link evidence supporting repeated failures, improvement, and remaining gaps. A missing executable, broken fixture, or faulty checker is an environment or exercise issue. A mismatch on a correctly functioning criterion is evidence about that attempt; infer a misconception only with supporting explanation or work.

Use this evidence to recommend targeted hints, a smaller exercise, or reduced support to `/teach`. Learning decision records should capture significant findings with links to the history, not duplicate every log. Learner-confirmed independent application remains the success criterion; a failed history does not disqualify later confirmation, and a passing check does not supply that confirmation by itself.
