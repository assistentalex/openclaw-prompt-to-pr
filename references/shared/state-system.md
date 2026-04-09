# Durable State System

Canonical rules for saving, restoring, and resuming prompt-to-pr workflows.
Use this file as the source of truth whenever the workflow must survive disconnects,
`/new`, model switches, crashes, or user interruptions.

---

## Core rule

**Never rely on chat history alone.**
Every important workflow transition must be persisted to disk.

Use two files together:
- `tasks/state.json` → machine-readable canonical state
- `tasks/todo.md` → human-readable summary and journal

`tasks/state.json` is the primary source of truth for resume.
`tasks/todo.md` is the human summary and audit trail.

---

## Required state fields

```json
{
  "version": 2,
  "mode": "feature|fix|review|refactor|test|docs|pr-feedback",
  "repo": "/abs/path",
  "branch": "feat/example",
  "phase": {
    "shared": "preflight|context-scan|triage|done",
    "mode": "clarify|plan|implement|test|verify|pr|report|done",
    "step": "short-human-label"
  },
  "task": "one-line user request",
  "status": "active|waiting-approval|interrupted|completed|aborted",
  "approvals": {
    "checkpoint1": false,
    "checkpoint2": false
  },
  "clarify": {
    "questionsAsked": [],
    "answers": [],
    "assumptions": [],
    "openQuestions": []
  },
  "plan": {
    "summary": "",
    "tasks": [],
    "risk": "low|medium|high",
    "confidence": "high|medium|low",
    "blastRadius": "narrow|moderate|broad",
    "rollback": "easy|moderate|hard"
  },
  "files": {
    "touched": [],
    "planned": []
  },
  "tests": {
    "baseline": "",
    "latest": "",
    "coverage": ""
  },
  "verify": {
    "summary": "",
    "readyForPr": false
  },
  "nextAction": "",
  "updatedAt": "ISO-8601"
}
```

---

## Persistence checkpoints

Write both `tasks/state.json` and `tasks/todo.md` after every major transition:
- after CLARIFY
- after PLAN
- after each IMPLEMENT task
- after TEST
- after VERIFY
- when waiting for approval
- when interrupted / aborted
- when completed

If the workflow is long-running, save after any meaningful decision, not just after edits.

---

## Resume contract

When the user says `resume`, `continuă`, or `reia`:
1. Read `tasks/state.json` first
2. Read `tasks/todo.md` second
3. Resume from `nextAction`
4. Do not reconstruct state from memory if the file exists

If `tasks/state.json` is missing but `tasks/todo.md` exists:
- warn that resume is degraded
- use `todo.md` as fallback

If both are missing:
- say no resumable state exists

---

## Safety rules

- Never mark approval checkpoints as passed unless the user explicitly approved in chat
- Never mark verify ready unless verify actually completed
- Never clear `openQuestions` unless they were answered or explicitly waived
- Never overwrite the entire state with a partial update that drops fields silently

---

## Batch implementation rule

For large features, implement in resumable batches.
Each batch must leave the skill in a valid, testable state.
