# Mode: 📖 Document

**Flow:** Clarify → Scan gaps → Prioritize → Plan → ⛔ APPROVE → Write docs → Verify accuracy → ⛔ APPROVE → PR

Load `references/shared/clarify.md` for clarification rules.
Load `references/shared/state-system.md` for durable save/resume behavior.
**Phase numbering note:** phase numbers below are local to the mode workflow and begin after the shared PREFLIGHT and CONTEXT SCAN steps.

Core principle: **documentation describes what code does, not what you wish it did.**
If the code is unclear, ask — never invent behavior.
**Preflight note:** missing tests are a warning in this mode, not a blocker. If the work expands from documentation-only into behavior-changing edits, stop and require a minimal test suite first.

---

## Phase 1 — CLARIFY

Ask targeted clarification questions only when needed.
Clarify which documentation layer matters most and whether any behavior-changing edits are expected.
Persist clarify summary to `tasks/state.json` and `tasks/todo.md` before scanning gaps.

## Phase 2 — SCAN DOCUMENTATION GAPS

Check each documentation layer:

### Layer 1 — Inline code docs
```bash
# Python: functions without docstrings
grep -rn "^def \|^async def \|^class " --include="*.py" . | \
  grep -v '"""' | grep -v "test_" | grep -v "__init__"

# TypeScript: exported functions without JSDoc
grep -n "^export function\|^export const\|^export class\|^export async" \
  --include="*.ts" -r src/ | grep -v "\.test\."

# Go: exported functions without comments
grep -n "^func [A-Z]" --include="*.go" -r .
```

### Layer 2 — README
Check for:
- [ ] What is this project? (1-paragraph description)
- [ ] How to install / set up locally
- [ ] How to run (dev, test, build)
- [ ] Environment variables required
- [ ] How to contribute
- [ ] License

### Layer 3 — API documentation
If REST API exists:
- [ ] All endpoints documented (route, method, params, response, errors)
- [ ] Auth requirements documented
- [ ] Example requests/responses present

If GraphQL: schema docs.
If CLI tool: help text / man page.

### Layer 4 — Architecture / design docs
- [ ] High-level architecture explained
- [ ] Key design decisions recorded
- [ ] Non-obvious patterns explained

### Layer 5 — Changelog / history
- [ ] CHANGELOG.md exists and is up to date (lower priority)

---

## Phase 3 — GAP REPORT

```
DOCUMENTATION GAP ANALYSIS
─────────────────────────────────────────────────────────
Inline docs:
  Missing docstrings: 23 functions
    HIGH priority (business logic): 8 functions
    MEDIUM priority (utils): 11 functions
    LOW priority (tests/helpers): 4 functions

README.md:
  ✅ Description present
  ❌ Setup instructions missing (no local dev guide)
  ❌ Environment variables not listed
  ✅ Run commands present
  ❌ Contribution guide missing

API docs:
  ❌ No API documentation found
  Detected 14 routes in src/routes/
  Coverage: 0/14 documented

Architecture:
  ❌ No architecture doc found
─────────────────────────────────────────────────────────
Total gaps: significant
```

---

## Phase 4 — PLAN

Prioritize by impact: README first (most visible), then public API, then code docs.
Include plan metadata: Overall Risk, Confidence, Blast Radius, Rollback, Unknowns, and whether fast path is allowed.

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  📖 DOCUMENTATION PLAN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  TASK 1 — Complete README.md                    LOW
  Add: local setup guide, env variables list,
       contribution guide
  Est: ~50 lines

  TASK 2 — Document 8 core business functions   MEDIUM
  Files: user.service.ts, payment.service.ts
  Format: JSDoc with @param, @returns, @throws
  Est: ~40 lines of docs

  TASK 3 — Create API.md                        MEDIUM
  Document all 14 routes:
    method, path, auth required, params, response, errors
  Est: ~120 lines

  SKIP (lower priority):
  - 11 utility function docstrings (MEDIUM)
  - Architecture doc (HIGH effort, future task)
  - CHANGELOG (future task)

  Branch: docs/readme-and-api
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ⛔ CHECKPOINT 1 — Approve documentation plan?
  Reply: yes / modify / abort
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Auto-approve mode
If `NIGHT_SHIFT_AUTO_APPROVE=1` is set in the environment, the agent **auto-approves** this checkpoint with a logged note instead of waiting for user input.

