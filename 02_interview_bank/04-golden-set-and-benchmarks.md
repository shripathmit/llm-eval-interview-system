# 04 - Golden Sets and Benchmarks

> A golden set is a contract: this is what good means, frozen, versioned, and defended against everyone, including you.

---

## 🏗️ The Setup: Components & Signals

### Flow

```
[Production inputs]
Inputs → Stratified sampling → Expert labeling → Golden set v1
                                                        │
                              ┌─────────────────────────┴─────────────────────────┐
                              ▼                                                   ▼
                     Tuning split (daily use)                     Held-out split (rare, guarded)
```

### Key Components

| Component | Responsibility |
|---|---|
| Seed Sampling | Pulls real production inputs across every segment that behaves differently |
| Expert Labels | Labels applied with a written rubric; a slice is double-labeled for agreement |
| Versioning | Immutable releases with a changelog: items added, removed, relabeled, and why |
| Held-Out Split | The confirmation set tuning never touches; divergence from it is the overfitting alarm |
| Refresh Process | New sampled items enter through the same labeling pipeline as the product changes |

### Signals & Tools

| Category | Example Signals & Tools |
|---|---|
| Health | Agreement on the double-labeled slice, item age, segment coverage |
| Integrity | Canary strings, leak checks, access log on the held-out split |
| Annotation | Label Studio, Argilla, in-house review queues |
| Reporting | Every score published with the set version that produced it |

---

## Q1. What is a golden set, and how is it different from a public benchmark? `[Basic]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **A golden set is yours:** your users' inputs, your distribution, your rubric, labeled by people who know your product.
2. **A public benchmark is shared:** the same items for everyone, built to compare models in general.
3. **The benchmark tells you a model is strong.** It says nothing about your workload, your edge cases, or your failure costs.
4. **The golden set tells you your product is safe to ship.** That is the question a release decision actually asks.
5. **Use both, for different jobs:** benchmarks for shortlisting models, the golden set for every ship, hold, or rollback call.

</details>

---

## Q2. How do you build the first version of a golden set? `[Basic]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Sample real production inputs,** stratified by segment: document type, locale, input length, user type. Never hand-pick the examples you demo with.
2. **Label with experts using a written rubric.** The rubric comes first; labels applied without one are opinions with extra steps.
3. **Double-label a slice** and measure agreement. Disagreements fix the rubric before they poison the set.
4. **Add the known hard cases deliberately:** past production failures, edge cases support keeps reporting, inputs the current system gets wrong.
5. **Start at 200-500 items.** Big enough to separate systems, small enough to label well.
6. **Freeze and version it before anyone tunes against it.** A set that changes while you tune is a moving target that flatters every change.

</details>

---

## Q3. How do you version a golden set without destroying comparability? `[Intermediate]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Versions are immutable.** Once v3 ships, v3 never changes. Corrections go into v4.
2. **Every change gets a changelog entry:** item added, item removed, label changed, with the reason. Silent edits are how trends get faked.
3. **Every score carries its set version.** "Accuracy 88" is meaningless. "Accuracy 88 on golden v4" is a fact.
4. **Re-baseline on material changes.** When the set changes significantly, score the current system on the old and new versions and publish both numbers.
5. **Keep a frozen core** across versions for long-range trend, even as the rest of the set refreshes around it.

</details>

---

## Q4. What is contamination, and how do you keep a golden set clean? `[Intermediate]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Contamination means eval items leak** into training data, fine-tuning sets, few-shot prompts, or the memories of the people tuning the system.
2. **The symptom:** scores on specific items jump in ways production never confirms. The system memorized the test.
3. **Detect it** with canary items (unique strings that should never appear in outputs), membership checks against training corpora, and per-item score audits.
4. **Prevent it** with access control: the held-out split is readable by few, usable in no prompt, and excluded from every training pipeline by an automated check, not by a promise.
5. **A leaked item is a dead item.** Replace it. Arguing about whether the leak mattered costs more than a fresh label.

</details>

---

## Q5. Tuning set versus held-out set: how do you run the split? `[Intermediate]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **The tuning set is the daily driver.** Engineers iterate against it freely. It is allowed to get overfit; that is its job.
2. **The held-out set is touched rarely,** ideally only at decision points: release gates, model swaps, major prompt changes.
3. **Guard it like a secret.** The fewer people and pipelines that can see it, the longer it stays honest.
4. **Watch the gap between the two.** When tuning scores climb and held-out scores stall, you are fitting the test, not the task.
5. **Be honest about peeking.** If the team checks held-out weekly, it is a second tuning set with extra steps. Name it that, and build a third set you actually protect.

</details>

---

## Q6. A public benchmark says the new model is better. Your golden set says it is worse. Who wins? `[Advanced]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **The golden set wins the ship decision.** It matches your distribution, your rubric, and your failure costs. The benchmark matches none of those.
2. **Benchmarks measure benchmark-shaped tasks.** Clean inputs, short answers, general knowledge. Your workload has its own shape.
3. **Investigate the disagreement anyway.** It teaches you exactly where your workload differs from the public one, which is valuable product knowledge.
4. **Check the benchmark side too:** the vendor may have trained on it. A contaminated benchmark flatters the model that ate it.
5. **Report both numbers with their sources.** Leadership hears "better on the public benchmark, worse on our data, shipping on our data." That sentence builds trust in the eval program.

</details>

---

## Q7. When does a golden set go stale, and how do you refresh it? `[Advanced]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Staleness shows up as drift between the set and the product:** new features with no items, dead features with many, new user segments, new failure types the set never scores.
2. **Refresh by adding,** not by editing. New items come from fresh production sampling, labeled through the same pipeline and rubric as the originals.
3. **Retire items for dead features** in a new version, with changelog entries. The old version stays intact for history.
4. **Never refresh by relabeling the items your system fails.** That is grading your own homework, and it converts the set from a measurement into a mirror.
5. **Schedule the audit:** once a quarter, compare set coverage against current production traffic and current failure reports.

</details>

---

## Q8. Scenario: after three months of tuning, golden set scores are up 10 points, and production complaints are flat. Diagnose it. `[Advanced]` `[Scenario]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Suspect the process before the product.** A 10-point gain users cannot feel usually means the team optimized the measurement, not the system.
2. **Check the split.** If tuning and decision-making used the same set, the gain is partly memorization. Compare against the held-out split: if it did not move, you have your answer.
3. **Audit for leakage.** Did eval items end up in prompts, few-shot examples, or fine-tuning data during those three months?
4. **Check what the set measures.** Bucket current production complaints and ask how many the golden set would even score. A set built for last quarter's failures can be blind to this quarter's.
5. **Re-baseline honestly.** Freeze a fresh sample from current production, label it, score the system cold, and publish that number next to the flattering one.
6. **Fix the process:** separate tuning and held-out sets, fresh sampling on a schedule, held-out confirmation before any improvement is claimed out loud.

</details>

---
