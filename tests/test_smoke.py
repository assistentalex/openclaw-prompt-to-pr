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
    assert "/ptopr" in content, "/ptopr invocation not found in SKILL.md"


def test_skill_has_two_step_menu():
    """Verify SKILL.md uses two-step menu: mode first, repo second."""
    skill = Path(__file__).resolve().parent.parent / "SKILL.md"
    content = skill.read_text()
    assert "Step 1" in content, "Step 1 (mode selection) not found in SKILL.md"
    assert "Step 2" in content, "Step 2 (repo selection) not found in SKILL.md"
    assert "1a" not in content, "Combined '1a' format still present — should be two-step"


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


def test_skill_has_mandatory_section():
    """Verify SKILL.md contains the ⛔ MANDATORY section."""
    skill = Path(__file__).resolve().parent.parent / "SKILL.md"
    content = skill.read_text()
    assert "⛔ MANDATORY" in content, "⛔ MANDATORY section not found in SKILL.md"


def test_mandatory_rules_in_skill():
    """Verify the 3 mandatory rules are present in SKILL.md."""
    skill = Path(__file__).resolve().parent.parent / "SKILL.md"
    content = skill.read_text()
    assert "Context banner in EVERY assistant turn" in content, "Rule 1 (per-turn banner) not found"
    assert "Real token counts only" in content, "Rule 2 (real tokens) not found"
    assert "Checkpoints are hard stops" in content, "Rule 3 (checkpoints) not found"


def test_never_do_has_phase_banner():
    """Verify NEVER DO section includes the phase banner rule."""
    skill = Path(__file__).resolve().parent.parent / "SKILL.md"
    content = skill.read_text()
    assert "Never start a phase without displaying the phase banner" in content, \
        "Phase banner rule not found in NEVER DO section"


def test_all_modes_have_banner_rule():
    """Verify all 6 mode files contain the phase banner mandatory line."""
    modes_dir = Path(__file__).resolve().parent.parent / "references" / "modes"
    mode_files = list(modes_dir.glob("*.md"))
    assert len(mode_files) >= 6, f"Expected 6+ mode files, found {len(mode_files)}"
    for mode_file in mode_files:
        content = mode_file.read_text()
        assert "Phase banner mandatory" in content, \
            f"Phase banner mandatory line not found in {mode_file.name}"


def test_phase_banner_references_mandatory_section():
    """Verify the shared rules phase banner section points to MANDATORY."""
    skill = Path(__file__).resolve().parent.parent / "SKILL.md"
    content = skill.read_text()
    assert "See ⛔ MANDATORY" in content, \
        "Phase banner section does not reference ⛔ MANDATORY block"


def test_per_turn_banner_rule():
    """Verify SKILL.md mandates context banner in every assistant turn."""
    skill = Path(__file__).resolve().parent.parent / "SKILL.md"
    content = skill.read_text()
    assert "every assistant turn" in content.lower(), \
        "Per-turn banner rule not found in SKILL.md"
    assert "no exceptions" in content.lower(), \
        "'No exceptions' clause not found for per-turn banner rule"


def test_skill_invocation_uses_ptopr():
    """Verify SKILL.md uses /ptopr (not /ptop) as the invocation command."""
    skill = Path(__file__).resolve().parent.parent / "SKILL.md"
    content = skill.read_text()
    assert "/ptopr" in content, "/ptopr invocation not found in SKILL.md"
    # Ensure old /ptop (without trailing 'r') is not used as a command
    # Allow 'prompt-to-pr' and '/ptopr' but not bare '/ptop'
    import re
    bare_ptop = re.findall(r'/ptop(?!r)\b', content)
    assert len(bare_ptop) == 0, f"Found old /ptop references (should be /ptopr): {bare_ptop}"