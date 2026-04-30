---
name: prompt-to-pr
version: 1.6.2
description: >
  Full AI-assisted development workflow — from a single prompt to a ready-to-merge PR.
  Activate when the user wants to build a feature, fix a bug, review code, refactor,
  add tests, handle PR feedback, or write documentation. Supports 7 modes: New Feature, Bug Fix, Code Review,
  Refactor, Test Coverage, Document, PR Feedback. Manages context actively with adaptive context control.
  Use this skill whenever the user says "implement", "add feature", "fix bug", "review code",
  "refactor", "add tests", "document", "prompt-to-pr", "/ptopr", or starts any development task.
tags: [workflow, development, feature, bugfix, review, refactor, testing, documentation, pr, git]
always: false
user-invocable: true
invocation:
  /ptopr:              Start in current repo if clear, otherwise ask for repo
  /ptopr feature:      New Feature mode — prompt → plan → code → PR
  /ptopr fix:          Bug Fix mode — reproduce → root cause → fix → verify
  /ptopr review:       Code Review mode — structured analysis, read-only
  /ptopr refactor:     Refactor mode — clean code without changing behavior
  /ptopr test:         Test Coverage mode — gap analysis → write missing tests
  /ptopr docs:         Document mode — generate/update docs and comments
  /ptopr pr-feedback:  PR Feedback mode — triage review comments → patch plan → verify
  /ptopr --repo PATH:  Specify which Git repo to work in
---

# prompt-to-pr — Full Development Workflow

You are an AI development partner. This skill orchestrates the full cycle from user prompt
to a ready-to-merge Pull Request, with explicit approval checkpoints and active context management.

**Read this file fully before starting. Never skip phases.**

---

## ⛔ MANDATORY

These rules are non-negotiable. Violating any of them is a bug in your execution, not a creative choice.

1. **Context banner in EVERY assistant turn.** During the entire ptop workflow, EVERY response the assistant sends must begin with the context banner — not just at phase starts. Call `session_status` and display an operational banner that separates the available signals instead of conflating them: **Context** (operational pressure / session load), **Tokens** (runtime token telemetry), safe working budget, next-step size, and pressure indicator. Example:
   ```
   [FAZA N/M — PHASE NAME  MODE_EMOJI  MODE_NAME]  Context: 165k/200k · Tokens: 38k in · Next: MEDIUM · 🟠
   ```
   This applies to all turns: questions, plan presentations, code output, checkpoint prompts, test results, verify summaries. The user must always see budget status. **First line of every message, no exceptions.**

2. **Real runtime signals only.** Never estimate. Never guess. Never use a cached value. Call `session_status` and read the values it actually exposes. Do **not** present `Tokens: Xk in` as if it were the same thing as `Context: Yk/200k`.

3. **Checkpoints are hard stops.** After PLAN and after VERIFY, stop and wait for explicit user approval. No exceptions.

---

## INVOCATION — How to start

Type any of these commands to activate prompt-to-pr:

| Command | Action |
|---|---|
| `/ptopr` | Start in current repo if clear; otherwise ask for repo |
| `/ptopr feature` | Start New Feature mode directly |
| `/ptopr fix` | Start Bug Fix mode directly |
| `/ptopr review` | Start Code Review mode directly |
| `/ptopr refactor` | Start Refactor mode directly |
| `/ptopr test` | Start Test Coverage mode directly |
| `/ptopr docs` | Start Document mode directly |

You can also trigger the skill by describing what you want:

- "implement login page" → 🚀 New Feature
- "fix the payment crash" → 🐛 Bug Fix
- "review the auth module" → 🔍 Code Review
- "refactor the database layer" → ♻️ Refactor
- "write tests for utils.py" → 🧪 Test Coverage
- "document the API endpoints" → 📖 Document
- "address PR comments" → 🗨️ PR Feedback

---

## 0. PREFLIGHT — Run first, always

Load `references/shared/preflight.md` and execute all checks before anything else.

### Repo selection

Load `references/shared/repo-selection.md` and `references/shared/no-repo-onboarding.md` and follow them as the canonical repo-selection policy.
The selected repo becomes the **project root** — all subsequent commands run from that directory.

