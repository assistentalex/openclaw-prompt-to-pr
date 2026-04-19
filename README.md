# prompt-to-pr

**Full AI-assisted development workflow — from a single prompt to a ready-to-merge PR.**

An OpenClaw skill that orchestrates the entire development cycle: from a natural-language description to a reviewed, tested, and documented Pull Request. Built for AI agents working with Git repositories.

## Features

- **7 workflow modes** — New Feature, Bug Fix, Code Review, Refactor, Test Coverage, Document, PR Feedback
- **Active context management** — stays within 200k token budget by scanning selectively, not reading everything
- **2 approval checkpoints per mode** — you approve the plan and the final result, nothing ships without you
- **hardshell integration** — enhanced code review when the hardshell skill is installed
- **Resume capability** — abort anytime, pick up where you left off

## Modes

| Mode | Trigger words | What it does |
|------|--------------|--------------|
| 🚀 New Feature | implement, add, build, create feature | Plan → implement → test → PR |
| 🐛 Bug Fix | fix, bug, broken, error, crash | Reproduce → root cause → fix → verify |
| 🔍 Code Review | review, check my code, look at this | Structured analysis report (read-only) |
| ♻️ Refactor | refactor, clean up, reorganize | Clean code without changing behavior |
| 🧪 Test Coverage | test, coverage, missing tests | Gap analysis → write missing tests |
| 📖 Document | document, docs, readme, docstring | Scan gaps → prioritize → write docs |

## Installation

### Via ClawHub (recommended)

```bash
clawhub install prompt-to-pr
```

### Manual

1. Download or clone this repository into your OpenClaw skills directory:
   ```bash
   git clone https://github.com/asistent-alex/openclaw-prompt-to-pr.git \
     ~/.openclaw/skills/prompt-to-pr
   ```

2. Restart OpenClaw or reload skills.

## Usage

### Recommended local prerequisite

Keep a minimal human-readable repo inventory in `REPOS.md`.
Use it as a simple local map so the user and the agent can disambiguate repo names, paths, aliases, and important subprojects.

Recommended fields per entry:
- Path
- Alias
- Type
- Status

Keep `REPOS.md` factual and lightweight.
If something needs richer description, put it in the repo's own docs instead of expanding the inventory schema.


### Start with `/ptopr`

Use `/ptopr` in the current repo if it is already clear, or provide a repo explicitly with `--repo`.

| Command | Mode |
|---|---|
| `/ptopr` | Start in current repo if clear; otherwise ask for repo |
| `/ptopr --repo /path/to/repo` | Select repo explicitly |
| `/ptopr feature` | 🚀 New Feature |
| `/ptopr fix` | 🐛 Bug Fix |
| `/ptopr review` | 🔍 Code Review |
| `/ptopr refactor` | ♻️ Refactor |
| `/ptopr test` | 🧪 Test Coverage |
| `/ptopr docs` | 📖 Document |
| `/ptopr pr-feedback` | 🗨️ PR Feedback |

You can also describe what you want to do:

```
"Implement a login page"       → 🚀 New Feature
"Fix the payment crash"        → 🐛 Bug Fix
"Review the auth module"       → 🔍 Code Review
"Refactor the database layer"  → ♻️ Refactor
"Write tests for utils.py"     → 🧪 Test Coverage
"Document the API endpoints"   → 📖 Document
"Address PR comments"          → 🗨️ PR Feedback
```

If the repo is unclear, the skill prefers the local repo map in `REPOS.md` when available; otherwise it asks directly for a repo path.
If the intent is unclear but the repo is already clear, it shows the mode menu.
If you do not have a repo yet, create one first, record it in `REPOS.md`, then run `/ptopr` again.

### Workflow Overview

```
PREFLIGHT → CONTEXT SCAN → MODE TRIAGE → MODE WORKFLOW → PR
```

Every mode follows the same guardrails:
1. **PREFLIGHT** — checks Git, tests, tools (hard stops if missing)
2. **CONTEXT SCAN** — maps the codebase, reads only what's needed
3. **MODE TRIAGE** — auto-detect or manually pick a mode
4. **MODE WORKFLOW** — each mode has phases with 2 approval checkpoints
5. **PR** — commit, branch, and PR created only after your final approval

### Approval Checkpoints

You always approve twice per mode:
- **Checkpoint 1:** After the plan is presented
- **Checkpoint 2:** After implementation, before PR

Nothing is committed or pushed without your explicit "yes".

## Development

### Prerequisites

- Python 3.8+
- pytest

### Running tests

```bash
python3 -m pytest tests/ -v
```

### No repo yet?

prompt-to-pr still requires Git. Recommended bootstrap for a brand-new project:

```bash
mkdir <project-name>
cd <project-name>
git init
printf "# <project-name>\n" > README.md
git add .
git commit -m "chore: initial commit"
```

After creation, record it in:
- `REPOS.md` — minimal human-readable inventory

### Project structure

```
prompt-to-pr/
├── SKILL.md                    # Main skill definition
├── references/
│   ├── shared/                 # Cross-mode references
│   │   ├── preflight.md        # Preflight check rules
│   │   ├── context-scan.md     # How to scan codebase selectively
│   │   ├── context-budget.md   # Token budget tracking
│   │   ├── compression.md      # Phase compression rules
│   │   ├── plan-format.md      # tasks/todo.md format
│   │   └── pr-format.md        # Commit/branch/PR conventions
│   └── modes/                  # Mode-specific workflows
│       ├── feature.md
│       ├── bugfix.md
│       ├── review.md
│       ├── refactor.md
│       ├── test-coverage.md
│       └── document.md
├── tests/
│   └── test_smoke.py
├── pyproject.toml
└── .gitignore
```

## License

MIT