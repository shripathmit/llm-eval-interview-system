# Ceiling Effects: An Eval Too Easy to Tell Systems Apart

> When every system scores 97%, your eval has stopped giving you information.

---

## What it is

A ceiling effect means your eval set is too easy for the current generation of systems. Every candidate scores near the top, the differences between them fall inside measurement noise, and launch decisions get made on gaps that are not real.

---

## How it shows up

- Competing models or versions cluster within a point or two of each other near the top of the scale
- Score changes between releases are smaller than the labeling noise in the set
- The remaining failures are mostly ambiguous items where annotators disagree with each other
- Hard, realistic cases from production score far below the set's average

---

## Why it happens

Sets are built against the system that existed at the time. That system improves, partly by fixing exactly the failures the set contains. What was a discriminating test becomes a victory lap. The set did its job; it just finished it.

---

## How to detect it

| Check | What it tells you |
|---|---|
| Score distribution across items | Whether most items are now trivially passed |
| Annotator agreement on the remaining failures | Whether the headroom is signal or label noise |
| A difficulty-stratified breakdown | Whether hard items still separate the systems |
| Fresh production failures scored on the side | The difficulty the set is missing |

---

## How to fix it

- Retire items every system passes and replace them with current production failures
- Add a hard slice deliberately: rare cases, adversarial inputs, the segments with the worst live scores
- Report the hard-slice score next to the headline score, and make decisions on the slice
- Keep the old set frozen as a regression check; build the comparison set separately, so the two jobs stop interfering with each other
