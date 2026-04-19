"""Smoke and regression tests for the prompt-to-pr skill docs."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "SKILL.md"
README = ROOT / "README.md"
CONTRIBUTING = ROOT / "CONTRIBUTING.md"
CHANGELOG = ROOT / "CHANGELOG.md"
GITIGNORE = ROOT / ".gitignore"
PREFLIGHT = ROOT / "references" / "shared" / "preflight.md"
CONTEXT_SCAN = ROOT / "references" / "shared" / "context-scan.md"
REPO_SELECTION = ROOT / "references" / "shared" / "repo-selection.md"
NO_REPO_ONBOARDING = ROOT / "references" / "shared" / "no-repo-onboarding.md"
MODE_POLICY = ROOT / "references" / "shared" / "mode-policy.md"
STATE_SYSTEM = ROOT / "references" / "shared" / "state-system.md"
CLARIFY = ROOT / "references" / "shared" / "clarify.md"
FAST_PATH = ROOT / "references" / "shared" / "fast-path.md"
REVIEW_PRESETS = ROOT / "references" / "shared" / "review-presets.md"
PR_FEEDBACK_FORMAT = ROOT / "references" / "shared" / "pr-feedback-format.md"
RELEASE_READINESS = ROOT / "references" / "shared" / "release-readiness.md"
DELEGATION = ROOT / "references" / "shared" / "delegation.md"
CONTEXT_POLICY = ROOT / "references" / "shared" / "context-policy.md"
PR_FEEDBACK_MODE = ROOT / "references" / "modes" / "pr-feedback.md"


def test_smoke():
    """If this passes, pytest is correctly configured."""
    assert True


def test_skill_file_exists():
    """Verify SKILL.md is present in the project root."""
    assert SKILL.is_file(), f"SKILL.md not found at {SKILL}"


def test_references_directory_exists():
    """Verify the references directory structure exists."""
    refs = ROOT / "references"
    assert refs.is_dir(), "references/ directory not found"
    assert (refs / "shared").is_dir(), "references/shared/ not found"
    assert (refs / "modes").is_dir(), "references/modes/ not found"


def test_shared_policy_files_exist():
    """Verify shared policy files exist for deduplicated rules."""
    assert REPO_SELECTION.is_file(), f"Missing {REPO_SELECTION}"
    assert NO_REPO_ONBOARDING.is_file(), f"Missing {NO_REPO_ONBOARDING}"
    assert MODE_POLICY.is_file(), f"Missing {MODE_POLICY}"
    assert STATE_SYSTEM.is_file(), f"Missing {STATE_SYSTEM}"
    assert CLARIFY.is_file(), f"Missing {CLARIFY}"
    assert FAST_PATH.is_file(), f"Missing {FAST_PATH}"
    assert REVIEW_PRESETS.is_file(), f"Missing {REVIEW_PRESETS}"
    assert PR_FEEDBACK_FORMAT.is_file(), f"Missing {PR_FEEDBACK_FORMAT}"
    assert RELEASE_READINESS.is_file(), f"Missing {RELEASE_READINESS}"
    assert DELEGATION.is_file(), f"Missing {DELEGATION}"
    assert CONTEXT_POLICY.is_file(), f"Missing {CONTEXT_POLICY}"
    assert PR_FEEDBACK_MODE.is_file(), f"Missing {PR_FEEDBACK_MODE}"
    assert GITIGNORE.is_file(), f"Missing {GITIGNORE}"


def test_preflight_has_repo_selection_and_repos_md_sections():
    """Verify preflight.md contains repo selection plus a soft REPOS.md check."""
    content = PREFLIGHT.read_text()
    assert "## Check 2 — Repo selection" in content
    assert "references/shared/repo-selection.md" in content
    assert "avoid broad startup discovery" in content
    assert "## Check 3 — REPOS.md (soft)" in content
    assert "REPOS.md not found" in content
    assert "references/shared/repo-registry.md" not in content


def test_repo_selection_policy_prefers_explicit_current_repo_and_repos_md():
    """Verify the canonical repo-selection policy prefers explicit/current selection, then REPOS.md."""
    content = REPO_SELECTION.read_text()
    assert "explicit `--repo` wins" in content
    assert "current repo is the only implicit default" in content
    assert "REPOS.md" in content
    assert "Be explicit first, then use current repo, then consult `REPOS.md` if available, then ask directly" in content
    assert "Alias match" not in content
    assert "Recent repos" not in content
    assert "Bounded local discovery" not in content


def test_preflight_repo_selection_is_direct_not_discovery_heavy():
    """Verify preflight points to the simpler repo-selection policy."""
    content = PREFLIGHT.read_text()
    assert "accept `--repo <path>` immediately when provided" in content
    assert "ask the user directly for a repo path" in content
    assert "installed skills, bundled skills, or GitHub" in content
    assert "references/shared/repo-registry.md" not in content


def test_mode_policy_matrix_covers_all_modes():
    """Verify the canonical mode matrix covers every supported mode."""
    content = MODE_POLICY.read_text()
    for label in ["🚀 Feature", "🐛 Bug Fix", "♻️ Refactor", "🧪 Test Coverage", "🔍 Review", "📖 Document", "🗨️ PR Feedback"]:
        assert label in content


def test_preflight_test_suite_check_is_mode_aware():
    """Verify test-suite handling differs by mode."""
    content = PREFLIGHT.read_text()
    assert "## Check 4 — Test suite (mode-aware)" in content
    assert "references/shared/mode-policy.md" in content
    assert "🚀/🐛/♻️/🧪 without tests" in content
    assert "🔍/📖 without tests" in content
    assert "SOFT WARNING" in content


def test_skill_references_canonical_policy_files():
    """Verify SKILL.md points to the shared policy docs."""
    content = SKILL.read_text()
    assert "references/shared/repo-selection.md" in content
    assert "references/shared/no-repo-onboarding.md" in content
    assert "references/shared/mode-policy.md" in content
    assert "references/shared/state-system.md" in content
    assert "references/shared/clarify.md" in content
    assert "references/shared/fast-path.md" in content
    assert "references/shared/pr-feedback-format.md" in content
    assert "references/shared/release-readiness.md" in content
    assert "references/shared/delegation.md" in content
    assert "references/shared/repo-registry.md" not in content
    assert "tasks/state.json" in content
    assert "Git not initialized → STOP" in content
    assert "Preview discipline before PR" in content
    assert "propose **1–2 concrete preview tests**" in content


def test_skill_invocation_uses_ptopr_and_repo_option():
    """Verify SKILL.md uses /ptopr and includes --repo."""
    content = SKILL.read_text()
    assert "/ptopr" in content
    assert "--repo" in content
    assert "am nevoie de repo" in content
    assert "/ptopr --repo ?:" not in content
    assert "scan skills + workspace" not in content
    bare_ptop = re.findall(r"/ptop(?!r)\b", content)
    assert len(bare_ptop) == 0, f"Found old /ptop references: {bare_ptop}"


def test_readme_is_aligned_with_ptopr_and_repo_selection_flow():
    """Verify README matches the current invocation contract."""
    content = README.read_text()
    assert "/ptopr" in content
    assert "/ptopr --repo /path/to/repo" in content
    assert "REPOS.md" in content
    assert "Recommended fields per entry:" in content
    for field in ["- Path", "- Alias", "- Type", "- Status"]:
        assert field in content
    assert "Registry: yes/no" not in content
    assert "PR Feedback" in content
    assert "prefers the local repo map in `REPOS.md`" in content
    assert "known repos from the registry" not in content
    assert "bounded local discovery" not in content
    assert "scan skills + workspace" not in content
    bare_ptop = re.findall(r"/ptop(?!r)\b", content)
    assert len(bare_ptop) == 0, f"Found old /ptop references in README: {bare_ptop}"


def test_contributing_and_changelog_are_aligned_with_current_conventions():
    """Verify supporting docs match the current command and branch conventions."""
    contributing = CONTRIBUTING.read_text()
    changelog = CHANGELOG.read_text()
    assert "feat/your-change" in contributing
    assert "feat/add-resume-mode" in contributing
    assert "feature/add-resume-mode" not in contributing
    assert "feat(modes): add resume capability" in contributing
    assert "## [1.5.0] - 2026-04-09" in changelog
    assert "/ptopr" in changelog
    bare_ptop = re.findall(r"/ptop(?!r)\b", contributing)
    assert len(bare_ptop) == 0, f"Found old /ptop references in CONTRIBUTING.md: {bare_ptop}"


def test_context_scan_uses_project_root():
    """Verify context-scan.md references PROJECT_ROOT."""
    content = CONTEXT_SCAN.read_text()
    assert "{PROJECT_ROOT}" in content, "PROJECT_ROOT placeholder not found in context-scan.md"


def test_context_budget_and_policy_avoid_claiming_exact_model_truth():
    """Verify context docs frame budgets as operational, not absolute truth."""
    budget = (ROOT / "references" / "shared" / "context-budget.md").read_text()
    policy = CONTEXT_POLICY.read_text()
    assert "safe working budget" in budget
    assert "not an absolute model truth" in budget
    assert "not a perfect measurement" in policy
    assert "operational limit" in policy or "operational" in policy
    assert "Context: Xk/200k" in budget
    assert "Tokens: Yk in" in budget
    assert "Do not present token counts as if they were equivalent" in policy
    assert "Divergence handling" in policy


def test_repo_selection_policy_has_local_fallback_rules():
    """Verify fallback behavior stays local and explicit."""
    content = REPO_SELECTION.read_text()
    assert "Fallback rules" in content
    assert "If shell access is restricted" in content
    assert "do not search broadly; consult `REPOS.md` if it exists, otherwise ask for a repo path" in content
    assert "unknown fields" in content


def test_no_repo_onboarding_doc_exists_and_recommends_creation():
    """Verify no-repo onboarding is documented."""
    content = NO_REPO_ONBOARDING.read_text()
    assert "prompt-to-pr still requires a Git repo" in content
    assert "create a new local repo" in content
    assert "REPOS.md" in content
    assert "Registry: yes/no" not in content
    assert "minimal human-readable inventory" in content


def test_review_mode_mentions_missing_tests_are_warning_only():
    """Verify review mode aligns with mode-aware preflight behavior."""
    review = (ROOT / "references" / "modes" / "review.md").read_text()
    assert "missing tests are a warning in this mode, not a blocker" in review


def test_document_mode_mentions_missing_tests_are_warning_only_until_behavior_changes():
    """Verify docs mode aligns with mode-aware preflight behavior."""
    document = (ROOT / "references" / "modes" / "document.md").read_text()
    assert "missing tests are a warning in this mode, not a blocker" in document
    assert "behavior-changing edits" in document


def test_all_modes_note_phase_numbers_are_local_except_shared_steps():
    """Verify every mode file explains that its phase numbers are local to the mode."""
    for path in (ROOT / "references" / "modes").glob("*.md"):
        content = path.read_text()
        assert "Phase numbering note:" in content, f"Missing phase numbering note in {path.name}"
        assert "references/shared/clarify.md" in content, f"Missing clarify reference in {path.name}"
        assert "references/shared/state-system.md" in content, f"Missing state-system reference in {path.name}"


def test_plan_format_mentions_state_json_and_clarify_summary():
    """Verify plan-format includes durable state and clarify sections."""
    content = (ROOT / "references" / "shared" / "plan-format.md").read_text()
    assert "tasks/state.json" in content
    assert "## Clarify Summary" in content
    assert "## Plan Metadata" in content
    assert "Fast Path: yes / no" in content
    assert "references/shared/state-system.md" in content


def test_runtime_artifacts_are_gitignored_and_documented_as_local():
    """Verify runtime state/review artifacts are local-only operational files."""
    gitignore = GITIGNORE.read_text()
    state_system = STATE_SYSTEM.read_text()
    readme = README.read_text()
    contributing = CONTRIBUTING.read_text()
    review_mode = (ROOT / "references" / "modes" / "review.md").read_text()
    skill = SKILL.read_text()

    assert "tasks/state.json" in gitignore
    assert "tasks/todo.md" in gitignore
    assert ".openclaw/reviews/" in gitignore
    assert "runtime working files" in state_system
    assert "ignored by git" in state_system
    assert "local runtime working files" in readme
    assert "operational runtime artifacts" in contributing
    assert "saved locally to `.openclaw/reviews/review-{YYYY-MM-DD}.md`" in review_mode
    assert "local runtime state" in skill
    assert "local runtime journal" in skill
    assert "not stable repository truth" in skill


def test_state_system_defines_resume_contract():
    """Verify durable state system defines save/resume rules."""
    content = STATE_SYSTEM.read_text()
    assert "Never rely on chat history alone" in content
    assert "tasks/state.json" in content
    assert "Resume contract" in content
    assert "nextAction" in content
    assert "Pressure-triggered minimum update set" in content
    assert "not durable repository content" in content


def test_pr_format_does_not_link_local_runtime_files_in_pr_body():
    """Verify PR template does not pretend local runtime files are repo artifacts."""
    content = PR_FEEDBACK_FORMAT.parent.joinpath("pr-format.md").read_text()
    assert "Generated by prompt-to-pr" in content
    assert "Plan: [tasks/todo.md](tasks/todo.md)" not in content
    assert "local runtime working files" in content
    assert "Do not link to them in PR bodies" in content


def test_clarify_doc_limits_questions_and_requires_persistence():
    """Verify clarify guidance is bounded and persisted."""
    content = CLARIFY.read_text()
    assert "at most 3–5 targeted questions" in content
    assert "tasks/state.json" in content
    assert "tasks/todo.md" in content


def test_fast_path_doc_requires_low_risk_and_durable_state():
    """Verify fast path remains safe and resumable."""
    content = FAST_PATH.read_text()
    assert "risk is LOW" in content
    assert "tasks/state.json" in content
    assert "Exit rule" in content


def test_review_presets_doc_lists_core_presets():
    """Verify review presets cover the intended use cases."""
    content = REVIEW_PRESETS.read_text()
    for phrase in [
        "Diff since main",
        "Changed files only",
        "Specific path",
        "PR or commit range",
        "Security boundaries",
        "Test gaps",
        "Architecture smells",
    ]:
        assert phrase in content


def test_review_mode_uses_review_presets():
    """Verify review mode loads and presents the preset menu."""
    content = (ROOT / "references" / "modes" / "review.md").read_text()
    assert "references/shared/review-presets.md" in content
    assert "[1] Diff since main" in content
    assert "[7] Architecture smells" in content


def test_mode_policy_mentions_fast_path_rules():
    """Verify mode policy references fast-path handling."""
    content = MODE_POLICY.read_text()
    assert "references/shared/fast-path.md" in content
    assert "Review mode does not use the implementation fast path" in content


def test_context_policy_defines_next_step_and_red_vs_critical_behavior():
    """Verify v3 context policy adds adaptive control concepts."""
    content = CONTEXT_POLICY.read_text()
    assert "Next-step heuristic" in content
    assert "tiny" in content and "small" in content and "medium" in content and "large" in content
    assert "Red" in content and "Critical" in content
    assert "checkpoint required" in content
    assert "save state and stop" in content
    assert "Mini v3 save-trigger contract" in content
    assert "nextAction" in content


def test_skill_references_context_policy_and_adaptive_monitoring():
    """Verify SKILL.md uses context-policy and adaptive wording."""
    content = SKILL.read_text()
    assert "references/shared/context-policy.md" in content
    assert "safe working budget" in content
    assert "next-step size" in content
    assert "Do not treat red as an automatic stop" in content
    assert "set `nextAction`, and stop" in content
    assert "Context: 165k/200k · Tokens: 38k in" in content
    assert "Do **not** present `Tokens: Xk in` as if it were the same thing as `Context: Yk/200k`" in content


def test_pr_feedback_mode_exists_and_references_shared_docs():
    """Verify PR feedback mode is wired correctly."""
    content = PR_FEEDBACK_MODE.read_text()
    assert "references/shared/clarify.md" in content
    assert "references/shared/state-system.md" in content
    assert "references/shared/pr-feedback-format.md" in content
    assert "MUST-FIX" in content
    assert "UNCLEAR" in content


def test_release_readiness_and_delegation_docs_exist_with_core_rules():
    """Verify release-readiness and delegation docs include core guidance."""
    release = RELEASE_READINESS.read_text()
    delegation = DELEGATION.read_text()
    assert "Merge readiness" in release
    assert "Rollback note" in release
    assert "Good delegation points" in delegation
    assert "Do not delegate" in delegation


def test_feature_bugfix_refactor_reference_release_readiness():
    """Verify ship-affecting modes reference release-readiness summary."""
    for name in ["feature.md", "bugfix.md", "refactor.md"]:
        content = (ROOT / "references" / "modes" / name).read_text()
        assert "references/shared/release-readiness.md" in content, f"Missing release-readiness in {name}"


def test_previewable_modes_propose_preview_tests_before_pr():
    """Verify relevant modes nudge preview testing before PR/commit."""
    for name in ["feature.md", "bugfix.md", "document.md", "refactor.md", "test-coverage.md"]:
        content = (ROOT / "references" / "modes" / name).read_text()
        assert "propose 1–2 concrete preview tests before PR/commit" in content, f"Missing preview-test rule in {name}"
        assert "Test 1: happy path preview" in content, f"Missing preview-test example in {name}"
        assert "Test 2: edge / empty / failure preview" in content, f"Missing preview-test example in {name}"


def test_pr_modes_use_consistent_checkpoint_2_wording():
    """Verify PR-producing modes use the same checkpoint-2 wording."""
    for name in ["feature.md", "bugfix.md", "refactor.md", "test-coverage.md", "document.md"]:
        content = (ROOT / "references" / "modes" / name).read_text()
        assert "⛔ CHECKPOINT 2 — Approve to create PR?" in content, f"Inconsistent checkpoint wording in {name}"
