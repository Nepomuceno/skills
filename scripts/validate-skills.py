# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml"]
# ///
"""Validate all skills in the repo.

Checks:
  - Every skills/<slug>/ directory contains a SKILL.md
  - SKILL.md has valid YAML frontmatter with required `name` and `description`
  - `name` in frontmatter matches the directory slug
  - Slug follows conventions (lowercase, hyphens, starts with letter)
  - Description is non-empty (at least 20 chars — enough for a real sentence)
  - SKILL.md body is under 500 lines

Exit code 0 = all valid, 1 = errors found.
"""

import re
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
SLUG_PATTERN = re.compile(r"^[a-z][a-z0-9-]*$")
MAX_BODY_LINES = 500
MIN_DESCRIPTION_LENGTH = 20


def parse_frontmatter(text: str) -> tuple[dict | None, str, str | None]:
    """Extract YAML frontmatter and body from a SKILL.md file.

    Returns (frontmatter_dict, body, error_message).
    """
    if not text.startswith("---"):
        return None, text, "Missing YAML frontmatter (file must start with ---)"

    parts = text.split("---", 2)
    if len(parts) < 3:
        return None, text, "Malformed frontmatter (missing closing ---)"

    try:
        fm = yaml.safe_load(parts[1])
    except yaml.YAMLError as e:
        return None, text, f"Invalid YAML in frontmatter: {e}"

    if not isinstance(fm, dict):
        return None, parts[2], "Frontmatter is not a YAML mapping"

    return fm, parts[2], None


def validate_skill(skill_dir: Path) -> list[str]:
    """Validate a single skill directory. Returns list of error messages."""
    errors: list[str] = []
    slug = skill_dir.name

    # Slug format
    if not SLUG_PATTERN.match(slug):
        errors.append(
            f"Invalid slug '{slug}': use lowercase letters, digits, and hyphens; "
            f"must start with a letter"
        )

    # SKILL.md exists
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        errors.append("Missing SKILL.md")
        return errors

    content = skill_md.read_text(encoding="utf-8")

    # Parse frontmatter
    fm, body, parse_err = parse_frontmatter(content)
    if parse_err:
        errors.append(parse_err)
        return errors

    assert fm is not None

    # Required fields
    if "name" not in fm:
        errors.append("Frontmatter missing required field: name")
    elif fm["name"] != slug:
        errors.append(
            f"Frontmatter name '{fm['name']}' does not match directory slug '{slug}'"
        )

    if "description" not in fm:
        errors.append("Frontmatter missing required field: description")
    else:
        desc = str(fm["description"]).strip()
        if len(desc) < MIN_DESCRIPTION_LENGTH:
            errors.append(
                f"Description too short ({len(desc)} chars, minimum {MIN_DESCRIPTION_LENGTH}). "
                f"Include trigger phrases so agents know when to activate this skill."
            )

    # Body line count
    body_lines = body.strip().splitlines()
    if len(body_lines) > MAX_BODY_LINES:
        errors.append(
            f"SKILL.md body is {len(body_lines)} lines (max {MAX_BODY_LINES}). "
            f"Move detailed content to references/."
        )

    return errors


def main() -> None:
    if not SKILLS_DIR.is_dir():
        print(f"Skills directory not found: {SKILLS_DIR}")
        sys.exit(1)

    skill_dirs = sorted(
        d for d in SKILLS_DIR.iterdir()
        if d.is_dir() and not d.name.startswith(".")
    )

    if not skill_dirs:
        print("No skill directories found under skills/")
        sys.exit(1)

    total_errors = 0
    for skill_dir in skill_dirs:
        errors = validate_skill(skill_dir)
        if errors:
            print(f"\n  skills/{skill_dir.name}/")
            for err in errors:
                print(f"    - {err}")
            total_errors += len(errors)
        else:
            print(f"  skills/{skill_dir.name}/ ... ok")

    print()
    if total_errors:
        print(f"Found {total_errors} error(s) across {len(skill_dirs)} skill(s).")
        sys.exit(1)
    else:
        print(f"All {len(skill_dirs)} skill(s) valid.")


if __name__ == "__main__":
    main()
