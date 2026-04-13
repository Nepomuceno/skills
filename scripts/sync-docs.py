# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml"]
# ///
"""Check that docs/index.html and docs/skills.html list every skill in skills/.

Reads SKILL.md frontmatter for each skill directory, then scans both HTML files
for references to each skill slug. Reports any skills missing from either page.

Exit code 0 = all in sync, 1 = drift detected.
"""

import re
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
DOCS_DIR = REPO_ROOT / "docs"

INDEX_HTML = DOCS_DIR / "index.html"
SKILLS_HTML = DOCS_DIR / "skills.html"


def get_skill_slugs() -> list[str]:
    """Return sorted list of skill slugs from skills/ directory."""
    return sorted(
        d.name
        for d in SKILLS_DIR.iterdir()
        if d.is_dir() and not d.name.startswith(".") and (d / "SKILL.md").is_file()
    )


def get_skill_metadata(slug: str) -> dict:
    """Read frontmatter from a skill's SKILL.md."""
    skill_md = SKILLS_DIR / slug / "SKILL.md"
    text = skill_md.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {"name": slug}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {"name": slug}
    try:
        fm = yaml.safe_load(parts[1])
        return fm if isinstance(fm, dict) else {"name": slug}
    except yaml.YAMLError:
        return {"name": slug}


def find_skill_references(html_content: str, slug: str) -> bool:
    """Check if a skill slug is referenced in an HTML file.

    Looks for the slug in GitHub links (skills/<slug>) or as heading text.
    """
    patterns = [
        rf"skills/{re.escape(slug)}",  # GitHub link path
        rf">{re.escape(slug)}<",       # Heading/link text
    ]
    return any(re.search(p, html_content) for p in patterns)


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

        for slug in slugs:
            if not find_skill_references(content, slug):
                errors.append(f"{relative} is missing skill: {slug}")

    if errors:
        print("Docs are out of sync with skills/ directory:\n")
        for err in errors:
            print(f"  - {err}")
        print(f"\nFound {len(errors)} issue(s).")
        print("\nTo fix: add catalog entries for the missing skills in the docs files.")
        sys.exit(1)
    else:
        print(f"Docs are in sync. All {len(slugs)} skill(s) listed in both pages.")


if __name__ == "__main__":
    main()
