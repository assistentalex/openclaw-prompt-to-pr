"""Smoke and regression tests for the prompt-to-pr skill docs."""

import os
import re
from pathlib import Path

SKILLS_DIR = Path(os.environ.get("OPENCLAW_SKILLS_DIR", Path.home() / ".openclaw" / "skills"))
NPM_SKILLS_DIR = Path(os.environ.get("OPENCLAW_NPM_SKILLS_DIR", Path.home() / ".npm-global" / "lib" / "node_modules" / "openclaw" / "skills"))
ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "SKILL.md"
PREFLIGHT = ROOT / "references" / "shared" / "preflight.md"
CONTEXT_SCAN = ROOT / "references" / "shared" / "context-scan.md"
REPO_SELECTION = ROOT / "references" / "shared" / "repo-selection.md"
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
STATE_JSON = ROOT / "tasks" / "state.json"


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
    assert STATE_JSON.is_file(), f"Missing {STATE_JSON}"


def test_preflight_has_repo_discovery_section():
    """Verify preflight.md contains the repo discovery section."""
    content = PREFLIGHT.read_text()
    assert "## Check 2 — Repo discovery" in content
    assert "references/shared/repo-selection.md" in content


def test_repo_selection_policy_requires_single_combined_menu():
    """Verify the canonical repo-selection policy rejects two-step selection."""
    content = REPO_SELECTION.read_text()
    assert "single combined menu" in content
    assert "Never" in content
    assert "mode first, repo second" not in content


def test_preflight_repo_selection_is_combined_not_two_step():
    """Verify preflight points to the canonical combined-selection policy."""
    content = PREFLIGHT.read_text()
    assert "single combined menu" in content
    assert "mode first, repo second" not in content
    assert "repo selection as **Step 2** after mode selection (Step 1)" not in content


def test_mode_policy_matrix_covers_all_modes():
    """Verify the canonical mode matrix covers every supported mode."""
    content = MODE_POLICY.read_text()
    for label in ["🚀 Feature", "🐛 Bug Fix", "♻️ Refactor", "🧪 Test Coverage", "🔍 Review", "📖 Document", "🗨️ PR Feedback"]:
        assert label in content



def test_preflight_test_suite_check_is_mode_aware():
    """Verify test-suite handling differs by mode."""
    content = PREFLIGHT.read_text()
    assert "## Check 3 — Test suite (mode-aware)" in content
    assert "references/shared/mode-policy.md" in content
    assert "🚀/🐛/♻️/🧪 without tests" in content
    assert "🔍/📖 without tests" in content
    assert "SOFT WARNING" in content


def test_skill_references_canonical_policy_files():
    """Verify SKILL.md points to the shared policy docs."""
    content = SKILL.read_text()
    assert "references/shared/repo-selection.md" in content
    assert "references/shared/mode-policy.md" in content
    assert "references/shared/state-system.md" in content
    assert "references/shared/clarify.md" in content
    assert "references/shared/fast-path.md" in content
    assert "references/shared/pr-feedback-format.md" in content
    assert "references/shared/release-readiness.md" in content
    assert "references/shared/delegation.md" in content
    assert "tasks/state.json" in content
    assert "Git not initialized → STOP" in content


def test_skill_invocation_uses_ptopr_and_repo_option():
    """Verify SKILL.md uses /ptopr and includes --repo."""
    content = SKILL.read_text()
    assert "/ptopr" in content
    assert "--repo" in content
    bare_ptop = re.findall(r"/ptop(?!r)\b", content)
    assert len(bare_ptop) == 0, f"Found old /ptop references: {bare_ptop}"


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


def test_repo_discovery_scans_skills_dir_if_present():
    """Verify that the skills directory, if present, contains visible subdirectories."""
    if SKILLS_DIR.is_dir():
        subdirs = [d for d in SKILLS_DIR.iterdir() if d.is_dir() and not d.name.startswith(".")]
        assert subdirs, f"Skills dir {SKILLS_DIR} exists but has no skill subdirectories"


def test_repo_discovery_finds_git_repos_if_skill_dirs_present():
    """Verify at least one skill repo exists when scanned skill dirs are present."""
    repos_found = []
    for skills_base in [SKILLS_DIR, NPM_SKILLS_DIR]:
        if skills_base.is_dir():
            for d in skills_base.iterdir():
                if d.is_dir() and not d.name.startswith(".") and (d / ".git").is_dir():
                    repos_found.append(d.name)
    if SKILLS_DIR.is_dir() or NPM_SKILLS_DIR.is_dir():
        assert repos_found, "No git repos found in discovered skills directories"


def test_repo_selection_policy_has_fallback_rules():
    """Verify fallback behavior is documented in the canonical repo-selection policy."""
    content = REPO_SELECTION.read_text()
    assert "Fallback rules" in content
    assert "If `gh` is missing or not authenticated" in content
    assert "If shell access is restricted" in content
    assert "mark unknown fields as `unknown`" in content


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



def test_state_system_defines_resume_contract():
    """Verify durable state system defines save/resume rules."""
    content = STATE_SYSTEM.read_text()
    assert "Never rely on chat history alone" in content
    assert "tasks/state.json" in content
    assert "Resume contract" in content
    assert "nextAction" in content
    assert "Pressure-triggered minimum update set" in content



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



def test_pr_modes_use_consistent_checkpoint_2_wording():
    """Verify PR-producing modes use the same checkpoint-2 wording."""
    for name in ["feature.md", "bugfix.md", "refactor.md", "test-coverage.md", "document.md"]:
        content = (ROOT / "references" / "modes" / name).read_text()
        assert "⛔ CHECKPOINT 2 — Approve to create PR?" in content, f"Inconsistent checkpoint wording in {name}"
