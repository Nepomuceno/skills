---
name: architecture-diagram
description: >
  Generate SVG architecture diagrams, hero images, system overview illustrations, tool-ecosystem maps,
  methodology/cycle diagrams, apparatus diagrams, catalog-contract-consumer diagrams, and synchronized-state
  tables for project READMEs and documentation.
  Use this skill whenever the user mentions creating a hero diagram, architecture SVG, system diagram, README hero image,
  project overview illustration, OV-1 diagram, data flow diagram, pipeline diagram, ecosystem diagram, tool ecosystem,
  multi-row diagram, feedback-loop diagram, methodology diagram, or any kind of technical SVG illustration
  for documentation. Also trigger when the user wants a visual representation of their system's components, data flow,
  peer relationships between tools, or architecture in SVG format — even if they just say "make a diagram" or
  "create a visual for the README".
  This skill produces hand-crafted SVG with IBM Plex Mono typography, clean geometric shapes, and a configurable
  color palette, supporting layouts from a simple three-panel pipeline up to full multi-row ecosystem maps
  (1200×860) with sub-card grids, cross-cutting dashed connectors, and feedback arcs.
  Diagrams render natively on any git forge that displays SVGs (GitHub, etc.) and include PNG fallback generation via Playwright.
---

# Architecture Diagram Skill

Generate production-quality SVG architecture diagrams for project READMEs and documentation. These diagrams follow an engineering-schematic visual language: monospace typography, geometric precision, zero border-radius, and a clear left-to-right information flow.

## When to Use

- Creating a `hero.svg` for a project README
- Visualizing system architecture, data pipelines, or component relationships
- Generating OV-1 (Operational View) diagrams
- Any time a project needs a technical SVG illustration

## Design Principles

The diagrams are inspired by engineering schematics and brutalist typography:

- **Monospace only** — IBM Plex Mono at every scale, no sans-serif mixing
- **Geometric precision** — rectangles, lines, arrows, circles; no organic shapes or gradients
- **Zero radius** — sharp corners everywhere (`rx="0"` or omitted)
- **Left-to-right flow** — inputs on the left, processing in the center, outputs on the right
- **Dark title bar** — full-width header strip with project name left and subtitle right
- **Structural hierarchy** — dark header bars on section boxes, divider lines between subsections
- **Purposeful color** — accent color used sparingly for highlights and status indicators

## SVG Structure

Every diagram shares the same outer chrome — a dark **title bar** with project name and subtitle, an optional **subhead strip** (1-line summary on the left, status/qualifier on the right), an inner content area, and a **footer** with tagline (optionally followed by a small "Built with X" attribution mark). What lives between header and footer is **whatever layout best represents the system** — the three-panel pipeline is one option, not the rule.

### Dimensions

- **Viewbox**: `1200 × 430` (standard pipeline), `1200 × 600–900` (ecosystem / multi-row), `1200 × 500` (with subhead strip + footer logo)
- **Outer border**: 3px stroke, primary color
- **Title bar**: 36px tall, primary fill, 14px bold project name left, 11px subtitle right (muted color)
- **Subhead strip** (optional): 26–30px tall, no fill, 1px muted border, 9px text inside
- **Section header bars on panels**: 22–32px tall, primary fill, 10–13px bold background-color text
- **Section padding**: 16px from panel edges; text x = panel-x + 16
- **Arrow markers**: 7×7 polygon, `refX="6" refY="3.5" orient="auto"`; reuse via `<defs><marker id="a">…</marker></defs>` and `marker-end="url(#a)"`

### Panel Layouts — Pick Whatever Fits

The layouts below are all drawn from production examples. Choose by **what the system actually is**, not by default.

| Layout | When to use | viewBox | Example |
|--------|-------------|---------|---------|
| **Three-panel pipeline** | Input → Process → Output flow (converters, compilers, sync tools) | 1200×430 | `kit`, `rune`, `pipeline` |
| **Two-panel** | One system producing many outputs | 1200×430 | simple generators |
| **Four-panel** | Context → Input → Process → Output | 1200×430–500 | `hero-harness` (Dev → Harness → Outputs with substrate) |
| **Hub-and-spoke** | One core process with radiating inputs/outputs | 1200×430+ | central engines |
| **Multi-row grid** | Tool ecosystem with peer relationships, one component installs/orchestrates others | 1200×600–900 | `ecosystem.svg` (rune+synthesist row, muxr row, kit row) |
| **Catalog + consumer** | Reusable components on one side, consumers on the other, contract in the middle | 1200×430 | `pipeline.svg` |
| **Cycle / feedback loop** | Build → Measure → Refine with arc back to start | 1200×430 | `hero-methodology.svg` |
| **Apparatus** | Domain → Apparatus → Discoveries+Outputs (apparatus larger than the rest) | 1200×430 | `hero-apparatus.svg` |
| **Synchronized state table** | Show multiple subsystems kept in lockstep with column-aligned rows | 1200×430 | `muxr.svg` outputs panel |

