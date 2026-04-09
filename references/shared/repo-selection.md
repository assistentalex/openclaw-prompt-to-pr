# Repo Selection Policy

Canonical rules for discovering and selecting the target repo.
Use this file as the source of truth whenever prompt-to-pr needs to decide **where** to work.

---

## Core rule

**Auto-detect first, ask only when ambiguous.**

1. If the user specified `--repo <path>` or clearly named a project → use that repo directly.
2. If only one candidate git repo is found → use it silently.
3. If multiple candidate repos are found → show a **single combined menu** for mode + repo selection.
4. If discovery is partial because tools are limited → say discovery was partial and ask the user to choose from the candidates found.

**Never** ask two separate questions when one combined choice will do.
**Never** ask for repo selection before you know whether the repo is actually ambiguous.

---

## Discovery sources

Check candidate repos in this order:

1. Workspace git repo(s)
2. Installed skill repos under `~/.openclaw/skills/`
3. Installed bundled skill repos under `~/.npm-global/lib/node_modules/openclaw/skills/`
4. Recent GitHub repos if `gh` is available and authenticated

For each candidate, detect when possible:
- path
- primary language
- test framework
- rough test count

If any metadata cannot be detected, keep the repo in the list and mark unknown fields as `unknown`.

---

## Fallback rules

- If `gh` is missing or not authenticated → skip GitHub discovery.
- If shell access is restricted → inspect likely repo roots with available file reads.
- If discovery remains incomplete → surface the discovered candidates and state that discovery was partial.
- If no candidate repos are found at all → stop and tell the user prompt-to-pr needs a git repo.

---

## Menu contract

If repo selection is needed, it must appear inside the same prompt as mode selection.

Example shape:

```text
🚀 prompt-to-pr — ce facem și unde?

  [1] Feature      [4] Refactor
  [2] Bug Fix      [5] Tests
  [3] Review       [6] Docs

  Repos:
    [a] ~/repo-a
    [b] ~/repo-b

  Type e.g. "1a" or describe what you need.
```
