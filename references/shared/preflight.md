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

## Check 2 — Repo selection

**This check MUST run before test suite and coverage checks,** because the selected
repo determines which directory to scan for tests.

Load `references/shared/repo-selection.md` and `references/shared/no-repo-onboarding.md` and follow them as the canonical repo-selection policy.
At minimum, preflight must:
- accept `--repo <path>` immediately when provided
- prefer the current git repo when the command is already running inside one
- otherwise, ask the user directly for a repo path
- avoid broad startup discovery across installed skills, bundled skills, or GitHub
- if the user has no repo yet, recommend creating one and recording it in `REPOS.md`

```
🔴 STOP — Repo not selected.

prompt-to-pr needs a Git repository to work in. Either:
  - Run /ptopr from inside a Git repo
  - Specify --repo <path>
  - Clone a repo first: git clone <url>
  - Or create a new repo, then record it in REPOS.md
```

---

## Check 3 — REPOS.md (soft)

Check whether `REPOS.md` exists in the workspace or project context.

- ✅ Found → note that it can be used as the local repo map when repo selection is unclear
- ⚠️ Missing → continue, but recommend creating it

```
🟡 WARNING — REPOS.md not found.

prompt-to-pr can still work with:
  - --repo <path>
  - current repo

But `REPOS.md` is recommended as the local repo map for known repos and subprojects.
Consider creating it to reduce ambiguity.
```

---

## Check 4 — Test suite (mode-aware)

Load `references/shared/mode-policy.md` and use it as the canonical strictness matrix.

Look for any of the following (in order of priority):

| Signal | Detected as |
|---|---|
| `package.json` with `"test"` script | Node/JS test suite |
| `pytest.ini`, `pyproject.toml` with `[tool.pytest]`, `setup.cfg` | Python/pytest |
| `go test ./...` runnable | Go test suite |
| `Makefile` with `test` target | Generic make-based |
| `*.test.*`, `*.spec.*`, `tests/`, `__tests__/` directory | Test files present |
| `cargo test` runnable | Rust |

Then apply the mode policy:
- 🚀/🐛/♻️/🧪 without tests → **HARD STOP**
- 🔍/📖 without tests → **SOFT WARNING**, continue
- 🧪 without coverage tooling → **HARD STOP** for coverage analysis

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

## Check 5 — Coverage tool (soft)

Check if a coverage tool exists (nyc, c8, pytest-cov, go cover, etc.).

- ✅ Found → note it for Test Coverage mode
- ❌ Not found → soft warning, only relevant if using 🧪 Test Coverage mode

```
🟡 WARNING — No coverage tool detected.
Test Coverage mode will run tests but cannot generate a coverage report.
Install a coverage tool to get gap analysis. Continuing.
```

---

## Check 6 — Project conventions (soft)

```bash
ls SKILL.md 2>/dev/null || ls .openclaw/CONVENTIONS.md 2>/dev/null
```

- ✅ Found → read SKILL.md (or CONVENTIONS.md) for project-specific conventions before context scan
- ❌ Not found → soft warning

```
🟡 WARNING — No project conventions found (no SKILL.md or conventions section).
Project-specific conventions won't be loaded. Continuing with defaults.
Consider documenting conventions inside SKILL.md (e.g., a "conventions" or "lessons" section) so tools and peers can load them automatically.
```

---

## Check 7 — hardshell (soft)

Check if `hardshell` skill is installed (OpenClaw locations):
```bash
ls ~/.openclaw/skills/hardshell/SKILL.md 2>/dev/null || \
ls SKILL.md 2>/dev/null
```

- ✅ Found → note for IMPLEMENT and VERIFY phases
- ❌ Not found → note, use built-in checklists

```
ℹ️  hardshell not detected in OpenClaw locations. Built-in quality checklists will be used.
Install hardshell in ~/.openclaw/skills/hardshell/ for enhanced security and architecture rules.
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
  REPOS.md         ✅  found / ⚠️  missing but optional
  Coverage tool    ✅  (nyc)
  Conventions (SKILL.md)   ⚠️  not found
  hardshell        ⚠️  not installed
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Status: READY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Or if hard stop:
```
  Status: ❌ STOPPED — see errors above
```