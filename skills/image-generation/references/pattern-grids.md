# Pattern: Image Grids

Generate multiple related assets in a single API call — icon sets, thumbnail
variants, style explorations. One call instead of N.

## Requirements

- **Size:** `1024x1024` — **Background:** `transparent` — **Quality:** `high`
- Always `--background transparent`. Without it you can't trim, validate, or distinguish empty cells from background.

## Grid sizes

| Grid | Tiles | Tile size | Notes |
|------|-------|-----------|-------|
| 2x2 | 4 | 512x512 | Simpler, works even with shorter prompts |
| 3x3 | 9 | ~341x341 | Needs detailed prompts + `--trim` to crop tiles to content |

More than 9? Use multiple grids or individual 1024x1024 calls.

## Prompt rules

- **Describe every cell by position and content** — "Row 1: (1) house icon, (2) search icon, (3) gear icon"
- **Never ask for grid lines, borders, or dividers** — the model draws them at arbitrary positions that don't align with the mathematical tile boundaries
- **Never ask for text labels** — they get clipped by the split
- **Append a default suffix** (below) to handle layout, spacing, and anti-bleed

## Default prompt suffixes

Append one of these to your content prompt. They handle layout, spacing, and
rendering style only — your base prompt controls what icons look like, colors,
and per-cell content.

### 3x3 — flat

```
Flat vector style, solid fills, clean geometric shapes, no gradients, no shadows, no 3D effects, consistent stroke weight across all icons. Layout: each icon is centered precisely in its grid cell with equal padding on all four sides. Every icon occupies the same proportional area within its cell — uniform sizing across all 9 positions. Maintain at least 15% transparent padding between each icon and the edges of its cell on every side. No icon element extends beyond its cell boundary. Each icon is a self-contained shape that does not touch, overlap, or visually connect with any neighboring icon. The 9 cells are evenly spaced in a perfect 3x3 arrangement with consistent gutters. No borders, no grid lines, no dividers, no text labels, no text of any kind.
```

### 3x3 — detailed

```
Soft gradient style with subtle depth, gentle shading, and polished micro-detail on each icon. Each icon is a small, self-contained illustration floating alone in generous empty transparent space. Layout: every icon is centered in its grid cell using at most 55% of the cell area, leaving at least 25% transparent padding on every side. No icon touches or overlaps any edge of its cell boundary. No icon element bleeds into or visually connects with any neighboring cell. All 9 icons maintain uniform sizing — each one occupies the same proportional footprint within its cell. The 9 cells are evenly spaced in a perfect 3x3 arrangement with wide consistent gutters between them. Think of each cell as an independent artboard. No borders, no grid lines, no dividers, no text labels, no text of any kind.
```

### 2x2 — flat

```
Flat vector style, solid fills, clean geometric shapes, no gradients, no shadows, no 3D effects, consistent stroke weight across all icons. Layout: each icon is centered precisely in its grid cell with equal padding on all four sides. Every icon occupies the same proportional area within its cell — uniform sizing across all 4 positions. Maintain at least 15% transparent padding between each icon and the edges of its cell on every side. No icon element extends beyond its cell boundary. Each icon is a self-contained shape that does not touch, overlap, or visually connect with any neighboring icon. The 4 cells are evenly spaced in a perfect 2x2 arrangement with consistent gutters. No borders, no grid lines, no dividers, no text labels, no text of any kind.
```

### 2x2 — detailed

```
Soft gradient style with subtle depth, gentle shading, and polished micro-detail on each icon. Each icon is a small, self-contained illustration floating alone in generous empty transparent space. Layout: every icon is centered in its grid cell using at most 55% of the cell area, leaving at least 25% transparent padding on every side. No icon touches or overlaps any edge of its cell boundary. No icon element bleeds into or visually connects with any neighboring cell. All 4 icons maintain uniform sizing — each one occupies the same proportional footprint within its cell. The 4 cells are evenly spaced in a perfect 2x2 arrangement with wide consistent gutters between them. Think of each cell as an independent artboard. No borders, no grid lines, no dividers, no text labels, no text of any kind.
```

## Example: 3x3 with flat suffix

Content prompt (you write this part):

> A 3x3 grid of 9 icons on a transparent background. Each icon occupies exactly one cell. The 9 icons from left-to-right, top-to-bottom are: Row 1: (1) a house icon, (2) a magnifying glass search icon, (3) a gear settings icon. Row 2: (4) a person/user icon, (5) a heart favorites icon, (6) a bell notification icon. Row 3: (7) an envelope mail icon, (8) a star icon, (9) a download arrow icon. All icons in solid charcoal gray (#333333).

Then append the **3x3 flat suffix** from above. Full command:

```bash
uv run skills/image-generation/scripts/generate-image.py \
  --endpoint $ENDPOINT --deployment gpt-image-1.5 \
  --prompt "<content prompt> <flat suffix>" \
  --size 1024x1024 --quality high --background transparent \
  --output grid.png
```

## Splitting

```bash
# 2x2
uv run skills/image-generation/scripts/split-grid.py \
  --input grid.png --rows 2 --cols 2 --output-dir tiles/ --trim --validate

# 3x3
uv run skills/image-generation/scripts/split-grid.py \
  --input grid.png --rows 3 --cols 3 --output-dir tiles/ --trim --validate
```

`--trim` crops each tile to its content bounding box. `--validate` checks each
tile has non-transparent pixels (default 1% threshold, adjust with `--min-content-pct`).

## When grids don't work

Fall back to individual 1024x1024 calls when:
- Validation reports empty cells
- Icons have very different shapes/sizes
- You need pixel-perfect control per asset
