# Small-Task Fast Path

Canonical rules for compact execution when the task is genuinely small and low-risk.
Use this file to reduce ceremony **without** sacrificing safety or resumability.

---

## Eligibility

A task may use the fast path only if **all** are true:
- scope is narrow
- expected touch set is small (typically 1–2 files)
- risk is LOW
- no schema or migration changes
- no public API contract changes
- no security-sensitive auth/permission changes
- no multi-step rollout or deploy coordination needed
- success criteria are obvious

If any of these are false, do not use the fast path.

---

## Fast path behavior

Fast path still requires:
- durable state persistence to `tasks/state.json`
- human summary persistence to `tasks/todo.md`
- at least one explicit approval checkpoint before code changes
- verification before PR/commit

What gets shorter:
- clarification may be skipped with a recorded reason
- plan can be compact
- output can summarize instead of expanding every obvious subtask

---

## Compact plan contract

A fast-path plan should still include:
- task summary
- files expected to change
- risk: LOW
- confidence
- blast radius
- rollback complexity
- done criteria

Example:

```text
FAST PATH PLAN
- Task: adjust review preset wording
- Files: references/modes/review.md, tests/test_smoke.py
- Risk: LOW
- Confidence: HIGH
- Blast Radius: narrow
- Rollback: easy
- Done when: docs updated and pytest passes
```

---

## Exit rule

If the task grows during implementation, immediately exit fast path and continue with the full workflow.
Record in state that fast path was abandoned and why.
