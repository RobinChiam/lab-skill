# Teaching workspace and handoff

Read this when creating, resuming, or reporting a lab. Paths below are relative to the learner's teaching workspace, not the installed skill package.

## Layout

Create only materials needed for the selected exercise. A typical lab uses:

```text
labs/
  0001-file-processing/
    BRIEF.md
    worked-example/
    challenge/
    logs/checks/
    REPORT.md
learning-records/
```

`worked-example/` contains the explained solution and supporting fixtures. `challenge/` contains the learner's brief, starter materials, and work. Put shared fixtures or verification helpers inside the lab directory when useful. Markdown is sufficient for v1; use another presentation format only when it helps the task.

Choose the next unused number from existing lab directories when creating a lab. Resume an existing lab when requested or clearly active; do not silently replace its files. For a new attempt, use a fresh subdirectory or preserve prior work before changing it. Describe reset steps that operate on generated disposable data and retain learner edits unless the learner requests otherwise.

## Brief

Keep `BRIEF.md` concise, covering:

- Capability and connection to the teaching mission.
- Relevant Bloom's processes and established prerequisites.
- Available environment and assumptions.
- Links to the worked example and challenge.
- Expected results, how to check them, and how to reset disposable fixtures.
- The logging-enabled check command and where to find timestamped run output.
- Relevant sources when needed.

The model chooses practical complexity and support from current teaching context. Do not infer a universal learner level from a Bloom's label.

## Report

Create an initial report when presenting the lab and update it after feedback or at a pause. Use these headings as a small default, adding detail only when it changes future teaching:

```md
# Lab report: <capability>

## Current state
In progress, learner-confirmed independent application, or environment blocked.
Describe the point to resume from when unfinished.

## Work and verification
Link the brief and relevant learner artifacts. State checks actually performed,
their results, and any unavailable verification. Distinguish agent observations
from learner reports. Link relevant check logs and summarise repeated failures,
resolved criteria, and remaining issues; distinguish learner runs from agent runs.

## Learner confirmation and reasoning
Record the learner's independence statement, or say it has not been provided.
Capture relevant explanations, known misconceptions, and assistance when known.
If reasoning was not observed, say so.

## Handoff to /teach
Summarise what this establishes and recommend a next activity when useful.
Link a learning record if one was written. Leave advancement to /teach.
```

Do not require attachments or diagnostic proof when the learner confirms capability without submitting artifacts. Accept the confirmation and clearly report the limits of observed evidence. Do not infer competence in adjacent capabilities or every Bloom's process.

## Learning decision record

Read existing teaching records before adding one. Reuse the local convention; if no records exist, create `learning-records/` lazily and use `0001-<capability>.md` with a title and a short paragraph. An example:

> The learner confirmed they can process files with spaces in their names without guidance after the file-processing lab. The observed manifest checks passed; reasoning about argument handling was discussed. See the lab report for the task and verification. `/teach` can use this when selecting the next exercise.

Adapt claims to the actual session. A confirmation without inspected work should explicitly be described as learner-reported. When useful, include significant check-history findings with links to the relevant runs, distinguishing observed failing criteria from inferred misconceptions. Before appending, check whether the capability and the same lab result are already recorded; do not duplicate the record during a resumed handoff. Link the record from the report so subsequent invocations can find it.

In-progress reports preserve session state. Learning records preserve significant learning decisions; they are not an automatic activity log for every attempt.
