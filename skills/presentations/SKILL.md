---
name: presentations
description: >
  Create slide deck presentations from scratch using a script-first workflow.
  Generates a structured presentation script from a topic prompt, then produces
  React+TypeScript slide components for Gabe's presentation platform (React 18,
  Tailwind CSS v4, Framer Motion). Use this skill whenever the user mentions
  creating a presentation, building slides, making a slide deck, presentation
  from a topic, slide show, talk preparation, conference talk, keynote, lightning
  talk, pitch deck, tech talk, brownbag, lunch-and-learn, or wants help turning
  an idea into presentation slides.
---

# Presentations

Script-first slide deck creation. Turns a topic into a structured presentation
script with speaker notes, then generates React slide components for Gabe's
presentation platform.

The workflow has five phases. Complete each one in order — each phase has a
checkpoint where you stop and wait for user input before continuing.

```
Phase 1: Discovery  -->  Phase 2: Script  -->  Phase 3: Review
    |                                               |
    v                                               v
  (ask questions,                           (user approves or
   wait for answers)                         requests changes)
                                                    |
                                                    v
                                Phase 4: Slides  -->  Phase 5: Register
```

---

## Phase 1: Discovery

Goal: understand what the user wants before writing a single word.

Ask all required questions in a single message.
Include optional questions in the same message when relevant.

### Required questions (always ask)

1. **Audience**
   - Question: "Who is the audience?"
   - Options: Engineers, Executives/Leadership, Mixed technical + business,
     Students/beginners, Conference attendees, Custom
   - Why: controls jargon depth, example choice, assumed knowledge level

2. **Duration**
   - Question: "How long is the talk?"
   - Options: 5 min (lightning talk), 10 min, 15 min, 20 min, 30 min,
     45 min, 60 min
   - Why: determines slide count (see table below)

3. **Goal**
   - Question: "What is the primary goal of this presentation?"
   - Options: Inform (share knowledge), Persuade (change minds),
     Teach (build skills), Entertain, Sell (pitch a product/idea)
   - Why: persuasion needs hooks and objection handling; teaching needs
     progressive complexity; selling needs a clear CTA

4. **Tone**
   - Question: "What tone should the presentation have?"
   - Options: Professional, Casual/conversational, Provocative/opinionated,
     Inspirational, Deeply technical
   - Why: affects word choice, humor, slide density, visual intensity

### Optional questions (add when relevant)

5. **Key points** — ask when the topic is broad (e.g., "AI" vs "AI routing patterns")
   - "Are there specific points or subtopics you want covered?"

6. **Existing material** — ask when the user mentions having content already
   - "Do you have quotes, data, articles, or references to include?"

7. **Stance** — ask when the topic is debatable
   - "Should this be opinionated/one-sided or balanced/neutral?"

8. **Visual density** — ask when the user seems design-conscious
   - "Visual style preference?" Options: Minimal (big text, few elements),
     Data-heavy (charts, metrics, comparisons), Balanced

### After receiving answers

Summarize what you understood back to the user in a short paragraph:

> "Got it. I'll create a **15-minute persuasive talk** for **engineering managers**
> about why story points don't work. Tone: **provocative but professional**.
> I'll include the Jeffries and Fowler quotes you mentioned. That gives us
> roughly **10-12 slides**. Let me write the script."

Wait for the user to confirm or correct before moving to Phase 2.

### Slide count reference

| Duration | Slide count | Breakdown |
|----------|-------------|-----------|
| 5 min | 5-7 | 1 title + 3-5 content + 1 close |
| 10 min | 7-9 | 1 title + 5-7 content + 1 close |
| 15 min | 8-12 | 1 title + 6-10 content + 1 close |
| 20 min | 11-15 | 1 title + 9-13 content + 1 close |
| 30 min | 14-18 | 1 title + 12-16 content + 1 close |
| 45 min | 18-24 | 1 title + 16-22 content + 1 close |
| 60 min | 22-30 | 1 title + 20-28 content + 1 close |

Add +1 for a citations slide if the script references external sources.
The guideline is ~1 content slide per 1.5-2 minutes of speaking time.

---

## Phase 2: Script Generation

Goal: write a structured markdown script the user can read, understand, and
approve without needing to see any code.

**Before writing**, read `references/script-format.md` for the full template.

### What the script must include

For every presentation:

1. **Header** — title, author, audience, duration, goal, tone
2. **TL;DR** — 3-6 bullet executive summary (this is for the reader, not a slide)
3. **Narrative arc** — a 2-3 sentence description of the story structure
   (e.g., "Open with a provocative hook, build the case through three failure modes,
   pivot to solutions, close with a call to action")
4. **Slide mapping** — numbered list of all slides with one-line descriptions
5. **Per-slide sections** — one `## Slide N: Name` section for each slide containing:
   - **What this slide communicates** — the ONE point this slide makes, in one sentence
   - **Content** — the actual text, quotes, data, or arguments shown on the slide
   - **Speaker notes** — what the presenter should SAY while this slide is on screen
     (2-5 sentences, conversational, covering context the slide doesn't show)
   - **Visual approach** — which layout pattern to use (hero, quote, comparison, data,
     list, story, diagram, close) and any specific details about the arrangement
   - **Transition** — which slide transition to use (fade, slide, up, scale)

### Speaker notes matter

Speaker notes are what make the script actually useful as a "follow the script"
document. They bridge the gap between the sparse slide content and the full talk.

Good speaker notes:
- Are written in first person, as if the presenter is speaking
- Include the opening line for the slide ("So here's the thing about velocity...")
- Call out when to pause, when to make eye contact, when to click
- Reference what's on screen ("As you can see on the left column...")
- Include backup talking points for Q&A-heavy audiences

Bad speaker notes:
- Just repeat what's on the slide
- Are too long (keep under 100 words per slide)
- Use formal essay voice instead of conversational speech

### Narrative arc patterns

Choose the arc that fits the goal:

| Goal | Arc | Structure |
|------|-----|-----------|
| Persuade | Problem → Evidence → Solution | Hook → failure modes → alternatives → CTA |
| Teach | Foundation → Build → Apply | Concept → examples → exercise/demo → summary |
| Inform | Context → Details → Implications | Why this matters → what happened → what's next |
| Sell | Pain → Solution → Proof | Problem → product → demo/case study → CTA |
| Entertain | Setup → Tension → Payoff | Opening joke/story → escalation → punchline/insight |

### Script file

Save the script as `<slug>-script.md` in the presentation folder or working
directory. Present the full script to the user for review.

### Checkpoint

After writing the script, stop and tell the user:

> "Here's the script with N slides. Each slide section includes what's shown on
> screen, speaker notes for what to say, and the visual layout. Please review and
> let me know if you'd like to:
> - Add, remove, or reorder slides
> - Change the content or emphasis of any slide
> - Adjust speaker notes
> - Change the overall tone or arc
>
> Once you're happy with the script, I'll generate the slide components."

Do not proceed to Phase 3 until the user explicitly approves or says to continue.

---

## Phase 3: Review & Iteration

Goal: incorporate user feedback until they approve the script.

- If the user requests changes, update the script and present it again
- If the user asks to add/remove slides, update the slide mapping and renumber
- If the user approves, move to Phase 4
- If the user says something ambiguous ("looks good but maybe..."), ask for
  clarification — don't guess

---

## Phase 4: Slide Generation

Goal: convert the approved script into React components.

**Before generating**, read `references/slide-patterns.md` for the full component
pattern library, CSS reference, and animation guidelines.

### Step-by-step

1. **Create the folder** at `src/presentations/<slug>/slides/`

2. **Generate each slide** as a separate `.tsx` file in the `slides/` folder.
   Map each script section to a component using the visual approach specified:

   | Script visual approach | Component pattern to use |
   |----------------------|--------------------------|
   | hero | Title slide — centered gradient text, animated underline, chips |
   | quote | Quote slide — blockquote card, highlighted keywords, attribution |
   | comparison | Two-column — grid with surface cards, contrasting elements |
   | data | Metrics — large numbers in gradient text, or animated bar charts |
   | list | Grid slide — 2x2 or 3x1 surface cards with title + description |
   | story | Story slide — single large paragraph, minimal decoration |
   | diagram | Diagram — flex/grid boxes with connecting visual elements |
   | close | Close slide — centered gradient text, optional subtitle |

3. **Generate the deck router** as `<Name>Deck.tsx` in the slug folder root.
   It imports all slides and switches on `slide.id`.

4. **Apply transitions** from the script. Use the transition specified in each
   slide's script section. If none was specified, vary them:
   - Title and close: `fade` (clean entrance/exit)
   - Content slides: alternate between `up`, `slide`, `fade`, `scale`
   - Never use the same transition for 3+ consecutive slides

### Key constraints

- One `.tsx` file per slide — no multi-slide files
- Each slide is a self-contained React component with no shared state
- Import only `motion` from `framer-motion` — nothing else external
- Use theme CSS variables (`var(--accent)`, `var(--muted)`, etc.) never hardcoded colors
- Use Tailwind CSS v4 utility classes — no CSS modules, no styled-components
- Use `surface` class for glass-morphism cards
- Wrap content in `<div className="mx-auto max-w-5xl w-full">` (or `max-w-6xl`)
- Responsive text: `text-3xl md:text-4xl` breakpoint pattern

### After generating

Show the user the file list and a brief summary:

> "Generated 12 slide components + deck router:
> - `src/presentations/storypoints/StoryPointsDeck.tsx` (router)
> - `src/presentations/storypoints/slides/Title.tsx`
> - `src/presentations/storypoints/slides/HookJeffries.tsx`
> - ... (list all)
>
> Next I'll register the deck so it appears in the presentation list."

---

## Phase 5: Registration

Goal: wire the deck into the platform so it's accessible via the UI.

1. Add an import to `src/presentations/public.ts` (or `private.ts` for private decks):
   ```tsx
   import MyDeck from './<slug>/<Name>Deck'
   ```

2. Add an entry to the `publicPresentations` array:
   ```tsx
   {
     id: '<slug>',
     title: '<Title from script>',
     subtitle: '<Subtitle from script>',
     slides: [
       { id: 'title', transition: 'fade' },
       { id: 'slide-two', transition: 'up' },
       // ... one entry per slide, matching slide.id values from the router
     ],
     component: MyDeck,
   }
   ```

3. The `slides` array order determines presentation order. Each `id` must match
   a `case` in the deck router's switch statement.

4. Tell the user the deck is registered and how to view it:

> "Deck registered. Run `bun dev` and navigate to `/p/<slug>` to view it.
> Use arrow keys or swipe to navigate. Press S for music, T for theme picker."

---

## Resources

| File | What it contains | When to read |
|------|-----------------|--------------|
| `references/script-format.md` | Script template, section types, narrative arcs, writing rules | Before Phase 2 |
| `references/slide-patterns.md` | Component patterns, CSS/animation reference, theme system | Before Phase 4 |
| `references/example-script.md` | Complete example script (Story Points talk) with speaker notes | When user wants to see a finished script |
