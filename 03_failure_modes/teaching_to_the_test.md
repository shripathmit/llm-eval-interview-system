# Teaching to the Test: Optimizing to the Eval Until the Eval Lies

> An eval used as a target stops working as a measurement.

---

## What it is

Teaching to the test means tuning the system directly against the eval set until the eval score reflects familiarity with those specific items instead of general quality. The set becomes training data in everything but name. The score keeps rising and stops predicting production.

---

## How it shows up

- Eval scores rise steadily while production metrics stay flat
- Fixes land for categories that are heavy in the eval set and rare in real traffic
- Engineers can describe individual eval items from memory
- A fresh sample from production scores far below the curated set

---

## Why it happens

The eval set is the number the team is judged on, so the team rationally optimizes the number. Failure buckets from the set drive the roadmap, prompt changes get tested against the same items they were designed for, and every iteration leaks a little more of the set into the system. The loop itself is sound: score, bucket the failures, fix the biggest bucket, re-score. It breaks when the set being scored is the same set being fixed against, with no held-out check.

---

## How to detect it

| Check | What it tells you |
|---|---|
| A held-out set nobody tunes against | The honest score, next to the tuned one |
| Fresh production sample scored each cycle | Whether gains transfer to real traffic |
| Item-level review of recent fixes | Whether fixes target items or the underlying failure class |

---

## How to fix it

- Split the set: a working set for tuning, a held-out set for decisions, and never let the second leak into the first's workflow
- Rotate fresh production items into the working set so it tracks the real distribution
- Fix failure classes, not items: a fix is done when the class improves on held-out items, not when the original item passes
- Report the held-out score as the headline number, even when it is lower
