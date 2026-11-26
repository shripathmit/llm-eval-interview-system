# Agreement Metrics: Percent Agreement, Kappa, and Alpha

> Agreement metrics answer one question: do two raters mean the same thing by the rubric? Pick the metric that matches your rater count and label type, or the number will flatter you.

---

## The Three Metrics

### Percent Agreement

The fraction of items where the raters gave the same label. Simple, explainable, and misleading on its own: it never corrects for chance, and it inflates when one label dominates. If 90% of outputs pass, two raters who pass everything agree 90% of the time while measuring nothing.

**Use it for:** quick calibration checks, stakeholder reporting, a first look before the real metric.

### Cohen's Kappa

Agreement corrected for chance. Kappa compares the observed agreement to the agreement expected from each rater's label distribution alone:

```
kappa = (observed agreement - expected agreement) / (1 - expected agreement)
```

Kappa is 1 at perfect agreement, 0 at chance level, and negative when raters agree less than chance. It needs exactly two raters and categorical labels. It punishes lazy rating: a rater who labels everything "pass" drags expected agreement up and kappa down.

**Use it for:** two human raters, an LLM judge versus a human, any pass/fail or category rubric.

### Krippendorff's Alpha

The general case. Alpha handles any number of raters, missing labels (not every rater rates every item), and nominal, ordinal, or interval data. It is the right metric for pooled annotation, where five raters each label a slice and overlaps are partial. It is harder to compute by hand, so teams usually take it from a library.

**Use it for:** three or more raters, partial overlap designs, ordinal scales where "good versus ok" is a smaller miss than "good versus bad".

---

## When Each Applies

| Situation | Metric | Why |
|---|---|---|
| Two raters, quick check | Percent agreement | Fast, and everyone understands it |
| Two raters, launch grade labels | Cohen's kappa | Chance correction exposes lazy or loose rating |
| Judge versus human majority | Cohen's kappa | Same two-rater shape, and the false pass analysis pairs with it |
| Three plus raters, full overlap | Krippendorff's alpha | Built for many raters |
| Raters label different slices, partial overlap | Krippendorff's alpha | Tolerates missing data by design |
| Ordinal rubric (bad, ok, good) | Krippendorff's alpha (ordinal) | Counts near misses as partial agreement |
| Scores on a 0 to 10 scale | Spearman or Pearson correlation | Agreement metrics are for categories; correlation is for scores |

---

## Interpretation Bands

Bands for kappa and alpha are conventions, not physics. Use them to start conversations, not to end them.

| Value | Reading | Action |
|---|---|---|
| Below 0.20 | Slight | Stop labeling. The rubric is not shared; rewrite it and recalibrate |
| 0.20 to 0.40 | Fair | Draft quality only. Work the disagreement list before scaling up |
| 0.40 to 0.60 | Moderate | Usable with spot checks. Tighten the rubric on the worst category |
| 0.60 to 0.80 | Substantial | Good enough for most golden sets and judge validation |
| Above 0.80 | Almost perfect | Rare on subjective tasks. Check the task is not too easy |

---

## Traps

- **The prevalence trap.** With heavily skewed labels, percent agreement looks great while kappa stays low. Both numbers are telling the truth about different things; report both.
- **Agreement is not correctness.** Two raters can agree on a wrong label. Agreement proves the rubric is shared, not that it is right. Correctness comes from expert review of a sample, a separate check.
- **Averaging hides the fight.** A single agreement number across all categories hides the one category where raters disagree completely. Always slice agreement by category before you trust it.
- **Calibrate before you measure.** Agreement computed on untrained raters measures their first guesses. Run a calibration round, discuss the disagreements, then measure.
