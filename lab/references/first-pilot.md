# Optional first pilot: file manifests

Use this only when no supplied objective is more relevant and a local Bash exercise suits the learner. The pilot practises safe file iteration and verifiable output; it is not a placement test. Use a simpler or different exercise if `/teach`'s context indicates that is appropriate.

## Objective

Generate a deterministic manifest containing one basename per matching regular file, including filenames with spaces and leading hyphens. Operate on immediate directory children only, and leave source files unchanged. For this small exercise, fixture names contain no newline characters. Empty input must produce empty output. Store the manifest outside the input directory. Exclude symbolic links.

This primarily exercises **Apply**. Diagnosing a flawed approach can exercise **Analyze**; discussing two approaches can exercise **Evaluate**; designing a general-purpose extension can exercise **Create**. Offer extensions only if useful to the current mission.

## Worked example

Create a disposable fixture directory with `server.log`, `error report.log`, `-startup.log`, `readme.txt`, `.hidden.log`, and a directory named `archive.log`. The text contents can be arbitrary and should be retained.

Explain and run this solution with fixture paths supplied as its two arguments:

```bash
#!/usr/bin/env bash
set -euo pipefail
input_dir=$1
output_file=$2
shopt -s nullglob dotglob
{
  for file in "$input_dir"/*.log; do
    [[ -f "$file" && ! -L "$file" ]] || continue
    printf '%s\n' "${file##*/}"
  done
} | LC_ALL=C sort > "$output_file"
```

Explain why directory expansion and argument handling matter, how unmatched patterns and hidden names are handled, why directories and symbolic links are skipped, and how sorting makes output deterministic. The supplied directory must exist; resolving invalid paths is outside this pilot's objective.

The expected manifest is:

```text
-startup.log
.hidden.log
error report.log
server.log
```

## Related learner challenge

Create distinct challenge fixtures: `notes.txt`, `meeting notes.txt`, `-draft.txt`, `.private.txt`, `trace.log`, and a directory named `old.txt`. Optionally add a symbolic link named `alias.txt` to `notes.txt` to illustrate its exclusion.

Ask the learner to produce a manifest of immediate `.txt` regular files, applying the same principle to different inputs. Keep the worked example freely accessible and let the learner choose an implementation. Present expected behaviour and checking instructions, but initially leave the challenge solution for the learner to write.

## Suggested verification

For the supplied fixtures, compare output to these basenames in C-locale order:

```text
-draft.txt
.private.txt
meeting notes.txt
notes.txt
```

Also exercise an empty directory, run the solution twice to check stable output, and compare source names and contents before and after. Verification should assess the objective rather than require the learner to copy the worked solution. Choose simpler checks when the context calls for them; report which checks were actually performed.

Offer an explanation prompt about why a whitespace-splitting approach could fail. At completion, accept the learner's explicit confirmation that they can handle the capability without guidance and record it with available observations. Running this pilot as an author check does not establish a learner's competence.
