# Repo Selection Policy

Canonical rules for selecting the target repo.
Use this file as the source of truth whenever prompt-to-pr needs to decide **where** to work.

---

## Core rule

**Be explicit first, local second, ask directly otherwise.**

1. If the user specified `--repo <path>` or clearly named a project/path → use that repo directly.
2. If the current working directory is already inside a git repo → use that repo silently.
3. If the repo is still unclear → ask the user directly for the repo path or project name.

**Never** start prompt-to-pr by scanning installed skills, bundled skills, or recent GitHub repos.
**Never** make startup repo selection depend on broad multi-source discovery.
**Never** ask two separate questions when one direct repo prompt will do.

---

## Startup contract

The startup path should stay predictable:

- explicit `--repo` wins
- current repo is the only implicit default
- otherwise ask for a repo path

This means prompt-to-pr should prefer:
- "working in current repo"
- or "give me `--repo <path>`"

instead of trying to assemble a smart list from many locations.

---

## Fallback rules

- If shell access is restricted → ask the user for `--repo <path>` or a project path/name.
- If the current directory is not inside a git repo → do not search broadly; ask for a repo path.
- If the user explicitly asks to browse candidates → keep the list narrow and local, and be honest if it is partial.
- If no repo is available at all → stop and tell the user prompt-to-pr needs a git repo.

If metadata cannot be detected for a user-provided repo, continue with unknown fields marked as `unknown` rather than expanding discovery scope.

---

## Prompt contract

If repo selection is needed, prefer a direct prompt over a discovery menu.

Example shape:

```text
🚀 prompt-to-pr — am nevoie de repo.

Trimite un path Git repo sau pornește comanda cu:
  /ptopr --repo /path/to/repo

Dacă ești deja în repo-ul corect, rulează /ptopr de acolo.
```
