# skills

Portable catalog of reusable AI agent skills.

## What this is

A repository that hosts self-contained skills for AI coding agents. Each skill is a folder under `skills/` with a `SKILL.md` that agents load on demand.

## Layout

```
skills/<slug>/SKILL.md       # skill instructions (required)
skills/<slug>/scripts/        # helper scripts (optional)
skills/<slug>/references/     # supplementary docs (optional)
skills/<slug>/assets/         # templates, files (optional)
templates/skill-template/     # starter template for new skills
scripts/new-skill.py          # creates a skill from the template
docs/                         # GitHub Pages site
AGENTS.md                     # agent guidance for this repo
```

## Add a new skill

```bash
uv run scripts/new-skill.py my-skill-name
```

Or copy `templates/skill-template/` to `skills/<slug>/` manually.

Then:
1. Edit `skills/<slug>/SKILL.md` — fill in name, description, instructions.
2. Add an entry to `docs/skills.md`.

## Conventions

- One folder per skill, always.
- Slug format: lowercase, hyphens (`frontend-design`).
- `SKILL.md` is the only required file per skill.
- Keep skills concise — use `references/` for large docs.
- Python scripts: prefer `uv run`. TypeScript: prefer `bun run`.
- No unnecessary dependencies or build steps.

## Docs

Published via GitHub Pages from the `/docs` folder on `main`. Plain Markdown, no Jekyll.

To preview locally, use any static file server:

```bash
python -m http.server 8000 -d docs
```

## Agent guidance

See [AGENTS.md](AGENTS.md) for coding agent instructions.
