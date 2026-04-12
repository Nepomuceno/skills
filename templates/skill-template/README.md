# Skill template

Copy this folder to `skills/<your-slug>/` to start a new skill.

## What goes here

| Path | Purpose | Required |
|------|---------|----------|
| `SKILL.md` | Agent instructions with YAML frontmatter | Yes |
| `scripts/` | Helper scripts (Python with `uv`, TS with `bun`) | No |
| `references/` | Supplementary docs loaded on demand | No |
| `assets/` | Templates, icons, static files | No |

## Quick start

```bash
# Automated
uv run scripts/new-skill.py my-skill

# Manual
cp -r templates/skill-template skills/my-skill
# Edit skills/my-skill/SKILL.md
```

After creating your skill, add an entry to `docs/skills.md`.