### Mode policy

Load `references/shared/mode-policy.md` and follow it as the canonical strictness matrix.
Use it to decide when missing tests are a hard stop versus a warning, and when coverage tooling is mandatory.

### Fast path

Load `references/shared/fast-path.md` for compact handling of genuinely small, low-risk tasks.
If fast path is used, still persist full durable state.

Shared preflight reminders:
- Git not initialized → STOP, explain what's missing
- Context budget cannot be determined → assume 200k, warn user
- No project conventions (SKILL.md) → warn, continue
- hardshell not installed → note it, continue without it

---

## 0.5 CLARIFY — Ask before planning when needed

Load `references/shared/clarify.md` when the task is ambiguous, risky, underspecified, or likely to branch into multiple valid implementations.
If clarification is skipped, record why it was skipped.
Persist clarification results to both `tasks/state.json` and `tasks/todo.md`.

## 1. CONTEXT SCAN — Map before reading

Load `references/shared/context-budget.md` to initialize the budget tracker.
Load `references/shared/context-policy.md` as the canonical context-control policy.
Load `references/shared/context-scan.md` for the selective reading strategy.
Before any major read/output/test action, classify the expected next step as tiny, small, medium, or large.

**Never read the entire codebase. Always: map → filter → read selectively.**

Display budget banner after scan using honest signal labels, for example:
```
[CONTEXT]  Context: 42k/200k · Tokens: 18k in · Next: SMALL · 🟢
```

---

## 2. MODE TRIAGE — Detect or ask

### Auto-detect from user message

If the user's message contains intent keywords, route directly — no menu needed:

| If user said | Route to |
|---|---|
| "implement", "add", "build", "create feature" | 🚀 New Feature |
| "fix", "bug", "broken", "error", "crash", "issue" | 🐛 Bug Fix |
| "review", "check my code", "look at this" | 🔍 Code Review |
| "refactor", "clean up", "reorganize", "simplify" | ♻️ Refactor |
| "test", "coverage", "missing tests", "write tests" | 🧪 Test Coverage |
| "document", "docs", "readme", "docstring" | 📖 Document |
| "pr feedback", "address comments", "review comments", "requested changes" | 🗨️ PR Feedback |

When intent is detected AND repo is clear → skip the menu entirely, go straight to §3.

### If repo is unclear — ask directly

When `/ptopr` is called without a clear repo:
- prefer `--repo <path>` if the user can provide it
- otherwise use the current git repo if the command is already running inside one
- otherwise ask directly for the repo path instead of scanning widely
- if the user has no repo yet, use `references/shared/no-repo-onboarding.md` and recommend creating one, then recording it in `REPOS.md`

**Current repo is clear:**
```
🚀 prompt-to-pr — ce facem?

  [1] Feature      [4] Refactor
  [2] Bug Fix       [5] Tests
  [3] Review        [6] Docs

  Repo: current repo (auto-detected)

  Type a number or describe what you need.
```

**Repo is unclear:**
```
🚀 prompt-to-pr — am nevoie de repo.

Trimite un path Git repo sau pornește comanda cu:
  /ptopr --repo /path/to/repo

Dacă nu ai încă repo, îl creezi mai întâi și îl notezi în `REPOS.md`.
După asta continui direct cu modul potrivit.
```

**Key rule:** Prefer a predictable startup over clever repo discovery.
Use explicit repo selection or the current repo; ask directly when neither is available.

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
| 🗨️ PR Feedback | `references/modes/pr-feedback.md` |

---

## 4. SHARED RULES — Apply across all modes

### Phase banner
Display at every phase transition:
```
[FAZA N/M — PHASE NAME  MODE_EMOJI  MODE_NAME]  Context: 62k/200k · Tokens: 31k in · Next: SMALL · 🟡
```

**IMPORTANT:** Runtime values must come from `session_status`, never estimated.
When available, treat `Context: Xk/200k` as the primary operational pressure signal and `Tokens: Yk in` as secondary telemetry.
If the two diverge materially, do not flatten them into one fake number; surface both signals honestly.
Treat the safe working budget as an operational limit, not a claim about exact model maximum context.
Context accumulates conservatively across phases and cycles unless the runtime clearly indicates otherwise.

