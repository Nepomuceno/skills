# AGENTS.md

## Repo purpose

Portable catalog of reusable AI agent skills. One folder per skill under `skills/`.

## Repo layout

```
skills/<slug>/SKILL.md      # required — skill instructions
skills/<slug>/scripts/       # optional — helper scripts
skills/<slug>/references/    # optional — docs loaded on demand
skills/<slug>/assets/        # optional — templates, icons, etc.
templates/skill-template/    # copy this to start a new skill
scripts/new-skill.py         # creates a new skill from the template
docs/                        # GitHub Pages site (published from /docs)
```

## Creating a new skill

```bash
uv run scripts/new-skill.py <slug>
```

Or manually: copy `templates/skill-template/` to `skills/<slug>/` and edit.

Slug rules: lowercase, hyphens, no underscores. Example: `frontend-design`.

## SKILL.md requirements

Every skill folder must contain a `SKILL.md`. It is the only required file.

Required frontmatter fields:

```yaml
---
name: <slug>
description: <when to trigger and what it does — be specific and trigger-rich>
---
```

Body rules:
- Operational instructions only — no filler, no motivation, no decorative prose
- Prefer imperative voice
- Keep under 500 lines; use `references/` for overflow
- Colocate scripts, references, and assets inside the skill folder
- Explain *why* behind constraints — models respond better to reasoning than to `MUST`/`NEVER`
- Include concrete examples when shorter than explanation

Description field rules:
- Must say what the skill does AND when to use it
- Include trigger phrases a user would actually type
- Lean slightly "pushy" — err toward triggering rather than missing
- No vague marketing language

## Writing style

- Concise, direct, specific
- No wasted tokens
- No decorative headings or filler sections
- Prefer scripts over long natural-language procedures
- Prefer examples over explanation when shorter
- No enterprise boilerplate

## Implementation preferences

- Python scripts: use `uv run` with inline dependency metadata when practical
- TypeScript scripts: use `bun run`
- Fall back to plain Python if `uv`/`bun` add no value
- No Docker, no heavy build systems
- No unnecessary dependencies

## Docs

- Every real skill must have an entry in `docs/skills.md`
- Docs must stay aligned with actual skill folders
- Docs publish from `/docs` via GitHub Pages — plain Markdown, no Jekyll

## Anti-patterns

- Giant monolithic skills — split into references
- Duplicated instructions across files
- Speculative abstractions or unused tooling
- Hidden magic or implicit conventions
- Config files that don't change behavior
- Wrapper scripts around single commands
