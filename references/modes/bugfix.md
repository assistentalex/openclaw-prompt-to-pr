# Mode: 🐛 Bug Fix

**Flow:** Clarify → Reproduce → Root Cause → Fix Plan → ⛔ APPROVE → Implement Fix → Verify Fix + Regression → ⛔ APPROVE → PR

Load `references/shared/clarify.md` for clarification rules.
Load `references/shared/state-system.md` for durable save/resume behavior.
**Phase numbering note:** phase numbers below are local to the mode workflow and begin after the shared PREFLIGHT and CONTEXT SCAN steps.

Key principle: **never propose a fix before reproducing the bug.**
A fix without reproduction is a guess, not a fix.

---

## Phase 1 — CLARIFY

Ask targeted clarification questions only when needed.
Bug reports often need clarification about exact error, environment, repro steps, and expected behavior.
Persist clarify summary to `tasks/state.json` and `tasks/todo.md` before reproduction.

## Phase 2 — REPRODUCE

### Gather information first
If not already provided by the user, ask:
```
To find and fix this bug, I need a few details:

1. What's the exact error message or unexpected behavior?
2. How do I reproduce it? (steps, input, environment)
3. What's the expected behavior?
4. When did it start? (after a specific commit / always / intermittent)
```

### Attempt to reproduce
```bash
# Run the test that exercises the broken path
npm test -- --testNamePattern="relevant test"

# Or run the application and trigger the bug
npm run dev  # then reproduce manually
```

### If cannot reproduce → STOP
```
🔴 CANNOT REPRODUCE — Bug Fix stopped

I ran the following steps and could not reproduce the reported behavior:
  1. {step}
  2. {step}

Without reproduction, any fix would be a guess.

Options:
  [1] Provide more details about how to reproduce
  [2] Share the exact error log or stack trace
  [3] Identify the commit that introduced this bug (git bisect)
```

### If reproduced → document
Record reproduction evidence in durable state and summarize:
- exact trigger
- expected vs actual behavior
- stack/error evidence
- whether a regression test is planned

```
✅ BUG REPRODUCED

Trigger: POST /api/auth/register with duplicate email
Error: UnhandledPromiseRejection — Unique constraint failed on field: email
Stack: src/services/user.service.ts:47
Frequency: 100% reproducible
```

---

## Phase 3 — ROOT CAUSE ANALYSIS

Do not jump to the fix. Trace the bug to its origin.

1. Read the stack trace top-to-bottom
2. Identify the exact line where the error originates
3. Trace backwards: what called this? what data was passed?
4. Ask: is this a symptom or the root cause?

Common root cause patterns to check:
- Missing null/undefined check
- Race condition (async code not awaited properly)
- Wrong error not caught at boundary
- Incorrect assumption about data shape
- Dependency version incompatibility
- Missing environment variable / config

### Root cause report
```
ROOT CAUSE IDENTIFIED

Location: src/services/user.service.ts line 47
Cause: Prisma unique constraint error is not caught — bubbles up as
       UnhandledPromiseRejection instead of returning a 409 response.

This is the ROOT CAUSE (not a symptom): the error handling layer
does not handle database constraint violations specifically.

Fix scope: 1 file, ~10 lines
Risk: LOW — additive error handling, no logic change
```

---

## Phase 4 — FIX PLAN

Load `references/shared/plan-format.md`.

Keep the fix minimal — the principle of least change.
Include plan metadata: Overall Risk, Confidence, Blast Radius, Rollback, Unknowns, and whether fast path is allowed.


```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🐛 BUG FIX PLAN — Duplicate email crash
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ROOT CAUSE: Unhandled Prisma P2002 (unique constraint)
  in user.service.ts registerUser()

  TASK 1 — Catch constraint error in registerUser()    LOW
  File: src/services/user.service.ts (modify)
  What: Wrap Prisma call, catch P2002, throw ConflictError
  Est: ~12 lines

  TASK 2 — Add ConflictError handler to error middleware  LOW
  File: src/middleware/error.middleware.ts (modify)
  What: Return 409 with "Email already in use" message
  Est: ~8 lines

  TASK 3 — Add regression test                          LOW
  File: tests/auth/register.test.ts (modify)
  What: Test that duplicate email returns 409 (not 500)
  Est: ~15 lines

  Branch: fix/duplicate-email-crash
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ⛔ CHECKPOINT 1 — Approve fix plan?
  Reply: yes / modify / abort
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Phase 5 — IMPLEMENT FIX

Same rules as feature.md IMPLEMENT phase, plus:

- **Minimal change principle**: fix only what's broken, touch nothing else
- If you notice other bugs while fixing: note them in Lessons Learned, do NOT fix them now
- If the fix requires more changes than planned → stop and revise the plan with user

---

## Phase 6 — VERIFY FIX

### Step 1 — Reproduce the original bug again
Using the exact same reproduction steps from Phase 1.
Expected result: bug no longer occurs.

```bash
# Run the specific test case
npm test -- --testNamePattern="should return 409 for duplicate email"
```

If bug persists → the root cause identification was wrong. Go back to Phase 2.

### Step 2 — Run full test suite (regression check)
```bash
npm test
```

Check: did the fix break anything else?

### Step 3 — Retry logic
Same as feature mode: max 2 automatic retries on test failures.

### Release readiness
Load `references/shared/release-readiness.md` and include a short release-readiness summary after VERIFY.

### Verify presentation
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ✅ FIX VERIFIED — 🐛 Duplicate email crash
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Original bug: ✅ No longer reproducible
  Root cause addressed: ✅ P2002 caught and mapped to 409
  Regression tests: 47 passed, 0 failed (+1 new)
  Side effects: none detected

  Files changed:
  ~ src/services/user.service.ts       (+12 lines)
  ~ src/middleware/error.middleware.ts  (+8 lines)
  ~ tests/auth/register.test.ts        (+15 lines)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ⛔ CHECKPOINT 2 — Approve to create PR?
  Reply: yes / request changes / abort
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Phase 7 — PR

Load `references/shared/pr-format.md`.
Use `fix/` prefix for branch.
Include "Root Cause" section in PR body (see pr-format.md).

Commit format: `fix(auth): return 409 on duplicate email registration`
