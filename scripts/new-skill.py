# /// script
# requires-python = ">=3.10"
# ///
"""Create a new skill from the template."""

import re
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = REPO_ROOT / "templates" / "skill-template"
SKILLS_DIR = REPO_ROOT / "skills"
SLUG_PATTERN = re.compile(r"^[a-z][a-z0-9-]*$")


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: uv run scripts/new-skill.py <slug>")
        sys.exit(1)

    slug = sys.argv[1]

    if not SLUG_PATTERN.match(slug):
        print(f"Invalid slug: {slug!r}")
        print("Use lowercase letters, digits, and hyphens. Must start with a letter.")
        sys.exit(1)

    dest = SKILLS_DIR / slug
    if dest.exists():
        print(f"Skill already exists: {dest}")
        sys.exit(1)

    shutil.copytree(TEMPLATE_DIR, dest)

    # Replace placeholders in SKILL.md
    skill_md = dest / "SKILL.md"
    content = skill_md.read_text()
    content = content.replace("<slug>", slug)
    content = content.replace("<Skill Name>", slug.replace("-", " ").title())
    skill_md.write_text(content)

    print(f"Created: {dest}")
    print(f"Next: edit {skill_md} and add catalog entries to docs/index.html and docs/skills.html")


if __name__ == "__main__":
    main()
