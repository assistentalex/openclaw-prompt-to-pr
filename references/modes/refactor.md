# Mode: ♻️ Refactor

**Flow:** Baseline tests → Analyze → Plan → ⛔ APPROVE → Implement → Tests must match baseline → ⛔ APPROVE → PR

**Phase banner mandatory:** Display `[FAZA N/M — ...]` banner at the start of EVERY assistant turn during the workflow — not just at phase starts. See ⛔ MANDATORY in SKILL.md.

Core constraint: **zero behavior change**.
The test suite is the safety net. If any test breaks, the refactor is wrong — not the test.

---

## Phase 1 — BASELINE

Before touching a single line of code, capture the current state.

### Run full test suite
```bash
npm test        # or pytest / go test ./... / cargo test
```

Record exactly:
- Total tests: N
- Passing: N
- Failing: N (pre-existing failures — note them, do not fix them now)
- Skipped: N

Save to todo.md:
```markdown
## Refactor Baseline
- Tests before: 47 passed, 0 failed, 2 skipped
- Pre-existing failures: none
- Date: {timestamp}
```

**If there are pre-existing failures:**
```
⚠️ {N} tests are already failing before refactoring starts.

I will NOT fix these. They are pre-existing and out of scope.
After refactoring, exactly the same tests should fail — no more, no less.

Noted failures:
  - {test name}: {reason}

Continuing with refactor.
```

---

## Phase 2 — ANALYZE

Identify what to refactor and why. Common targets:

| Code smell | Refactor technique |
|---|---|
| Function does too many things | Extract function |
| Duplicate logic in multiple places | Extract and centralize |
| Deep nesting (3+ levels) | Early return / guard clauses |
| Large file with mixed concerns | Split into modules |
| Hard-to-read conditional | Named variable or extract method |
| Primitive obsession | Value object / type |
| Long parameter list | Options object |
| Magic numbers/strings | Named constants |
| Commented-out code | Delete it |

### Analysis report (show to user before plan)
```
REFACTOR ANALYSIS — src/services/user.service.ts

Issues found:
  - processUser() is 187 lines — does validation, DB write, email, logging
  - Email validation duplicated in 3 places (lines 23, 67, 134)
  - Magic string "admin" appears 7 times without constant
  - 4 levels of nesting in handleRegistration()
  - Dead code: processLegacyUser() never called (line 89–120)

Recommended techniques:
  - Extract: validateEmail(), createUser(), sendWelcomeEmail()  
  - Centralize: isValidEmail() used everywhere
  - Constant: USER_ROLES.ADMIN = "admin"
  - Guard clauses: flatten handleRegistration() nesting
  - Delete: remove processLegacyUser()
```

---

## Phase 3 — PLAN

Load `references/shared/plan-format.md`.

Critical rule for refactor plans: **one behavior-preserving transformation per task**.
Do not bundle multiple techniques into one task — it makes failures hard to debug.

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ♻️ REFACTOR PLAN — user.service.ts cleanup
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  BASELINE: 47 tests passing ← must match after refactor

  TASK 1 — Extract validateEmail() helper         LOW
  Technique: Extract function
  Where: Move duplicated validation to shared utils
  Behavior change: NONE — same logic, different location

  TASK 2 — Add USER_ROLES constant                LOW
  Technique: Named constant
  Where: src/constants/roles.ts (new file)
  Behavior change: NONE — string value identical

  TASK 3 — Flatten handleRegistration() nesting   MEDIUM
  Technique: Guard clauses / early return
  Where: src/services/user.service.ts:45–89
  Behavior change: NONE — same conditions, different structure

  TASK 4 — Split processUser() into 3 functions   MEDIUM
  Technique: Extract function
  Where: src/services/user.service.ts:100–187
  Creates: createUser(), sendWelcomeEmail(), logRegistration()
  Behavior change: NONE — same calls, same order

  TASK 5 — Delete processLegacyUser()             LOW
  Technique: Dead code removal
  Verification: grep confirms no callers exist
  Behavior change: NONE — unreachable code

  Branch: refactor/user-service-cleanup
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ⛔ CHECKPOINT 1 — Approve refactor plan?
  Reply: yes / modify / abort
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Phase 4 — IMPLEMENT

Execute one task at a time. After EACH task:

```bash
npm test
```

If tests still pass → continue to next task.
If tests fail → **stop immediately**.

```
🔴 REFACTOR VIOLATION — Task 3 broke a test

Failed test: "handleRegistration should reject duplicate email"
This means the refactoring changed behavior.

I am reverting Task 3 changes.
Would you like me to:
  [1] Try a different approach for this specific task
  [2] Skip this task and continue with Task 4
  [3] Abort and return to the last clean state
```

**Never continue with a failing test during refactor.** Revert before proceeding.

### Dead code removal — extra verification
Before deleting any function/class:
```bash
grep -r "processLegacyUser" --include="*.ts" .
```
Confirm zero references outside the function definition itself.

---

## Phase 5 — VERIFY — Behavior Unchanged

### Run final test suite
```bash
npm test
```

Compare to baseline:
- Same total: ✅
- Same passing: ✅
- Same failing (pre-existing only): ✅
- Same skipped: ✅

**If any number differs → the refactor changed behavior. Do not proceed to PR.**

### Show before/after metrics
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ✅ REFACTOR VERIFIED — ♻️ user.service.ts
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Tests:     47 → 47 ✅ (unchanged)
  Passing:   47 → 47 ✅
  Failing:    0 →  0 ✅
  
  Code metrics (before → after):
  Lines in processUser():  187 → split into 3 functions (avg 45 lines)
  Duplication: 3 copies validateEmail() → 1 shared util
  Magic strings: 7 → 0 (extracted to USER_ROLES constant)
  Max nesting depth: 4 → 2
  Dead code removed: 31 lines

  Behavior change: NONE ✅
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ⛔ CHECKPOINT 2 — Approve PR?
  Reply: yes / request changes / abort
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Phase 6 — PR

Load `references/shared/pr-format.md`.
Use `refactor/` prefix for branch.
Include "Behavior Unchanged" section in PR body.

Commit format: `refactor(user): extract helpers, remove duplication`
