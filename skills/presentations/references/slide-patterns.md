# Slide Patterns

Component patterns and styling reference for generating presentation slides.
This file is the code companion to the script — use it to turn each script
section into a working React component.

## How to Use This File

1. Read the script's "Visual approach" for a slide (e.g., "quote", "comparison")
2. Find the matching pattern in the Core Patterns section below
3. Copy the pattern and replace placeholder content with the script's Content section
4. Apply the transition specified in the script to the registration entry

## Script Visual Approach → Code Pattern

| Script says | Use this pattern | Section in this file |
|-------------|-----------------|---------------------|
| `hero` | Title Slide | Core Patterns → Title Slide |
| `quote` | Quote Slide | Core Patterns → Quote Slide |
| `comparison` | Comparison / Two-Column | Core Patterns → Comparison / Two-Column Slide |
| `data` | Data / Metrics Slide | Core Patterns → Data / Metrics Slide |
| `list` | List / Grid Slide | Core Patterns → List / Grid Slide |
| `story` | Story / Focus Slide | Core Patterns → Story / Focus Slide |
| `diagram` | Diagram / Process Slide | Core Patterns → Diagram / Process Slide |
| `close` | Close / CTA Slide | Core Patterns → Close / CTA Slide |

If the script specifies an animated bar chart (common in `comparison` and `data`
slides), see the Animated Bar Chart sub-pattern.

## Tech Stack

- React 18 + TypeScript
- Tailwind CSS v4 (plugin-based, no tailwind.config.js)
- Framer Motion (animations)
- Vite 5 (build)
- Bun (package manager)

## Project Structure

Each presentation lives under `src/presentations/<slug>/`:

```
src/presentations/<slug>/
├── <Name>Deck.tsx          # Router component
├── slides/
│   ├── Title.tsx
│   ├── SlideTwo.tsx
│   └── ...
└── images/                 # Optional SVGs or assets
```

## Theme Variables

All slides use CSS custom properties — never hardcode colors.

```
var(--bg)          Dark background (#0d1117 default)
var(--fg)          Light foreground (#e6edf3)
var(--muted)       Muted text (#9fb0c3)
var(--accent)      Primary accent (#7c3aed violet)
var(--accent2)     Secondary accent (#22c55e green)
var(--accent-rgb)  RGB for rgba() usage (124, 58, 237)
var(--accent2-rgb) RGB for rgba() usage (34, 197, 94)
var(--line)        Border color (#2a3340)
var(--surface)     Glass card bg (rgba(255,255,255,0.03))
```

The theme system swaps these at runtime (4 themes: Midnight Neon, Deep Ocean, Amber Haze, Forest Glow).

## Tailwind v4 Color Tokens

Tailwind v4 uses `@theme` tokens. These map to the CSS variables:

```
from-accent / to-accent2    Gradient using accent colors
text-[var(--muted)]          Muted text
border-[var(--line)]         Border color
```

## Core Patterns

### Title Slide

```tsx
import { motion } from 'framer-motion'

export default function Title() {
  const chips = ['Concept One', 'Concept Two', 'Concept Three']
  return (
    <div className="mx-auto max-w-5xl w-full text-center">
      <h1 className="text-[clamp(28px,6vw,64px)] font-extrabold tracking-tight">
        <span className="bg-gradient-to-r from-accent to-accent2 bg-clip-text text-transparent">
          Presentation Title Here
        </span>
      </h1>
      <div className="mt-1 text-[var(--muted)]">Author Name</div>
      <motion.div
        initial={{ scaleX: 0 }}
        animate={{ scaleX: 1 }}
        transition={{ duration: 0.6, ease: 'easeOut' }}
        className="mt-3 mx-auto h-2 rounded-full bg-gradient-to-r from-accent to-accent2 w-[min(52vw,560px)] origin-left"
      />
      <p className="mt-3 text-[var(--muted)]">
        Subtitle or tagline goes here.
      </p>
      <div className="mt-6 flex gap-2 justify-center flex-wrap">
        {chips.map((c, i) => (
          <motion.span
            key={c}
            className="surface border border-[var(--line)] rounded-full px-3 py-1 text-sm font-semibold"
            initial={{ opacity: 0, y: 8, scale: 0.98 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            transition={{ delay: i * 0.08 }}
          >
            {c}
          </motion.span>
        ))}
      </div>
    </div>
  )
}
```

### Quote Slide

