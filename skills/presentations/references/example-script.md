# Example Script: Story Points

This is a real script that was used to generate a 12-slide presentation.
It demonstrates the full format including speaker notes, narrative arc,
visual approach, and transitions for every slide.

---

# Story Points Aren't Going to Fix Anything

**Author:** Gabriel Nepomuceno
**Audience:** Product leaders, engineering managers, scrum masters, senior ICs
**Duration:** 15 minutes
**Goal:** Persuade
**Tone:** Provocative but professional

---

## TL;DR

* Story points don't measure value; they mostly measure effort/complexity and team calibration.
* Tracking estimates vs. actuals is wasteful; comparing teams by points/velocity is harmful (Jeffries).
* Points are regularly weaponized (inside and across teams), creating gaming, inflation, and pressure.
* Over horizons that matter, points are no more predictive than story counting (Fowler).
* By Goodhart/Campbell, making points a target distorts behavior away from outcomes.
* Replace with value-centric flow: throughput, lead time/cycle time, WIP limits, DORA metrics.

---

## Narrative Arc

Problem → Evidence → Solution. Open with a provocative hook from Ron Jeffries
(the co-creator of story points) to establish credibility and surprise. Build
the case through three failure modes (complexity trap, weaponization, Goodhart's Law),
then pivot to concrete alternatives. Close with a before/after example that
makes the argument tangible, and a memorable call to action.

The emotional shape: curiosity → discomfort → relief → motivation.

---

## Slide Mapping

1. Title / Hero — introduce the talk and preview key concepts
2. Hook: Ron Jeffries — if the inventor says it's broken, listen
3. 50 ≠ 50: Complexity Trap — equal points, wildly different value
4. Weaponization & Vanity — perverse incentives inside and across teams
5. Accuracy vs. Counting — story counting predicts just as well (Fowler)
6. Goodhart/Campbell — making points a target distorts behavior
7. Value > Effort — high-value fix beats low-value feature regardless of points
8. Focus, Prioritization, Impact — what to optimize for instead
9. What to Use Instead — concrete replacement metrics and practices
10. Mini Example — before/after case study with real numbers
11. Close — call to action
12. Citations — sources

---

## Slide 1: Title

### What this slide communicates
This talk will argue that story points are counterproductive, and offer alternatives.

### Content
- **Title:** "Story Points Aren't Going to Fix Anything"
- **Subtitle:** "Points pull focus away from value; here's what to do instead."
- **Author:** Gabriel Nepomuceno
- **Chips:** Value over points, Throughput, Cycle time, WIP limits, DORA

### Speaker notes
"Hey everyone, thanks for joining. I'm Gabe, and today I'm going to make the case
that story points — the thing most of us spend hours estimating every sprint —
aren't actually helping us deliver better outcomes. In fact, I think they're
actively hurting us. I'll show you why, and more importantly, what to do instead.
Let's get into it."

### Visual approach
hero — centered gradient text, animated underline bar, chip tags staggering in from below

### Transition
fade

---

## Slide 2: Hook — Ron Jeffries

### What this slide communicates
The co-creator of story points himself says tracking them is wasteful and comparing teams by velocity is harmful.

### Content
> "I think tracking how actuals compare with estimates is at best **wasteful**;
> I think comparing teams on quality of estimates or velocity is **harmful**."
> — Ron Jeffries, *Story Points Revisited*

Framing line below the quote: "If the originator says it's **wasteful** and **harmful**, we should listen."

### Speaker notes
"So let's start with the elephant in the room. Ron Jeffries — he literally
co-created Extreme Programming and helped popularize story points. And even he
says tracking them is wasteful. Not 'suboptimal.' Not 'could be improved.'
Wasteful. And comparing teams by velocity? Harmful. When the inventor tells you
the tool is broken, that should make us pause. Let that sit for a moment."

### Visual approach
quote — blockquote in surface card, "wasteful" and "harmful" highlighted in
gradient text with delayed reveal (0.25s and 0.4s delays), attribution at bottom

### Transition
up

---

## Slide 3: 50 ≠ 50 — Complexity Trap

### What this slide communicates
Two sprints with identical story point totals can deliver wildly different customer value.

### Content
- Sprint A: 50 SP — released onboarding checklist → activation +12%, support tickets -18%
- Sprint B: 50 SP — complex refactor → performance +3%, no adoption change
- Both sprints: identical muted SP progress bars (equal), dramatically different gradient value bars (85% vs 25%)
- Large ≠ symbol
- Bottom text: "Points ≈ complexity/effort — not customer value."

### Speaker notes
"Here's a scenario I think everyone's lived. Same team, same sprint length, same
velocity — 50 story points both times. Sprint A shipped a simple onboarding
checklist. Activation went up 12%, support tickets dropped by 18%. Sprint B was
a big complex refactor. Performance improved by 3%. Nobody noticed. As you can
see from the bars, same points, completely different value. The problem is
structural: points measure how hard something felt, not how useful it was."

### Visual approach
comparison — two-column grid with surface cards. Each card shows a muted SP bar
(animated to 100%, same for both) and a gradient value bar (animated, 85% vs 25%).
Large gradient ≠ symbol centered below the grid.

### Transition
slide

---

## Slide 4: Weaponization & Vanity

### What this slide communicates
Points create perverse incentives that degrade quality and trust, both inside teams and across the organization.

### Content
**Inside the Team:**
- Velocity goals create pressure to inflate points
- Quality suffers: rushed testing, skipped refactors, "good enough" definitions of done
- "When the scoreboard rewards complexity, simplicity is penalized"

**Across Teams:**
- Story points are not comparable across teams by design
- Organizations compare velocity anyway → political pressure, sandbagging, distrust
- Creates leaderboard dynamics nobody asked for

### Speaker notes
"Now let's talk about what happens when points become a target. Inside the team,
velocity goals create pressure. People start inflating estimates to look
productive. Testing gets rushed. Refactors get punted. And across teams? Even
though story points are explicitly designed to be incomparable across teams,
leadership compares them anyway. Team A does 80 points, Team B does 40 — clearly
Team A is twice as productive, right? Wrong. But now Team B is on the defensive.
That's a toxic dynamic."

### Visual approach
comparison — two surface cards side by side. "Inside the Team" card with bullet
points, "Across Teams" card with bullet points. Key phrases in gradient text.

### Transition
fade

---

## Slide 5: Accuracy vs. Counting

### What this slide communicates
Story counting predicts delivery just as well as story points, without the estimation ceremony overhead.

### Content
> "Teams work well with **story points** and **story counting** and I have **no preference**."
> — Martin Fowler, *Story Counting*

Supporting text: "Over time, counting stories forecasts as well as points — without
the overhead. Estimation rituals consume hours; the opportunity cost is real and recurring."

### Speaker notes
"Martin Fowler — not exactly a controversial figure — looked at the data and
basically said: counting stories works just as well. No preference. Think about
that. All those planning poker sessions, all those debates about whether
something is a 5 or an 8... they don't actually improve your forecasting accuracy
over just counting how many stories you finish per sprint. And those ceremonies
cost real time every single sprint."

### Visual approach
quote — blockquote in surface card with "story points," "story counting," and
"no preference" in gradient text. Supporting paragraph below the card.

### Transition
up

---

## Slide 6: Goodhart/Campbell

### What this slide communicates
When you optimize for a proxy metric (points), the metric stops measuring what you care about (value).

### Content
> "When a **measure** becomes a **target**, it ceases to be a good measure."
> — Goodhart's Law

Targeting points causes:
- Larger story slices (more points per item)
- Estimate padding (safe overestimates)
- Cherry-picking "point-rich" tasks with poor customer impact
- Forecast theater: beautiful charts, unreliable delivery

### Speaker notes
"Goodhart's Law is one of those principles that explains half of organizational
dysfunction. The moment you make story points a target — velocity goals, sprint
commitments, performance reviews — people optimize for points, not outcomes.
Stories get bigger because bigger means more points. Estimates get padded because
padding is safe. Teams pick the 13-point tech debt ticket over the 2-point
customer fix because the scoreboard rewards it. The metric is now meaningless."

### Visual approach
quote — large quote in surface card with "measure" and "target" in gradient text.
Bullet list of distortions below the card, each appearing with stagger animation.

### Transition
fade

---

## Slide 7: Value > Effort

### What this slide communicates
A small high-value fix is worth more than a large low-value feature, regardless of point totals.

### Content
**High-value simple fix (3 SP):**
- Onboarding checklist tweak
- Activation +12%

**Low-value complex feature (20 SP):**
- Ambitious analytics dashboard
- No measurable adoption impact

Bottom text: "If your scoreboard rewards complexity, your roadmap drifts from your customer."

### Speaker notes
"Let me make this really concrete. A 3-point story — tiny, almost embarrassingly
small — tweaked the onboarding flow and increased activation by 12 percent. A
20-point story — big, complex, the kind that makes you feel productive — built an
analytics dashboard nobody uses. Which one actually mattered? If your system
rewards the 20-pointer, your roadmap will drift toward complexity and away from
your customer. That's the fundamental problem."

### Visual approach
comparison — two surface cards with metrics. The 3 SP card shows "+12% activation"
in large gradient text. The 20 SP card shows "0% adoption impact" in muted text.
Bottom quote centered.

### Transition
slide

---

## Slide 8: Focus, Prioritization, Impact

### What this slide communicates
Three principles that replace story-point-driven planning: reduce WIP, rank by impact, measure outcomes.

### Content
Three cards:
1. **Focus** — Reduce WIP. Fewer things in flight means faster flow and less context switching.
2. **Prioritization** — Rank by impact × confidence × urgency. Make cost visible through cycle time, not points.
3. **Impact** — Measure what changed for customers. Adoption, conversion, support tickets, NPS.

### Speaker notes
"So if we're dropping points, what fills the vacuum? Three things. First: focus.
Cap your work-in-progress. Teams that do fewer things simultaneously finish things
faster — that's Little's Law, it's math. Second: prioritize by impact, not effort.
What moves the needle most? That goes first. Third: measure impact. Not how hard
it was. Not how many points it cost. Did customers benefit? That's the only
question that matters."

### Visual approach
list — three surface cards in a row (grid-cols-3), each with a bold gradient
title and muted description text. Cards stagger in with 0.12s delay each.

### Transition
up

---

## Slide 9: What to Use Instead

### What this slide communicates
Five concrete metrics and practices that replace story points.

### Content
1. **Throughput** — Story count per timebox. Track trend and variability; forecast with percentiles.
2. **Cycle Time & Lead Time** — Start→finish and request→delivery. Lower is better; track distribution.
3. **WIP Limits** — Cap concurrency. Expect faster flow and more predictable delivery.
4. **DORA Metrics** — Deployment frequency, lead time for changes, change failure rate, MTTR.
5. **Outcome Metrics** — Adoption, time-to-task, conversion, revenue, NPS, support tickets.

### Speaker notes
"Here are the five things I'd put on your dashboard instead. Throughput — just
count finished stories, track the trend. Cycle time — how long from starting work
to shipping it. WIP limits — cap how many things are in flight at once. DORA
metrics — these are the gold standard for engineering effectiveness. And outcome
metrics — the ones that tell you if customers actually benefited. None of these
require estimation ceremonies. All of them give you better signal."

### Visual approach
list — five surface cards in a 2-column grid (last item spans full width or
uses a 3+2 layout). Each card has a numbered gradient title and description.

### Transition
slide

---

## Slide 10: Mini Example

### What this slide communicates
Revisit the 50 vs 50 example with concrete outcomes to drive the point home one final time.

### Content
**Sprint A (50 SP):**
- Released onboarding checklist
- Activation +12%
- Support tickets -18%

**Sprint B (50 SP):**
- Complex internal refactor
- Performance +3%
- No adoption change

**Takeaway:** "Same points. Very different value."

### Speaker notes
"One more time — because I want this to stick. Sprint A, Sprint B, both 50 points.
Sprint A: simple feature, customers loved it, support tickets dropped. Sprint B:
complex refactor, nobody noticed. If your velocity chart shows two identical sprints,
your velocity chart is lying to you. Same points. Very different value. That's the
whole talk in one slide."

### Visual approach
comparison — two surface cards side by side with metrics. Sprint A metrics in
gradient text (positive), Sprint B metrics in muted text (neutral). Takeaway
line centered below in large text with "Very different value" in gradient.

### Transition
fade

---

## Slide 11: Close

### What this slide communicates
Stop optimizing for story points. Start optimizing for customer value and flow.

### Content
"Value-Centric Flow Over Point Theater"

### Speaker notes
"So here's my ask. Stop optimizing for story points. Start optimizing for value and
flow. Measure what matters to customers. Cap your WIP. Track cycle times. Use
throughput for forecasting. You'll get better outcomes, happier teams, and
honestly, fewer pointless meetings. Thank you. I'll take questions."

### Visual approach
close — centered, large gradient text. No cards, no bullets. Just the statement.

### Transition
fade

---

## Slide 12: Citations

### Content
- Ron Jeffries — *Story Points Revisited*: https://ronjeffries.com/articles/019-01ff/story-points/Index.html
- Allen Holub — *#NoEstimates, An Introduction*: https://holub.com/noestimates-an-introduction/
- Martin Fowler — *Story Counting*: https://martinfowler.com/bliki/StoryCounting.html
- Goodhart's Law: https://en.wikipedia.org/wiki/Goodhart%27s_law
- DORA / State of DevOps: https://cloud.google.com/devops/state-of-devops

### Speaker notes
"All these sources are linked if you want to dig deeper. The Jeffries and Fowler
pieces are especially worth reading in full."

### Visual approach
Clean list of linked sources in a surface card. Each source is a line with
author, title (linked), and URL.

### Transition
up
