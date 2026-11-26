# Which Eval When: Choosing the Eval Stack

> The right eval depends on four facts: whether ground truth exists, how much a wrong answer costs, what you can spend, and where the system is in its life. Decide from the facts, not from habit.

---

## The Four Factors

| Factor | Question to answer | Why it decides |
|---|---|---|
| Ground truth | Do labeled examples exist, or can users generate them? | Labels decide whether you score against truth or against judgment |
| Risk | What does one wrong answer cost: money, trust, safety? | Risk sets the bar and decides how much human review stays in the loop |
| Budget | How much labeling and judging can you afford per run? | Budget decides sample sizes and which tiers you can run every time |
| Stage | Prototype, pre-launch, or production? | Stage decides whether you are exploring, gating, or monitoring |

---

## The Decision Flow

```
Do you have ground truth?
|
|-- Yes --> Score against it. Add a judge for the qualities
|           labels cannot express (tone, completeness).
|
|-- No ---> Can real users touch the system safely?
            |
            |-- Yes --> Limited beta. Corrections become ground
            |           truth. See 04_patterns, beta as ground truth.
            |
            |-- No ---> Build a seed set by hand (50 to 200 items,
                        expert labeled), judge the rest, and treat
                        every score as provisional until the seed
                        set grows.
```

---

## Stage by Stage

| Stage | Eval stack | Bar | Human role |
|---|---|---|---|
| Prototype | Weak rules, small hand labeled seed set, judge for iteration | None formal; you are looking for failure modes, not a number | Read outputs yourself; every failure teaches the taxonomy |
| Pre-launch | Golden set, judge validated against humans, regression gate in CI | Set from the cost of error; see bar_setting_decision_tree.md | Label the golden set, adjudicate disagreements, own the launch call |
| Production | All of the above, plus sampled production scoring, drift monitoring, coverage audits | The launch bar, held; dips trigger the dip process | Sample review on a cadence; audit quarterly |

---

## Risk Adjustments

| Risk level | Adjustment |
|---|---|
| Low (internal tool, drafts, suggestions) | Judge heavy stack is fine; spot check monthly |
| Medium (customer facing, reversible errors) | Judge plus human labeled golden set; gate launches on the set |
| High (money movement, regulated output, safety) | Human review stays in the loop for launch decisions; judge is advisory; bars set per use case, not globally |

---

## Budget Adjustments

- **Almost no budget:** weak rules on 100% of traffic, plus 30 minutes of human reading per week, targeted at failures the rules surface. Small and honest beats large and fake.
- **Moderate budget:** label a golden set once, validate a judge against it, then let the judge carry iteration while humans re-check a sample each release.
- **Real budget:** tiered eval (rules, then judge, then humans on the hard slice), production sampling, and a quarterly coverage audit. See 08_evaluation/eval_coverage_audit.md.

---

## Rules of Thumb

- No ground truth plus high risk means beta or seed set first. Shipping unmeasured at high risk is not a schedule decision; it is an unpriced loan against user trust.
- If you can only afford one artifact, afford the golden set. Judges, gates, and audits all stand on it.
- Match the eval to the decision it feeds. Iteration wants speed (judge), launches want truth (humans and the set), production wants coverage (sampling and monitors).
