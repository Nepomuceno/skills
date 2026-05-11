---
name: architecture-diagram
description: >
  Use this skill whenever the user asks for a hero image for a README, an
  architecture diagram, a system overview SVG, a data-flow or pipeline diagram,
  a tool-ecosystem map, a methodology / cycle diagram, an OV-1 (Operational View)
  illustration, a feedback-loop diagram, or any kind of hand-crafted technical
  SVG illustration for documentation. Also trigger on vaguer phrasing like
  "make a diagram for the README", "visualize the system architecture", or
  "show how these components connect". Produces hand-crafted SVG with
  IBM Plex Mono typography, sharp geometric shapes, and a configurable color
  palette. Supports layouts from a simple three-panel pipeline up to multi-row
  ecosystem maps (1200×860) with sub-card grids, cross-cutting dashed connectors,
  and curved feedback arcs. Diagrams render natively on any forge that displays
  SVGs and have an optional PNG fallback via Playwright.
---

# Architecture Diagram Skill

Generate production-quality SVG architecture diagrams for project READMEs and documentation. The visual language is engineering-schematic: monospace typography, sharp corners, geometric precision, purposeful color.

## When to Use

- Creating a `hero.svg` for a project README
- Visualizing system architecture, data pipelines, or component relationships
- Generating OV-1 diagrams
- Any time a project needs a technical SVG illustration

## Design Principles

- **Monospace only** — IBM Plex Mono at every scale, no sans-serif mixing
- **Geometric precision** — rectangles, lines, arrows, circles; no organic shapes or gradients
- **Zero radius** — sharp corners everywhere (`rx="0"` or omitted)
- **Left-to-right flow** when the system is a pipeline; pick a different topology when it is not
- **Dark title bar** — full-width header strip with project name left and subtitle right
- **Structural hierarchy** — dark header bars on section boxes, divider lines between subsections
- **Purposeful color** — accent color used sparingly for highlights and status only

Why monospace and sharp corners: these diagrams sit next to source code in READMEs. Rounded corners and sans-serif fonts read as marketing; sharp corners and monospace read as engineering. The constraint protects the tone.

## SVG Structure

Every diagram shares the same outer chrome:

- A dark **title bar** with project name (left) and subtitle (right)
- An optional **subhead strip** (one-line summary left, status qualifier right)
- An **inner content area** — the only part that varies between layouts
- A **footer** with tagline, optionally followed by a small "Built with X" attribution mark

What lives between header and footer is whatever layout best represents the system — the three-panel pipeline is one option, not the rule.

### Dimensions

- **viewBox**: `1200 × 430` (standard pipeline), `1200 × 500` (with subhead strip), `1200 × 600–900` (ecosystem / multi-row)
- **Outer border**: 3px stroke, primary color
- **Title bar**: 36px tall, primary fill; 14px bold project name; 11px subtitle in muted color
- **Subhead strip** (optional): 26–30px tall, no fill, 1px muted border, 9px text inside
- **Section header bars on panels**: 22–32px tall, primary fill, 10–13px bold text in background color
- **Section padding**: 16px from panel edges (text x = panel-x + 16)
- **Arrow markers**: 7×7 polygon, `refX="6" refY="3.5" orient="auto"`; define once in `<defs>` and reference via `marker-end="url(#a)"`

### Panel Layouts — Pick Whatever Fits

Choose by **what the system actually is**, not by default.

| Layout | When to use | viewBox |
|--------|-------------|---------|
| **Three-panel pipeline** | Input → Process → Output flow (converters, compilers, sync tools) | 1200×430 |
| **Two-panel** | One system producing many outputs | 1200×430 |
| **Four-panel** | Context → Input → Process → Output | 1200×430–500 |
| **Hub-and-spoke** | One core process with radiating inputs/outputs | 1200×430+ |
| **Multi-row grid** | Tool ecosystem with peer components, one of them orchestrating others | 1200×600–900 |
| **Catalog + consumer** | Reusable components on one side, consumers on the other, contract in the middle | 1200×430 |
| **Cycle / feedback loop** | Build → Measure → Refine with arc back to start | 1200×430 |
| **Apparatus** | Domain → Apparatus → Discoveries+Outputs (apparatus larger than the wings) | 1200×430 |
| **Synchronized state table** | Show multiple subsystems kept in lockstep with column-aligned rows | 1200×430 |

