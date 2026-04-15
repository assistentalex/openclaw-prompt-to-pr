# prompt-to-pr — 🚀 v3 context control
**Date:** 2026-04-09 17:37
**Task:** Build prompt-to-pr v3 adaptive context control
**Branch:** feat/prompt-to-pr-v3-context-control

---

## Preflight
- Git: ✅
- Tests: ✅ (pytest)
- Coverage: ⚠️ pytest-cov not installed
- Conventions (SKILL.md): ⚠️ not found
- hardshell: ✅ installed

## Context Summary
- Language: Python (Markdown skill package)
- Framework: pytest
- Core files: SKILL.md, references/shared/context-*.md, references/shared/state-system.md, tests/test_smoke.py
- Goal: replace the coarse context bar with an adaptive context-control system

## Clarify Summary
- Questions asked: skipped
- Answers received:
  - design a v3 plan for the context/control bar
  - continue and implement after approval
  - continue with Batch 2 because it is the practical part
- Assumptions:
  - v3 will be implemented in resumable batches
  - Batch 2 should stay minimal and practical, not overengineered
- Open questions: none

## Plan Metadata
- Overall Risk: MEDIUM
- Confidence: HIGH
- Blast Radius: moderate
- Rollback: easy
- Unknowns: runtime/model metadata visibility may stay limited
- Fast Path: no

## Tasks
- [x] 1. Create canonical context-policy spec — Risk: HIGH — Est: ~120 lines
- [x] 2. Replace fixed-200k-as-truth framing — Risk: HIGH — Est: ~60 lines
- [x] 3. Update banner/monitoring language in SKILL.md — Risk: MEDIUM — Est: ~35 lines
- [x] 4. Expand tests for v3 context semantics — Risk: MEDIUM — Est: ~40 lines
- [x] 5. Batch 2 — next-step heuristic + phase-aware behavior
- [ ] 6. Batch 3 — save-state triggers + docs polish

## Test Plan
- Run pytest after each batch
- Verify context docs describe safe working budget, not model truth
- Verify next-step and red/critical semantics are documented
- Verify SKILL.md references adaptive context policy
- Verify scan/compression docs are aware of next-step size

## Completed Tasks
- [x] Added `references/shared/context-policy.md`
- [x] Refactored `references/shared/context-budget.md`
- [x] Updated `SKILL.md` for adaptive context control wording
- [x] Expanded regression tests for v3 semantics
- [x] Added minimal next-step heuristic mapping
- [x] Added phase-aware decision rules by workflow stage
- [x] Updated context-scan and compression guidance to use next-step size

## Test Results
- Suite: pytest
- Run: 32 passed, 0 failed

## Verify Summary
- Batch 1 complete
- Batch 2 complete
- prompt-to-pr now has a canonical context-control policy, a minimal next-step heuristic, and phase-aware behavior
- Ready to either stop here with a useful v3 core or do Batch 3 save-state trigger polish

## Session State
- Status: ACTIVE
- Current batch: Batch 2 completed
- Next action: Decide whether to do Batch 3 save-state trigger polish now or stop after the useful core
- Canonical state file: tasks/state.json
- Resume prompt: `resume prompt-to-pr`

## Lessons Learned
- 2026-04-09: A context bar should drive safe workflow behavior, not pretend to be exact telemetry.
- 2026-04-09: Treating a fallback budget as model truth makes the skill more annoying than safe.
- 2026-04-09: The useful part is not just showing pressure, but adjusting behavior based on the size of the next step.
- 2026-04-09: TEST needs stricter pressure handling than PLAN or IMPLEMENT.

---

# prompt-to-pr — 🐛 Context banner honesty fix
**Date:** 2026-04-15 23:07
**Task:** Fix prompt-to-pr context banner so it stops conflating Tokens with Context and shows honest pressure signals
**Branch:** feat/context-banner-dual-signal

---

## Preflight
- Git: ✅
- Tests: ✅ (pytest)
- Coverage: ⚠️ pytest-cov not explicitly confirmed
- Conventions (SKILL.md): ✅ present
- hardshell: ✅ installed

## Context Summary
- Repo already had context-control docs and smoke tests.
- The defect was semantic/policy-level:
  - `session_status` exposes both `Tokens` and `Context`
  - old prompt-to-pr wording told the agent to use `Tokens: Xk in`
  - old banner examples then presented that as if it were context occupancy
- This created misleading UX when `Tokens` and `Context` diverged materially.

## Plan Metadata
- Overall Risk: MEDIUM
- Confidence: HIGH
- Blast Radius: moderate
- Rollback: easy
- Unknowns: none blocking
- Fast Path: no

## Completed Tasks
- [x] Updated `SKILL.md` mandatory banner contract to separate `Context` from `Tokens`
- [x] Updated `references/shared/context-policy.md` to define Context vs Tokens semantics and divergence handling
- [x] Updated `references/shared/context-budget.md` to align pressure logic and banner examples
- [x] Updated `tests/test_smoke.py` to lock in the new wording/semantics
- [x] Ran `pytest -q`

## Test Results
- Suite: pytest
- Run: 34 passed, 0 failed

## Verify Summary
- `prompt-to-pr` no longer instructs the agent to present `Tokens` as if they were `Context used`
- Banner examples now show both signals honestly:
  - `Context: Xk/200k`
  - `Tokens: Yk in`
- Context policy now defines:
  - Context = primary operational pressure signal when available
  - Tokens = secondary telemetry
  - divergence handling = show both, do not flatten into one fake used number
- Ready for checkpoint 2 approval

## Session State
- Status: WAITING_APPROVAL
- Next action: approve PR creation for the context banner honesty fix
- Canonical state file: tasks/state.json
- Resume prompt: `resume prompt-to-pr`
- Saved: 2026-04-15 23:07 UTC
