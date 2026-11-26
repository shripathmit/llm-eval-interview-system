# Sampling Strategies: You Cannot Label Everything, So Choose What Represents Everything

> Every eval score is a claim about traffic you did not measure, based on traffic you did - sampling is where that claim is won or lost.

---

## What is Sampling in Eval?

Sampling is choosing which outputs get scored. Human labels are expensive, judge calls cost money, and production traffic is effectively infinite. So you score a slice and generalize. The quality of the generalization depends entirely on how the slice was chosen.

A cherry-picked sample produces a score that describes the sample, not the system. Most eval failures that look like metric problems are sampling problems underneath.

---

## Strategy Catalog: 3 Approaches

### 1. Random Sampling

**Mechanism:** Draw outputs uniformly at random from the full traffic or output pool, with a fixed seed so the draw is reproducible.

**Pros:** Unbiased by construction; the score estimates the true population rate; simple to defend
**Cons:** Rare failures may not appear at all; wastes labels on the easy majority
**When to use:** The default for headline scores, launch gates, and any number you will quote to leadership

### 2. Stratified Sampling

**Mechanism:** Split traffic into segments that behave differently (locale, document type, user tier, model version), then sample within each segment, in proportion or with deliberate oversampling of small segments.

**Pros:** Every segment gets a score, so a failing minority segment cannot hide inside a healthy average; small segments become visible
**Cons:** More bookkeeping; segment scores need weighting to recombine into a headline number
**When to use:** Any system whose users or inputs are not uniform, which is nearly all of them

### 3. Failure-Weighted Sampling

**Mechanism:** Oversample the outputs most likely to be wrong: low-confidence cases, long inputs, cases near the decision boundary, cases where cheap signals (retries, edits, escalations) suggest trouble.

**Pros:** Finds failures per label spent far faster than random; ideal for building fix lists and failure buckets
**Cons:** The raw score is biased by design and cannot be quoted as a population rate; needs a parallel random sample for honest reporting
**When to use:** Tuning and debugging, alongside (never instead of) a random sample for the headline number

---

## Sample Size Intuition

You do not need a statistics degree. You need three anchor numbers for a pass/fail style score near the middle of its range:

| Sample size | Rough margin of error (95%) | Good for |
|---|---|---|
| 100 | About plus or minus 10 points | Spotting disasters only |
| 400 | About plus or minus 5 points | Weekly monitoring, segment checks |
| 1,000 | About plus or minus 3 points | Launch decisions near the bar |

Two rules fall out of the table:

1. **If two versions score within the margin of error of each other, you have not measured a difference.** Re-sampling or arguing will not change that. Get more labels or accept the tie.
2. **Decisions near the bar need the biggest samples.** A system at 97 against a bar of 85 needs little data. A system at 86 against a bar of 85 needs a lot, because the cost of a wrong call is highest exactly there.

---

## Sampling Production Traffic

Production is the only source with a perfect distribution match, and the only one that keeps up with drift. A working pattern:

```python
import random

def stratified_sample(outputs: list[dict], per_segment: int = 100, seed: int = 7) -> list[dict]:
    """Sample evenly across segments so small segments stay visible.

    Random within each segment, fixed seed for reproducibility.
    Recombine segment scores with traffic weights for the headline
    number; report segment scores separately so failures cannot hide.
    """
    rng = random.Random(seed)
    by_segment: dict[str, list[dict]] = {}
    for out in outputs:
        by_segment.setdefault(out["segment"], []).append(out)
    sample = []
    for segment_items in by_segment.values():
        sample.extend(rng.sample(segment_items, min(per_segment, len(segment_items))))
    return sample
```

Three habits make production sampling trustworthy:

- **Sample on a schedule, not on suspicion.** Sampling only when something looks wrong teaches you about incidents, not about the system.
- **Keep the seed and the segment definitions versioned.** A score you cannot reproduce is a rumor.
- **Never let the tuning set and the reporting set become the same set.** If you fix against the sample you report on, the reported number stops describing production.
