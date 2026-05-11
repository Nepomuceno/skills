# SVG Examples

## Three-Panel Pipeline (canonical layout)

The default layout. Left-to-right flow: Input → Process → Output. Good for converters, compilers, and sync tools.

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 430" width="1200" height="430">
  <defs>
    <marker id="a" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto">
      <polygon points="0,0 7,3.5 0,7" fill="PRIMARY"/>
    </marker>
  </defs>

  <!-- Background + border -->
  <rect x="0" y="0" width="1200" height="430" fill="BACKGROUND" stroke="PRIMARY" stroke-width="3"/>

  <!-- Title bar -->
  <rect x="0" y="0" width="1200" height="36" fill="PRIMARY"/>
  <text x="16" y="24" font-family="'IBM Plex Mono', monospace"
        font-size="14" fill="BACKGROUND" font-weight="bold">project-name</text>
  <text x="1184" y="24" font-family="'IBM Plex Mono', monospace"
        font-size="11" fill="MUTED" text-anchor="end">Short subtitle</text>

  <!-- Optional subhead strip -->
  <rect x="40" y="52" width="1120" height="26" fill="none" stroke="MUTED" stroke-width="1"/>
  <text x="56" y="69" font-family="'IBM Plex Mono', monospace"
        font-size="9" fill="SECONDARY">pipeline description &#183; key detail</text>

  <!-- LEFT PANEL: Inputs -->
  <rect x="40" y="94" width="260" height="250" fill="none" stroke="PRIMARY" stroke-width="2"/>
  <rect x="40" y="94" width="260" height="28" fill="PRIMARY"/>
  <text x="170" y="112" font-family="'IBM Plex Mono', monospace"
        font-size="11" fill="BACKGROUND" text-anchor="middle" font-weight="bold">INPUTS</text>

  <!-- Section label (bold) -->
  <text x="56" y="142" font-family="'IBM Plex Mono', monospace"
        font-size="9" fill="PRIMARY" font-weight="bold">config file</text>
  <!-- Description lines -->
  <text x="56" y="158" font-family="'IBM Plex Mono', monospace"
        font-size="9" fill="SECONDARY">  key: value pairs</text>

  <!-- Divider line within panel -->
  <line x1="56" y1="170" x2="284" y2="170" stroke="MUTED" stroke-width="0.8"/>

  <!-- Arrow: Input → Process -->
  <line x1="300" y1="219" x2="360" y2="219" stroke="PRIMARY"
        stroke-width="1.5" marker-end="url(#a)"/>

  <!-- CENTER PANEL: Process -->
  <rect x="370" y="94" width="340" height="250" fill="none" stroke="PRIMARY" stroke-width="2.5"/>
  <rect x="370" y="94" width="340" height="32" fill="PRIMARY"/>
  <text x="540" y="115" font-family="'IBM Plex Mono', monospace"
        font-size="13" fill="BACKGROUND" text-anchor="middle" font-weight="bold">PROCESS</text>

  <!-- Arrow: Process → Output -->
  <line x1="710" y1="219" x2="770" y2="219" stroke="PRIMARY"
        stroke-width="1.5" marker-end="url(#a)"/>

  <!-- RIGHT PANEL: Outputs -->
  <rect x="780" y="94" width="380" height="250" fill="none" stroke="PRIMARY" stroke-width="2"/>
  <rect x="780" y="94" width="380" height="28" fill="PRIMARY"/>
  <text x="970" y="112" font-family="'IBM Plex Mono', monospace"
        font-size="11" fill="BACKGROUND" text-anchor="middle" font-weight="bold">OUTPUTS</text>

  <!-- Footer -->
  <line x1="40" y1="368" x2="1160" y2="368" stroke="MUTED" stroke-width="1"/>
  <text x="600" y="390" font-family="'IBM Plex Mono', monospace"
        font-size="10" fill="SECONDARY" text-anchor="middle">tagline or summary</text>
