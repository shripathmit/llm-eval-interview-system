# Benchmark Contamination: The Test Was in the Training Data

> A contaminated benchmark measures memory, not ability.

---

## What it is

Benchmark contamination means items from your eval set, or near copies of them, ended up in the data the system was trained or tuned on. The system has effectively seen the exam before sitting it. Scores come back high and mean almost nothing.

---

## How it shows up

- Benchmark scores far above what production performance suggests
- Near-perfect answers on famous public test items, weak answers on fresh items of the same type
- A sharp score drop when you swap in newly written items at the same difficulty
- Exact or near-exact reproduction of reference answers, including their quirks

---

## Why it happens

Public benchmarks get scraped into training corpora. Internal eval sets leak when engineers paste examples into prompts, tickets, and tuning datasets. Synthetic data generation makes it worse: a model asked to invent practice items often recreates well-known benchmark items from memory.

---

## How to detect it

| Check | What it tells you |
|---|---|
| Overlap scan of eval items against training and tuning data | Direct evidence of leakage |
| Fresh item set written after the model's data cutoff | A clean score to compare against the suspect one |
| Performance gap between public items and private equivalents | A gap points at memorization, not skill |
| Canary strings in private eval sets | Whether set contents surface in model outputs later |

---

## How to fix it

- Keep the golden set private, access-controlled, and out of every tuning pipeline
- Refresh a slice of the set on a schedule with items written after each model update
- Run overlap checks whenever training or tuning data changes
- Report scores on the fresh slice separately from the long-lived set, so contamination shows up as a gap instead of hiding inside an average
