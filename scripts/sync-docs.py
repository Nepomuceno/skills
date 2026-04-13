# /// script
# requires-python = ">=3.10"
# ///
"""Check that docs/index.html and docs/skills.html stay aligned with skills/.

Validates the skill catalog cards in both HTML files by checking:
  - every real skill has exactly one GitHub link card
  - no deleted/stale skill cards remain
  - each card includes the expected slug heading
  - each card includes the expected install command
  - each card advertises the current scripts/ and references/ counts

Exit code 0 = all in sync, 1 = drift detected.
"""

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
DOCS_DIR = REPO_ROOT / "docs"

INDEX_HTML = DOCS_DIR / "index.html"
SKILLS_HTML = DOCS_DIR / "skills.html"
GITHUB_SKILL_LINK_RE = re.compile(
    r'https://github\.com/Nepomuceno/skills/tree/main/skills/([a-z][a-z0-9-]*)'
)


def get_skill_slugs() -> list[str]:
    """Return sorted list of skill slugs from skills/ directory."""
    return sorted(
        d.name
        for d in SKILLS_DIR.iterdir()
        if d.is_dir() and not d.name.startswith(".") and (d / "SKILL.md").is_file()
    )


def get_skill_counts(slug: str) -> tuple[int, int]:
    """Return (scripts_count, references_count) for a skill directory."""
    skill_dir = SKILLS_DIR / slug

    def count_files(subdir: str) -> int:
        path = skill_dir / subdir
        if not path.is_dir():
            return 0
        return sum(1 for entry in path.iterdir() if entry.is_file() and not entry.name.startswith("."))

    return count_files("scripts"), count_files("references")


def get_doc_skill_links(html_content: str) -> list[str]:
    """Return all skill slugs linked from GitHub catalog cards."""
    return GITHUB_SKILL_LINK_RE.findall(html_content)


def validate_skill_card(html_content: str, slug: str) -> list[str]:
    """Validate the visible catalog data for a single skill card."""
    errors: list[str] = []
    match = GITHUB_SKILL_LINK_RE.search(html_content)
    while match and match.group(1) != slug:
        match = GITHUB_SKILL_LINK_RE.search(html_content, match.end())

    if not match:
        return [f"missing GitHub card for skill: {slug}"]

    window = html_content[match.start():match.start() + 2500]
    scripts_count, references_count = get_skill_counts(slug)

    if not re.search(rf">\s*{re.escape(slug)}\s*<", window):
        errors.append(f"skill card for {slug} is missing its slug heading")
    if not re.search(rf"--skill.*?{re.escape(slug)}", window, re.DOTALL):
        errors.append(f"skill card for {slug} is missing its install command")
    if not re.search(rf">\s*{scripts_count}\s+scripts\s*<", window):
        errors.append(f"skill card for {slug} has wrong scripts count (expected {scripts_count})")
    if not re.search(rf">\s*{references_count}\s+references\s*<", window):
        errors.append(f"skill card for {slug} has wrong references count (expected {references_count})")

    return errors


def main() -> None:
    slugs = get_skill_slugs()

    if not slugs:
        print("No skills found in skills/ directory.")
        sys.exit(1)

    errors: list[str] = []

    # Check each docs file
    for html_file in [INDEX_HTML, SKILLS_HTML]:
        if not html_file.is_file():
            errors.append(f"Docs file not found: {html_file.relative_to(REPO_ROOT)}")
            continue

        content = html_file.read_text(encoding="utf-8")
        relative = html_file.relative_to(REPO_ROOT)
        linked_slugs = get_doc_skill_links(content)
        linked_set = set(linked_slugs)
        actual_set = set(slugs)

        for slug in sorted(actual_set - linked_set):
            errors.append(f"{relative} is missing skill card: {slug}")
        for slug in sorted(linked_set - actual_set):
            errors.append(f"{relative} has stale skill card: {slug}")
        for slug in sorted({slug for slug in linked_slugs if linked_slugs.count(slug) > 1}):
            errors.append(f"{relative} has duplicate skill card: {slug}")

        for slug in slugs:
            for err in validate_skill_card(content, slug):
                errors.append(f"{relative}: {err}")

    if errors:
        print("Docs are out of sync with skills/ directory:\n")
        for err in errors:
            print(f"  - {err}")
        print(f"\nFound {len(errors)} issue(s).")
        print("\nTo fix: update the catalog cards in docs/index.html and docs/skills.html.")
        sys.exit(1)
    else:
        print(f"Docs are in sync. All {len(slugs)} skill(s) have valid catalog cards in both pages.")


if __name__ == "__main__":
    main()
