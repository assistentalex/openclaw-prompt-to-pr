# Repo Registry Design

The repo registry is a persistent JSON file that stores known repositories for quick selection.

**Location:** `~/.openclaw/workspace/prompt-to-pr-repo-registry.json`

---

## Schema

```json
{
  "version": 1,
  "roots": [
    "~/.openclaw/skills",
    "~/projects"
  ],
  "aliases": {
    "ptopr": "~/.openclaw/skills/prompt-to-pr",
    "imm": "~/.openclaw/skills/imm-romania"
  },
  "recentRepos": [
    {
      "path": "~/.openclaw/skills/prompt-to-pr",
      "lastUsed": "2026-04-09T17:52:00Z"
    }
  ],
  "lastActiveRepo": "~/.openclaw/skills/prompt-to-pr"
}
```

---

## Fields

### `roots`

Array of local directory roots. When `--repo ?` is used, bounded local discovery scans only these roots (non-recursively or with depth 1) for Git repositories.

**Purpose:** Scope discovery so it stays fast and predictable.

### `aliases`

Short human-readable names mapped to repo paths. When a user provides a name that matches an alias, resolve it directly instead of searching.

**Purpose:** Quick access — `/ptopr --repo ptopr` instead of the full path.

### `recentRepos`

List of recently used repos with timestamps, sorted by most recent first.

**Purpose:** Present the most likely candidates first when repo selection is ambiguous.

### `lastActiveRepo`

The repo path from the last successful prompt-to-pr run.

**Purpose:** Default suggestion if no other selection is available.

---

## Lifecycle

1. **On startup** — if the registry file exists, load it. If not, continue without it (registry is optional).
2. **On repo selection** — update `lastActiveRepo` and add/update the entry in `recentRepos` (keep last 10, deduplicated by path).
3. **On `--repo ?`** — present:
   - Aliases first (if any)
   - Recent repos (most recent first)
   - Repos discovered under `roots` (depth 1)
4. **On alias usage** — resolve the alias to its path and proceed.

---

## Fallback

If the registry file is missing or corrupted:
- Prompt-to-pr falls back to explicit `--repo`, current repo detection, or asking for a path.
- Never block the workflow on a missing registry.

---

## Privacy

- The registry contains only local paths and timestamps.
- Never include remote URLs, credentials, or personal data.
- The file is local to the workspace and never synced externally.