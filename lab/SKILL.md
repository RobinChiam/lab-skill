---
name: lab
description: Create and guide practical software or technical labs with a worked example and a related learner challenge, alongside an existing teaching workspace or a supplied learning objective. Use for hands-on learning and lab feedback, rather than ordinary implementation requests or whole-course planning.
metadata:
  version: "0.0.2"
---

# Lab

Help the learner apply a concept through a solved example and a related unsolved challenge. Work alongside `/teach`: it owns the mission, starting-level assessment, learning path, and advancement decisions. This skill owns practical lab creation, guidance, and a report that the teaching session can use.

## Establish context

Use the current teaching session and its workspace. Read its `MISSION.md`, relevant `learning-records/`, `NOTES.md`, and applicable `RESOURCES.md` entries when present. Also read the relevant existing `labs/` brief, report, and check-run logs when resuming. Resolve the teaching workspace from session context or an explicit path; ask only if multiple plausible workspaces remain. Do not treat this skill's development notes as a learner's teaching mission.

Carry forward the target capability, established prerequisites, suitable challenge level, environment constraints, and success criteria. Starting-level assessment belongs to `/teach`; do not administer a second placement assessment. If context is incomplete, use a reasonable, stated assumption for a low-impact choice and ask only for information necessary to create a relevant lab. A supplied objective is enough to create a standalone lab; return a handoff report even if `/teach` is unavailable.

Read [workspace.md](references/workspace.md) when creating, resuming, or reporting a lab. Keep generated lab materials under the teaching workspace's `labs/` directory unless the user specifies another destination.

## Design the practical work

- Select one manageable capability aligned with the mission. Use revised Bloom's **Apply, Analyze, Evaluate, and Create** to describe the relevant practical objectives. Choose the processes the capability needs; neither every process nor a fixed order is required.
- Use `/teach`'s account of the learner's Zone of Proximal Development to choose complexity and support. Adapt to the learner's questions and attempts. If a missing prerequisite emerges, report it to `/teach` and offer a smaller exercise or explanation. Do not redefine the mission or impose a new course sequence.
- Produce a worked example and a related challenge in distinct locations. Explain the example's important decisions, expected behaviour, and verification. Change meaningful details in the challenge while preserving the principle being practised; provide an objective and observable success criteria without supplying the completed answer initially.
- References, solved examples, hints, documentation, and AI help are unrestricted. Keep the worked example accessible. Separate materials for clarity, not secrecy. Provide a full solution if requested and preserve the learner's opportunity to try another task.
- Decide the appropriate lifecycle and verification for the task. Default to small local files and code exercises in a disposable lab area. Choose fixtures, checks, rubrics, setup, and reset instructions proportional to the objective. Check the proposed exercise when feasible; state exactly what was checked and what remains unverified. If the environment is unavailable, explain the limitation and offer an appropriate alternative.
- Use available trusted resources and the workspace's documentation lookup conventions for unfamiliar or version-dependent facts. Keep references close to the decisions they support.

## Log every check run

Read [check-logging.md](references/check-logging.md) when creating or updating a check script. Every learner-facing check command must record its own run automatically, including runs outside the chat. Use the bundled runner or equivalent instrumentation to save UTC timestamps, complete stdout and stderr output, and the check's exit code under the lab's `logs/checks/`. Keep one separate record per invocation, including failed and silent runs. Preserve the history during retries and fixture resets.

Provide one documented check entry point that routes all supported verification commands through logging. Mark agent-authored validation runs as `agent` so they are distinguishable from learner attempts. When updating an existing lab, retain its checks and learner files, adding logging to its public check entry points. Do not fabricate historical logs for earlier runs; describe a gap if earlier output is unavailable.

Before feedback or handoff, inspect the check history alongside the learner's work. Identify repeated failing criteria, changes between attempts, and issues that were resolved. Separate script or environment failures from evidence about the target capability. Logs show observed results, not the learner's reasoning, assistance, or a precise ZPD measurement; establish those from the teaching conversation when available.

For a first lab without a more relevant objective, consider the optional [file-processing pilot](references/first-pilot.md). It is a starting example, not a prerequisite or fixed curriculum. Choose another pilot when the mission calls for it.

## Guide the learner

Present the objective, entry points, and how to attempt and check the challenge. Let the learner drive the attempt. Explain, give hints, or demonstrate as requested; avoid completing the challenge unasked. Additional completion exercises, transfer tasks, or later review may be offered when useful, but are not mandatory gates.

Use feedback appropriate to the task: code or output checks for observable behaviour, explanation and tradeoff discussion for reasoning. Accept valid alternative approaches. Treat setup failures as environment issues, and preserve existing learner work during retries or repairs.

Trust the learner's restraint and account of their work. Do not introduce proctoring, cheating detection, closed-book conditions, mandatory timers, or mastery scores. Assistance can be noted when volunteered or directly observed; do not require an assistance questionnaire.

**Success is learner-confirmed independent application.** When the learner indicates completion, use their explicit statement that they can now handle this capability without guidance. If that statement is missing, ask a brief, neutral confirmation question. Referencing a worked example during practice does not disqualify later confirmation. Do not require an additional unaided exam or delay before accepting it. Completion of teaching materials or successful checks alone does not supply this confirmation.

## Report and resume

Write a concise `REPORT.md` containing the exercise, submission or artifact links, verification results, learner confirmation, observed reasoning, remaining misconceptions, and a suggested next activity. Link relevant check-run logs and summarise the failure-to-success history, unresolved criteria, and useful support observed. Distinguish learner-reported capability from checks actually performed. Report only what is available; mark unobserved reasoning or unknown details as such.

Use `/teach`'s learning decision records as the durable progress store. Follow the existing format and numbering. After an explicit independence confirmation, append a concise learning record identifying the capability, the learner's confirmation, relevant observed results, and the lab report. Also record a significant established misconception if useful to future teaching. Use significant patterns in the check history to inform these records and recommendations for ZPD-appropriate support; retain raw runs in the lab rather than creating a learning record for every failure. Do not create a competing progress ledger, rewrite the path, or declare that the learner passed an unseen `/teach` assessment.

Keep an in-progress report when the learner pauses so the next invocation can read the current teaching context and lab files together. At handoff, tell the model to consult the report alongside `/teach`'s learning records. `/teach` makes advancement and review decisions. A file-based handoff does not automatically modify or invoke another skill; make the report location explicit in the conversation.
