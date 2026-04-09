# Mode Policy Matrix

Canonical policy for what each prompt-to-pr mode is allowed to do and what preflight must enforce.
Use this file as the source of truth whenever prompt-to-pr needs to decide **how strict** to be.

---

| Mode | Code changes allowed | Tests required to continue | Coverage required | PR allowed |
|---|---:|---|---|---:|
| 🚀 Feature | Yes | **Required** | Recommended | Yes |
| 🐛 Bug Fix | Yes | **Required** | Recommended | Yes |
| ♻️ Refactor | Yes | **Required** | Recommended | Yes |
| 🧪 Test Coverage | Yes | **Required** | **Required for coverage analysis** | Yes |
| 🔍 Review | No (read-only) | Warning only | No | No |
| 📖 Document | Yes, but documentation-first | Warning only unless work expands into behavior-changing edits | No | Yes |

---

## Enforcement rules

### Hard-stop modes
- 🚀 Feature
- 🐛 Bug Fix
- ♻️ Refactor
- 🧪 Test Coverage

If no test suite is detected in these modes, stop and ask for a minimal test setup.

### Warning-only modes
- 🔍 Review
- 📖 Document

If no test suite is detected in these modes, warn and continue.
For 📖 Document, stop if the work expands from documentation-only into behavior-changing edits.

### Coverage handling
- Coverage tooling is mandatory only for 🧪 Test Coverage mode.
- In all other modes, missing coverage tooling is a warning, not a blocker.
