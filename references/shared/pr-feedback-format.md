# PR Feedback Format

Canonical formatting rules for collecting, triaging, planning, and summarizing PR feedback.

---

## Triage buckets

Every feedback item must land in exactly one bucket:
- MUST-FIX
- OPTIONAL
- UNCLEAR

Do not skip the triage step.
Do not mix unresolved ambiguity into MUST-FIX silently.

---

## Item format

```text
[F1] MUST-FIX
Source: PR review by @reviewer
Path: src/services/auth.service.ts
Summary: Missing error-path handling for expired tokens
Action: add expired-token branch + regression test
```

Fields:
- ID
- bucket
- source
- path (if known)
- summary
- proposed action

---

## Plan summary format

Use this structure in chat and in `tasks/todo.md`:

```text
PR FEEDBACK PLAN
- Must-fix now: N
- Optional: N
- Unclear: N
- Files: ...
- Tests: ...
- Risk: ...
- Confidence: ...
- Blast Radius: ...
- Rollback: ...
```

---

## Completion summary format

```text
PR FEEDBACK SUMMARY
- Fixed now: ...
- Deferred: ...
- Still unclear: ...
- Tests run: ...
- Suggested PR response: ...
```

Persist both the triage output and completion summary in durable state.
