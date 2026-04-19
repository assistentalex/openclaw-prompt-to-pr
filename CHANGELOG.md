# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.6.2] - 2026-04-19

### Changed
- Localized runtime artifacts (`tasks/state.json`, `tasks/todo.md`, `.openclaw/reviews/`) as local-only working files instead of committed repository truth
- Aligned `SKILL.md`, the PR template, and shared docs with the runtime-artifact contract
- Added regression coverage to prevent runtime-artifact contract drift

## [1.6.1] - 2026-04-19

### Changed
- Removed the undocumented repo-registry concept from primary repo-selection guidance
- Simplified repo selection docs to: explicit `--repo`, current repo, otherwise ask directly
- Kept `REPOS.md` as the minimal human-readable repo map

## [1.6.0] - 2026-04-10

### Changed
- Added explicit no-repo onboarding guidance with a recommendation to create a repo first when needed
- Added `references/shared/no-repo-onboarding.md` as the canonical no-repo policy
- Documented `REPOS.md` as the human-readable companion to the prompt-to-pr repo registry

## [1.5.0] - 2026-04-09

### Changed
- Simplified startup repo selection: explicit `--repo`, otherwise current repo, otherwise ask directly for a path
- Removed broad startup repo discovery from the canonical repo-selection flow and preflight contract
- Updated `SKILL.md` and `README.md` to use `/ptopr` consistently and describe the new repo-selection behavior
- Added/updated smoke tests to prevent regression to the old discovery-heavy startup flow

## [1.4.0] - 2026-04-08

### Changed
- Token tracking now uses real `session_status` data instead of estimates
- Context counter never resets between phases or cycles (accumulates correctly)
- `context-budget.md`: replaced "How to Estimate" with "How to Track Real Token Usage"
- `SKILL.md`: phase banners must call `session_status` for actual token count

## [1.3.0] - 2026-04-08

### Changed
- Renamed `/p2p` to `/ptop` for easier mobile typing (no keyboard switch needed)

## [1.2.0] - 2026-04-08

### Added
- `/p2p` invocation commands — explicit start button for each mode
- Invocation section in SKILL.md with slash command table
- README updated with `/p2p` usage examples

## [1.1.0] - 2026-04-08

### Added
- Undo feature for checkpoint rejection: git stash before IMPLEMENT, clean restore on rejection
- Three rejection options: full undo, keep changes, or partial keep

## [1.0.0] - 2026-04-08

### Added
- 6 workflow modes: New Feature, Bug Fix, Code Review, Refactor, Test Coverage, Document
- Active context management with 200k token budget
- Approval checkpoints (plan + verify) for all modes
- Preflight checks (Git, test suite, coverage tool, hardshell)
- Resume capability for interrupted sessions
- hardshell skill integration for enhanced code review
- Phase compression to stay within context budget