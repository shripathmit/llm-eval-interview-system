# Eval Statistics: How Many Labels Before You May Believe a Number?

> Most eval arguments are sample size arguments in disguise - a 2-point gap on 100 items is weather, not climate.

---

## The Core Problem

An eval score is an estimate, not a fact. Score 200 items and get 86%; the true quality of the system on the full distribution sits somewhere in a range around 86%, and the range is wider than most teams assume. Every launch argument of the form "the new version is better, 87 vs 85" is really a question: is that gap larger than the noise?

Three tools answer most of these questions in practice: sample size planning, confidence intervals, and paired comparisons.

---

## Sample Size: What the Numbers Actually Buy

For a pass/fail or percentage score near 85%, the 95% confidence interval shrinks like this:

| Items scored | Interval width (roughly) | What you can claim |
|---|---|---|
| 50 | plus or minus 10 points | Direction, nothing more |
| 200 | plus or minus 5 points | Big regressions, not small gains |
| 500 | plus or minus 3 points | Launch decisions on meaningful gaps |
| 1,000 | plus or minus 2 points | Fine distinctions, at real labeling cost |
| 5,000 | plus or minus 1 point | Rarely worth it outside high-risk launches |

```python
import math

def ci_width(p: float, n: int, z: float = 1.96) -> float:
    """Half-width of the 95% confidence interval for a proportion."""
    return z * math.sqrt(p * (1 - p) / n)

# Score near 0.85: how wide is the uncertainty?
for n in (50, 200, 500, 1000, 5000):
    print(n, round(ci_width(0.85, n), 3))
```

Read the table before designing any eval. If your decision needs to detect a 2-point change, a 200-item set cannot do it no matter how carefully it is labeled. Either fund more labels, accept a coarser decision, or use pairing (below) to get more signal per item.

---

## When Is a Difference Real?

A practical decision rule, in order:

1. **Compute the interval for each score.** If the intervals do not overlap, the difference is probably real.
2. **If they overlap, you have not proven "no difference."** You have proven your sample cannot tell. Say that, in those words, in the launch review.
3. **Check the slices.** A real total difference driven by one segment is a segment finding, not a system finding.
4. **Replicate on a second sample before acting on a surprising result.** Surprising results are where labeling errors and sample quirks live.

For scores that are averages of graded ratings rather than percentages, the same logic applies with the standard error of the mean. The mechanics differ; the discipline does not: report the interval with the score, always.

---

## Paired Comparisons: More Signal Per Label

When two versions score the **same items**, the comparison gets far more sensitive, because item difficulty cancels out. A version that wins on the items both found hard is showing something real, even when the total gap is small.

- **Paired win/loss counting:** For each item, record win, loss, or tie between versions. Test the wins against the losses, ignoring ties. 60 wins to 40 losses on 100 decided items is meaningful evidence; the same totals as independent averages might not be.
- **Same annotators, blind to version:** Pairing the items but not the raters reintroduces rater variance. Keep both paired.
- **Judge-based pairing:** Ask the judge which of two outputs is better, with position randomized, instead of scoring each alone. Judges are more reliable at choosing than at absolute scoring, and position randomization cancels the known position bias.

Pairing is the working answer to the labeling budget problem: it routinely buys the sensitivity of 2-4x the sample at the same annotation cost.

---

## Traps That Produce Confident Nonsense

**Comparing across different samples.** Version A scored on last month's traffic vs version B on this month's measures traffic change plus version change. Uninterpretable. Score both on the same set.

**Peeking and stopping.** Scoring a little, checking, scoring more until the gap looks good, then stopping. The stopping rule manufactures significance. Fix the sample size before scoring.

**Multiple slices, one winner.** Score 30 slices and one will show a big gap by chance. Treat slice findings as hypotheses: confirm on fresh data before acting.

**Averaging ordinal scales.** A rubric scored 1-5 is not a ruler. Report distributions and the share at each level, not just the mean, and never quote a mean to two decimal places.

**Ignoring annotator disagreement.** If humans agree with each other only 80% of the time on an item type, a system score of 90% on that type is measuring luck. Report agreement alongside accuracy; it is the ceiling your scores live under.
