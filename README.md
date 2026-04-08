# prompt-to-pr

**Full AI-assisted development workflow — from a single prompt to a ready-to-merge PR.**

An OpenClaw skill that orchestrates the entire development cycle: from a natural-language description to a reviewed, tested, and documented Pull Request. Built for AI agents working with Git repositories.

## Features

- **6 workflow modes** — New Feature, Bug Fix, Code Review, Refactor, Test Coverage, Document
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
   git clone https://github.com/assistentalex/openclaw-prompt-to-pr.git \
     ~/.openclaw/skills/prompt-to-pr
   ```

2. Restart OpenClaw or reload skills.

## Usage

Just describe what you want to do. The skill auto-detects the mode from your message:

```
"Implement a login page"       → 🚀 New Feature
"Fix the payment crash"        → 🐛 Bug Fix
"Review the auth module"       → 🔍 Code Review
"Refactor the database layer"  → ♻️ Refactor
"Write tests for utils.py"     → 🧪 Test Coverage
"Document the API endpoints"   → 📖 Document
```

If the intent is unclear, the skill shows a mode menu to pick from.

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