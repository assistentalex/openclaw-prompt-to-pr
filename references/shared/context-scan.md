# Context Scan Strategy

**Core rule: never read the whole codebase. Map → Filter → Read selectively.**

Budget for this phase: 40k tokens max.

---

## Step 1 — Map (cheap, ~2k tokens)

Get the full file tree without reading content.
Run from the **project root** (selected repo), not necessarily CWD:

```bash
cd {PROJECT_ROOT} && git ls-files | head -200
```

If no git:
```bash
cd {PROJECT_ROOT} && find . -type f \
  -not -path '*/node_modules/*' \
  -not -path '*/.git/*' \
  -not -path '*/dist/*' \
  -not -path '*/build/*' \
  -not -path '*/__pycache__/*' \
  -not -path '*/.venv/*' \
  | sort | head -200
```

Where `{PROJECT_ROOT}` is the repo selected during preflight (or specified via `--repo`).
All subsequent commands in context scan also run from `{PROJECT_ROOT}`.

From the file tree, identify:
- Primary language(s)
- Project structure pattern (MVC, layered, monorepo, etc.)
- Where the relevant code likely lives

---

## Step 2 — Filter (keyword-based, ~3k tokens)

Based on the task description, generate 3–6 keywords.

Examples:
- "add user authentication" → `auth, login, user, session, token, middleware`
- "fix email not sending" → `email, mail, smtp, send, notification, queue`
- "refactor payment module" → `payment, billing, invoice, stripe, charge, transaction`

Search for relevant files:
```bash
git grep -l "KEYWORD1\|KEYWORD2\|KEYWORD3" 2>/dev/null | head -30
```

Also always include:
- Entry points: `index.*`, `main.*`, `app.*`, `server.*`
- Config: `package.json`, `pyproject.toml`, `go.mod`, `Makefile`
- CLAUDE.md (if exists)

---

## Step 3 — Prioritize files

Classify each file into one of three tiers:

### Tier 1 — Core (read completely)
Files that will definitely be modified or are directly involved.
Budget: up to 15k tokens total across all Tier 1 files.

### Tier 2 — Adjacent (read signatures only)
Files that will be called or will call the modified code.
Read only: function/class signatures, imports, exports.
Skip: function bodies, inline comments.
Budget: up to 10k tokens.

### Tier 3 — Peripheral (read first 20 lines only)
Files that provide context but won't be touched.
Read only: file header, imports, main exports.
Budget: up to 5k tokens.

---

## Step 4 — Read selectively

### For Tier 1 files (full read):
```bash
cat path/to/file.ts
```

### For Tier 2 files (signatures only):
Read the file but mentally extract (or grep):
```bash
# Python: function/class signatures
grep -n "^def \|^class \|^async def " path/to/file.py

# TypeScript/JS: exports and function declarations  
grep -n "^export \|^function \|^const \|^class " path/to/file.ts

# Go: function signatures
grep -n "^func " path/to/file.go
```

### For Tier 3 files (header only):
```bash
head -20 path/to/file
```

---

## Step 5 — Build context summary

After reading, produce a compact summary (not a list of file contents):

```
PROJECT CONTEXT SUMMARY
─────────────────────────────────────────
Language: TypeScript (Node.js)
Framework: Express + Prisma
Test suite: Jest (npm test)
Architecture: Layered — routes → services → repositories

Relevant to task "add email verification":
  CORE:     src/services/user.service.ts (auth logic lives here)
            src/routes/auth.routes.ts (entry point)
  ADJACENT: src/middleware/auth.middleware.ts (will need to call)
            src/models/user.model.ts (schema to extend)
  PERIPHERAL: src/config/email.config.ts (email setup reference)

Files explicitly excluded (irrelevant):
  src/services/payment.service.ts
  src/routes/admin.routes.ts
  migrations/ (32 files)
─────────────────────────────────────────
Context used: 28k / 40k budget
```

---

## Files to always exclude

Never read these regardless of task:

```
node_modules/       .venv/          vendor/
dist/               build/          .next/
*.min.js            *.bundle.js     *.map
*.lock              package-lock.json  yarn.lock  poetry.lock
*.png  *.jpg  *.gif  *.svg  *.ico  *.woff  *.ttf
*.pdf  *.zip  *.tar
migrations/         (unless task is explicitly about migrations)
__pycache__/        .mypy_cache/    .pytest_cache/
.git/               .DS_Store       *.log
```

---

## If the codebase is too large (> 40k tokens of relevant files)

1. Read only Tier 1 files in full
2. For Tier 2: signatures only
3. Skip Tier 3 entirely, note what was skipped
4. Warn user:
```
⚠️ Large codebase detected. Read 12 core files (full) + 8 adjacent (signatures only).
Skipped 3 peripheral files to stay within context budget.
If I miss something important, tell me and I'll read that file specifically.
```