The three-panel left-to-right flow is one starting point. For ecosystem diagrams (multiple peer tools that compose), use **multi-row grid** — do not force them into Input/Process/Output. For methodology/process diagrams, use the **cycle** layout with a curved feedback arc.

### Multi-Row Grid Layout

For tool-ecosystem diagrams (multiple cooperating components, not a single linear flow), use a multi-row layout. The pattern from `ecosystem.svg`:

```
┌──────────────────────────────────────────────────────────────┐
│ TITLE BAR                                                    │
├───────────────────────────┬──────────────────────────────────┤
│  TOOL A (peer)            │  TOOL B (peer)                   │   ← row 1: peers
│  description + commands   │  description + commands          │
├───────────────────────────┴──────────────────────────────────┤
│              ↘ dashed cross-arrows down ↙                    │   ← arrow zone with
│              italic captions ("skills →")                    │     italic labels
├──────────────────────────────────────────────────────────────┤
│  ORCHESTRATOR (full width, dashed border = container)        │
│  ┌─────────┬─────────┬─────────┬─────────┐                   │   ← row 2: sub-cards
│  │ subcard │ subcard │ subcard │ subcard │  (sessions,       │     in a grid
│  │         │         │         │ dashed= │   instances,      │
│  │         │         │         │ remote  │   tenants…)       │
│  └─────────┴─────────┴─────────┴─────────┘                   │
│  command examples in accent color below                      │
├──────────────────────────────────────────────────────────────┤
│              ↑ solid arrow up: "installs all" ↑              │
├──────────────────────────────────────────────────────────────┤
│  FOUNDATION (full width — registry, substrate, kernel)       │   ← row 3: foundation
│  provides: a · b · c · d · e · f ...                         │
├──────────────────────────────────────────────────────────────┤
│ FOOTER (tagline + optional attribution mark)                 │
└──────────────────────────────────────────────────────────────┘
```

Key measurements for multi-row grid (1200 × 860):
- Row 1: y=48–210 (162px tall), two boxes split at 30/615 with 30px gutter
- Arrow zone 1: y=210–320 (110px) — dashed lines, italic captions
- Row 2: y=320–600 (280px tall) — full-width container, often dashed border; inner sub-cards on a 4-column grid starting at x=50 with 240px width and 20px gutters
- Arrow zone 2: y=600–660 (60px) — single solid vertical arrow with caption
- Row 3: y=660–760 (100px tall) — full-width foundation
- Footer: y=780+

Use `stroke-dasharray="5,3"` (border) and a `#6b5d4f` (muted) header bar on sub-cards to indicate **remote / future / optional** instances.

## Color Palettes

Read `references/palettes.md` for the full palette definitions. The skill supports multiple palettes:

### Choosing a Palette

- **Ask the user** if they have a preference or existing brand colors
- **Match the project** — if the project already has a design system (like DESIGN.md), derive the palette from it
- **Default to Industrial** if no preference is given

The palette defines 5 roles:
1. **primary** — text, borders, title bar fill (darkest color)
2. **background** — SVG background (lightest color)
3. **secondary** — body text, descriptions
4. **muted** — dividers, subtle text, decorative lines
5. **accent** — highlights, status indicators, callouts (used sparingly)

## Text Hierarchy

| Role | Size | Weight | Color |
|------|------|--------|-------|
| Project name (title bar) | 14px | bold | background |
| Subtitle (title bar) | 11px | normal | muted |
| Section header (dark bar) | 11-13px | bold | background |
| Subhead / label | 9px | bold | primary |
| Body text | 9px | normal | secondary |
| Caption / annotation | 8-10px | normal | muted |
| Footer tagline | 10px | normal | secondary |