```tsx
import { motion } from 'framer-motion'

export default function QuoteSlide() {
  return (
    <div className="mx-auto max-w-5xl w-full">
      <motion.h2
        initial={{ opacity: 0, y: 6 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-3xl md:text-4xl font-extrabold tracking-tight"
      >
        Speaker Name
      </motion.h2>
      <motion.div
        initial={{ scaleX: 0 }}
        animate={{ scaleX: 1 }}
        transition={{ duration: 0.5, ease: 'easeOut' }}
        className="mt-2 mb-4 h-1.5 w-40 rounded-full bg-gradient-to-r from-accent to-accent2 origin-left"
      />
      <motion.blockquote
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="surface p-6"
      >
        <p className="text-2xl md:text-3xl leading-relaxed">
          "Quote text with{' '}
          <span className="bg-gradient-to-r from-accent to-accent2 bg-clip-text text-transparent font-extrabold">
            highlighted keywords
          </span>
          ."
        </p>
        <motion.footer
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.55 }}
          className="mt-3 text-sm text-[var(--muted)]"
        >
          — Attribution
        </motion.footer>
      </motion.blockquote>
    </div>
  )
}
```

### Comparison / Two-Column Slide

```tsx
import { motion } from 'framer-motion'

export default function ComparisonSlide() {
  return (
    <div className="mx-auto max-w-6xl w-full">
      <h2 className="text-3xl md:text-4xl font-extrabold tracking-tight mb-3">
        Side A vs Side B
      </h2>
      <p className="text-[var(--muted)] mb-4">
        Context line with <span className="bg-gradient-to-r from-accent to-accent2 bg-clip-text text-transparent font-extrabold">key term</span>.
      </p>
      <div className="grid md:grid-cols-2 gap-6">
        {['Side A', 'Side B'].map((label, i) => (
          <motion.div
            key={label}
            className="surface p-5"
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.15 }}
          >
            <h3 className="text-lg font-bold mb-2">{label}</h3>
            <p className="text-[var(--muted)]">Description of this side.</p>
          </motion.div>
        ))}
      </div>
    </div>
  )
}
```

### Data / Metrics Slide

```tsx
import { motion } from 'framer-motion'

export default function MetricsSlide() {
  const metrics = [
    { label: 'Metric A', value: '+42%', description: 'Improved significantly' },
    { label: 'Metric B', value: '3.2s', description: 'Average response time' },
    { label: 'Metric C', value: '99.9%', description: 'Uptime achieved' },
  ]
  return (
    <div className="mx-auto max-w-5xl w-full">
      <h2 className="text-3xl md:text-4xl font-extrabold tracking-tight mb-6">
        The Numbers
      </h2>
      <div className="grid md:grid-cols-3 gap-5">
        {metrics.map((m, i) => (
          <motion.div
            key={m.label}
            className="surface p-6 text-center"
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: i * 0.12 }}
          >
            <div className="text-4xl md:text-5xl font-extrabold bg-gradient-to-r from-accent to-accent2 bg-clip-text text-transparent">
              {m.value}
            </div>
            <div className="mt-2 font-semibold">{m.label}</div>
            <div className="mt-1 text-sm text-[var(--muted)]">{m.description}</div>
          </motion.div>
        ))}
      </div>
    </div>
  )
}
```

### Animated Bar Chart

```tsx
import { motion } from 'framer-motion'

function Bar({ label, height, delay = 0 }: { label: string; height: number; delay?: number }) {
  return (
    <div className="flex flex-col items-center gap-2">
      <div className="relative h-48 w-16">
        <motion.div
          initial={{ height: '0%' }}
          animate={{ height: `${Math.round(height * 100)}%` }}
          transition={{ duration: 1.2, ease: 'easeOut', delay }}
          className="absolute bottom-0 left-0 right-0 rounded-t bg-gradient-to-t from-accent to-accent2"
        />
      </div>
      <span className="text-sm text-[var(--muted)]">{label}</span>
    </div>
  )
}
```

### List / Grid Slide

```tsx
import { motion } from 'framer-motion'

export default function ListSlide() {
  const items = [
    { title: 'Item 1', description: 'Details about item 1' },
    { title: 'Item 2', description: 'Details about item 2' },
    { title: 'Item 3', description: 'Details about item 3' },
    { title: 'Item 4', description: 'Details about item 4' },
  ]
  return (
    <div className="mx-auto max-w-5xl w-full">
      <h2 className="text-3xl md:text-4xl font-extrabold tracking-tight mb-6">
        Key Points
      </h2>
      <div className="grid md:grid-cols-2 gap-4">
        {items.map((item, i) => (
          <motion.div
            key={item.title}
            className="surface p-5"
            initial={{ opacity: 0, x: -8 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: i * 0.1 }}
          >
            <h3 className="font-bold mb-1">{item.title}</h3>
            <p className="text-sm text-[var(--muted)]">{item.description}</p>
          </motion.div>
        ))}
      </div>
    </div>
  )
}
```

