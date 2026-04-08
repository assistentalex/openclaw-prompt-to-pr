# Context Budget Management

Total assumed budget: **200,000 tokens**
This applies to all models unless the user specifies otherwise.

---

## Phase Budget Allocation

| Phase | Budget | Max Tokens | Purpose |
|---|---|---|---|
| PREFLIGHT | 0.5% | 1,000 | Checks only, no code reading |
| CONTEXT SCAN | 20% | 40,000 | Mapping + selective reading |
| PLAN | 5% | 10,000 | Plan generation + user review |
| IMPLEMENT | 40% | 80,000 | Code writing, largest phase |
| TEST | 15% | 30,000 | Test output + retry cycles |
| VERIFY | 10% | 20,000 | Diff + checklist |
| PR | 5% | 10,000 | Commit, branch, PR body |
| ERROR RESERVE | 4.5% | 9,000 | Unexpected retries, edge cases |

---

## Monitoring Thresholds

Track cumulative token usage across all phases.

### Green Zone: 0–60%  (0–120k tokens)
- Work normally
- No restrictions
- Banner: `████████░░  96k/200k (48%)`

### Yellow Zone: 60–80%  (120k–160k tokens)
Switch to compact mode automatically:
- Summarize instead of quoting full file content
- Replace file bodies with function signatures only
- Shorten plan entries to one line each
- Skip optional context (comments, docstrings) when reading code
- Banner: `🟡 ████████░░  144k/200k (72%)`

### Orange Zone: 80–90%  (160k–180k tokens)
Warn user explicitly:
```
🟠 CONTEXT WARNING — 82% used (164k/200k)
Switching to aggressive compression. Output will be more concise.
Current phase will complete, then I'll pause for your input.
```
- Compress all previous phase summaries to bullet points
- Only keep the active task in full detail
- Save state to tasks/todo.md immediately

### Red Zone: 90%+  (180k+ tokens)
Force stop:
```
🔴 CONTEXT LIMIT — 91% used (182k/200k)
Stopping to prevent context overflow.

State saved to tasks/todo.md
To resume: "resume prompt-to-pr"
```
- Save full session state
- Do not attempt to continue
- Show resume instructions

---

## How to Track Real Token Usage

**Always use real token counts, never estimates.**

At the start of every phase, call `session_status` to get actual token usage:

```
session_status → look for "Tokens: Xk in" line
```

Use the `Xk` value as your current context usage. Calculate the percentage
against the total budget (default 200k, or custom if specified).

### Why real counts?
- Estimates are unreliable — a 10KB file can be 2k or 5k tokens depending on content
- Cumulative context includes all prior conversation, not just files you read
- Resetting the counter between cycles is WRONG — context accumulates

### Accumulation rule
Context tokens only go UP. Never reset the counter.
If you start a new /ptop cycle, context from the previous cycle is still there.
Banner at cycle start should reflect accumulated total, not zero.

### Fallback (if session_status unavailable)
Use these rough multipliers only as last resort:

| Content type | Tokens per line |
|---|---|
| Code (dense) | 8–12 tokens |
| Code (sparse/comments) | 4–6 tokens |
| Plain text / docs | 4–5 tokens |
| JSON / config | 6–10 tokens |
| Test output | 3–4 tokens |

**Quick estimate:** `file size in KB × 250 ≈ tokens`

Example: a 10KB file ≈ 2,500 tokens

---

## Budget Banner Format

Display at every phase transition:

```
[FAZA 3/6 — IMPLEMENT 🚀 New Feature]  Context: ███████░░░  140k/200k (70%) 🟡
```

Color indicators:
- No emoji = green (< 60%)
- 🟡 = yellow (60–80%)
- 🟠 = orange (80–90%)
- 🔴 = red (90%+)

---

## Custom Budget

If the user specifies a different context size:
```
User: "meu model are 128k context"
```
Recalculate all phase budgets proportionally.
Display: `Using custom budget: 128k tokens`

Store the custom value and use it for all subsequent calculations in the session.
