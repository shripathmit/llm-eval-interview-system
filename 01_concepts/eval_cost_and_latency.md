# Eval Cost and Latency: Signal Per Dollar, Not Scores Per Run

> Eval has a budget like everything else - the design question is which items earn expensive measurement and which get the cheap check.

---

## Where Eval Money Goes

Four cost centers, in the order teams usually discover them:

- **Human labels:** The most expensive signal per item, and the slowest. Expert annotators on hard items are a scarce resource, not a line item.
- **Judge calls:** Cheap per item, but agent traces and long documents multiply tokens fast. Scoring everything with the biggest judge model is a budget decision made by accident.
- **Latency:** Eval in the request path (guardrails, self-checks) adds user-visible delay. Eval outside the path adds pipeline delay: slower CI, slower launches.
- **Maintenance:** Sets, rubrics, and harnesses decay. An unmaintained eval costs little to run and produces expensive false confidence.

The unit that matters is **cost per point of signal**: what did we spend, and how much decision-quality did it buy? A $500 human round that settles a launch argument is cheap. A $5,000 judge sweep that moves no decision is waste.

---

## Tiered Eval: The Standard Shape

Run cheap checks on everything, expensive checks on what earns them:

```
Tier 1  Deterministic checks     100% of items      ~free, instant
        Schema, format, exact fields, banned content, length, language
Tier 2  Small judge / heuristics sampled or triggered  low cost
        Single-property rubric scores, similarity to references
Tier 3  Strong judge             failures and borderline items only
        Multi-property scoring, pairwise comparison, trace review
Tier 4  Human annotators         small, deliberate samples
        Golden sets, judge calibration, disputed items, launch bars
```

Design rules for the tiers:

- **Escalate on uncertainty, not on schedule.** Items pass up a tier when a lower tier cannot decide: borderline scores, judge disagreement, new input types.
- **Every tier calibrates against the one above it.** Periodically send tier 2 items to tier 4 and measure agreement. An uncalibrated cheap tier is a random number generator with good uptime.
- **Keep tier 1 ruthless.** Deterministic gates catch a surprising share of real failures (broken formats, missing fields, empty outputs) at zero marginal cost.

---

## Latency Budgets

Eval latency bites in three places:

| Placement | Budget reality | What belongs there |
|---|---|---|
| In the request path | Milliseconds to low seconds; users feel every check | Tier 1 rules, tiny classifiers, cached verdicts |
| In CI / pre-release | Minutes to an hour; slower gates get bypassed | Golden and regression sets, judge scoring |
| Offline / scheduled | Hours are fine | Human rounds, deep trace review, drift analysis |

The failure mode to avoid is a pre-release gate so slow that engineers batch changes to amortize it, which makes every failure harder to attribute. If the gate takes an hour, split it: a fast gate (tier 1 plus a judge-scored smoke set) on every change, the full suite nightly and before releases.

---

## Spending Rules That Work

**Spend humans on judgment, machines on volume.** Humans label what defines the bar and what calibrates the judges. Everything else is machine work audited by humans.

**Spend on the decision, not the dashboard.** Before funding an eval expansion, name the decision it changes. "We would hold a launch if this slice fell below X" funds it. "It would be nice to know" does not.

**Reallocate from green areas.** Slices that have been stable and well above bar for months need less sampling. Move that budget to new features, new segments, and known failure buckets. Eval budgets should follow risk, and risk moves.

**Count the cost of not measuring.** A missed regression that reaches users costs support time, trust, and sometimes a rollback. Tier 4 human rounds look expensive until priced against one bad launch in a regulated workflow, where a wrong output can mean a compliance incident, not a bad review.

---

## Worked Example: Cutting a Judge Bill Without Losing the Signal

A team scored every production output with a large judge model on five properties. The monthly judge bill rivaled the product's inference bill. Analysis showed two properties were near-deterministic in practice (format and language checks, better done by rules), and most items scored identically across the remaining properties month after month.

The redesign: rules took the two deterministic properties at tier 1. The judge scored a stratified sample plus every item the rules flagged. Humans audited a small slice of judge verdicts weekly. Total eval spend fell by roughly 80%, the launch bar stayed human-anchored, and the freed budget funded human labeling for a new document type the old setup had never measured at all.