Behavior in auto-approve mode:
- Log: "Auto-approved (night shift mode) — proceeding with implementation"
- Continue immediately
- Stash before IMPLEMENT still runs normally
```

---

## Phase 5 — WRITE DOCS

### JSDoc / docstring format

TypeScript:
```typescript
/**
 * Registers a new user and sends a verification email.
 *
 * @param data - User registration data (name, email, password)
 * @returns The created user object without the password field
 * @throws {ConflictError} If email is already registered
 * @throws {ValidationError} If required fields are missing or invalid
 */
async function registerUser(data: RegisterDTO): Promise<SafeUser> {
```

Python:
```python
async def register_user(data: RegisterDTO) -> SafeUser:
    """
    Register a new user and send a verification email.

    Args:
        data: User registration data containing name, email, and password.

    Returns:
        The created user object with password field excluded.

    Raises:
        ConflictError: If the email address is already registered.
        ValidationError: If required fields are missing or invalid.
    """
```

### README sections template

```markdown
## Getting Started

### Prerequisites
- Node.js 20+
- PostgreSQL 15+
- Redis (for sessions)

### Installation
\`\`\`bash
git clone {repo}
cd {project}
npm install
cp .env.example .env   # Edit with your values
npm run db:migrate
npm run dev
\`\`\`

### Environment Variables
| Variable | Required | Description | Example |
|---|---|---|---|
| DATABASE_URL | ✅ | PostgreSQL connection string | postgresql://... |
| JWT_SECRET | ✅ | Secret for signing tokens | any random 32+ char string |
| SMTP_HOST | ✅ | Email server host | smtp.gmail.com |
| REDIS_URL | ❌ | Redis URL (defaults to localhost) | redis://localhost:6379 |
```

### API doc format

```markdown
## POST /api/auth/register

Register a new user account.

**Auth required:** No

**Request body:**
\`\`\`json
{
  "name": "string (required)",
  "email": "string (required, valid email)",
  "password": "string (required, min 8 chars)"
}
\`\`\`

**Success response:** `201 Created`
\`\`\`json
{ "id": "uuid", "name": "string", "email": "string", "createdAt": "ISO date" }
\`\`\`

**Error responses:**
| Code | Reason |
|---|---|
| 400 | Missing or invalid fields |
| 409 | Email already registered |
| 500 | Server error |
```

### When code is unclear — ask, don't invent
```
❓ I'm documenting `calculateFinalPrice()` in pricing.service.ts
but I'm not sure how the `discountStack` parameter works.

Looking at the code, it seems to apply discounts in order, but
I'm not certain if they stack multiplicatively or additively.

Can you clarify so I document the actual behavior?
```

---

## Phase 6 — VERIFY ACCURACY

For every documentation item written:
1. Cross-reference with actual code — does the doc match what the code does?
2. Check @param names match actual parameter names
3. Check @throws errors are actually thrown in that function
4. Check example values are realistic and valid

If the documentation produces a previewable output (rendered README/docs site, generated HTML/docs artifact, email/template output), propose 1–2 concrete preview tests before PR/commit.
Default shape:
- Test 1: happy path preview
- Test 2: edge / empty / failure preview

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ✅ DOCS VERIFIED — 📖 Document
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  README.md:     completed ✅ (+3 sections)
  Docstrings:    8/8 functions documented ✅
  API.md:        14/14 routes documented ✅
  Accuracy:      all cross-referenced with code ✅

  Files changed: 4
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ⛔ CHECKPOINT 2 — Approve to create PR?
  Reply: yes / request changes / abort
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Auto-approve mode
If `NIGHT_SHIFT_AUTO_APPROVE=1` is set in the environment, the agent **auto-approves** this checkpoint with a logged note instead of waiting for user input.

Behavior in auto-approve mode:
- Log: "Auto-approved (night shift mode) — creating PR"
- Continue immediately
- If tests failed after 2 retries → STOP and report failure (do NOT auto-approve past failures)
```

---

## Phase 7 — PR

Load `references/shared/pr-format.md`.
Use `docs/` prefix for branch.
List what was documented in PR body.

Commit format: `docs(api): add README setup guide and API reference`
