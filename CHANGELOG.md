# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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