For ecosystem diagrams (multiple peer tools that compose), use **multi-row grid** — do not force them into Input/Process/Output. For methodology/process diagrams, use the **cycle** layout with a curved feedback arc. Full SVG skeletons for every layout are in `references/examples.md`.

### Multi-Row Grid Layout

For tool-ecosystem diagrams, use a multi-row layout:

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
│  │         │         │         │ dashed = │   instances,     │
│  │         │         │         │ remote   │   tenants…)      │
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

Reference measurements for 1200 × 860:

- Row 1: y=48–210 (162px), two boxes split at x=30/615 with 30px gutter
- Arrow zone 1: y=210–320 (110px) — dashed lines, italic captions
- Row 2: y=320–600 (280px) — full-width container, often dashed border; inner sub-cards on a 4-column grid starting at x=50 with 240px width and 20px gutters
- Arrow zone 2: y=600–660 (60px) — single solid vertical arrow with caption
- Row 3: y=660–760 (100px) — full-width foundation
- Footer: y=780+

Use `stroke-dasharray="5,3"` on a sub-card's border and a muted header bar to indicate **remote / future / optional** instances.

## Color Palettes

See `references/palettes.md` for the full palette catalog. The skill supports multiple palettes; default to **Industrial** if the user has no preference. If the project has its own design system (e.g. a `DESIGN.md`), derive the palette from it.

Every palette defines 5 semantic roles:

1. **primary** — text, borders, title bar fill (darkest color)
2. **background** — SVG background (lightest color)
3. **secondary** — body text, descriptions
4. **muted** — dividers, subtle text, decorative lines
5. **accent** — highlights, status indicators, callouts (used sparingly)

Throughout this document, code snippets use the placeholders `PRIMARY`, `BACKGROUND`, `SECONDARY`, `MUTED`, `ACCENT` — substitute the actual hex values from the chosen palette when authoring.

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

- **Input panel**: what the system consumes — file formats, APIs, configuration, user input. List concrete types and examples.
- **Process panel**: what the system does — transformation steps, algorithms, key operations. Can include a mini schematic.
- **Output panel**: what the system produces — file formats, reports, artifacts, side effects. Include concrete examples.

### Writing style

- Lowercase for descriptions, UPPERCASE for labels and headers
- Keep lines short (fit within panel width — see character-width estimation in `references/examples.md`)
- Use `&#183;` (middle dot) as a separator in inline lists
- Use `&#8594;` (→) for flow descriptions
- Be specific — "parse KeBNF source" not "process input"
- Include version numbers, file extensions, protocol names where relevant

### Visual elements within panels

Beyond text, panels can contain:

- **Mini wireframes** — simplified UI representations using rectangles and text
- **Sparklines** — simple polyline charts for data visualization concepts
- **Color swatches** — small rectangles showing a palette
- **Status indicators** — small filled circles for state representation
- **Multiplexer symbols** — three input rails with `circle r="3"` terminals converging through a small square junction labeled "M", then a single output rail with an arrow
- **Tree structures** — indented text with connector lines
- **Column-aligned state tables** — for "synchronized state" diagrams: 3+ columns with a thin header line, then stacked rows of small bordered boxes; use `stroke-dasharray="5,3"` on rows representing remote/future state
- **Sub-card grids** — inside a full-width row, embed 3–4 smaller bordered cards in a horizontal grid (e.g. 240×140 cards on a 4-column grid)
- **Inline command examples** — drop literal CLI invocations into a panel using the muted/accent color so they read as code
- **Stacked component cards** — multiple small panels stacked vertically with their own mini header bar (good for the left column of a catalog+consumer layout)

### Section labels above panels

For more typographic structure, place a small uppercase label *above* the panel border instead of (or in addition to) a header bar inside it:

```xml
<text x="40" y="98" font-family="'IBM Plex Mono', monospace"
      font-size="9" fill="MUTED" letter-spacing="0.08em"
      font-weight="500">DOMAIN</text>
<rect x="40" y="106" width="220" height="220" fill="none" stroke="PRIMARY" stroke-width="2"/>
```

Use this when you want the panel itself to feel "framed" rather than "headered".

### Soft-fill highlighting

