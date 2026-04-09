# Context Budget Management

This file defines the conservative operating budget used by prompt-to-pr.
It does **not** claim to be the model's exact maximum context window.
For behavioral rules, load `references/shared/context-policy.md` as the canonical source.

---

## Safe Working Budget

Default conservative fallback budget: **200,000 tokens**

Use this only when no better budget signal is available.
If the user specifies a budget or the runtime exposes a better one, prefer that.

Think of this number as the skill's **safe working budget**, not an absolute model truth.

---

## Phase Budget Allocation

Apply these percentages against the resolved safe working budget.

| Phase | Budget | Purpose |
|---|---|---|
| PREFLIGHT | 0.5% | Checks only, no code reading |
| CONTEXT SCAN | 20% | Mapping + selective reading |
| PLAN | 5% | Plan generation + user review |
| IMPLEMENT | 40% | Code writing, largest phase |
| TEST | 15% | Test output + retry cycles |
| VERIFY | 10% | Diff + checklist |
| PR | 5% | Commit, branch, PR body |
| ERROR RESERVE | 4.5% | Unexpected retries, edge cases |

---

## Monitoring thresholds

Track cumulative token usage across the session.
Use `session_status` as the primary signal, then apply the behavior rules from `context-policy.md`.

### Green Zone: 0–60%
- Work normally

### Yellow Zone: 60–80%
- Switch to compact mode automatically
- Summarize instead of quoting full file content
- Replace file bodies with function signatures or short summaries when possible

### Orange Zone: 80–90%
- Save durable state proactively
- Summarize before medium/large actions
- Warn the user when helpful

### Red Zone: 90%+
- Require a checkpoint before medium/large actions
- Save durable state before continuing
- Continue only for tiny/small actions when safe and resumable

### Critical Zone
- Save state and stop
- Do not continue into medium/large actions

---

## How to track real usage

Always prefer runtime token data from `session_status`.
Look for the `Tokens: Xk in` line.
Use that as the current session-pressure signal.

Important:
- this is the best available real signal, not perfect truth
- compaction and caching may change practical pressure
- future tool output size is still estimated, not known

---

## Banner format

Every ptop workflow message should begin with a context banner.
Prefer operational clarity over fake precision.

Recommended format:

```text
[FAZA N/M — PHASE NAME  MODE_EMOJI  MODE_NAME]  Context: 165k used · Safe: 200k · Next: MEDIUM · 🟠
```

Minimum fields:
- current used tokens
- safe working budget
- next-step size
- pressure indicator

---

## Custom budget

If the user specifies a different context size or safe budget, store and reuse it for the session.
Recalculate phase budgets proportionally.

Example:
`User: modelul meu are 128k context`

Display:
`Using custom safe budget: 128k tokens`
