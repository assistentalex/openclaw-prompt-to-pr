# Contributing to prompt-to-pr

Thank you for your interest in contributing!

## How to Contribute

1. **Fork** the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes
4. **Run tests:** `python3 -m pytest tests/ -v`
5. Commit with a clear message (see conventions below)
6. Open a Pull Request

## Branch Naming

| Type | Prefix | Example |
|------|--------|---------|
| New feature | `feature/` | `feature/add-resume-mode` |
| Bug fix | `fix/` | `fix/context-budget-overflow` |
| Documentation | `docs/` | `docs/readme-and-contributing` |
| Refactor | `refactor/` | `refactor/simplify-preflight` |

## Commit Format

```
type(scope): description

# Examples:
docs(readme): add installation and usage sections
fix(preflight): handle missing git gracefully
feature(modes): add resume capability
```

Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`

## Code Style

- This is a markdown-based skill — keep references clear and well-structured
- Python files (tests, scripts) follow PEP 8
- All new modes or reference files should be documented in SKILL.md

## Pull Requests

- Keep PRs focused — one concern per PR
- Ensure tests pass before submitting
- The skill itself uses prompt-to-pr's review mode — meta!

## Questions?

Open an issue on [GitHub](https://github.com/assistentalex/openclaw-prompt-to-pr/issues).