To draw subtle attention to a primary item in a list of sub-cards without breaking the monochrome look, use the primary color at low opacity as a fill *behind* the same primary stroke:

```xml
<rect x="56" y="120" width="188" height="42" fill="PRIMARY" opacity="0.04"/>
<rect x="56" y="120" width="188" height="42" fill="none" stroke="PRIMARY" stroke-width="1.5"/>
```

The first rect is the tinted background, the second is the crisp border. Opacity 0.03–0.06 gives a "selected" or "active" feel without introducing color. Why two rects instead of `fill-opacity`: the stroke must stay at full opacity for the border to read cleanly.

### Dashed strokes for state

- `stroke-dasharray="3,3"` — speculative / future / planned items
- `stroke-dasharray="5,3"` — remote / external / non-local
- `stroke-dasharray="6,3"` — cross-row / cross-cutting relationship arrows
- `stroke-dasharray="8,4"` — container boundary around a group (the dashed outer frame around a row that holds sub-cards)

### Feedback / loop arcs

For cycle and methodology diagrams, draw a curved dashed path from the last panel back to the first using a single `<path>` with quadratic curves at each corner:

```xml
<path d="M 1145 360 Q 1145 380 1100 380 L 100 380 Q 55 380 55 360"
      fill="none" stroke="MUTED" stroke-width="1" stroke-dasharray="4,3"/>
<text x="600" y="376" font-family="'IBM Plex Mono', monospace"
      font-size="8" fill="MUTED" text-anchor="middle">discoveries inform what to build next</text>
```

For cross-row diagonal arrows between non-adjacent peers (ecosystem-style), use a straight dashed line with an italic caption:

```xml
<line x1="200" y1="210" x2="160" y2="320" stroke="MUTED" stroke-width="1.5"
      stroke-dasharray="6,3" marker-end="url(#ards)"/>
<text x="220" y="268" font-style="italic" fill="MUTED"
      font-family="'IBM Plex Mono', monospace" font-size="8">skills →</text>
```

Define a second arrow marker (e.g. `id="ards"`) in muted color so dashed cross-arrows don't compete visually with the primary solid arrows.

### Footer

A divider line + a centered tagline. Optionally append a small "Built with X" attribution mark below it — keep it muted so it doesn't compete with the diagram body:

```xml
<line x1="40" y1="370" x2="1160" y2="370" stroke="MUTED" stroke-width="1"/>
<text x="600" y="392" font-family="'IBM Plex Mono', monospace"
      font-size="10" fill="SECONDARY" text-anchor="middle">tagline</text>
<!-- optional attribution: -->
<text x="600" y="416" text-anchor="middle" fill="PRIMARY"
      font-family="'IBM Plex Mono', monospace" font-size="9" font-weight="600">Built with X</text>
```

Adjust the y coordinates relative to the SVG height (the line sits ~60px above bottom for 430-height; ~80px for taller diagrams).

## Generating the SVG

1. Analyze the project to understand its architecture
2. Choose the appropriate panel layout (see the table above)
3. Select or derive a color palette
4. Write the SVG by hand — do NOT use a library or tool; hand-tuned coordinates produce the engineering-schematic look
5. Place text carefully, measuring approximate character widths (5.4px per char at 9px font size)
6. Test that the SVG renders correctly in a browser

### SVG Hygiene

- Always include `xmlns="http://www.w3.org/2000/svg"`
- Define arrow markers in `<defs>` and reference via `marker-end="url(#a)"`
- Use `text-anchor="middle"` for centered text, `"end"` for right-aligned
- Keep stroke widths consistent: 3px outer, 2–2.5px section boxes, 1.5px arrows, 0.8–1px dividers
- Font fallback: SVG text relies on the viewer having IBM Plex Mono installed or loaded via Google Fonts. GitHub renders SVGs in an `<img>` tag so fonts may fall back to system monospace — this is acceptable

### PNG Fallback

For viewers that don't render SVG well (or for embedding in slides), generate a PNG companion via Playwright. The full script is in `references/png-fallback.md`. Short version: render the SVG inside an HTML page that loads IBM Plex Mono from Google Fonts, then screenshot the page at 2× device scale.

## README Integration

Place the hero as the very first line of the README:

```markdown
![hero](hero.svg)

# Project Name

...
```

Convention: hero first, then title, then badges, then description.
