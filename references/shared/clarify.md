# Clarification Phase

Canonical rules for the pre-plan clarification step.
Use this file when the task is ambiguous, underspecified, risky, or likely to branch into multiple valid implementations.

---

## Goal

Clarify the task before planning so the plan reflects the real user intent.

Ask **at most 3–5 targeted questions**.
If the task is already clear and low-risk, skip clarification and record why it was skipped.

---

## When to clarify

Clarify when one or more of these are true:
- scope is ambiguous
- success criteria are unclear
- multiple repos or multiple modules are plausible
- risk is medium/high
- user constraints are missing
- the task could be solved in meaningfully different ways

Skip clarification when all are true:
- task is specific
- repo is clear
- scope is narrow
- success criteria are obvious
- risk is low

---

## Question categories

Prefer questions in this order:
1. Goal / success criteria
2. Scope boundaries (what is in/out)
3. Constraints (tech, style, security, performance, deadlines)
4. Validation expectations (tests, review, deploy implications)
5. Missing artifacts (logs, errors, examples, screenshots)

---

## Output contract

After clarification, persist:
- questions asked
- answers received
- assumptions made
- open questions still unresolved
- whether clarification was skipped or completed

This information must be written to `tasks/state.json` and summarized in `tasks/todo.md`.

---

## Example

```text
CLARIFY SUMMARY
- Goal: add PR feedback handling after review comments
- In scope: parse review comments, group them, propose fix plan
- Out of scope: direct GitHub API integration in v2 batch 1
- Constraints: keep current approval model; no forced PR creation
- Open question: should PR feedback be a new mode or folded into review?
```
