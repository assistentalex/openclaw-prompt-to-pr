# Release Readiness Summary

Canonical format for post-verify readiness reporting.
Use this after VERIFY in Feature, Bug Fix, and Refactor modes.

---

## Goal

Summarize whether the change is actually ready to merge or deploy, not just whether code was edited.

---

## Required sections

```text
RELEASE READINESS
- Scope: what changed
- Verification: what was tested / checked
- Risk: low / medium / high
- Known limitations: ...
- Rollback note: ...
- Merge readiness: yes / no
```

---

## Guidance

- Keep it honest and short
- Mention known gaps explicitly
- Do not say "ready" if verify is incomplete
- If rollback is unclear, say so instead of guessing