All text uses `font-family="'IBM Plex Mono', monospace"`.

## Content Guidelines

### What goes in each panel

**Input panel**: What the system consumes — file formats, APIs, configuration, user input. List concrete types and examples.

**Process panel**: What the system does — transformation steps, algorithms, key operations. Can include a mini schematic (multiplexer symbol, pipeline stages, state machine).

**Output panel**: What the system produces — file formats, reports, artifacts, side effects. Include concrete examples.

### Writing style

- Use lowercase for descriptions, UPPERCASE for labels and headers
- Keep lines short (fit within panel width)
- Use `&#183;` (middle dot) as a separator in inline lists
- Use `&#8594;` (→) for flow descriptions
- Be specific — "parse KeBNF source" not "process input"
- Include version numbers, file extensions, protocol names where relevant

### Visual elements within panels

Beyond text, panels can contain:

- **Mini wireframes** — simplified UI representations using rectangles and text
- **Sparklines** — simple polyline charts for data visualization concepts
- **Color swatches** — small rectangles showing a palette
- **Status indicators** — small circles (filled) for state representation
- **Multiplexer symbols** — converging lines through a junction box (see `muxr.svg`: three input rails with `circle r="3"` terminals converging through a small square junction labeled "M", then a single output rail with arrow)
- **Tree structures** — indented text with connector lines
- **Column-aligned state tables** — for "synchronized state" diagrams, lay out 3+ columns with a thin header line, then stacked rows of small bordered boxes; use `stroke-dasharray="5,3"` on rows representing remote/future state (see `muxr.svg` outputs panel: TMUX SESSION | SESSION FILE | RUNTIME ID)
- **Sub-card grids** — inside a full-width row, embed 3–4 smaller bordered cards in a horizontal grid (see `ecosystem.svg` row 2: four 240×140 session cards)
- **Inline command examples** — drop literal CLI invocations into a panel using the accent/muted color, e.g. `<text fill="#c4b99a">kit setup --registry ...</text>`
- **Stacked component cards** — multiple small panels stacked vertically with their own mini header bar (see `pipeline.svg` left column: rust-cli, latex-paper, cloudflare-pages, container-image)

### Section labels above panels

For more typographic structure, place a small uppercase label *above* the panel border instead of (or in addition to) a header bar inside it:

```xml
<text x="40" y="98" font-family="'IBM Plex Mono', monospace"
      font-size="9" fill="#6b5d4f" letter-spacing="0.08em"
      font-weight="500">DOMAIN</text>
<rect x="40" y="106" width="220" height="220" fill="none" stroke="#2c2417" stroke-width="2"/>
```

This is the `hero-apparatus.svg` pattern. Use it when you want the panel itself to feel "framed" rather than "headered".

### Soft-fill highlighting

To draw subtle attention to a primary item in a list of sub-cards without breaking the monochrome look, use the primary color at low opacity as a fill on top of the same primary stroke:

```xml
<rect x="56" y="120" width="188" height="42" fill="#2c2417" opacity="0.04"/>
<rect x="56" y="120" width="188" height="42" fill="none" stroke="#2c2417" stroke-width="1.5"/>
```

The first rect is a tinted background, the second is the crisp border. Opacity values 0.03–0.06 give a "selected" or "active" feel without color.

### Dashed strokes for state

- `stroke-dasharray="3,3"` — speculative / future / planned items
- `stroke-dasharray="5,3"` — remote / external / non-local
- `stroke-dasharray="6,3"` — cross-row / cross-cutting relationship arrows
- `stroke-dasharray="8,4"` — container boundary around a group (e.g. ecosystem.svg row 2 outer dashed border indicating "this is the orchestrator's surface")

### Feedback / loop arcs

For cycle and methodology diagrams, draw a curved dashed path from the last panel back to the first using a single `<path>` with cubic/quadratic curves:

```xml
<path d="M 1145 360 Q 1145 380 1100 380 L 100 380 Q 55 380 55 360"
      fill="none" stroke="#c4b99a" stroke-width="1" stroke-dasharray="4,3"/>
<text x="600" y="376" font-family="'IBM Plex Mono', monospace"
      font-size="8" fill="#9c9890" text-anchor="middle">discoveries inform what to build next</text>
```

For cross-row diagonal arrows between non-adjacent peers (ecosystem-style), use a straight dashed line with an italic caption:

