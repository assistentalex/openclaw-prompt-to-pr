# Repo Selection Policy

Canonical rules for selecting the target repo.
Use this file as the source of truth whenever prompt-to-pr needs to decide **where** to work.

---

## Selection order (highest priority first)

1. **Explicit `--repo <path>`** — if the user provides an explicit path, use it directly.
2. **Current Git repo** — if the command is run inside a Git repository, use that repo silently.
3. **REPOS.md** — if present and repo is still unclear, use it as the local repo map.
4. **Manual path** — fall back to asking the user for an explicit repo path.

---

## Core rule

**Be explicit first, then use current repo, then consult `REPOS.md` if available, then ask directly.**

---

## Startup contract

The startup path should stay predictable:

- explicit `--repo` wins
- current repo is the only implicit default from the environment
- otherwise, consult `REPOS.md` if it exists
- if no clear repo emerges, ask for a path

This means prompt-to-pr should prefer:
- "working in current repo"
- or "give me `--repo <path>`"
- or "use the local repo map in `REPOS.md`"

instead of trying to assemble a smart list from many locations at startup.

---

## Fallback rules

- If shell access is restricted → ask the user for `--repo <path>` or a project path/name.
- If the current directory is not inside a git repo → do not search broadly; consult `REPOS.md` if it exists, otherwise ask for a repo path.
- If `REPOS.md` is missing → continue, but recommend creating it as the local repo map.
- If no repo is available at all → stop and tell the user prompt-to-pr needs a git repo, recommend creating one, and suggest recording it in `REPOS.md`.

If metadata cannot be detected for a user-provided repo, continue with unknown fields marked as `unknown` rather than expanding discovery scope.

---

## Prompt contract

If repo selection is needed, prefer a direct prompt.

Example shape:

```text
🚀 prompt-to-pr — am nevoie de repo.

Trimite un path Git repo sau pornește comanda cu:
  /ptopr --repo /path/to/repo

Dacă ești deja în repo-ul corect, rulează /ptopr de acolo.
```

---

Keep `REPOS.md` as the minimal human-readable repo map for names, paths, aliases, type, and status.
If it does not exist yet, recommend creating it, but do not block the workflow on it.
