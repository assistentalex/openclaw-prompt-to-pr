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


def test_preflight_has_repo_discovery_section():
    """Verify preflight.md contains the repo discovery section."""
    content = PREFLIGHT.read_text()
    assert "## Check 2 — Repo discovery" in content
    assert "single unified menu" in content


def test_preflight_repo_selection_is_combined_not_two_step():
    """Verify preflight does not instruct a separate mode-first-then-repo question flow."""
    content = PREFLIGHT.read_text()
    assert "single combined menu" in content
    assert "mode first, repo second" not in content
    assert "repo selection as **Step 2** after mode selection (Step 1)" not in content


def test_preflight_test_suite_check_is_mode_aware():
    """Verify test-suite handling differs by mode."""
    content = PREFLIGHT.read_text()
    assert "## Check 3 — Test suite (mode-aware)" in content
    assert "🚀/🐛/♻️/🧪 modes" in content
    assert "🔍/📖 modes" in content
    assert "SOFT WARNING" in content


def test_skill_hard_stops_are_mode_aware():
    """Verify SKILL.md documents mode-aware test-suite hard stops."""
    content = SKILL.read_text()
    assert "Test suite missing in **Feature / Fix / Refactor / Test Coverage** modes → STOP" in content
    assert "Test suite missing in **Review / Docs** modes → warn, continue" in content


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


def test_preflight_has_fallback_rules():
    """Verify fallback behavior is documented for limited tooling."""
    content = PREFLIGHT.read_text()
    assert "Fallback rules:" in content
    assert "If `gh` is missing or not authenticated" in content
    assert "If shell access is restricted" in content
    assert "mark fields as `unknown`" in content


def test_review_mode_mentions_missing_tests_are_warning_only():
    """Verify review mode aligns with mode-aware preflight behavior."""
    review = (ROOT / "references" / "modes" / "review.md").read_text()
    assert "missing tests are a warning in this mode, not a blocker" in review


def test_document_mode_mentions_missing_tests_are_warning_only_until_behavior_changes():
    """Verify docs mode aligns with mode-aware preflight behavior."""
    document = (ROOT / "references" / "modes" / "document.md").read_text()
    assert "missing tests are a warning in this mode, not a blocker" in document
    assert "behavior-changing edits" in document
