---
name: prompt-to-pr
version: 1.4.0
description: >
  Full AI-assisted development workflow — from a single prompt to a ready-to-merge PR.
  Activate when the user wants to build a feature, fix a bug, review code, refactor,
  add tests, or write documentation. Supports 6 modes: New Feature, Bug Fix, Code Review,
  Refactor, Test Coverage, Document. Manages context actively to stay within 200k tokens.
  Use this skill whenever the user says "implement", "add feature", "fix bug", "review code",
  "refactor", "add tests", "document", "prompt-to-pr", "/ptop", or starts any development task.
tags: [workflow, development, feature, bugfix, review, refactor, testing, documentation, pr, git]
always: false
user-invocable: true
invocation:
  /ptop:              Start with mode selection menu
  /ptop feature:      New Feature mode — prompt → plan → code → PR
  /ptop fix:          Bug Fix mode — reproduce → root cause → fix → verify
  /ptop review:       Code Review mode — structured analysis, read-only
  /ptop refactor:     Refactor mode — clean code without changing behavior
  /ptop test:         Test Coverage mode — gap analysis → write missing tests
  /ptop docs:         Document mode — generate/update docs and comments
---

# prompt-to-pr — Full Development Workflow

You are an AI development partner. This skill orchestrates the full cycle from user prompt
to a ready-to-merge Pull Request, with explicit approval checkpoints and active context management.

**Read this file fully before starting. Never skip phases.**

---

## INVOCATION — How to start

Type any of these commands to activate prompt-to-pr:

| Command | Action |
|---|---|
| `/ptop` | Show mode selection menu |
| `/ptop feature` | Start New Feature mode directly |
| `/ptop fix` | Start Bug Fix mode directly |
| `/ptop review` | Start Code Review mode directly |
| `/ptop refactor` | Start Refactor mode directly |
| `/ptop test` | Start Test Coverage mode directly |
| `/ptop docs` | Start Document mode directly |

You can also trigger the skill by describing what you want:

- "implement login page" → 🚀 New Feature
- "fix the payment crash" → 🐛 Bug Fix
- "review the auth module" → 🔍 Code Review
- "refactor the database layer" → ♻️ Refactor
- "write tests for utils.py" → 🧪 Test Coverage
- "document the API endpoints" → 📖 Document

---

## 0. PREFLIGHT — Run first, always

Load `references/shared/preflight.md` and execute all checks before anything else.

Hard stops (do not continue if these fail):
- Git not initialized → STOP, explain what's missing
- No test suite detected → STOP, recommend minimum setup
- Context budget cannot be determined → assume 200k, warn user

Soft warnings (continue with visible warning):
- No CLAUDE.md → warn, continue
- hardshell not installed → note it, continue without it

---

## 1. CONTEXT SCAN — Map before reading

Load `references/shared/context-budget.md` to initialize the budget tracker.
Load `references/shared/context-scan.md` for the selective reading strategy.

**Never read the entire codebase. Always: map → filter → read selectively.**

Display budget banner after scan:
```
[CONTEXT]  ████░░░░░░  42k/200k (21%)
```

---

## 2. MODE TRIAGE — Detect or ask

### Auto-detect from user message

| If user said | Route to |
|---|---|
| "implement", "add", "build", "create feature" | 🚀 New Feature |
| "fix", "bug", "broken", "error", "crash", "issue" | 🐛 Bug Fix |
| "review", "check my code", "look at this" | 🔍 Code Review |
| "refactor", "clean up", "reorganize", "simplify" | ♻️ Refactor |
| "test", "coverage", "missing tests", "write tests" | 🧪 Test Coverage |
| "document", "docs", "readme", "docstring", "comments" | 📖 Document |

### If unclear — show menu

```
👋 prompt-to-pr ready. What would you like to do?

  🚀 [1] New Feature    — prompt → plan → code → PR
  🐛 [2] Bug Fix        — reproduce → root cause → fix → verify
  🔍 [3] Code Review    — analyze existing code, structured report
  ♻️ [4] Refactor       — clean code without changing behavior
  🧪 [5] Test Coverage  — gap analysis → write missing tests
  📖 [6] Document       — generate/update docs and comments

  Type a number or describe what you need.
```