### Close / CTA Slide

```tsx
import { motion } from 'framer-motion'

export default function CloseSlide() {
  return (
    <div className="mx-auto max-w-4xl w-full text-center">
      <motion.h2
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-4xl md:text-5xl font-extrabold tracking-tight"
      >
        <span className="bg-gradient-to-r from-accent to-accent2 bg-clip-text text-transparent">
          Call to Action
        </span>
      </motion.h2>
      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.3 }}
        className="mt-4 text-xl text-[var(--muted)]"
      >
        What the audience should do next.
      </motion.p>
    </div>
  )
}
```

### Story / Focus Slide

Use for narrative moments where you want the audience to read a single powerful
statement or short paragraph. Minimal decoration — let the words carry the slide.

```tsx
import { motion } from 'framer-motion'

export default function StorySlide() {
  return (
    <div className="mx-auto max-w-4xl w-full text-center">
      <motion.p
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="text-2xl md:text-3xl leading-relaxed"
      >
        "A single powerful statement or narrative paragraph goes here.
        Highlight the{' '}
        <span className="bg-gradient-to-r from-accent to-accent2 bg-clip-text text-transparent font-extrabold">
          key phrase
        </span>
        {' '}that carries the point."
      </motion.p>
      <motion.div
        initial={{ scaleX: 0 }}
        animate={{ scaleX: 1 }}
        transition={{ duration: 0.6, delay: 0.3, ease: 'easeOut' }}
        className="mt-6 mx-auto h-1 w-24 rounded-full bg-gradient-to-r from-accent to-accent2 origin-left"
      />
    </div>
  )
}
```

### Diagram / Process Slide

Use for step-by-step flows, architectures, or timelines. Each node is a surface
card. Connect them visually with arrows or numbering.

```tsx
import { motion } from 'framer-motion'

export default function ProcessSlide() {
  const steps = [
    { num: '1', title: 'Step One', desc: 'What happens first' },
    { num: '2', title: 'Step Two', desc: 'What happens next' },
    { num: '3', title: 'Step Three', desc: 'Final result' },
  ]
  return (
    <div className="mx-auto max-w-5xl w-full">
      <h2 className="text-3xl md:text-4xl font-extrabold tracking-tight mb-8">
        How It Works
      </h2>
      <div className="flex items-start gap-4">
        {steps.map((s, i) => (
          <motion.div
            key={s.num}
            className="flex-1 flex flex-col items-center"
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.15 }}
          >
            <div className="surface p-5 w-full text-center">
              <div className="text-2xl font-extrabold bg-gradient-to-r from-accent to-accent2 bg-clip-text text-transparent mb-2">
                {s.num}
              </div>
              <h3 className="font-bold mb-1">{s.title}</h3>
              <p className="text-sm text-[var(--muted)]">{s.desc}</p>
            </div>
            {i < steps.length - 1 && (
              <div className="mt-3 text-2xl text-[var(--muted)]">&rarr;</div>
            )}
          </motion.div>
        ))}
      </div>
    </div>
  )
}
```

## Deck Router Component

The router switches on `slide.id`:

```tsx
import type { DeckComponentProps } from '../../types'
import Title from './slides/Title'
import SlideTwo from './slides/SlideTwo'
import CloseSlide from './slides/CloseSlide'

export default function MyDeck({ slide }: DeckComponentProps) {
  switch (slide.id) {
    case 'title':
      return <Title />
    case 'slide-two':
      return <SlideTwo />
    case 'close':
      return <CloseSlide />
    default:
      return <div className="placeholder">Missing slide: {slide.id}</div>
  }
}
```

## Registration in public.ts

```tsx
import MyDeck from './my-slug/MyDeck'

// Add to the publicPresentations array:
{
  id: 'my-slug',
  title: 'Presentation Title',
  subtitle: 'Short description',
  slides: [
    { id: 'title', transition: 'fade' },
    { id: 'slide-two', transition: 'up' },
    { id: 'close', transition: 'fade' },
  ],
  component: MyDeck,
}
```

## Type Definitions

```typescript
type SlideMeta = {
  id: string
  transition?: 'fade' | 'slide' | 'up' | 'scale'
  className?: string
}

type DeckComponentProps = {
  slide: SlideMeta
  idx?: number
}

type PresentationEntry = {
  id: string
  title: string
  subtitle?: string
  slides: SlideMeta[]
  component: React.ComponentType<DeckComponentProps>
  passwordHash?: string   // optional SHA-256 hex for client-side gate
}
```

