# Mode: 🧪 Test Coverage

**Flow:** Coverage report → Gap analysis → Plan → ⛔ APPROVE → Write tests → Verify coverage delta → ⛔ APPROVE → PR

**Phase banner mandatory:** Display `[FAZA N/M — ...]` banner as the FIRST action of every phase. See ⛔ MANDATORY in SKILL.md.

---

## Phase 1 — COVERAGE REPORT

### Check for coverage tool
```bash
# Jest
npx jest --coverage 2>/dev/null

# pytest
pytest --cov=. --cov-report=term-missing 2>/dev/null

# Go
go test ./... -cover 2>/dev/null

# NYC (older Jest setups)
npx nyc npm test 2>/dev/null
```

**If no coverage tool found → HARD STOP:**
```
🔴 STOP — No coverage tool detected.

Cannot run gap analysis without a coverage tool.

Install one:
  # Jest (already using Jest)
  jest.config.js → add: collectCoverage: true, coverageThreshold: {}

  # pytest
  pip install pytest-cov

  # Go — built in, no install needed

  # Istanbul/nyc
  npm install --save-dev nyc

Then restart prompt-to-pr in 🧪 Test Coverage mode.
```

---

## Phase 2 — GAP ANALYSIS

Parse coverage output and identify uncovered areas.

Prioritize by:
1. **Business logic** — highest priority (services, use cases, domain logic)
2. **Error paths** — second priority (catch blocks, validation failures)
3. **Utility functions** — third priority
4. **Boilerplate / generated code** — skip (ORM migrations, auto-generated types)

### Gap analysis report
```
COVERAGE GAP ANALYSIS
─────────────────────────────────────────────────────────
Overall coverage: 58% (target: 80% on business logic)

Top uncovered areas (by business impact):

  src/services/payment.service.ts         12% coverage
    Uncovered: processRefund(), validateCard(), handleDecline()
    Risk: HIGH — financial logic with no test safety net

  src/services/notification.service.ts    34% coverage
    Uncovered: sendPushNotification(), error retry logic
    Risk: MEDIUM — user-facing feature

  src/utils/date.utils.ts                 0% coverage
    Uncovered: all 8 utility functions
    Risk: LOW — pure functions, easy to test

  src/middleware/rate-limiter.ts          45% coverage
    Uncovered: edge cases (burst, whitelist logic)
    Risk: MEDIUM — security boundary

SKIPPED (boilerplate/generated):
  prisma/generated/  — auto-generated, skip
  src/db/migrations/ — migration files, skip
─────────────────────────────────────────────────────────
```

---

## Phase 3 — PLAN

Load `references/shared/plan-format.md`.

Present test plan sorted by priority (business impact first).

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🧪 TEST COVERAGE PLAN
  Current: 58% → Target: 80% (business logic)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  PRIORITY 1 — payment.service.ts (12% → target 80%)
  Tests to write:
    - processRefund(): happy path, already refunded, invalid amount
    - validateCard(): valid card, expired, invalid format
    - handleDecline(): soft decline, hard decline, retry logic
  Est: ~12 tests, ~80 lines

  PRIORITY 2 — rate-limiter.ts (45% → target 80%)
  Tests to write:
    - Burst requests (should block at threshold)
    - Whitelist bypass (whitelisted IPs should pass)
    - Reset after window expires
  Est: ~6 tests, ~50 lines

  PRIORITY 3 — date.utils.ts (0% → 100%)
  Tests to write: all 8 pure functions, happy + edge cases
  Est: ~16 tests, ~60 lines

  SKIP: notification.service.ts (requires external mock setup — mark as future)

  Branch: test/payment-and-ratelimiter-coverage
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ⛔ CHECKPOINT 1 — Approve test plan?
  Reply: yes / modify / abort
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Phase 4 — WRITE TESTS

### Test quality rules

Every test must follow this structure:
```
Arrange → Act → Assert
```

Each test must:
- Test one behavior only (one assertion concept per test)
- Have a descriptive name: `should {do what} when {condition}`
- Be isolated — no shared state between tests
- Not test implementation details — test behavior from the outside

### Test categories to write per function

For each function, write:
1. **Happy path** — normal input, expected output
2. **Edge cases** — empty input, zero, max value, boundary conditions
3. **Error paths** — invalid input, external service failure, permission denied

Example for `processRefund(orderId, amount)`:
```typescript
describe('processRefund', () => {
  it('should refund full amount when order exists and is refundable', ...)
  it('should throw AlreadyRefundedError when order was already refunded', ...)
  it('should throw InvalidAmountError when amount exceeds original', ...)
  it('should throw OrderNotFoundError when orderId does not exist', ...)
  it('should handle payment gateway timeout with retry', ...)
})
```

### Mocking rules
- Mock external services (payment gateway, email, DB in unit tests)
- Do not mock the code under test
- Integration tests should use real DB (test database / in-memory)
- Name mocks clearly: `mockPaymentGateway`, not just `mock`

---

## Phase 5 — VERIFY COVERAGE DELTA

### Run coverage again
```bash
npm test -- --coverage
```

Compare before and after:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ✅ COVERAGE DELTA — 🧪 Test Coverage
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Overall:                    58% → 74% (+16%)

  payment.service.ts          12% → 83% ✅
  rate-limiter.ts             45% → 81% ✅
  date.utils.ts                0% → 100% ✅

  Tests added: 34
  All new tests: passing ✅
  Pre-existing tests: all still passing ✅
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ⛔ CHECKPOINT 2 — Approve PR?
  Reply: yes / request changes / abort
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**If coverage did not reach target:** explain why and what would be needed to reach it.

---

## Phase 6 — PR

Load `references/shared/pr-format.md`.
Use `test/` prefix for branch.
Include Coverage Delta table in PR body.

Commit format: `test(payment): add coverage for refund and validation flows`
