# Mode: 🔍 Code Review

**Flow:** Clarify → Define scope → Analyze → Structured report

Load `references/shared/clarify.md` for clarification rules.
Load `references/shared/state-system.md` for durable save/resume behavior.
Load `references/shared/review-presets.md` for canonical scope presets.
**Phase numbering note:** phase numbers below are local to the mode workflow and begin after the shared PREFLIGHT and CONTEXT SCAN steps.

**This mode is READ-ONLY. No code is modified. No commits. No PR.**
**Preflight note:** missing tests are a warning in this mode, not a blocker. Continue the review, but flag the absence of tests as process risk when relevant.

Output: a structured review report saved locally to `.openclaw/reviews/review-{YYYY-MM-DD}.md`

---

## Phase 1 — CLARIFY

Ask targeted clarification questions only when needed.
Clarify review target, desired depth, and whether the user wants security, architecture, testing, or general review emphasis.
Persist clarify summary to `tasks/state.json` and `tasks/todo.md` before defining scope.

## Phase 2 — DEFINE SCOPE

Ask if not specified, using the review presets:
```
What should I review?

  [1] Diff since main
  [2] Changed files only
  [3] Specific path
  [4] PR or commit range
  [5] Security boundaries
  [6] Test gaps
  [7] Architecture smells
```

Persist the selected preset to `tasks/state.json` and summarize it in `tasks/todo.md`.

If scope is too large for context budget:
```
⚠️ The selected scope contains ~{N}k tokens, which exceeds the review budget.

I'll review the most critical areas first:
  - Files changed most recently (git log)
  - Files with the highest complexity indicators
  - Entry points and security boundaries

Alternatively, specify a narrower scope.
```

---

## Phase 3 — ANALYZE

Read files using the selective strategy from `references/shared/context-scan.md`.

For each file, check all of the following:

### Security checks
- [ ] Input validation present at entry points
- [ ] No secrets, tokens, or credentials in code
- [ ] Queries parameterized (no string interpolation in SQL/NoSQL)
- [ ] Authorization verified before performing actions
- [ ] User input cannot reach: file paths, shell commands, eval(), deserialization
- [ ] API endpoints rate-limited where appropriate
- [ ] Sensitive data not logged

### Architecture checks
- [ ] Layer boundaries respected (no business logic in routes/controllers)
- [ ] Dependencies point inward (outer depends on inner, not reverse)
- [ ] No circular dependencies
- [ ] Public interfaces are minimal and clean
- [ ] External services wrapped behind interfaces (swappable)

### Code quality checks
- [ ] Function names reveal intent
- [ ] Functions have single responsibility (< ~25 lines)
- [ ] No duplicate logic
- [ ] No magic numbers or unexplained strings
- [ ] Error handling present — no silent catches
- [ ] Comments explain *why*, not *what*

### Testing checks
- [ ] Test coverage exists for modified/new code
- [ ] Tests cover edge cases, not just happy paths
- [ ] Tests are isolated (no order dependency)

---

## Phase 4 — STRUCTURED REPORT

Save locally to `.openclaw/reviews/review-{YYYY-MM-DD}.md`

```markdown
# Code Review — {scope description}
**Date:** {YYYY-MM-DD}
**Reviewer:** prompt-to-pr (AI)
**Files reviewed:** {N}
**hardshell applied:** yes/no

---

## Summary

{2–4 sentences: overall quality, biggest strengths, biggest concerns}

---

## Issues Found

### 🔴 SECURITY — {count} issue(s)

#### [S1] SQL injection risk in user search
**File:** src/repositories/user.repository.ts:34
**Severity:** CRITICAL
**Problem:** User input concatenated directly into query string.
**Current code:**
```
const query = `SELECT * FROM users WHERE name = '${name}'`
```
**Fix:**
```
const query = `SELECT * FROM users WHERE name = $1`
db.query(query, [name])
```

---

### 🟡 ARCHITECTURE — {count} issue(s)

#### [A1] Business logic in route handler
**File:** src/routes/user.routes.ts:67–89
**Severity:** MEDIUM
**Problem:** Password hashing and email validation happen directly in the route handler.
**Pattern violated:** Separation of Concerns
**Recommendation:** Extract to UserService. Route should only handle request/response.

---

### 🔵 CLEAN CODE — {count} issue(s)

#### [C1] Function does more than one thing
**File:** src/services/user.service.ts:112
**Severity:** LOW
**Problem:** `processUserRegistration()` handles validation, DB insert, email send, and logging.
**Recommendation:** Split into: `validateRegistrationData()`, `createUser()`, `sendWelcomeEmail()`

---

### 🟠 PROCESS — {count} issue(s)

#### [P1] Missing tests for error paths
**File:** tests/auth/register.test.ts
**Severity:** MEDIUM
**Problem:** Only happy path is tested. No tests for: duplicate email, invalid input, DB failure.
**Recommendation:** Add at minimum 3 edge case tests.

---

## Positives

- {what's done well — be specific, not just "good code"}
- Input validation is consistent across all route handlers
- Error middleware correctly separates operational vs programmer errors

---

## Priority Order for Fixes

1. 🔴 [S1] SQL injection — fix immediately, security critical
2. 🟠 [P1] Missing tests — before next deploy
3. 🟡 [A1] Business logic in routes — next refactor cycle
4. 🔵 [C1] Function decomposition — low priority, technical debt

---

## Metrics

| Category | Issues | Critical | Medium | Low |
|---|---|---|---|---|
| Security | {N} | {N} | {N} | {N} |
| Architecture | {N} | {N} | {N} | {N} |
| Clean Code | {N} | {N} | {N} | {N} |
| Process | {N} | {N} | {N} | {N} |
| **Total** | **{N}** | **{N}** | **{N}** | **{N}** |
```

---

## After the report

Display summary in chat:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🔍 CODE REVIEW COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Files reviewed: 8
  Issues found: 12 (1 critical, 4 medium, 7 low)

  🔴 SECURITY:     1 critical (SQL injection)
  🟡 ARCHITECTURE: 3 issues
  🔵 CLEAN CODE:   5 issues
  🟠 PROCESS:      3 issues

  Full local report: .openclaw/reviews/review-2025-04-09.md

  Next steps:
  → Fix [S1] SQL injection now
  → Run prompt-to-pr in 🐛 Bug Fix or ♻️ Refactor mode
    to address the remaining issues
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

No checkpoints in this mode — the report itself is the output.
The user decides what to do with it.