## Animation Guidelines

- Use `motion` from `framer-motion` for all animations
- Stagger children with incremental `delay` (0.08-0.15s per item)
- Common patterns:
  - Fade in: `initial={{ opacity: 0 }} animate={{ opacity: 1 }}`
  - Slide up: `initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}`
  - Scale in: `initial={{ opacity: 0, scale: 0.98 }} animate={{ opacity: 1, scale: 1 }}`
  - Bar grow: `initial={{ scaleX: 0 }} animate={{ scaleX: 1 }}` with `origin-left`
  - Height grow: `initial={{ height: '0%' }} animate={{ height: target }}`
- Transition durations: 0.3-0.6s for elements, 1.0-1.6s for bars/charts
- Highlight keywords with gradient text: `bg-gradient-to-r from-accent to-accent2 bg-clip-text text-transparent font-extrabold`

## Text Sizing

| Element | Size |
|---------|------|
| Title slide heading | `text-[clamp(28px,6vw,64px)]` |
| Slide heading | `text-3xl md:text-4xl` |
| Large body / quote | `text-2xl md:text-3xl` |
| Regular body | `text-xl md:text-2xl` |
| Supporting text | `text-base md:text-lg` |
| Caption / attribution | `text-sm` |
| Chip / tag | `text-sm` |

## Layout Rules

- Always wrap slide content in `<div className="mx-auto max-w-5xl w-full">` (or max-w-6xl for data-heavy slides)
- Use `text-center` only for title and close slides
- Content slides use left-aligned text by default
- Grid layouts: `grid md:grid-cols-2 gap-6` or `grid md:grid-cols-3 gap-5`
- Spacing between sections: `mb-3` to `mb-6`
- Surface cards: use the `surface` class (defined globally as glass-morphism card)

## Transition Variety

Vary transitions across slides for visual rhythm:

```
title:    fade    (clean entrance)
slide 2:  up      (energy)
slide 3:  slide   (horizontal movement)
slide 4:  fade    (pause)
slide 5:  up      (energy again)
slide 6:  scale   (emphasis)
...
close:    fade    (clean exit)
```

Avoid using the same transition for more than 2 consecutive slides.

## Content Density Guidelines

How much content belongs on each slide type:

| Pattern | Max text elements | Rule of thumb |
|---------|-------------------|---------------|
| hero / title | 1 heading + 1 subtitle + 5 chips | The title slide should be readable in 2 seconds |
| quote | 1 quote (1-3 sentences) + 1 framing line | Let the quote breathe — don't crowd it |
| comparison | 2 cards with 3-4 bullets each | Each card fits in one glance |
| data | 3-4 metrics max | Big numbers, short labels — no paragraphs |
| list | 4-6 items max | If you need 8+ items, split into two slides |
| story | 1-3 sentences | This pattern exists to focus — one idea, big text |
| diagram | 3-5 nodes | More than 5 steps becomes unreadable at presentation scale |
| close | 1 statement + 1 optional subtitle | The simplest slide in the deck |

If you find yourself cramming content into a slide, split it. Two focused slides
beat one overloaded slide every time.

## Common Mistakes to Avoid

1. **Hardcoded colors** — Always use `var(--accent)`, `var(--muted)`, etc. Never
   write `text-purple-600` or `color: #7c3aed` directly. The theme system needs
   CSS variables to swap themes at runtime.

2. **Missing animation imports** — Every slide that uses `<motion.div>` needs
   `import { motion } from 'framer-motion'` at the top.

3. **Shared state between slides** — Each slide is a standalone component. Don't
   use React context, global state, or props beyond `DeckComponentProps`. The
   deck router renders one slide at a time; there's no inter-slide communication.

4. **Overflow on large text** — Use `clamp()` or responsive breakpoints for
   headings. Test that text doesn't overflow on a 1280x720 viewport (the
   standard slide aspect ratio).

5. **Too many animations** — Stagger delays should total under 1.5s for the full
   slide. If the audience is waiting 3 seconds for all elements to appear, the
   animation is hurting, not helping.

6. **Forgetting the default case** — The deck router's switch statement must
   include `default: return <div className="placeholder">Missing slide: {slide.id}</div>`
   to catch typos in slide IDs.

7. **Mismatched IDs** — The slide `id` in the `public.ts` registration must
   exactly match the `case` string in the deck router. Use lowercase hyphenated
   slugs for both (e.g., `hook-jeffries`, not `hookJeffries`).
