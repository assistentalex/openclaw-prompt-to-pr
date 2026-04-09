# Review Scope Presets

Canonical presets for code review mode.
Use these presets so review requests are faster to specify and easier to resume.

---

## Presets

### 1. Diff since main
Review all changes since the default branch.
Best for pre-merge review.

### 2. Changed files only
Review only files changed in the working tree or current branch.
Best for local work-in-progress.

### 3. Specific path
Review a specific file or directory.
Best for focused module review.

### 4. PR or commit range
Review a PR branch, PR number, or explicit commit range.
Best for targeted historical review.

### 5. Security boundaries
Prioritize auth, input validation, secrets, dangerous sinks, and permission checks.
Best for high-risk surfaces.

### 6. Test gaps
Prioritize missing happy-path, edge-case, and error-path coverage.
Best for stabilization work.

### 7. Architecture smells
Prioritize layering violations, coupling, circular dependencies, and oversized functions/modules.
Best for refactor planning.

---

## Output contract

Persist the selected preset in `tasks/state.json`.
Include it in the review report summary and in `tasks/todo.md`.

If the user gives no scope, present these presets first.
If the user gives a scope directly, map it to the nearest preset and record that mapping.
