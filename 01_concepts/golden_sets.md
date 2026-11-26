# Golden Sets: The Fixed Benchmark Every Version Must Face

> A golden set is your memory: the fixed set of cases that lets you compare a version from March with a version from October and trust the comparison.

---

## What is a Golden Set?

A golden set (also called a gold set or golden dataset) is a curated, labeled set of test cases with trusted expected answers, kept stable across versions. Every serious change runs against it. Because the cases and labels do not move, a score change means the system changed.

Golden sets are built from the cases that matter most: representative traffic, the hardest known cases, every production failure that ever embarrassed the team, and the edge cases where a wrong answer costs the most.

---

## Building One

1. **Source from reality.** Production logs, beta feedback, support tickets, and known failures. Invented cases test what the writer imagined; real cases test what users do.
2. **Label with your best process.** Your most calibrated annotators, double labeling on disagreements, expert review for the high-stakes slice. Golden labels are the reference standard; budget accordingly.
3. **Cover the failure taxonomy.** Map cases to the failure buckets you actually see (see failure_bucketing.md) and fill the thin buckets deliberately. A golden set that mirrors average traffic underweights exactly the cases that decide launches.
4. **Record provenance.** Each item keeps where it came from, who labeled it, and under which rubric version. A label nobody can explain is a label nobody can defend.

A worked pattern: a document parser team bought its ground truth through a limited beta, where verified user corrections became labels. Those verified cases became the golden set. Every later parser change was graded against failures real users had actually hit, not against a test writer's imagination.

---

## Versioning and Held-Out Sets

Two disciplines keep a golden set honest:

**Versioning.** The set changes over time: new failures get added, dead cases retire. Version it like code, with a changelog. A score on version 12 of the set is not comparable to a score on version 11 unless the overlap is known. Report the set version next to every score, always.

**Held-out sets.** Keep a portion of labeled cases that the tuning process never sees: not in prompt examples, not in failure reviews, not in the fix loop. The working set tells you whether you fixed what you aimed at. The held-out set tells you whether the fix generalized or whether you memorized the test.

```
Golden set
  |- Working set     Used in the fix loop, bucket reviews, tuning
  |- Held-out set    Touched only at decision points: launch gates,
                     model swaps, major prompt rewrites
```

If held-out scores fall while working-set scores rise, you are overfitting the eval. That divergence is one of the most valuable signals in the whole system, and it is free once the discipline exists.

---

## Contamination

Contamination is test data leaking into the system being tested: golden cases in training data, in fine-tuning sets, or pasted into prompts as few-shot examples. The score then measures memory, not ability.

Defenses:

- **Access control:** the golden set lives apart from training pipelines, with an owner and an access list.
- **Canary items:** a few unique, identifiable cases whose verbatim reproduction in outputs proves leakage.
- **Rotation:** a held-out reserve lets you swap in fresh cases when leakage is suspected, without rebuilding from zero.

Public benchmarks carry the worst contamination risk, because everyone trains on the internet. Treat public benchmark scores as marketing until you replicate the ranking on your own golden set.

---

## Who May Change the Set

Governance is the unglamorous part that decides whether the set survives contact with deadline pressure:

- **Adding a production failure:** always allowed, encouraged, fast. New failures are the set doing its job.
- **Removing or relabeling a case the current version fails:** requires review by someone who does not own the version being graded. This is the moment golden sets die: a failing case gets "fixed" instead of the system.
- **Every change:** logged with a reason. The changelog is the audit trail that makes scores defensible months later, to leadership or to an actual auditor.
