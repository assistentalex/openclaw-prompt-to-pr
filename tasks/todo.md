# prompt-to-pr — ♻️ Skill hardening round 3
**Date:** 2026-04-09 15:10
**Task:** Deduplicate repo-selection and mode-policy rules into shared references, then lock consistency with tests
**Branch:** fix/ptopr-skill-hardening

---

## Preflight
- Git: ✅
- Tests: ✅ (pytest, 17 tests)
- Coverage: ⚠️ pytest-cov not installed
- CLAUDE.md: ⚠️ not found
- hardshell: ✅ installed

## Context Summary
- Language: Python (Markdown skill package)
- Framework: pytest
- Core files: SKILL.md, references/shared/preflight.md, references/shared/repo-selection.md, references/shared/mode-policy.md, tests/test_smoke.py
- Goal: reduce duplicated rules, create clear canonical policy files, and prevent wording drift with stronger tests

## Tasks
- [x] 1. Create canonical shared repo-selection policy — Risk: MEDIUM — Est: ~60 lines
- [x] 2. Create canonical shared mode-policy matrix — Risk: MEDIUM — Est: ~40 lines
- [x] 3. Replace duplicated wording in SKILL.md with references to shared policy files — Risk: LOW — Est: ~20 lines
- [x] 4. Replace duplicated wording in preflight.md with references to shared policy files — Risk: MEDIUM — Est: ~35 lines
- [x] 5. Extend regression tests for canonical policy files and consistency checks — Risk: MEDIUM — Est: ~60 lines
- [x] 6. Run pytest, fix one regression, and verify green state — Risk: LOW — Est: test run

## Test Plan
- Verify shared policy files exist
- Verify repo-selection policy requires a single combined menu
- Verify mode-policy matrix covers all supported modes
- Verify SKILL.md and preflight.md point to the canonical policy files
- Verify fallback rules remain documented after deduplication

## Completed Tasks
- [x] Added `references/shared/repo-selection.md`
- [x] Added `references/shared/mode-policy.md`
- [x] Simplified `SKILL.md` to reference canonical policy docs instead of duplicating rules
- [x] Simplified `preflight.md` to reference canonical policy docs while preserving user-facing stop/warning messages
- [x] Strengthened regression tests and repaired one failing expectation after deduplication
- [x] Ran pytest successfully

## Test Results
- Suite: pytest
- Run: 17 passed, 0 failed

## Verify Summary
- Files changed: 6
- Repo-selection and mode-strictness rules now have single sources of truth
- Tests cover shared-policy existence, consistency, and anti-drift behavior
- Ready for PR / summary work

## Session State
Completed.

## Lessons Learned
- 2026-04-09: If a rule appears in more than one file, it needs a canonical source or it will drift.
- 2026-04-09: Tests should be updated to follow the source of truth after refactors, not the old location of the text.
- 2026-04-09: Good deduplication keeps user-facing stop/warning messages intact while moving policy logic into reusable references.
