# Context Compression

After each phase completes, apply these compression rules before moving to the next phase.
Goal: free up context space by replacing raw content with structured summaries.

**Write summaries to `tasks/todo.md` before dropping the raw content.**

---

## After PREFLIGHT

DROP:
- Command outputs from checks
- Full file listings

KEEP (write to todo.md):
- Preflight status (pass/fail per check)
- Detected: language, test suite, coverage tool, hardshell present/absent

---

## After CONTEXT SCAN

DROP:
- Raw file contents of Tier 2 and Tier 3 files
- Full grep outputs
- Directory listings

KEEP (write to todo.md):
- Context summary block (as defined in context-scan.md Step 5)
- List of Tier 1 files with their purpose (these stay in context for IMPLEMENT)
- List of Tier 2/3 files (path only, purpose in one line)

Rule: Tier 1 file contents stay in context through IMPLEMENT, then drop after.

---

## After PLAN

DROP:
- Intermediate thinking / alternative plans considered
- Full conversation turns during plan refinement

KEEP (in todo.md, already written there):
- Final approved plan with numbered tasks
- Risk notes per task

---

## After IMPLEMENT (each task)

DROP after each task completes:
- Intermediate code versions / failed attempts
- Compiler/linter output if successful (keep only if it had meaningful warnings)

KEEP:
- Final code (stays in context until VERIFY)
- One-line summary of what each task changed

KEEP in todo.md:
```markdown
## Completed Tasks
- [x] Task 1 — added `verifyEmail()` to user.service.ts
- [x] Task 2 — added `/verify-email` route to auth.routes.ts
- [ ] Task 3 — send verification email on register
```

---

## After all IMPLEMENT tasks done

DROP:
- Tier 1 file contents as they were *before* changes (originals)
- The plan details (already in todo.md)

KEEP:
- Final versions of modified files (for VERIFY diff)
- List of all files touched

---

## After TEST

DROP:
- Full test runner output (can be hundreds of lines)
- Passing test details

KEEP:
- Final test result: total passed / failed / skipped
- If any failures: only the failing test name + error message (not full stack)
- New tests written: file paths only

KEEP in todo.md:
```markdown
## Test Results
- Suite: Jest
- Run: 47 passed, 0 failed (3 new tests added)
- Coverage delta: 71% → 78%
```

---

## After VERIFY

DROP:
- Full diff output
- Checklist working notes

KEEP:
- Verify summary: what was checked, what passed, any flagged issues
- Final list of files changed (for PR body)

KEEP in todo.md:
```markdown
## Verify Summary
- Files changed: 3
- Tests: 47 passed
- Checklist: all green
- hardshell: no issues flagged
- Ready for merge: YES
```

---

## Emergency Compression (triggered at 80%+ context)

Apply immediately when entering Orange Zone with a medium/large next step, or any time the current phase is TEST and pressure is orange or higher.

1. Summarize ALL previous phase content to 3 bullet points per phase
2. Drop all code snippets from context EXCEPT currently active file
3. Replace todo.md content in context with: "See tasks/todo.md for full plan"
4. Keep only: active task, current file, test results summary

After emergency compression, display:
```
🟠 Emergency compression applied. Detailed history moved to tasks/todo.md.
Continuing with minimal context. Next-step size will be re-evaluated before the next major action.
```
