# Mode: 🚀 New Feature

**Flow:** Prompt → Context → Plan → ⛔ APPROVE → Implement → Test → Verify → ⛔ APPROVE → PR

**Phase banner mandatory:** Display `[FAZA N/M — ...]` banner as the FIRST action of every phase. See ⛔ MANDATORY in SKILL.md.

Load this file after PREFLIGHT and CONTEXT SCAN are complete.

---

## Phase 2 — PLAN

Load `references/shared/plan-format.md` for the todo.md structure.

### What to include in the plan

1. Break the feature into the smallest independent tasks possible
2. Order tasks by dependency (what must exist before what)
3. Identify which files are created vs modified
4. Estimate risk per task (LOW / MEDIUM / HIGH)
5. Define what "done" looks like for each task

### Plan presentation format

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🚀 NEW FEATURE PLAN — Email Verification
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  TASK 1 — Add email service function         LOW
  File: src/services/email.service.ts (new)
  What: Create sendVerificationEmail(userId, email)
  Est: ~30 lines

  TASK 2 — Extend user service               MEDIUM
  File: src/services/user.service.ts (modify)
  What: Call email service after registerUser()
  Est: ~15 lines

  TASK 3 — Add verification route             LOW
  File: src/routes/auth.routes.ts (modify)
  What: GET /verify-email?token={token}
  Est: ~20 lines

  TASK 4 — Schema migration                  HIGH ⚠️
  File: prisma/schema.prisma (modify)
  What: Add emailVerified Boolean, verificationToken String?
  Note: Requires prisma migrate dev

  Tests to write: 3 new tests in tests/auth/

  Branch: feat/email-verification
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ⛔ CHECKPOINT 1 — Approve to start coding?
  Reply: yes / modify / abort
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Wait for explicit approval before proceeding.**

---

## Phase 3 — IMPLEMENT

Execute tasks in order. For each task:

1. State what you're about to do:
   `→ Starting Task 2: extending user.service.ts`

2. Write the code

3. Apply hardshell rules if installed:
   - No secrets in code
   - Input validation at entry point
   - Single responsibility per function
   - Dependency injection for external services

4. After writing, show a brief summary:
   `✅ Task 2 done — added 3 lines in registerUser(), injected emailService`

5. Mark as complete in todo.md: `- [x] 2. Modify registerUser()...`

6. Check budget after each task. If > 80%, apply compression.

### For HIGH risk tasks
Display before executing:
```
⚠️ HIGH RISK — Task 4 involves a schema migration.
This will modify the database schema and require a migration file.
The change is: add emailVerified (Boolean, default false) to User.

Confirm: yes / skip / abort
```

### What NOT to do during implement
- Do not modify files outside the plan
- Do not refactor unrelated code you happen to notice (note it in Lessons Learned instead)
- Do not add speculative features ("while I'm here I'll also add...")
- Do not skip task summaries

---

## Phase 4 — TEST

### Step 1 — Run baseline (if not already done)
```bash
npm test   # or pytest / go test ./... / etc
```
Record: total tests, pass/fail before changes.

### Step 2 — Write new tests
For each new function or route added:
- Happy path test
- At least one edge case
- At least one error path

Place tests in the project's existing test directory following existing naming conventions.

### Step 3 — Run full suite
```bash
npm test
```

### Retry logic (max 2 automatic retries)
If tests fail:

**Retry 1:**
- Read the error message carefully
- Identify: is it a test issue or a code issue?
- Fix the root cause (not just the test)
- Run again

**Retry 2:**
- Same process
- If still failing after 2 retries → STOP

```
🔴 TEST FAILURE — 2 retries exhausted

Failing test: "should send verification email on register"
Error: Cannot read property 'sendVerificationEmail' of undefined

I was unable to fix this automatically. 
What would you like to do?
  [1] Show me the failing code and I'll fix it
  [2] Skip this test for now and continue
  [3] Abort
```

### Coverage (if tool available)
```bash
npm test -- --coverage   # jest
pytest --cov             # pytest
go test ./... -cover     # go
```

Record coverage before and after. Note delta in todo.md.

---

## Phase 5 — VERIFY

Load checklist. If hardshell is installed, use hardshell §4.
If not, use this built-in checklist:

**Correctness**
- [ ] Feature does exactly what was requested
- [ ] Edge cases handled (empty input, null, unauthorized access)
- [ ] Error messages are user-friendly and don't leak internals

**Security**
- [ ] No secrets or tokens in code or comments
- [ ] Input validated at entry point
- [ ] Authorization checked (can only verified users access protected routes?)
- [ ] No SQL/NoSQL injection vectors

**Architecture**
- [ ] Layer boundaries respected (no business logic in routes)
- [ ] New service is injected, not instantiated inline
- [ ] No circular dependencies introduced

**Code quality**
- [ ] Function names reveal intent
- [ ] No function longer than ~25 lines without good reason
- [ ] No duplicate code
- [ ] No magic strings/numbers — use constants

**Tests**
- [ ] Happy path covered
- [ ] Edge cases covered
- [ ] Error paths covered
- [ ] All existing tests still pass

### Show diff summary
```bash
git diff main --stat
```

### Verify presentation
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ✅ VERIFY COMPLETE — 🚀 Email Verification
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Files changed: 4 (+127 lines, -3 lines)
  Tests: 50 passed, 0 failed (3 new)
  Coverage: 71% → 78%
  Checklist: all green
  hardshell: no issues flagged

  Changes:
  + src/services/email.service.ts       (new, 32 lines)
  ~ src/services/user.service.ts        (+15 lines)
  ~ src/routes/auth.routes.ts           (+22 lines)
  ~ prisma/schema.prisma                (+2 lines + migration)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ⛔ CHECKPOINT 2 — Approve to create PR?
  Reply: yes / request changes / abort
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Phase 6 — PR

Load `references/shared/pr-format.md`.

Execute git sequence:
1. `git checkout -b feat/{slug}`
2. `git add {only files from plan}`
3. `git diff --staged --stat` (show to user)
4. `git commit -m "feat({scope}): {description}"`
5. `git push origin feat/{slug}`
6. Create PR with generated body

Write Lessons Learned to todo.md:
- What went smoothly
- Any surprises encountered
- Any rules to add to CLAUDE.md

Display:
```
🎉 PR created: feat/email-verification
   Branch pushed, PR open for review.
   
   See: tasks/todo.md for full session log.
```
