# prompt-to-pr — 🚀 v2 implementation
**Date:** 2026-04-09 15:47
**Task:** Build prompt-to-pr v2 with durable resume and clarification-first workflow
**Branch:** feat/prompt-to-pr-v2

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
- Core files: SKILL.md, references/shared/*.md, references/modes/*.md, tests/test_smoke.py
- Goal: evolve prompt-to-pr into a v2 workflow with durable recovery, clearer planning, PR feedback handling, and modern agent workflow features

## Clarify Summary
- Questions asked: skipped
- Answers received:
  - Implement all useful v2 features, rand pe rand
  - Build an implementation system so work survives disconnects
- Assumptions:
  - Implement in resumable batches
  - Batch 1 covers durable state + clarification phase foundations
  - Batch 2 covers risk metadata + fast path + review presets
  - Batch 3 covers PR feedback + release readiness + delegation hooks
- Open questions: none

## Plan Metadata
- Overall Risk: MEDIUM
- Confidence: MEDIUM
- Blast Radius: moderate
- Rollback: easy
- Unknowns: final polish around PR feedback integration with real provider tooling can come later
- Fast Path: no (program is broad and multi-batch)

## Tasks
- [x] 1. Add durable state system docs and canonical state file — Risk: HIGH — Est: foundational
- [x] 2. Add canonical clarification phase docs — Risk: MEDIUM — Est: ~40 lines
- [x] 3. Wire state/clarify docs into SKILL.md — Risk: MEDIUM — Est: ~30 lines
- [x] 4. Wire clarification/state behavior into all mode files — Risk: MEDIUM — Est: multi-file docs update
- [x] 5. Update plan-format for state.json + clarify summary — Risk: MEDIUM — Est: ~25 lines
- [x] 6. Expand regression tests for state/clarify system — Risk: MEDIUM — Est: ~40 lines
- [x] 7. Add fast-path policy and documentation — Risk: MEDIUM — Est: ~40 lines
- [x] 8. Add review scope presets and review-mode wiring — Risk: MEDIUM — Est: ~40 lines
- [x] 9. Expand plan metadata with risk/confidence/blast-radius/rollback — Risk: MEDIUM — Est: ~25 lines
- [x] 10. Expand regression tests for Batch 2 — Risk: MEDIUM — Est: ~35 lines
- [x] 11. Add PR feedback mode and shared feedback format — Risk: HIGH — Est: ~80 lines
- [x] 12. Add release-readiness summary format — Risk: MEDIUM — Est: ~20 lines
- [x] 13. Add delegation hooks foundation — Risk: MEDIUM — Est: ~25 lines
- [x] 14. Wire Batch 3 docs into SKILL and mode policy — Risk: MEDIUM — Est: ~25 lines
- [x] 15. Expand regression tests for Batch 3 — Risk: MEDIUM — Est: ~35 lines

## Test Plan
- Run pytest after each batch
- Assert shared state/clarify files exist
- Assert fast-path and review-presets files exist
- Assert PR feedback / release readiness / delegation docs exist
- Assert SKILL.md and mode docs reference canonical shared docs
- Assert review mode presents presets
- Assert PR feedback mode wiring exists

## Completed Tasks
- [x] Added `references/shared/state-system.md`
- [x] Added `references/shared/clarify.md`
- [x] Added canonical `tasks/state.json`
- [x] Updated `SKILL.md` to require durable state persistence and clarification-first behavior
- [x] Updated all mode files to reference clarify/state-system and added Phase 1 — CLARIFY
- [x] Updated `references/shared/plan-format.md`
- [x] Added `references/shared/fast-path.md`
- [x] Added `references/shared/review-presets.md`
- [x] Updated `references/shared/mode-policy.md` with fast-path handling and PR Feedback mode
- [x] Updated `references/modes/review.md` to use preset-based scope selection
- [x] Added `references/modes/pr-feedback.md`
- [x] Added `references/shared/pr-feedback-format.md`
- [x] Added `references/shared/release-readiness.md`
- [x] Added `references/shared/delegation.md`
- [x] Updated feature/bugfix/refactor guidance with release-readiness hooks
- [x] Expanded regression tests and validated them

## Test Results
- Suite: pytest
- Run: 29 passed, 0 failed

## Verify Summary
- Batch 1 complete
- Batch 2 complete
- Batch 3 complete
- Workflow now has durable state, clarification-first behavior, richer plan metadata, fast-path rules, review scope presets, PR feedback mode, release-readiness summaries, and delegation foundations
- Ready for merge / PR preparation

## Session State
- Status: WAITING_APPROVAL
- Current batch: Batch 3 completed
- Next action: checkpoint 2 approval, then commit/PR preparation
- Canonical state file: tasks/state.json
- Resume prompt: `resume prompt-to-pr`

## Lessons Learned
- 2026-04-09: Disconnect safety needs a machine-readable source of truth, not just a human summary.
- 2026-04-09: Clarification should be explicit and persisted, otherwise planning quality depends too much on transient chat context.
- 2026-04-09: Compact workflows still need full state persistence or they become the first thing to break under interruption.
- 2026-04-09: PR workflows are incomplete if they stop at branch creation; review-comment handling needs its own mode and summary format.
