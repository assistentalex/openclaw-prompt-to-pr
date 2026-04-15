# Context Control Policy

Canonical policy for how prompt-to-pr interprets context pressure and changes behavior.
This file defines the operational logic behind the context banner, compression, checkpointing, and stop/resume behavior.

---

## Core principle

**The context banner is a workflow control signal, not a perfect measurement of remaining model capacity.**

Use it to drive safe behavior:
- when to stay verbose
- when to compress
- when to save state
- when to checkpoint
- when to stop

Do not treat the displayed number as exact proof of how many tokens remain.

---

## Two separate concepts

### Session Pressure
The current session load reported by the runtime, usually from `session_status`.

Prefer the runtime's **Context** value (for example `Context: 93k/200k`) as the primary operational pressure signal when it is available.
Treat this as the closest thing to session-load / crowding telemetry.

### Token Telemetry
The runtime may also expose **Tokens** (for example `Tokens: 38k in`).
This is useful telemetry, but it is not automatically the same thing as context occupancy.
Do not present token counts as if they were equivalent to `Context` usage.

Both signals are still approximate because:
- runtime compaction may change effective context shape
- cache hits reduce practical cost
- future tool output size is unknown
- token accounting and context accounting may diverge in the runtime

### Safe Working Budget
The conservative workflow budget used by prompt-to-pr to decide how aggressively to operate.

This is not necessarily the model's maximum context window.
It is the skill's operational comfort budget.

---

## Budget resolution order

Determine the safe working budget in this order:
1. explicit user-provided budget
2. explicit skill/repo policy value
3. runtime/model-derived value if available
4. conservative fallback budget

If no better signal exists, use a conservative fallback.
Do not describe the fallback as model truth.

---

## Pressure values

Track these values explicitly:
- `rawPressure` = session context / safe working budget when Context is available
- `fallbackPressure` = session tokens / safe working budget when Context is unavailable
- `effectivePressure` = adjusted operational pressure after considering cache/compaction hints when available

If Context is unavailable, fall back to Tokens.
If no meaningful adjustment signal exists, treat `effectivePressure == rawPressure` (or the fallback pressure when Context is missing).

## Divergence handling

If `Context` and `Tokens` differ materially, do not flatten them into a single fake `used` number.
Instead:
- show both signals in the banner
- drive risk decisions primarily from `Context` when available
- optionally note that the runtime signals diverge if the difference is large enough to matter operationally

---

## Next-step heuristic

Before major actions, classify the expected size of the next step:
- `tiny`
- `small`
- `medium`
- `large`

Examples:
- tiny: short user question, short summary, short approval prompt
- small: read one small file section, show compact diff stat, update one task note
- medium: present a full plan, read several targeted files, show medium test output summary
- large: run full tests with noisy output, read large files, generate long PR bodies, show broad diffs

### Minimal v3 heuristic mapping

Use these default mappings unless the task clearly indicates a larger cost:
- one short reply / approval prompt → `tiny`
- one targeted file read / diff stat / one state update → `small`
- plan presentation / multiple targeted reads / compact test summary → `medium`
- full test run / large file read / long PR body / broad diff output → `large`

When uncertain, round up one level rather than down.

The next-step size must influence behavior. Current pressure alone is not enough.

---

## Zone semantics

### Green
- work normally
- no extra restrictions

### Yellow
- switch to concise mode
- reduce quoting and long file dumps

### Orange
- summarize before medium/large actions
- proactively save durable state
- warn user only when helpful

### Red
- checkpoint required before medium/large actions
- mandatory state save before continuing
- may continue only for tiny/small actions when the workflow remains resumable

### Critical
- save state and stop
- do not continue into a medium/large step

---

## Phase-aware behavior

Different phases tolerate pressure differently.

### PREFLIGHT
Usually cheap. Keep concise.

### CONTEXT SCAN
Can grow quickly. Prefer selective reads and summaries.
At orange or above, avoid broad file reads if the next step is medium/large.

### PLAN
Can remain active at higher pressure if compact and resumable.
At red, continue only if the next step is tiny/small or the plan is being summarized.

### IMPLEMENT
May continue under higher pressure only if:
- state is already saved
- the next action is small
- touched files are tracked

### TEST
Most dangerous phase for context growth.
Use the strictest compression and summarization rules here.
At orange, prefer compact summaries over raw output.
At red, do not start a full noisy test run unless the state is saved and the user has explicitly chosen to continue.

### VERIFY
Allow compact summaries, not raw noisy output unless essential.
At orange/red, summarize diff/test findings instead of quoting them.

### PR
Generate concise PR content if pressure is high.
At red, produce a compact PR summary before any long-form body generation.

---

## Minimal decision rules

Apply these default rules:
- if pressure is green → continue normally
- if pressure is yellow → continue concisely
- if pressure is orange and next step is tiny/small → continue after proactive save
- if pressure is orange and next step is medium/large → summarize first, then continue
- if pressure is red and next step is tiny/small → continue only if resumable state is already saved
- if pressure is red and next step is medium/large → checkpoint before continuing
- if pressure is critical → save state and stop

---

## Save-state rules

- At orange: save state proactively
- At red: save state before any medium/large step
- At critical: save state, then stop

Never stop without first attempting to persist durable state.

### Mini v3 save-trigger contract

When a pressure-triggered save happens, update at minimum:
- `phase.shared` / `phase.mode` / `phase.step`
- `status`
- `files.touched` when files changed
- `tests.latest` when tests just ran
- `approvals` when waiting for a checkpoint
- `nextAction`
- `updatedAt`

Pressure-specific behavior:
- orange → save a resumable snapshot before continuing into medium/large work
- red → save a resumable snapshot before any medium/large work and before waiting on a checkpoint
- critical → save a resumable snapshot, set the next action to resume, then stop

---

## Banner guidance

The banner should display operationally useful information, not just a percentage.
Prefer showing:
- current context load
- token telemetry
- safe working budget
- next-step size
- pressure indicator

Example:
`Context: 165k/200k · Tokens: 38k in · Next: LARGE · 🟠`

---

## Truthfulness rule

Never claim the skill knows the exact remaining context window unless the runtime exposes that directly.
Prefer wording like:
- "safe budget"
- "session pressure"
- "operational limit"

Avoid wording like:
- "true remaining tokens"
- "exact context left"
