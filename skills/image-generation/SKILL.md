---
name: image-generation
description: >
  Generate images, post-process assets, and prepare visual content for any project
  using Azure AI Foundry models or other configured image providers. Use this skill
  whenever the user mentions image generation, generating visuals, creating
  presentation backgrounds, website hero images, transparent PNG inserts, Remotion
  scene imagery, icon assets, image grids, grid splitting, image post-processing,
  background removal, image optimization, asset preparation, Azure Foundry image
  models, or any kind of generated visual content for their application. Also trigger
  when the user asks about wiring image generation endpoints, building an image
  service, creating a prompt builder, splitting a generated grid into individual
  assets, or optimizing images for web or slides. If the user wants any kind of
  generated or processed image integrated into their project, this is the skill.
---

# Image Generation

Generate images via Azure AI Foundry and post-process them with command-line
tools. Supports OpenAI models (gpt-image-1.5) and Black Forest Labs models
(FLUX.2-pro, FLUX.2-flex) — the script auto-routes to the correct API.

## Prerequisites

- `az` CLI logged in (`az login`) to a subscription with an AI Services resource
- `uv` ([astral.sh/uv](https://docs.astral.sh/uv/)) — runs scripts with inline dependency metadata
- `magick` (ImageMagick) — required for FLUX transparency and grid trim

## Setup

Discover available image models:

```bash
az account set --subscription <SUBSCRIPTION_ID>   # if needed
uv run skills/image-generation/scripts/discover-models.py \
  --resource-group <RG> --account <ACCOUNT_NAME>
```

Default to `gpt-image-1.5` if available — it supports all parameters including
transparent background. FLUX models are also supported but with limitations
(see below).

## Model Differences

The script handles routing automatically based on deployment name.

| Capability | gpt-image-1.5 | FLUX.2-pro / FLUX.2-flex |
|------------|---------------|--------------------------|
| Transparent background | Native | Emulated via chroma key (automatic) |
| Quality parameter | Yes | Ignored |
| API endpoint | `cognitiveservices.azure.com` | `services.ai.azure.com` |
| Requires `magick` for transparency | No | Yes (for chroma key removal) |

When `--background transparent` is used with FLUX models, `generate-image.py`
appends a chroma key background color to the prompt. Then run `chroma-key.py`
to strip the background:

```bash
uv run skills/image-generation/scripts/generate-image.py \
  --endpoint $ENDPOINT --deployment FLUX.2-pro \
  --prompt "..." --output raw.png --background transparent

uv run skills/image-generation/scripts/chroma-key.py \
  --input raw.png --output transparent.png
```

`chroma-key.py` uses progressive keying (4%→8%→12% fuzz + 1px alpha erosion)
to cleanly remove the background without eating into icon edges.

## Prompt Principle

Image cost is dominated by output pixels, not input text. **Always write the
longest, most specific prompt you can** — it costs almost nothing extra but
dramatically improves results on the first try.

## Image Generation

```bash
uv run skills/image-generation/scripts/generate-image.py \
  --endpoint <ENDPOINT_URL> \
  --deployment <DEPLOYMENT_NAME> \
  --prompt "Your image description" \
  --output path/to/output.png \
  [--size 1024x1024] [--quality medium] \
  [--background opaque] [--output-format png]
```

| Parameter | Values | Default | Notes |
|-----------|--------|---------|-------|
| `--size` | `1024x1024`, `1024x1536`, `1536x1024`, `auto` | `1024x1024` | All models |
| `--quality` | `low`, `medium`, `high` | `medium` | OpenAI only, ignored for FLUX |
| `--background` | `opaque`, `transparent` | `opaque` | All models (FLUX uses chroma key) |

## Post-Processing

Prefer CLI tools over Python image libraries. See `references/post-processing.md` for full reference.

| Task | Tool |
|------|------|
| Resize, convert, crop | `sips` (macOS built-in) |
| Precise crop, trim, composite | `magick` (ImageMagick) |
| Lossy PNG compression | `pngquant` |
| Lossless PNG optimization | `optipng` |
| Split grid into tiles | `split-grid.py` (included) |

## Generation Patterns

Pick the pattern that matches the task. **Read the reference only when needed.**

| Pattern | When to use | Reference |
|---------|-------------|-----------|
| Slide backgrounds | Presentation slides, deck backgrounds | `references/pattern-slides.md` |
| Transparent inserts | Icons, mascots, logos, overlays | `references/pattern-transparent.md` |
| Hero images / banners | Website headers, marketing banners | `references/pattern-hero.md` |
| Image grids | Batch 4-9 assets in one 2x2 or 3x3 call. Includes default prompt suffixes (flat + detailed) to append to your content prompt. | `references/pattern-grids.md` |

## Resources

| Path | Purpose |
|------|---------|
| `scripts/discover-models.py` | List image-capable deployments on an Azure AI Services account |
| `scripts/generate-image.py` | Generate an image and save to disk (auto-routes OpenAI vs FLUX) |
| `scripts/chroma-key.py` | Remove chroma key background from FLUX images (progressive keying) |
| `scripts/split-grid.py` | Split a grid image into tiles (`--trim`, `--validate`) |
| `references/post-processing.md` | CLI tools reference (sips, magick, pngquant, optipng) |
| `references/pattern-slides.md` | Slide / presentation background prompts |
| `references/pattern-transparent.md` | Transparent asset prompts (icons, inserts) |
| `references/pattern-hero.md` | Hero image / banner prompts |
| `references/pattern-grids.md` | Grid generation with default prompt suffixes |
