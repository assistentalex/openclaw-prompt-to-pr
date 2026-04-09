# Preflight Checks

Run all checks in order before any workflow starts.
Report results as a single block, then decide: continue or STOP.

---

## Check 1 — Git

```bash
git rev-parse --is-inside-work-tree 2>/dev/null
```

- ✅ Pass → continue
- ❌ Fail → **HARD STOP**

Message to user:
```
🔴 STOP — Git not initialized.

This project has no Git repository. prompt-to-pr requires Git
for branch management, commits, and PR creation.

To fix:
  git init
  git add .
  git commit -m "chore: initial commit"

Then restart prompt-to-pr.
```

---

## Check 2 — Repo discovery

**This check MUST run before test suite and coverage checks,** because the selected
repo determines which directory to scan for tests.

### Auto-detect first, ask only when ambiguous

1. If user specified `--repo <path>` or mentioned a project name → use that repo directly.
2. If only one git repo is found → use it silently, **do not ask**.
3. If multiple repos are found → **do NOT show a separate repo menu here.** Instead, pass
   the repo list to the Mode Triage (§2) which will show a single unified menu
   combining mode + repo selection. This avoids asking the user two separate questions.
4. If discovery is partial because tooling is unavailable or restricted → surface the
   discovered candidates, say discovery was partial, and ask the user to choose.

Scan for candidate repos:

1. **Workspace git repos** — check if the current workspace has a `.git` directory
2. **Installed skill repos** — scan `~/.openclaw/skills/` and `~/.npm-global/lib/node_modules/openclaw/skills/` for directories with `.git`
3. **GitHub repos** — if `gh` CLI is available, list recent repos with `gh repo list --limit 10`

Fallback rules:
- If `gh` is missing or not authenticated → skip GitHub discovery, continue with local repos only
- If shell access is restricted → inspect likely repo roots with available file reads, then ask for confirmation if multiple candidates remain
- If metadata like language/test framework cannot be detected → still list the repo, mark fields as `unknown`

For each candidate, detect: language, test framework, and rough test count.

- ✅ Single repo → proceed silently (use it, no question)
- ✅ Multiple repos → pass list to Mode Triage (§2), which will show a **single combined menu** for mode + repo selection
- ⚠️ Partial discovery with one or more candidates → ask the user to confirm from the discovered list
- ❌ No repos found → **HARD STOP**

```
🔴 STOP — No repos found.

prompt-to-pr needs a Git repository to work in. Either:
  - Run /ptopr from inside a Git repo
  - Specify --repo <path>
  - Clone a repo first: git clone <url>
```

---

## Check 3 — Test suite (mode-aware)

Look for any of the following (in order of priority):

| Signal | Detected as |
|---|---|
| `package.json` with `"test"` script | Node/JS test suite |
| `pytest.ini`, `pyproject.toml` with `[tool.pytest]`, `setup.cfg` | Python/pytest |
| `go test ./...` runnable | Go test suite |
| `Makefile` with `test` target | Generic make-based |
| `*.test.*`, `*.spec.*`, `tests/`, `__tests__/` directory | Test files present |
| `cargo test` runnable | Rust |

- ✅ Any detected → continue
- ❌ None detected in 🚀/🐛/♻️/🧪 modes → **HARD STOP**
- ❌ None detected in 🔍/📖 modes → **SOFT WARNING**, continue

Message to user for hard-stop modes:
```
🔴 STOP — No test suite detected.

prompt-to-pr requires at least a minimal test suite for Feature, Bug Fix,
Refactor, and Test Coverage modes. Without tests, there's no safety net
for changes and no way to verify them.

Minimum to get started:
  # Node.js
  npm init -y && npm install --save-dev jest
  # Add to package.json: "test": "jest"

  # Python
  pip install pytest && mkdir tests && touch tests/__init__.py

  # Go — already built in, just create *_test.go files

Add at least one smoke test, then restart prompt-to-pr.
```

Message to user for soft-warning modes:
```
🟡 WARNING — No test suite detected.

Continuing because the selected mode is Review or Docs, where code changes
may be read-only or documentation-only. If the task expands into behavior-
changing edits, stop and set up a minimal test suite first.
```

---

## Check 4 — Coverage tool (soft)

Check if a coverage tool exists (nyc, c8, pytest-cov, go cover, etc.).

- ✅ Found → note it for Test Coverage mode
- ❌ Not found → soft warning, only relevant if using 🧪 Test Coverage mode

```
🟡 WARNING — No coverage tool detected.
Test Coverage mode will run tests but cannot generate a coverage report.
Install a coverage tool to get gap analysis. Continuing.
```

---

## Check 5 — CLAUDE.md (soft)

```bash
ls CLAUDE.md 2>/dev/null || ls .claude/CLAUDE.md 2>/dev/null
```

- ✅ Found → read it for project conventions before context scan
- ❌ Not found → soft warning

```
🟡 WARNING — No CLAUDE.md found.
Project-specific conventions won't be loaded. Continuing with defaults.
Consider creating CLAUDE.md to persist conventions across sessions.
```

---

## Check 6 — hardshell (soft)

Check if `hardshell` skill is installed:
```bash
ls .claude/skills/hardshell/SKILL.md 2>/dev/null || \
ls ~/.claude/skills/hardshell/SKILL.md 2>/dev/null
```

- ✅ Found → note for IMPLEMENT and VERIFY phases
- ❌ Not found → note, use built-in checklists

```
ℹ️  hardshell not detected. Built-in quality checklists will be used.
Install hardshell for enhanced security and architecture rules.
```

---

## Preflight Summary Block

Always display before continuing:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  prompt-to-pr — PREFLIGHT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Repo             ✅  ~/.openclaw/skills/prompt-to-pr
  Git              ✅
  Test suite       ✅  (jest) / ⚠️  not detected but allowed in review/docs
  Coverage tool    ✅  (nyc)
  CLAUDE.md        ⚠️  not found
  hardshell        ⚠️  not installed
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Status: READY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Or if hard stop:
```
  Status: ❌ STOPPED — see errors above
```
