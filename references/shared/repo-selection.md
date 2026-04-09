# Repo Selection Policy

Canonical rules for selecting the target repo.
Use this file as the source of truth whenever prompt-to-pr needs to decide **where** to work.

---

## Selection order (highest priority first)

1. **Explicit `--repo <path>`** — if the user provides an explicit path, use it directly.
2. **Current Git repo** — if the command is run inside a Git repository, use that repo silently.
3. **Alias match** — if the user provides a name that matches an alias in the repo registry, use the mapped path.
4. **Recent repos** — if no explicit repo and not in a Git repo, suggest from the registry's `recentRepos` list (most recent first).
5. **Bounded local discovery** — if the user wants to browse, list repositories found only under the configured local roots in the registry.
6. **Manual path** — fall back to asking the user for an explicit repo path.

---

## Core rule

**Be explicit first, then use current repo, then consult the registry, then ask directly.**

---

## Startup contract

The startup path should stay predictable:

- explicit `--repo` wins
- current repo is the only implicit default from the environment
- otherwise, use the repo registry (aliases, recents, bounded discovery) to suggest options
- if the user wants to browse, show only repos from the configured local roots
- if no repo is available, ask for a path

This means prompt-to-pr should prefer:
- "working in current repo"
- or "give me `--repo <path>`"
- or "pick from your recent repos"
- or "browse your local roots"

instead of trying to assemble a smart list from many locations at startup.

---

## Fallback rules

- If shell access is restricted → ask the user for `--repo <path>` or a project path/name.
- If the current directory is not inside a git repo → do not search broadly; use the registry or ask for a repo path.
- If the user explicitly asks to browse candidates → keep the list narrow and local (bounded by registry roots), and be honest if it is partial.
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

Sau, dacă vrei să alegeri dintre repo-urile cunoscute:
  /ptopr --repo ?
```

---

## Repo Registry

Load `references/shared/repo-registry.md` for the canonical design of the persistent repo registry used by this policy.

The registry defines:
- `roots`: bounded local discovery scope
- `aliases`: human-readable names for quick access
- `recentRepos`: list of recently used repos
- `lastActiveRepo`: the repo from the last successful run

The registry is optional and meant to enhance UX — if missing, prompt-to-pr falls back to explicit `--repo`, current repo, or direct path prompt.