```xml
<line x1="200" y1="210" x2="160" y2="320" stroke="#6b5d4f" stroke-width="1.5"
      stroke-dasharray="6,3" marker-end="url(#ards)"/>
<text x="220" y="268" font-style="italic" fill="#6b5d4f"
      font-family="'IBM Plex Mono', monospace" font-size="8">skills →</text>
```

Define a second arrow marker (e.g. `id="ards"`) in muted color so dashed cross-arrows don't visually compete with the primary solid arrows.

### Footer

A divider line + a centered tagline. Optionally append a small "Built with X" attribution mark below it (project host, internal team, etc.) — keep it muted so it doesn't compete with the diagram body:

```xml
<line x1="40" y1="370" x2="1160" y2="370" stroke="#c4b99a" stroke-width="1"/>
<text x="600" y="392" font-family="'IBM Plex Mono', monospace"
      font-size="10" fill="#6b5d4f" text-anchor="middle">tagline</text>
<!-- optional attribution: -->
<text x="600" y="416" text-anchor="middle" fill="#2c2417"
      font-family="'IBM Plex Mono', monospace" font-size="9" font-weight="600">Built with X</text>
```

Adjust the y coordinates of the line and text relative to the SVG height (the line sits ~60px above bottom for 430-height; ~80px for taller diagrams).

## Generating the SVG

1. Analyze the project to understand its architecture
2. Choose the appropriate panel layout
3. Select or derive a color palette
4. Write the SVG by hand — do NOT use a library or tool
5. Place text carefully, measuring approximate character widths (5.4px per char at 9px font size)
6. Test that the SVG renders correctly

### SVG Hygiene

- Always include `xmlns="http://www.w3.org/2000/svg"`
- Define arrow markers in `<defs>` and reference via `marker-end="url(#a)"`
- Use `text-anchor="middle"` for centered text, `"end"` for right-aligned
- Keep stroke widths consistent: 3px outer, 2-2.5px section boxes, 1.5px arrows, 0.8-1px dividers
- Font loading: SVG text relies on the viewer having IBM Plex Mono installed or loaded via Google Fonts. GitHub renders SVGs in an `<img>` tag so fonts may fall back to system monospace — this is acceptable

## PNG Fallback

After creating the SVG, generate a PNG fallback using Playwright:

```typescript
import { chromium } from 'playwright';
import { readFileSync } from 'fs';

const svg = readFileSync('hero.svg', 'utf-8');
const html = `<!DOCTYPE html>
<html><head>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>body{margin:0;padding:0;}</style>
</head><body>${svg}</body></html>`;

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1200, height: 430 }, deviceScaleFactor: 2 });
await page.setContent(html, { waitUntil: 'networkidle' });
await page.waitForTimeout(1000);
await page.screenshot({ path: 'hero.png', clip: { x: 0, y: 0, width: 1200, height: 430 } });
await browser.close();
```

Adjust the viewport height to match the SVG viewBox height.

## README Integration

Place the hero as the very first line of the README:

```markdown
![hero](hero.svg)

# Project Name

...
```

Convention: hero first, then title, then badges, then description.

## Adaptation

The three-panel pipeline is one starting point of many. Adapt freely based on what the system actually is:

- **Linear flow** (converter, compiler, sync tool) → three-panel pipeline, 1200×430
- **Tool ecosystem** (multiple peer components that cooperate) → multi-row grid, 1200×600–900
- **Catalog + consumers** (reusable parts on one side, users on the other) → catalog/contract/consumer three-column, 1200×430
- **Methodology / cycle** (build → measure → refine, repeated) → three-panel with curved feedback arc back to the start
- **Apparatus / framework** (one big central thing, smaller things on either side) → asymmetric three-panel where the center is 1.5–2× wider than the wings
- **Synchronized state** (one address kept consistent across N subsystems) → column-aligned state table inside the outputs panel

Beyond layout, scale freely:

- **Wider diagrams**: increase viewBox width to 1400 or 1600 for dense content
- **Taller diagrams**: 600+ for multi-row, 860 for full ecosystems
- **Multiple rows**: stack panels vertically with dedicated arrow zones (60–110px) between rows
- **Embedded mini-diagrams**: include simplified UI wireframes, data models, multiplexer symbols, or state machines within panels
- **Project-specific accents**: pull the accent color from the project's design system

See `references/examples.md` for full SVG skeletons for each layout type.
