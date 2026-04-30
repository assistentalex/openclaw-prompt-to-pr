# Mode: 🗨️ PR Feedback

**Flow:** Clarify → Collect feedback → Triage → Plan → ⛔ APPROVE → Apply fixes → Verify → ⛔ APPROVE → Update branch/PR summary

Load `references/shared/clarify.md` for clarification rules.
Load `references/shared/state-system.md` for durable save/resume behavior.
Load `references/shared/pr-feedback-format.md` for canonical feedback grouping and response format.
**Phase numbering note:** phase numbers below are local to the mode workflow and begin after the shared PREFLIGHT and CONTEXT SCAN steps.

Core principle: **do not treat all PR comments equally.**
Group feedback into must-fix, optional, and unclear before changing code.

---

## Phase 1 — CLARIFY

Ask targeted clarification questions only when needed.
Clarify which PR, branch, or review thread is in scope and whether the goal is full resolution or partial response.
Persist clarify summary to `tasks/state.json` and `tasks/todo.md` before collecting feedback.

## Phase 2 — COLLECT FEEDBACK

Collect review comments, requested changes, and unresolved discussion threads.
Normalize them into a single list of actionable items.

Capture for each item:
- source (PR comment, review, discussion)
- file/path if known
- author
- summary of the issue
- whether the request is explicit or inferred

If the feedback is incomplete or contradictory, flag the unclear items instead of guessing.

## Phase 3 — TRIAGE

Group feedback into:
- MUST-FIX
- OPTIONAL
- UNCLEAR / NEEDS USER DECISION

Example:

```text
PR FEEDBACK TRIAGE

MUST-FIX
- Add missing error-path tests for duplicate email flow
- Rename ambiguous helper in auth service

OPTIONAL
- Shorten one oversized function during follow-up cleanup

UNCLEAR
- Reviewer asked for "simpler architecture" but did not specify whether
  they want service extraction now or later
```

Persist triage results to `tasks/state.json` and summarize them in `tasks/todo.md`.

## Phase 4 — PLAN

Load `references/shared/pr-feedback-format.md`.
Load `references/shared/plan-format.md`.

Build a patch plan that includes:
- which feedback items will be addressed now
- which items are deferred
- which items require user clarification
- files to change
- tests to run or add
- risk / confidence / blast radius / rollback / unknowns

```text
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🗨️ PR FEEDBACK PLAN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  MUST-FIX NOW
  1. Add duplicate-email regression test
  2. Rename `doAuthThing()` to `validateSessionToken()`

  DEFER
  3. Optional refactor of auth controller nesting

  NEEDS DECISION
  4. "Simpler architecture" request is ambiguous

  Files: src/services/auth.service.ts, tests/auth/register.test.ts
  Risk: LOW
  Confidence: MEDIUM
  Blast Radius: narrow
  Rollback: easy
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ⛔ CHECKPOINT 1 — Approve PR feedback plan?
  Reply: yes / modify / abort
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Auto-approve mode
If `NIGHT_SHIFT_AUTO_APPROVE=1` is set in the environment, the agent **auto-approves** this checkpoint with a logged note instead of waiting for user input.

Behavior in auto-approve mode:
- Log: "Auto-approved (night shift mode) — proceeding with implementation"
- Continue immediately
- Stash before IMPLEMENT still runs normally
```

## Phase 5 — APPLY FIXES

Apply only the approved must-fix and explicitly approved optional items.
Do not silently include unrelated cleanup.
Persist progress after each meaningful fix.

## Phase 6 — VERIFY

Re-run the relevant tests and any targeted checks required by the feedback.
Confirm:
- each must-fix item is addressed
- no deferred item is falsely marked complete
- tests relevant to the touched area pass

Prepare a summary of:
- fixed items
- deferred items
- unresolved questions
- test results

```text
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ✅ PR FEEDBACK VERIFIED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Fixed now: 2
  Deferred: 1
  Unclear: 1
  Tests: 26 passed, 0 failed
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ⛔ CHECKPOINT 2 — Approve branch/PR update?
  Reply: yes / request changes / abort
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Auto-approve mode
If `NIGHT_SHIFT_AUTO_APPROVE=1` is set in the environment, the agent **auto-approves** this checkpoint with a logged note instead of waiting for user input.

Behavior in auto-approve mode:
- Log: "Auto-approved (night shift mode) — creating PR"
- Continue immediately
- If tests failed after 2 retries → STOP and report failure (do NOT auto-approve past failures)
```

## Phase 7 — UPDATE BRANCH / PR SUMMARY

Update the branch and prepare a concise response summary for the PR:
- fixed now
- deferred intentionally
- still unclear / needs reviewer or user decision

Do not claim comments are resolved unless the underlying change was actually made and verified.