</svg>
```

Replace `PRIMARY`, `BACKGROUND`, `SECONDARY`, `MUTED`, and `ACCENT` with values
from the chosen palette (see palettes.md).

---

## Key Measurements

These measurements ensure consistent spacing across diagrams:

| Element | Value |
|---------|-------|
| Viewbox width | 1200 (standard), 1400-1600 (wide) |
| Viewbox height | 430 (standard), 500-600 (tall) |
| Outer border stroke | 3px |
| Title bar height | 36px |
| Title font size | 14px bold |
| Subtitle font size | 11px |
| Section box border | 2-2.5px |
| Section header bar | 28-32px tall |
| Section header font | 11-13px bold |
| Body text font | 9px |
| Caption font | 8-10px |
| Arrow stroke | 1.5px |
| Divider stroke | 0.8-1px |
| Panel internal padding | 16px |
| Inter-panel arrow gap | 50-60px |
| Footer line y-offset | ~24px from bottom content |
| Footer text y-offset | ~20px below footer line |

## Character Width Estimation

At 9px IBM Plex Mono, each character is approximately 5.4px wide.
Use this to estimate text positioning and prevent overflow:

- 40-char line ≈ 216px wide
- Panel width 260px allows ~44 chars with 16px padding each side
- Panel width 340px allows ~57 chars
- Panel width 380px allows ~64 chars

---

## Multi-Row Tool Ecosystem (1200 × 860)

Use this when the system is a set of peer tools that compose around a shared substrate/foundation — *not* a single linear pipeline.

```svg
<svg viewBox="0 0 1200 860" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arr" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="5" markerHeight="5" orient="auto">
      <path d="M 0 0 L 8 4 L 0 8 z" fill="PRIMARY"/>
    </marker>
    <marker id="ards" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="5" markerHeight="5" orient="auto">
      <path d="M 0 0 L 8 4 L 0 8 z" fill="MUTED"/>
    </marker>
  </defs>

  <rect x="0" y="0" width="1200" height="860" fill="BACKGROUND" stroke="PRIMARY" stroke-width="3"/>
  <rect x="0" y="0" width="1200" height="36" fill="PRIMARY"/>
  <text x="16" y="24" font-family="'IBM Plex Mono', monospace" font-size="14"
        fill="BACKGROUND" font-weight="bold">project -- tool ecosystem</text>
  <text x="1184" y="24" font-family="'IBM Plex Mono', monospace" font-size="11"
        fill="MUTED" text-anchor="end">tool-a · tool-b · tool-c · tool-d</text>

  <!-- ROW 1: two peer tools side by side  (y=48–210) -->
  <rect x="30"  y="48" width="555" height="162" fill="none" stroke="PRIMARY" stroke-width="2"/>
  <rect x="30"  y="48" width="555" height="24"  fill="PRIMARY"/>
  <text x="307" y="64" font-family="'IBM Plex Mono', monospace" font-size="11"
        fill="BACKGROUND" text-anchor="middle" font-weight="bold">tool-a -- one-line role</text>
  <!-- description + commands inside, accent color for command examples -->

  <rect x="615" y="48" width="555" height="162" fill="none" stroke="PRIMARY" stroke-width="2"/>
  <rect x="615" y="48" width="555" height="24"  fill="PRIMARY"/>
  <text x="892" y="64" font-family="'IBM Plex Mono', monospace" font-size="11"
        fill="BACKGROUND" text-anchor="middle" font-weight="bold">tool-b -- one-line role</text>

  <!-- ARROW ZONE 1: dashed cross-arrows down into row 2 (y=210–320) -->
  <line x1="200" y1="210" x2="160" y2="320" stroke="MUTED" stroke-width="1.5"
        stroke-dasharray="6,3" marker-end="url(#ards)"/>
  <line x1="307" y1="210" x2="490" y2="320" stroke="MUTED" stroke-width="1.5"
        stroke-dasharray="6,3" marker-end="url(#ards)"/>
  <text x="220" y="268" font-family="'IBM Plex Mono', monospace" font-size="8"
        fill="MUTED" font-style="italic">contribution →</text>

  <!-- ROW 2: orchestrator (full width, dashed container) with sub-card grid -->
  <rect x="30" y="320" width="1140" height="280" fill="none"
        stroke="PRIMARY" stroke-width="1.5" stroke-dasharray="8,4"/>
  <rect x="30" y="320" width="1140" height="24"  fill="PRIMARY"/>
  <text x="600" y="336" font-family="'IBM Plex Mono', monospace" font-size="11"
        fill="BACKGROUND" text-anchor="middle" font-weight="bold">orchestrator -- one-line role</text>

  <!-- Four sub-cards in a 4-column grid -->
  <!-- card 1 at x=50, card 2 at x=310, card 3 at x=570, card 4 at x=830 -->
  <!-- each 240×140; gutter = 20 -->
  <rect x="50"  y="370" width="240" height="140" fill="none" stroke="PRIMARY" stroke-width="1.5"/>
  <rect x="50"  y="370" width="240" height="20"  fill="PRIMARY"/>
  <text x="170" y="383" font-family="'IBM Plex Mono', monospace" font-size="9"
        fill="BACKGROUND" text-anchor="middle">instance-1</text>
  <!-- ...repeat for cards 2, 3, 4... -->

  <!-- Last card uses dashed stroke + muted header to indicate "remote/optional" -->
  <rect x="830" y="370" width="240" height="140" fill="none" stroke="PRIMARY"
        stroke-width="1.5" stroke-dasharray="5,3"/>
  <rect x="830" y="370" width="240" height="20"  fill="MUTED"/>
  <text x="950" y="383" font-family="'IBM Plex Mono', monospace" font-size="9"
        fill="BACKGROUND" text-anchor="middle">remote-A/instance</text>

  <!-- ARROW ZONE 2: single solid vertical arrow up from foundation (y=600–660) -->
  <line x1="600" y1="660" x2="600" y2="601" stroke="PRIMARY" stroke-width="2" marker-end="url(#arr)"/>
  <text x="614" y="638" font-family="'IBM Plex Mono', monospace" font-size="9"
        fill="MUTED">installs all tools</text>

  <!-- ROW 3: foundation (registry, substrate, kernel) full-width  (y=660–760) -->
  <rect x="30" y="660" width="1140" height="100" fill="none" stroke="PRIMARY" stroke-width="2"/>
  <rect x="30" y="660" width="1140" height="24"  fill="PRIMARY"/>
  <text x="600" y="676" font-family="'IBM Plex Mono', monospace" font-size="11"
        fill="BACKGROUND" text-anchor="middle" font-weight="bold">foundation -- one-line role</text>
  <text x="60" y="706" font-family="'IBM Plex Mono', monospace" font-size="9"
        fill="PRIMARY" font-weight="bold">provides:</text>
  <text x="160" y="706" font-family="'IBM Plex Mono', monospace" font-size="9"
        fill="SECONDARY">a · b · c · d · e · f · g ...</text>

  <!-- Footer (y=780+) -->
  <line x1="40" y1="780" x2="1160" y2="780" stroke="MUTED" stroke-width="1"/>
  <text x="600" y="800" font-family="'IBM Plex Mono', monospace" font-size="10"
        fill="SECONDARY" text-anchor="middle">one-line summary of the ecosystem</text>
