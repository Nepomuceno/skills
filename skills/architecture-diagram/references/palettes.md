# Color Palettes

## Industrial (Default)

The original Nomograph palette — warm parchment tones with dark brown ink.

```
primary:    #2c2417   (dark brown — text, borders, title bar)
background: #faf6ed   (warm parchment — SVG background)
secondary:  #6b5d4f   (medium brown — body text, descriptions)
muted:      #c4b99a   (tan — dividers, captions, subtle elements)
accent:     #e85d26   (burnt orange — highlights, warnings)
```

### CSS Variables
```css
--diagram-primary: #2c2417;
--diagram-bg: #faf6ed;
--diagram-secondary: #6b5d4f;
--diagram-muted: #c4b99a;
--diagram-accent: #e85d26;
```

---

## MBSE Portal

Derived from the MBSE Portal DESIGN.md — cool industrial greys with signal orange.

```
primary:    #0F0F10   (ink black — text, borders, title bar)
background: #F3F3F0   (warm grey — SVG background)
secondary:  #7A7A72   (technical grey — body text, descriptions)
muted:      #C8C8C0   (structural grey — dividers, captions)
accent:     #FF6A00   (signal orange — highlights, status)
```

### CSS Variables
```css
--diagram-primary: #0F0F10;
--diagram-bg: #F3F3F0;
--diagram-secondary: #7A7A72;
--diagram-muted: #C8C8C0;
--diagram-accent: #FF6A00;
```

---

## Midnight

Dark mode variant — deep navy with ice blue accents.

```
primary:    #E2E8F0   (ice white — text, borders)
background: #0F172A   (deep navy — SVG background)
secondary:  #94A3B8   (slate — body text)
muted:      #334155   (dark slate — dividers, subtle elements)
accent:     #38BDF8   (sky blue — highlights)
```

---

## Terminal

Hacker aesthetic — black background with green phosphor text.

```
primary:    #22C55E   (green — text, borders)
background: #0A0A0A   (near-black — SVG background)
secondary:  #16A34A   (dark green — body text)
muted:      #1A1A1A   (charcoal — dividers)
accent:     #F59E0B   (amber — highlights, warnings)
```

---

## Blueprint

Engineering blueprint style — white on deep blue.

```
primary:    #DBEAFE   (light blue — text, borders)
background: #1E3A5F   (blueprint blue — SVG background)
secondary:  #93C5FD   (medium blue — body text)
muted:      #2D4F7A   (dark blue — dividers, grid)
accent:     #FCD34D   (yellow — highlights, callouts)
```

---

## Monochrome

Pure black and white — maximum contrast, zero color.

```
primary:    #000000   (black — text, borders, title bar)
background: #FFFFFF   (white — SVG background)
secondary:  #666666   (grey — body text)
muted:      #CCCCCC   (light grey — dividers)
accent:     #000000   (black — highlights use weight/size, not color)
```

---

## Deriving a Custom Palette

When a project has its own design system:

1. **primary** = the darkest color used for text/headings
2. **background** = the lightest surface color
3. **secondary** = the muted text color (body copy)
4. **muted** = the border/divider color
5. **accent** = the brand/action color (buttons, links, status)

Keep contrast ratios above 4.5:1 for primary-on-background text.
The accent color should have enough contrast to be visible but is used sparingly — only for 1-3 elements per diagram.
