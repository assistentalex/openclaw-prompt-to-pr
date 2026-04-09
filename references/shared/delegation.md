# Delegation Hooks

Canonical guidance for optional multi-agent delegation in prompt-to-pr.
This is a foundation document: define where delegation is allowed without requiring it yet.

---

## Principle

Delegate only when it reduces risk or latency without fragmenting the workflow.
The parent workflow remains responsible for the final plan, approvals, verify summary, and durable state.

---

## Good delegation points

- Context scan in a very large repo
- Review-mode analysis on a narrow subsystem
- Test-gap analysis for coverage work
- PR feedback triage when comments are numerous

---

## Do not delegate

- final approval checkpoints
- final verify decision
- branch/PR claims to the user
- destructive operations without direct parent review

---

## Persistence rule

If delegation is used, record in `tasks/state.json`:
- delegated subtask
- target scope
- returned summary
- whether the parent accepted the result

Do not leave delegated work only in chat history.