</svg>
```

---

## Cycle / Methodology with Feedback Arc (1200 × 430)

Use this for "build → measure → refine" style processes.

```svg
<!-- Standard three panels (BUILD / MEASURE / REFINE) with arrows between -->
<!-- ... same as three-panel pipeline ... -->

<!-- Feedback loop arc from right panel back to left panel -->
<path d="M 1145 360 Q 1145 380 1100 380 L 100 380 Q 55 380 55 360"
      fill="none" stroke="MUTED" stroke-width="1" stroke-dasharray="4,3"/>
<text x="600" y="376" font-family="'IBM Plex Mono', monospace" font-size="8"
      fill="MUTED" text-anchor="middle" font-style="italic">discoveries inform what to build next</text>
```

The arc uses two quadratic curves (`Q`) for rounded corners and a straight line (`L`) across the bottom. The y-coordinates (360, 380) sit between the panel bottoms and the footer divider.

---

## Apparatus Layout (Domain → Apparatus → Discoveries+Outputs)

Asymmetric three-panel where the center is wider than the wings, and the right side is split into two stacked panels.

Key features:
- **Above-panel uppercase labels** with `letter-spacing="0.08em"` instead of dark header bars
- **Soft fill** on highlighted items: `fill="PRIMARY" opacity="0.04"` rect *behind* a `fill="none" stroke="PRIMARY"` rect
- **Dashed sub-items** for speculative/future entries (`stroke-dasharray="3,3"`)
- **Right column split vertically**: DISCOVERIES on top (100px tall), OUTPUTS below (with a 2×2 grid of small cards)
- **Feedback arc** wraps from outputs all the way back to domain (long path along the bottom)

```svg
<!-- Section label above the panel (not inside) -->
<text x="40" y="98" font-family="'IBM Plex Mono', monospace" font-size="9"
      fill="MUTED" letter-spacing="0.08em" font-weight="500">DOMAIN</text>
<rect x="40" y="106" width="220" height="220" fill="none" stroke="PRIMARY" stroke-width="2"/>

