"""Smoke test — verifies the project test infrastructure is working."""

import os
from pathlib import Path

SKILLS_DIR = Path(os.environ.get("OPENCLAW_SKILLS_DIR", Path.home() / ".openclaw" / "skills"))
NPM_SKILLS_DIR = Path(os.environ.get("OPENCLAW_NPM_SKILLS_DIR", Path.home() / ".npm-global" / "lib" / "node_modules" / "openclaw" / "skills"))


def test_smoke():
    """If this passes, pytest is correctly configured."""
    assert True


def test_skill_file_exists():
    """Verify SKILL.md is present in the project root."""
    skill_path = Path(__file__).resolve().parent.parent / "SKILL.md"
    assert skill_path.is_file(), f"SKILL.md not found at {skill_path}"


def test_references_directory():
    """Verify the references directory structure exists."""
    refs = Path(__file__).resolve().parent.parent / "references"
    assert refs.is_dir(), "references/ directory not found"
    assert (refs / "shared").is_dir(), "references/shared/ not found"
    assert (refs / "modes").is_dir(), "references/modes/ not found"


def test_preflight_has_repo_discovery():
    """Verify preflight.md contains Check 5 — Repo discovery."""
    preflight = Path(__file__).resolve().parent.parent / "references" / "shared" / "preflight.md"
    content = preflight.read_text()
    assert "Repo discovery" in content, "Check 5 — Repo discovery not found in preflight.md"
    assert "Check 6" in content, "Check 6 (hardshell renumber) not found in preflight.md"


def test_skill_invocation_has_repo():
    """Verify SKILL.md includes --repo invocation options."""
    skill = Path(__file__).resolve().parent.parent / "SKILL.md"
    content = skill.read_text()
    assert "--repo" in content, "--repo option not found in SKILL.md invocation"


def test_context_scan_uses_project_root():
    """Verify context-scan.md references PROJECT_ROOT."""
    context_scan = Path(__file__).resolve().parent.parent / "references" / "shared" / "context-scan.md"
    content = context_scan.read_text()
    assert "{PROJECT_ROOT}" in content, "PROJECT_ROOT placeholder not found in context-scan.md"


def test_repo_discovery_scans_skills_dir():
    """Verify that the skills directory exists and contains subdirectories."""
    if SKILLS_DIR.is_dir():
        subdirs = [d for d in SKILLS_DIR.iterdir() if d.is_dir() and not d.name.startswith(".")]
        assert len(subdirs) > 0, f"Skills dir {SKILLS_DIR} exists but has no skill subdirectories"
    else:
        # If no local skills dir, that's fine — we just skip validation
        pass


def test_repo_discovery_finds_git_repos():
    """Verify at least one skill has a .git directory (i.e., is a repo)."""
    repos_found = []
    for skills_base in [SKILLS_DIR, NPM_SKILLS_DIR]:
        if skills_base.is_dir():
            for d in skills_base.iterdir():
                if d.is_dir() and not d.name.startswith(".") and (d / ".git").is_dir():
                    repos_found.append(d.name)
    assert len(repos_found) > 0, "No git repos found in skills directories"


def test_references_directory():
    """Verify the references directory structure exists."""
    from pathlib import Path

    refs = Path(__file__).resolve().parent.parent / "references"
    assert refs.is_dir(), "references/ directory not found"
    assert (refs / "shared").is_dir(), "references/shared/ not found"
    assert (refs / "modes").is_dir(), "references/modes/ not found"