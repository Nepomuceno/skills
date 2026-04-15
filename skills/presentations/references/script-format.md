# Script Format

A presentation script is a structured markdown document that maps 1:1 to slides.
The agent writes this first; the user reviews and approves it before any code is
generated. The script serves two audiences:

1. **The user** — reads it to verify content, flow, and emphasis before slides exist
2. **The presenter** — uses speaker notes as a teleprompter during the actual talk

---

## Full Template

```markdown
# <Presentation Title>

**Author:** <name>
**Audience:** <who will watch this — be specific>
**Duration:** <X minutes>
**Goal:** <inform | persuade | teach | entertain | sell>
**Tone:** <professional | casual | provocative | inspirational | technical>

---

## TL;DR

* <Most important takeaway — the one thing people should remember>
* <Supporting point 2>
* <Supporting point 3>
* <Supporting point 4 (optional)>
* <What the audience should DO differently after this talk>

---

## Narrative Arc

<2-3 sentences describing the story structure. Name the pattern
(problem→evidence→solution, foundation→build→apply, etc.) and describe
how the talk flows emotionally — where is the hook, where is the tension,
where is the resolution.>

---

## Slide Mapping

1. Title / Hero — <one-line description>
2. <slide name> — <one-line description>
3. <slide name> — <one-line description>
...
N. Close / Call to Action — <one-line description>
N+1. Citations (if any external sources)

---

## Slide 1: Title

### What this slide communicates
<One sentence: what the audience takes away from seeing this slide>

### Content
- **Title:** "<The main heading>"
- **Subtitle:** "<Tagline or one-line summary>"
- **Author:** <name>
- **Chips:** <3-5 short concept tags that preview the talk>

### Speaker notes
<What to say while the title slide is showing. Usually a greeting,
a brief "here's what we're going to talk about" framing, and a hook
to get attention. Write in first person, conversational. 2-4 sentences.>

### Visual approach
hero — centered gradient text, animated underline bar, chip tags

### Transition
fade

---

## Slide 2: <Name>

### What this slide communicates
<One sentence: the SINGLE point this slide makes>

### Content
<The actual text, quotes, data, bullet points, or arguments that appear
on screen. Be specific — this is what gets rendered into the component.
Include exact quote text, exact numbers, exact labels.>

### Speaker notes
<What the presenter says OUT LOUD while this slide is showing. This is
NOT what's on screen — it's the surrounding context, the story, the
"here's why this matters" explanation. Write as speech, not essay.

Good example:
"So here's the thing about velocity — Ron Jeffries literally invented
story points as part of XP, and even HE says tracking them is wasteful.
When the inventor tells you the tool is broken, you should probably
listen. Let that sink in for a second."

Bad example:
"This slide shows a quote from Ron Jeffries about story points being
wasteful." (just repeats the slide — useless as notes)

### Visual approach
<Which layout pattern and any specific details:
- quote — blockquote card, "wasteful" and "harmful" in gradient text
- comparison — two columns, Sprint A vs Sprint B with animated bars
- data — three metric cards in a row with large gradient numbers
- list — 2x2 grid of surface cards
- story — single large paragraph, centered
- diagram — three boxes with arrows between them
- hero — centered gradient text (for section breaks)
- close — centered gradient text with subtitle>

### Transition
<fade | slide | up | scale>

---

... (repeat for each slide)

## Slide N: Close

### What this slide communicates
<The final takeaway or call to action>

### Content
"<The closing statement — make it quotable>"

### Speaker notes
<How to close the talk. Reference the opening hook to create a full-circle
moment. Include the "thank you" and any Q&A transition.>

### Visual approach
close — centered gradient text, large

### Transition
fade

---

## Slide N+1: Citations (if needed)

### Content
- <Author> — <Title>: <URL>
- <Author> — <Title>: <URL>

### Speaker notes
"These are all linked in the exported version if you want to dig deeper."

### Visual approach
Clean list of linked sources in a surface card

### Transition
up
```

---

## Narrative Arc Patterns

Choose the arc that matches the presentation goal. The arc shapes the
emotional journey — it determines which slide comes after which and why.

### Persuade: Problem → Evidence → Solution

Best for: changing minds, killing bad practices, advocating for a new approach.

```
1. Title
2. Hook — provocative quote or surprising fact that challenges the status quo
3-5. Evidence — 2-3 failure modes, data points, or case studies
6. Pivot — "so what should we do instead?"
7-8. Solutions — concrete alternatives with examples
9. Example — before/after or case study proving the alternative works
10. Close — memorable call to action
11. Citations
```

The emotional shape: curiosity → discomfort → relief → motivation.

### Teach: Foundation → Build → Apply

Best for: workshops, tutorials, skill-building talks.

```
1. Title
2. Why this matters — motivation and context
3. Core concept — the fundamental idea, defined clearly
4-6. Build up — progressive complexity, each slide adding one layer
7-8. Applied examples — real-world usage showing the concept in action
9. Common mistakes — what to watch out for
10. Summary — key takeaways in a grid
11. Close — "go try this"
12. Citations
```

