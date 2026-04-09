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
    for label in ["🚀 Feature", "🐛 Bug Fix", "♻️ Refactor", "🧪 Test Coverage", "🔍 Review", "📖 Document"]:
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
    """Verify SKILL.md points to the shared repo-selection and mode-policy docs."""
    content = SKILL.read_text()
    assert "references/shared/repo-selection.md" in content
    assert "references/shared/mode-policy.md" in content
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



def test_pr_modes_use_consistent_checkpoint_2_wording():
    """Verify PR-producing modes use the same checkpoint-2 wording."""
    for name in ["feature.md", "bugfix.md", "refactor.md", "test-coverage.md", "document.md"]:
        content = (ROOT / "references" / "modes" / name).read_text()
        assert "⛔ CHECKPOINT 2 — Approve to create PR?" in content, f"Inconsistent checkpoint wording in {name}"
