# Contributing to prompt-to-pr

Thank you for your interest in contributing!

## How to Contribute

1. **Fork** the repository
2. Create a focused branch: `git checkout -b feat/your-change` or `git checkout -b refactor/your-change`
3. Make your changes
4. **Run tests:** `python3 -m pytest tests/ -v`
5. Commit with a clear message (see conventions below)
6. Open a Pull Request

## Branch Naming

| Type | Prefix | Example |
|------|--------|---------|
| New feature | `feat/` | `feat/add-resume-mode` |
| Bug fix | `fix/` | `fix/context-budget-overflow` |
| Documentation | `docs/` | `docs/readme-and-contributing` |
| Refactor | `refactor/` | `refactor/simplify-preflight` |

## Commit Format

```
type(scope): description

# Examples:
docs(readme): add installation and usage sections
fix(preflight): handle missing git gracefully
feat(modes): add resume capability
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

## Local runtime artifacts

These files/directories are operational runtime artifacts and should stay local during normal use:
- `tasks/state.json`
- `tasks/todo.md`
- `.openclaw/reviews/`

Do not treat them as stable repository truth. If you need examples for docs, add explicit templates or reference snippets instead.

## Versioning note

Keep release/version metadata aligned:
- `CHANGELOG.md` is the release history
- `SKILL.md` carries the skill-facing version metadata
- `pyproject.toml` should stay aligned with the published/documents version story

## Questions?

Open an issue on [GitHub](https://github.com/asistent-alex/openclaw-prompt-to-pr/issues).