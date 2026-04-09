# prompt-to-pr — 🐛 Skill hardening
**Date:** 2026-04-09 14:45
**Task:** Harden repo selection, mode-aware preflight, and regression tests for prompt-to-pr
**Branch:** fix/ptopr-skill-hardening

---

## Preflight
- Git: ✅
- Tests: ✅ (pytest, 12 tests)
- Coverage: ⚠️ pytest-cov not installed
- CLAUDE.md: ⚠️ not found
- hardshell: ✅ installed

## Context Summary
- Language: Python (Markdown skill package)
- Framework: pytest
- Core files: SKILL.md, references/shared/preflight.md, tests/test_smoke.py
- Goal: remove repo-selection ambiguity, make test detection mode-aware, add fallback guidance, and lock behavior with regression tests

## Tasks
- [x] 1. Unify repo selection wording between SKILL.md and preflight.md — Risk: MEDIUM — Est: ~20 lines
- [x] 2. Make test-suite hard stop mode-aware — Risk: MEDIUM — Est: ~25 lines
- [x] 3. Add explicit execution fallback rules for limited tooling — Risk: LOW — Est: ~15 lines
- [x] 4. Replace stale/duplicate smoke tests with regression-oriented tests — Risk: MEDIUM — Est: ~80 lines
- [x] 5. Run pytest and verify the hardened workflow docs — Risk: LOW — Est: test run

## Test Plan
- Run suite after changes
- Verify repo-discovery wording is consistent
- Verify two-step repo-selection wording is rejected
- Verify mode-aware preflight rules are present
- Verify fallback rules are documented

## Completed Tasks
- [x] Updated SKILL.md hard-stop/warning behavior by mode
- [x] Updated preflight.md to require a single combined mode+repo menu
- [x] Added fallback handling notes for partial discovery / missing gh / restricted shell
- [x] Rewrote tests/test_smoke.py to remove duplicates and assert current rules
- [x] Ran pytest successfully

## Test Results
- Suite: pytest
- Run: 12 passed, 0 failed

## Verify Summary
- Files changed: 3
- Docs behavior aligned between SKILL.md and preflight.md
- Regression tests cover repo selection, mode-aware preflight, and fallback guidance
- Ready for next round of hardening

## Session State
Completed.

## Lessons Learned
- 2026-04-09: Repo selection rules must be stated identically in both SKILL.md and preflight.md, or agents will improvise the gap.
- 2026-04-09: Test-suite enforcement must depend on mode; a universal hard stop blocks valid review/docs flows.
- 2026-04-09: Skill tests should check for contradictory wording directly, not just presence of sections.
