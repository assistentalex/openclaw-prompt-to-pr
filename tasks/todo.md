# prompt-to-pr — 🚀 v3 context control
**Date:** 2026-04-09 17:37
**Task:** Build prompt-to-pr v3 adaptive context control
**Branch:** feat/prompt-to-pr-v3-context-control

---

## Preflight
- Git: ✅
- Tests: ✅ (pytest)
- Coverage: ⚠️ pytest-cov not installed
- CLAUDE.md: ⚠️ not found
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