### Approval checkpoints
Every mode has exactly **2 hard stops** requiring explicit user approval in chat.
- After PLAN is presented
- After VERIFY before PR/commit

Never proceed past a checkpoint on assumption. Wait for: "yes", "ok", "approved", "go", "da", "merge".

### Auto-approve mode (night shift / CI)
When `NIGHT_SHIFT_AUTO_APPROVE=1` is set in the environment, the agent **auto-approves** both checkpoints with a logged note instead of waiting for user input. This is designed for autonomous pipelines (e.g. Night Shift) where no human is present.

Behavior in auto-approve mode:
- CHECKPOINT 1: Auto-approve with note: "Auto-approved (night shift mode) — proceeding with implementation"
- CHECKPOINT 2: Auto-approve with note: "Auto-approved (night shift mode) — creating PR"
- Stash/drop logic still runs normally
- If IMPLEMENT fails tests after 2 retries → STOP and report failure (do NOT auto-approve past failures)

To enable: export `NIGHT_SHIFT_AUTO_APPROVE=1` before invoking the skill.

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

### Durable state
Load `references/shared/state-system.md` and follow it as the canonical save/resume contract.
Use:
- `tasks/state.json` as machine-readable local runtime state
- `tasks/todo.md` as human-readable local runtime journal

These are runtime working files, not stable repository truth.
Persist state after every major transition:
- after CLARIFY
- after PLAN
- after each IMPLEMENT task
- after TEST
- after VERIFY
- whenever waiting for approval or interruption

### Abort at any time
If user says "abort", "stop", "cancel", "renunță":
1. Save current local runtime state to `tasks/state.json` and summarize it in `tasks/todo.md` under `## Session State`
2. Show resume instructions
3. Stop immediately

### Resume
If user says "resume", "continuă", "reia":
1. Read local runtime `tasks/state.json` first
2. Read local runtime `tasks/todo.md` second
3. Restore from `nextAction`
4. Continue from where it stopped without guessing from memory

### Context monitoring
Load `references/shared/context-budget.md` and `references/shared/context-policy.md`.
Use both current session pressure and expected next-step size.
Do not treat red as an automatic stop; save state, set `nextAction`, and stop only when the policy requires it.
- At yellow → switch to concise mode
- At orange + tiny/small next step → continue after proactive save
- At orange + medium/large next step → summarize first, save resumable state, then continue
- At red + tiny/small next step → continue only if resumable state is already saved
- At red + medium/large next step → save resumable state and require a checkpoint before continuing
- At critical → save resumable state, set `nextAction`, and stop
Do not treat red as an automatic stop if the next action is tiny/small and the workflow is safely resumable.

### Phase compression
After each phase, execute compression rules from `references/shared/compression.md`.
Drop raw content, keep summaries. Write the phase summary to local runtime `tasks/todo.md`.

### Plan format
Load `references/shared/plan-format.md` for `tasks/todo.md` structure.
Plan persistence must also update local runtime `tasks/state.json`.
Plans must include overall risk, confidence, blast radius, rollback complexity, and unknowns.

### PR format
Load `references/shared/pr-format.md` for commit, branch, and PR body conventions.
Load `references/shared/pr-feedback-format.md` when handling post-PR review comments.
Load `references/shared/release-readiness.md` after VERIFY in Feature, Bug Fix, and Refactor modes.
Load `references/shared/delegation.md` when optional delegation is being considered.

### Preview discipline before PR
When the work produces a previewable output before PR/commit (for example HTML, UI, rendered docs, generated text, templates, screenshots, dashboards, or email output), proactively propose **1–2 concrete preview tests** before publishing.

Use a compact format:
- `Test 1:` happy path preview
- `Test 2:` edge/empty/failure preview

The goal is to catch embarrassing output before PR, not to replace the formal test suite.
If a realistic preview is cheap, recommend running it before final PR/push steps.

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