<!-- Highlighted "primary" item: tinted fill + crisp border -->
<rect x="56" y="120" width="188" height="42" fill="PRIMARY" opacity="0.04"/>
<rect x="56" y="120" width="188" height="42" fill="none" stroke="PRIMARY" stroke-width="1.5"/>
<text x="68" y="138" font-family="'IBM Plex Mono', monospace" font-size="10"
      fill="PRIMARY" font-weight="bold">primary item</text>

<!-- Speculative item: dashed border, no tint -->
<rect x="56" y="224" width="188" height="42" fill="none" stroke="PRIMARY"
      stroke-width="1" stroke-dasharray="3,3"/>
```

---

## Synchronized State Table (inside an outputs panel)

For showing N subsystems kept in lockstep on the same "address".

```svg
<!-- Three column headers -->
<text x="756"  y="142" font-family="'IBM Plex Mono', monospace" font-size="8"
      fill="MUTED">COL A</text>
<text x="940"  y="142" font-family="'IBM Plex Mono', monospace" font-size="8"
      fill="MUTED">COL B</text>
<text x="1080" y="142" font-family="'IBM Plex Mono', monospace" font-size="8"
      fill="MUTED">COL C</text>
<line x1="756" y1="148" x2="1144" y2="148" stroke="MUTED" stroke-width="0.8"/>

<!-- Row 1: solid (active) -->
<rect x="756"  y="154" width="170" height="22" fill="none" stroke="PRIMARY" stroke-width="1"/>
<rect x="934"  y="154" width="130" height="22" fill="none" stroke="PRIMARY" stroke-width="1"/>
<rect x="1072" y="154" width="72"  height="22" fill="none" stroke="PRIMARY" stroke-width="1"/>

<!-- Row 2: dashed (remote/optional) -->
<rect x="756"  y="206" width="170" height="22" fill="none" stroke="PRIMARY"
      stroke-width="1" stroke-dasharray="5,3"/>
<!-- ...repeat for other columns in this row... -->
```

Each row represents one synchronized address; each column represents one subsystem. Use solid borders for current state and dashed borders for remote / pending / future state.

---

## Catalog + Contract + Consumer (1200 × 430)

For reusable components that get consumed by multiple downstream projects.

Layout:
- **Left column**: stack of small component cards, each with its own mini header bar (22px tall) and 2-line description
- **Center column**: the "contract" — the rules consumers must follow, shown as bold statement headers with a dashed-bordered example block at the bottom
- **Right column**: list of consumers, grouped by which component they use, with thin dividers between groups

```svg
<!-- Stacked component cards on the left -->
<rect x="60" y="80"  width="280" height="65" fill="none" stroke="PRIMARY" stroke-width="2"/>
<rect x="60" y="80"  width="280" height="22" fill="PRIMARY"/>
<text x="200" y="96" font-family="'IBM Plex Mono', monospace" font-size="10"
      fill="BACKGROUND" text-anchor="middle" font-weight="bold">component-name</text>

<rect x="60" y="155" width="280" height="50" fill="none" stroke="PRIMARY" stroke-width="2"/>
<!-- ...etc... -->

<!-- Center contract panel with dashed-bordered example block -->
<rect x="475" y="228" width="260" height="85" fill="none"
      stroke="MUTED" stroke-width="1" stroke-dasharray="4,3"/>
<text x="485" y="245" font-family="'IBM Plex Mono', monospace" font-size="7"
      fill="MUTED">include:</text>
```

---

## Footer Block

Reusable footer (place at the bottom of any diagram):

```svg
<line x1="40" y1="FOOTER_Y" x2="1160" y2="FOOTER_Y" stroke="MUTED" stroke-width="1"/>
<text x="600" y="FOOTER_Y+20" font-family="'IBM Plex Mono', monospace" font-size="10"
      fill="SECONDARY" text-anchor="middle">tagline / summary</text>
<!-- Optional attribution line below the tagline: -->
<text x="600" y="FOOTER_Y+44" text-anchor="middle" fill="PRIMARY"
      font-family="'IBM Plex Mono', monospace" font-size="9" font-weight="600">Built with X</text>
```

Use `FOOTER_Y = height - 70` (e.g. 360 for height 430, 780 for height 860). Drop the attribution line entirely for a cleaner footer, or replace "X" with the project host / team / framework you want to credit. If a vendor logo is desired, inline its SVG paths inside a `<g transform="translate(cx, cy) scale(s)">` next to the attribution text.
