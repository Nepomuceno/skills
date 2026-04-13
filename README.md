# skills

Portable catalog of reusable AI agent skills.

## Install

Install all skills with a single command — no cloning required:

```bash
npx skills add Nepomuceno/skills
```

Or install a specific skill:

```bash
npx skills add Nepomuceno/skills --skill image-generation
npx skills add Nepomuceno/skills --skill voice-clone
```

Works with Claude Code, OpenCode, Cursor, Codex, GitHub Copilot, and [40+ other agents](https://github.com/vercel-labs/skills#supported-agents).

## Available skills

| Skill | Description |
|-------|-------------|
| [image-generation](skills/image-generation) | Generate images via Azure AI Foundry, split grids, and post-process with CLI tools |
| [voice-clone](skills/voice-clone) | Clone voices and generate speech via Azure Cognitive Services and Azure OpenAI TTS |

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
2. Add catalog entries to `docs/index.html` and `docs/skills.html`.

## Conventions

- One folder per skill, always.
- Slug format: lowercase, hyphens (`frontend-design`).
- `SKILL.md` is the only required file per skill.
- Keep skills concise — use `references/` for large docs.
- Python scripts: prefer `uv run`. TypeScript: prefer `bun run`.
- No unnecessary dependencies or build steps.

## Docs

Published via GitHub Pages from the `/docs` folder on `main`. Plain HTML, no Jekyll.

To preview locally:

```bash
make docs
```

## Validation

Validate all skills and check docs are in sync:

```bash
make validate     # check SKILL.md frontmatter and structure
make check-docs   # verify docs list every skill
```

These checks also run automatically on every PR via GitHub Actions.

## Agent guidance

See [AGENTS.md](AGENTS.md) for coding agent instructions.
