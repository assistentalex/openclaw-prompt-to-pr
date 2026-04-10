# No-Repo Onboarding

Use this reference when the user wants to use prompt-to-pr but does **not** have a Git repo yet.

## Goal

Turn "I have an idea but no repo" into a clean starting point without pretending prompt-to-pr can work without Git.

## Canonical behavior

If no repo exists yet:
1. **STOP the workflow** — prompt-to-pr still requires a Git repo.
2. **Offer two clear paths:**
   - clone an existing repo
   - create a new local repo
3. **Recommend recording the repo in a human-readable inventory** (`REPOS.md`) once created.
4. **Mark whether it should enter prompt-to-pr selection** using `Registry: yes/no`.
5. **If the machine registry is in use and the entry is `Registry: yes`, also add it there** after first successful run.

## Suggested user-facing response

```text
🔴 STOP — prompt-to-pr needs a Git repo before it can plan, branch, test, and prepare a PR.

If you already have a remote repo:
  git clone <url>
  cd <repo>
  /ptopr ...

If this is a brand new project, recommended bootstrap:
  mkdir <project-name>
  cd <project-name>
  git init
  printf "# <project-name>\n" > README.md
  git add .
  git commit -m "chore: initial commit"

Then record it in:
  - REPOS.md (human-readable inventory; include `Registry: yes/no`)
  - prompt-to-pr repo registry (optional machine-readable helper, only when `Registry: yes`)
```

## Recommendation policy

When the user has no repo yet, prefer recommending **creation** over leaving them stuck.
The agent should be helpful and concrete, but should not pretend prompt-to-pr can continue without Git.

## Minimal bootstrap advice

For a new repo, recommend at least:
- project folder
- `git init`
- a tiny `README.md`
- first commit
- optionally a minimal smoke test, depending on language

## Why REPOS.md matters

`REPOS.md` is the human-readable companion to the repo registry.
It helps the user and the agent remember:
- repo names
- paths
- aliases
- active vs archived status
- whether the repo should be synced into prompt-to-pr selection (`Registry: yes/no`)
- nested subprojects that are not separate repos
