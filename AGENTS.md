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

- Every real skill must have catalog entries in `docs/index.html` and `docs/skills.html`
- Docs must stay aligned with actual skill folders
- Docs publish from `/docs` via GitHub Pages — plain HTML, no Jekyll

## Anti-patterns

- Giant monolithic skills — split into references
- Duplicated instructions across files
- Speculative abstractions or unused tooling
- Hidden magic or implicit conventions
- Config files that don't change behavior
- Wrapper scripts around single commands

## Skill-building lessons

SKILL.md:
- SKILL.md loads on every invocation — every token counts. Move detailed instructions, examples, and pattern-specific guidance into `references/`
- Never put environment-specific info (endpoints, subscription IDs, account names) in the skill. Use a discovery script at runtime instead. Model-family defaults (e.g. `gpt-4o-mini-tts`) are acceptable since they identify the capability, not a specific deployment — but always allow overriding via environment variable or CLI flag
- The description field should list every phrase a user might type that should activate the skill

Scripts:
- Separate concerns into independent scripts. If a workflow has a step you might want to iterate on, make it its own script so you don't re-run expensive earlier steps
- Auto-detect rather than assume. If a model or tool produces approximate results, detect the actual output and adapt rather than hardcoding expected values
- Progressive/multi-pass approaches beat single-pass when dealing with fuzzy boundaries or gradual transitions

References:
- Default prompt suffixes or templates should only control layout/structure, not content-specific details like colors. The caller controls appearance
- State a principle once in SKILL.md. Don't copy-paste the same instruction into every reference file

Testing:
- Use a gitignored workspace directory for test artifacts
- A/B test with the user — generate multiple variants with different techniques, let the user judge, codify the winner
