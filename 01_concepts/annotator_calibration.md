# Annotator Calibration: Your Human Scorers Are a Measurement Instrument, Tune Them Like One

> Two annotators who disagree are not two opinions - they are one broken instrument, and every score it produces is suspect.

---

## What is Calibration?

Calibration is the work of making annotators apply the same rubric the same way: training them, testing them against known answers, measuring their agreement, and correcting drift over time. Human labels are the reference standard for the whole eval stack. If the reference moves, every score built on it moves too, and nothing in the dashboard will tell you.

Uncalibrated annotation does not produce noise that averages out. It produces confident, precise-looking scores that describe the annotator pool more than the system being graded.

---

## The Calibration Toolkit

### 1. Training With Worked Examples

**Mechanism:** Before labeling real items, annotators study the rubric with scored examples: clear passes, clear failures, and the borderline cases where reasonable people diverge, each with the reasoning written out.

**Pros:** Aligns everyone to the same interpretation before money is spent on production labels
**Cons:** Example sets age as the product changes; borderline cases are where the real disagreements live and they are finite
**When to use:** Always, at onboarding; refresh whenever the rubric changes

### 2. Gold Questions

**Mechanism:** Items with known correct labels are mixed silently into the work queue. An annotator's accuracy on gold items is tracked continuously.

**Pros:** Detects a drifting or careless annotator in days, not at the next audit; gives an objective quality number per annotator
**Cons:** Gold sets leak and get memorized if reused too long; gold items must be unambiguous, so they under-represent the hard cases
**When to use:** Always, in any program that runs longer than a week

### 3. Agreement Checks

**Mechanism:** A slice of items is labeled by two or more annotators independently. Agreement is measured (percent agreement, or Cohen's kappa for a chance-corrected view) and disagreements are reviewed.

**Pros:** The only direct measurement of whether the rubric is being applied consistently; disagreement patterns point at rubric ambiguity, not just annotator error
**Cons:** Costs double labels on the overlap slice; high agreement can still mean everyone is wrong the same way
**When to use:** At program start, after every rubric change, and on a standing sample forever

```
Reading an agreement number (percent agreement on a binary task):

90%+     Rubric is clear; disagreements are mostly genuine edge cases
80-90%   Workable; review disagreements weekly, sharpen the rubric
Below 80%  Stop and fix: the rubric, the training, or the task design.
           More labels will not rescue an unclear rubric.
```

### 4. Recalibration Sessions

**Mechanism:** The team reviews real disagreements together, decides the correct interpretation, and writes the decision back into the rubric as a new example or rule.

**Pros:** Converts disagreement into rubric improvement; the rubric gets sharper every cycle instead of just older
**Cons:** Takes annotator time away from labeling; decisions made in the room must actually reach the written rubric or they evaporate
**When to use:** Weekly during active programs; after any disagreement spike

---

## Drift: The Slow Failure

Annotator drift has three common shapes:

- **Individual drift:** one annotator's standard quietly loosens or tightens over weeks. Gold questions catch this.
- **Pool drift:** the whole pool shifts together, usually after a memorable edge case becomes an unwritten rule. Only comparison against a frozen reference set catches this.
- **Rubric drift:** the product changed and the rubric did not. Scores stay consistent and become wrong. Caught by re-reading the rubric against current product behavior, on a schedule.

The defense is boring and total: gold questions always on, an overlap slice always labeled twice, a frozen reference set re-scored on a schedule, and recalibration decisions written into the rubric the same day they are made.

---

## Why This Matters Beyond Labels

Calibration data is also diagnostic data for the system. Persistent annotator disagreement on one failure type usually means the category itself is ill-defined, in the rubric and often in the product. A launch program for a voice product in India ran blind human scoring against fixed weekly tasks precisely so that when scores moved, the team could trust the movement was in the system, not in the scorers. That trust is what calibration buys. Without it, every score change starts an argument about the measurement instead of a decision about the product.
