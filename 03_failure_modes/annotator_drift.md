# Annotator Drift: Your Raters Slowly Change the Rubric

> The rubric stays the same on paper while the humans applying it move.

---

## What it is

Annotator drift is the gradual shift in how human raters apply a scoring rubric over time. Standards loosen or tighten, edge case calls flip, new raters interpret criteria differently from the raters who set the baseline. The eval set did not change. The measuring instrument did.

---

## How it shows up

- Scores trend up or down with no matching change in the system
- Agreement between raters falls over weeks, especially on borderline items
- The same output, re-labeled months later, gets a different score
- New raters systematically score higher or lower than the original cohort

---

## Why it happens

Rating is judgment, and judgment moves. Raters get faster and stop reading carefully. They see so many bad outputs that mediocre ones start to look good. They talk to each other and converge on unwritten rules that were never in the rubric. In one voice product eval, the fix was structural: annotators worked blind, never knowing which model or locale they were judging, because a rater who knows what they are scoring will drift toward what they expect to see.

---

## How to detect it

| Check | What it tells you |
|---|---|
| Inter-annotator agreement tracked over time | Falling agreement is drift arriving |
| Seed items with known scores mixed into the work | Whether each rater still lands on the known answer |
| Re-labeling a fixed reference set every cycle | Direct measurement of how far the standard moved |
| Score distribution per rater | Which raters moved, and in which direction |

---

## How to fix it

- Run calibration sessions where raters score the same items and argue the disagreements out loud
- Keep seed items with agreed scores in every batch, and review raters whose seed scores wander
- Version the rubric, and write down every interpretation decision as it is made
- Blind the raters to model, version, and segment wherever the setup allows it
- Re-baseline scores after any rubric or cohort change instead of comparing across the break