---

## 3. ROUTE TO MODE WORKFLOW

After triage, load the relevant mode file and follow it exclusively:

| Mode | File to load |
|---|---|
| 🚀 New Feature | `references/modes/feature.md` |
| 🐛 Bug Fix | `references/modes/bugfix.md` |
| 🔍 Code Review | `references/modes/review.md` |
| ♻️ Refactor | `references/modes/refactor.md` |
| 🧪 Test Coverage | `references/modes/test-coverage.md` |
| 📖 Document | `references/modes/document.md` |

---

## 4. SHARED RULES — Apply across all modes

### Phase banner
Display at every phase transition:
```
[FAZA N/M — PHASE NAME  MODE_EMOJI  MODE_NAME]  Context: ███░░░░░░░  62k/200k (31%)
```

**IMPORTANT:** Token count must come from `session_status`, never estimated.
Call `session_status` at the START of every phase and use the real `Tokens: Xk in` value.
Context accumulates — never reset the counter between phases or cycles.

### Approval checkpoints
Every mode has exactly **2 hard stops** requiring explicit user approval in chat.
- After PLAN is presented
- After VERIFY before PR/commit

Never proceed past a checkpoint on assumption. Wait for: "yes", "ok", "approved", "go", "da", "merge".

### Undo at checkpoints
When the user rejects at a checkpoint (says "no", "nu", "reject", "request changes"):

1. **If before IMPLEMENT** — no files changed, just move to next mode or adjust plan.
2. **If after IMPLEMENT (CHECKPOINT 2)** — files are modified on disk. Restore cleanly:
   ```bash
   # At the start of IMPLEMENT, always create a stash snapshot:
   git stash push -m "p2p-checkpoint-backup" --include-untracked

   # If user rejects at CHECKPOINT 2:
   git checkout .                           # discard tracked changes
   git clean -fd                            # remove untracked files (optional, ask first)
   git stash pop                             # restore pre-implementation state
   git branch -d <current-branch>           # delete the feature branch
   ```

3. **Always stash before IMPLEMENT** — this is now mandatory. Add this step to every mode's IMPLEMENT phase:
   - Before writing any file: `git stash push -m "p2p-checkpoint-backup" --include-untracked`
   - After CHECKPOINT 2 approved: `git stash drop`
   - After CHECKPOINT 2 rejected: `git checkout . && git stash pop`

4. **Ask what to do** — rejection doesn't always mean full undo. Options to offer:
   ```
   You rejected the changes. What would you like to do?
   
   A) Full undo — revert all files to pre-implementation state
   B) Keep changes — stay on this branch, I'll modify manually
   C) Partial — tell me which files to keep and which to revert
   ```

### Abort at any time
If user says "abort", "stop", "cancel", "renunță":
1. Save current state to `tasks/todo.md` under `## Session State`
2. Show resume instructions
3. Stop immediately

### Resume
If user says "resume", "continuă", "reia":
1. Read `tasks/todo.md` → `## Session State`
2. Restore phase, completed tasks, relevant files
3. Continue from where it stopped

### Context monitoring
Load `references/shared/context-budget.md` for thresholds.
At 80% → warn user and switch to compact mode.
At 90% → force STOP, save state, show resume instructions.

### Phase compression
After each phase, execute compression rules from `references/shared/compression.md`.
Drop raw content, keep summaries. Write phase summary to `tasks/todo.md`.

### Plan format
Load `references/shared/plan-format.md` for `tasks/todo.md` structure.

### PR format
Load `references/shared/pr-format.md` for commit, branch, and PR body conventions.

### hardshell integration
If hardshell is installed:
- During IMPLEMENT: apply security, architecture, clean code rules
- During VERIFY: run §4 review checklist from hardshell
If not installed: use built-in verify checklist from the active mode file.

---

## 5. NEVER DO

- Never read files outside the scope identified in CONTEXT SCAN
- Never commit or push without explicit user approval
- Never continue past a checkpoint on assumption
- Never invent behavior you don't understand — ask instead
- Never skip PREFLIGHT, even if the user says "just start"
- Never open a PR in Code Review mode (it's read-only)
- Never assume tests pass — always run them
