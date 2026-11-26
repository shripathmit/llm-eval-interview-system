# Drift Monitoring: Scores Move Because the World Moves

> Production quality rarely collapses in a day; it erodes segment by segment - drift monitoring exists to catch the erosion while it is still cheap.

---

## What Drifts

Four things move under a live system, and each needs its own watch:

- **Input drift:** The traffic changes. New locales, new document types, new user populations, new phrasings of the same task.
- **Concept drift:** The right answer changes. Policies update, products change, last year's correct response is this year's violation.
- **Model drift:** The model changes under you: provider updates, silent version swaps, your own prompt and retrieval edits accumulating.
- **Judge drift:** The measurement changes. The judge model is updated, annotators rotate, rubric interpretation creeps. The system looks different because the ruler changed.

A monitoring setup that only watches the output score cannot tell these apart, and the fix for each is different. Track the score, the input mix, and the measurement stack as three separate lines.

---

## Slice Everything

Averages are where drift hides. The minimum slicing for any production eval:

| Slice by | Drift it reveals |
|---|---|
| Locale / language | A language setup degrading, a new market behaving differently |
| Document or task type | A new type entering traffic, a hard type growing as a share |
| User segment | Enterprise vs consumer, new vs experienced users diverging |
| Model / prompt version | Your own changes, provider updates |
| Time cohort | Week over week trend, slow erosion vs sudden break |

Rule: every alert fires on a slice, not on the total. A total-score alert tells you something is wrong somewhere. A slice alert tells you where, and usually why.

---

## Setting Alert Thresholds That People Trust

Alert design has one failure mode that kills monitoring systems: false alarms. A team that gets paged for noise starts ignoring pages, and then the real drift passes silently. Set thresholds from your own variance:

1. **Measure the noise floor first.** Run the eval on unchanged traffic for several cycles. Record how much each slice score moves on its own.
2. **Alert outside the band.** Threshold at a multiple of observed noise (2-3x the typical swing), not at a round number that feels right.
3. **Use two tiers.** A warning tier for investigation during work hours, a page tier for confirmed user-facing harm. Most drift belongs in the warning tier.
4. **Require persistence for slow signals.** A slice below threshold for two or three consecutive windows is drift. One window is weather.
5. **Shrink the band as samples grow.** Small slices are noisy. Weight thresholds by sample size, or set a minimum sample before a slice can alert at all.

---

## The Monitoring Stack

```
Production traffic
      |
      v
Outcome signals (all traffic) -----> segment dashboards
      |                                    |
      v                                    v
Rolling sample for scoring          slice alerts
(judge + rules, human audit slice)  (warning / page)
      |
      v
Weekly human-rated sample ----------> proxy calibration check
```

Three habits make the stack work:

- **Score a rolling sample continuously**, not a big batch monthly. Small daily samples catch slope; monthly batches catch history.
- **Keep a human-rated slice in the loop.** A few hundred human-scored items per cycle, compared against the judge's scores on the same items. When judge and human diverge, it is judge drift until proven otherwise.
- **Review the input mix, not just scores.** A weekly look at what traffic arrived (new types, shifting shares) predicts next month's score movement better than the score itself.

---

## Worked Example: Catching Erosion by Locale

A voice product scored goal success out of 100, tracked by locale from launch. The total held steady for months. The locale slices told a different story: one code-switched language setup was eroding a point or two per cycle as usage grew beyond the early-adopter population to mainstream users, whose mixing patterns were messier than the beta cohort's.

Because the slice had its own trend line and its own bar, the erosion triggered a warning while the total still looked healthy. The response was targeted: fresh data collection for that locale's real usage patterns, added to the regression set, and tuning aimed at that slice. Without per-locale tracking, the first visible symptom would have been the total score falling months later, with no record of when it started or which population it started with.