The emotional shape: curiosity → understanding → confidence → eagerness.

### Inform: Context → Details → Implications

Best for: status updates, research presentations, "here's what happened" talks.

```
1. Title
2. Context — why are we here, what's the backdrop
3-5. Details — what happened, what we found, what the data says
6-7. Analysis — what it means, patterns, insights
8. Implications — what changes as a result
9. Next steps — what we're doing about it
10. Close
```

The emotional shape: attention → engagement → insight → clarity.

### Sell: Pain → Solution → Proof

Best for: product pitches, internal advocacy, funding requests.

```
1. Title
2. Pain — the problem your audience feels (make them nod)
3. Failed attempts — what doesn't work (optional, adds credibility)
4. Solution intro — your approach in one sentence
5-6. How it works — 2-3 key capabilities or features
7. Demo/proof — case study, metrics, or live demo reference
8. Differentiator — why this beats alternatives
9. Close — clear CTA (try it, fund it, adopt it)
```

The emotional shape: frustration → hope → conviction → action.

### Entertain: Setup → Tension → Payoff

Best for: lightning talks, dinner talks, "fun" topics.

```
1. Title — intriguing/funny hook
2-3. Setup — establish the world, build context
4-6. Escalation — things get more interesting/absurd/intense
7. Twist or climax — the surprise, the punchline, the "aha"
8. Reflection — why this matters (optional, gives substance)
9. Close — memorable last line
```

The emotional shape: intrigue → amusement → surprise → satisfaction.

---

## Section Types Reference

Each slide should specify a visual approach from this list:

| Type | When to use | What it looks like |
|------|-------------|-------------------|
| `hero` | Title slides, major section breaks | Centered, large gradient text, animated underline bar, optional chip tags below |
| `quote` | Authoritative quotes, testimonials | Blockquote in a surface card, speaker name as heading, key words in gradient text, attribution at bottom |
| `comparison` | Before/after, A vs B, pros/cons | Two-column grid with surface cards, contrasting metrics or bar charts |
| `data` | Metrics, statistics, KPIs | Large numbers in gradient text inside surface cards (3-col grid), or animated bar charts |
| `list` | Key points, steps, features | 2x2 or 2x3 grid of surface cards, each with a bold title and muted description |
| `story` | Narrative moments, case studies, focus points | Single paragraph in large text, minimal decoration, maybe one gradient-highlighted phrase |
| `diagram` | Process flows, architecture, timelines | Flex/grid boxes connected with lines or arrows, step numbers, surface card per node |
| `close` | Final slide | Centered gradient text (large), optional muted subtitle below, no cards |

---

## Writing Rules

### One slide, one point
If you have two ideas, make two slides. A slide that makes two points
makes neither effectively. The "what this slide communicates" section must
be a single sentence — if you can't write one sentence, split the slide.

### Write for the eye, speak for the ear
Slide content = what's SHOWN (minimal, scannable, visual).
Speaker notes = what's SAID (conversational, contextual, detailed).
The slide should be readable in 3-5 seconds. The notes carry the rest.

### Front-load importance
"Revenue dropped 40%" not "We observed a decrease of approximately 40% in revenue."
"3x faster" not "significantly faster than the previous approach."

### Concrete over vague
Numbers, names, dates. "Activation increased 12% in 2 weeks" beats "Adoption improved."

### Quotes: keep them sharp
1-3 sentences max. Cut to the part that hits hardest. If a quote is 5 sentences,
extract the 1 sentence that makes the point and use only that.

### Speaker notes: write like you talk
First person. Contractions. Natural pauses. The notes should sound like a human
giving a talk, not a textbook.

Good: "So here's where it gets interesting — same team, same sprint length,
same number of points... but wildly different outcomes."

Bad: "This slide illustrates the phenomenon wherein equivalent story point
totals can correspond to divergent value delivery outcomes."

---

## Transition Assignment

Assign a transition to each slide. The goal is visual rhythm — variety without
randomness.

| Position | Recommended | Why |
|----------|-------------|-----|
| Title (first slide) | `fade` | Clean, neutral entrance |
| After title | `up` | Energy, sets pace |
| Quote slides | `fade` | Let the words breathe |
| Comparison/data | `slide` or `up` | Movement matches the "versus" or "build-up" energy |
| Section pivots | `scale` | Draws attention to the shift |
| Close (last content) | `fade` | Clean, settled exit |
| Citations | `up` | Quick, doesn't linger |

Rule: never use the same transition for 3+ slides in a row.

---

## Naming Conventions

- Script file: `<slug>-script.md` (e.g., `storypoints-script.md`)
- Slide mapping IDs: lowercase, hyphenated (e.g., `hook-jeffries`, `complexity-trap`)
- Component files: PascalCase (e.g., `HookJeffries.tsx`, `ComplexityTrap.tsx`)
- Deck router: `<PascalName>Deck.tsx` (e.g., `StoryPointsDeck.tsx`)
