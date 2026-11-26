# Ground Truth: Where Your Labels Come From Determines What Your Scores Mean

> Every eval score is only as trustworthy as the labels underneath it - ground truth is the most underrated eval design decision.

---

## What is Ground Truth?

Ground truth is the reference you score against: the label, correction, or expected answer that says what the system should have produced. Every eval metric is a comparison between system output and ground truth. Change the source of the labels and you change what the score means, even if the metric formula stays the same.

Ground truth is not one thing. It is a supply chain. Human annotators, beta users, production logs, other models, and hand-written rules all produce labels, at very different cost, speed, and trust levels. Designing an eval means designing that supply chain first.

---

## Why It Is the Hard Part

Models are cheap to run. Labels are not. Three forcing functions make ground truth the bottleneck of every eval system:

1. **Cost:** An expert label takes minutes of skilled human time. A benchmark of 1,000 items is a budget line, not an afternoon.
2. **Disagreement:** On anything subjective, two good annotators disagree. Your ground truth carries that disagreement inside it, and your score inherits it.
3. **Drift:** The right answer changes. Products change, policies change, user behavior changes. A label set frozen last year grades this year's system against last year's world.

This forces a choice about where labels come from:

```
Human labels        High trust, slow, expensive
Beta feedback       High trust, real tasks, messy and incomplete
Production logs     Real distribution, labels must be extracted
Synthetic labels    Fast and cheap, inherits the generating model's blind spots
Weak rules          Instant and narrow, only catches what a rule can express
```

Your job as an eval designer is to pick the source whose failure modes you can live with, and to know exactly what your score can and cannot prove because of that choice.

---

## Source Catalog: 5 Approaches

### 1. Human Labels

**Mechanism:** Trained annotators score outputs against a written rubric: absolute scores, pairwise preference, or pass/fail on defined criteria.

**Pros:** Highest trust; the only source that captures judgment, tone, and edge cases a rubric writer did not foresee
**Cons:** Slow and expensive; annotators drift and need calibration; throughput caps how much you can label
**When to use:** Golden sets, launch decisions, calibrating and auditing every cheaper label source

### 2. Beta and Field Feedback

**Mechanism:** A limited cohort of real users works with the system on real tasks. Their corrections, ratings, and completed or abandoned tasks become labels.

**Pros:** Real tasks and real distribution; users surface failure modes no test set writer imagined; corrections are labels with context attached
**Cons:** Messy and incomplete; beta users are not your full population; feedback skews toward failures and power users
**When to use:** No labeled set exists yet; pre-launch tuning; any system whose quality only shows up in real use

### 3. Production Logs

**Mechanism:** Mine live traffic for eval material: sample outputs, attach outcome signals (completion, retry, escalation), and send a slice for labeling.

**Pros:** Perfect distribution match; volume is unlimited; catches drift because the supply never stops
**Cons:** Raw logs carry no labels; outcome signals are proxies, not judgments; privacy and retention rules apply
**When to use:** Ongoing monitoring, regression sets that must stay current, sourcing items for human labeling

```python
import random

def sample_for_labeling(outputs: list[dict], n: int = 200, seed: int = 42) -> list[dict]:
    """Random sample of production outputs to send for human labeling.

    Random, not cherry-picked: a biased sample produces a biased score.
    Stratify by segment (locale, document type, model version) when
    segments behave differently, and keep the seed fixed so the sample
    is reproducible.
    """
    rng = random.Random(seed)
    if len(outputs) <= n:
        return outputs
    return rng.sample(outputs, n)
```

### 4. Synthetic Labels

**Mechanism:** A model generates test cases, expected answers, or scores. A strong model labels the outputs of the system under test.

**Pros:** Fast, cheap, unlimited volume; can generate rare and adversarial cases on demand
**Cons:** The labeler shares blind spots with the system being graded; style bias toward model-like phrasing; errors compound when synthetic labels both train and evaluate
**When to use:** Volume and coverage, never as the only source of truth; validate on a human-labeled slice before trusting any synthetic score

### 5. Weak Rules

**Mechanism:** Programmatic checks label what a rule can express: schema validity, format, exact-match fields, banned content, numeric ranges.

**Pros:** Instant, free, deterministic; runs on 100% of traffic, not a sample
**Cons:** Only catches known, expressible failures; silent on quality, tone, and correctness of content
**When to use:** As the first tier of every eval stack, and as hard gates in CI; never as the whole eval

---

## Worked Example: Buying Ground Truth With a Beta

A document parser reached about 80% accuracy on table recognition. There was no labeled set, so nobody could say how far from good enough 80% was, or tune against anything real. Leadership wanted a full launch at that fidelity.

The team ran a limited beta instead. A small set of business users worked with the parser on real documents, with the accuracy number stated honestly. Their corrections were collected and verified, and the verified corrections became labels.

Two things happened. Accuracy climbed from 80% to 86-88%, tuned against real failures instead of guesses. And the team now owned a ground truth set built from production work, which became the regression set for every later change. The beta did not just delay the launch decision; it bought the asset every future decision depended on.
