# 02 - Human Evaluation

> Humans are the slowest and most expensive judge you have, and the only one whose scores define truth.

---

## 🏗️ The Setup: Components & Signals

### Flow

```
[System outputs]
Outputs → Sampler → Blind scoring queue
                          │
Rubric + trained pool ────┤
                          ▼
              Scores → Agreement check → Adjudication
                          │
                          ▼
              Final labels → Failure buckets → Golden set
```

### Key Components

| Component | Responsibility |
|---|---|
| Rubric | Defines good and bad in writing, with a worked example at every score level |
| Annotator Pool | Trained raters who score without knowing which system produced the output |
| Sampling | Decides which outputs get human eyes; random and stratified, never cherry-picked |
| Calibration | Training rounds and agreement checks that keep every rater scoring the same way |
| Adjudication | A senior second pass that resolves disagreements and fixes the rubric items that caused them |

### Signals & Tools

| Category | Example Signals & Tools |
|---|---|
| Agreement | Inter-rater agreement rate, disagreement rate per rubric item |
| Throughput | Items per hour, cost per label, queue age |
| Annotation | Label Studio, Argilla, in-house review queues |
| Quality control | Gold probe items with known labels, hidden inside the queue |

---

## Q1. Why pay for human evaluation when automated metrics and judge models are cheaper? `[Basic]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Humans define the target.** Every automated score is a proxy. A proxy is only valid while it tracks human judgment, and only humans can check that.
2. **Humans catch what metrics cannot phrase.** Tone, usefulness, the answer that is technically correct and still wrong for the user.
3. **Human labels are the raw material for everything else.** Golden sets, judge validation, and calibration sets all start as human labels.
4. **Cost is a design problem, not a reason to skip.** Sample instead of scoring everything. Tier the work. Spend humans where errors are expensive.
5. **Rule of thumb:** if a wrong output can cost trust, money, or safety, humans stay in the loop at some sample rate forever.

</details>

---

## Q2. What makes a rubric that people can actually score with? `[Basic]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **One thing per item.** A rubric item that mixes accuracy, tone, and format produces a score nobody can interpret.
2. **Define every level with an example, not an adjective.** "Good" is not a definition. A scored example is.
3. **Write in the edge cases you already know:** the partial answer, the right answer in the wrong format, the fluent nonsense.
4. **Keep it short enough to hold in memory.** A 40-item rubric gets applied inconsistently by item 15.
5. **Pilot before you scale.** Two raters, 30 items, compare scores. Every disagreement is a rubric bug until proven otherwise.

</details>

---

## Q3. How do you run blind testing, and why does blindness matter? `[Intermediate]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Strip identity from every item.** No model name, no version, no locale, nothing that tells the rater which system produced the output.
2. **Randomize order.** If all outputs from one system cluster together, raters start scoring the cluster, not the item.
3. **Score against the rubric only.** The rater's job is the output in front of them, not the system they believe in.
4. **Why it matters:** raters who know the source favor the system they expect to win. Blindness is what makes the score evidence instead of opinion.

Real case: a voice product launching in India was scored at three levels, speech success, NLP success, and goal success, each out of 100, with a bar of 85. Annotators scored blind, never knowing which model or locale they were judging. That blindness is what made the launch decision defensible when the scores came in close.

</details>

---

## Q4. Pairwise comparison or an absolute scale like Likert: which do you use, and when? `[Intermediate]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Pairwise is easier on raters.** "Which of these two is better" is a natural judgment, and agreement runs higher.
2. **Pairwise gives you a ranking, not a bar.** It can tell you system A beats system B. It cannot tell you both are bad.
3. **Absolute scales give you a number against a bar.** That is what ship and hold decisions need. The cost: raters drift, and one rater's 4 is another rater's 3.
4. **Use pairwise for model selection,** when the question is which candidate to take forward.
5. **Use absolute scales for release gates,** when the question is whether this output clears a fixed bar. Calibrate hard, because the number will be quoted back at you.

</details>

---

## Q5. How do you calibrate annotators and measure whether they agree? `[Intermediate]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Start with a training set** of items with known, adjudicated labels. New raters score it before they touch live work.
2. **Double-label a slice of everything, continuously.** Not once at onboarding. Agreement is a metric you monitor, not a box you tick.
3. **Track agreement overall and per rubric item.** The overall number hides the one item where raters split every time.
4. **Hide gold probes in the queue.** Items with known labels, scored like any other item. A rater drifting off the gold labels gets retrained before their scores spread.
5. **Feed disagreements back into the rubric.** Adjudicated examples become new rubric examples. Calibration is a loop, not an event.

</details>

---

## Q6. Your annotators disagree a lot, and it is getting worse. What do you do? `[Advanced]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

Diagnose before you blame the raters. Bucket the disagreements first:

1. **Rubric ambiguity.** Two raters read the same item in the rubric two ways. This is the most common cause, and it is your bug, not theirs.
2. **Genuinely hard items.** The output sits on a real boundary. Adjudicate these and add them to the rubric as examples.
3. **Rater drift.** One rater's scores move away from the gold probes over time. Retrain that rater, quietly and specifically.
4. **The task itself changed.** New output types arrived that the rubric never covered. Extend the rubric, then re-baseline.
5. **If the judgment is truly subjective,** stop forcing one number. Switch that dimension to pairwise, or report the distribution honestly.

Never average away disagreement and call the result truth. The disagreement is data about your rubric.

</details>

---

## Q7. How do you keep human evaluation affordable as traffic grows? `[Advanced]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Tier the pipeline.** Rules and judges score everything. Humans score a sample.
2. **Oversample where it matters:** failures, new segments, and the outputs whose errors cost the most.
3. **Shrink the human sample as judge agreement is proven,** and grow it back the moment the system, the prompt, or the rubric changes.
4. **Adjudicate selectively.** Senior time goes to high-disagreement items, not to a flat percentage of everything.
5. **Budget per decision, not per item.** A launch decision buys more labels than a tuning run, because the cost of being wrong is different.

</details>

---

## Q8. Scenario: offline retrieval metrics improve after a switch to semantic chunking, but your human reviewers say the answers got worse. What do you do? `[Advanced]` `[Scenario]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Believe the humans provisionally.** They score the end answer, which is the product. The metrics score a proxy for one stage of it.
2. **Read the actual failures before arguing.** In the real case, answers came back stuffed with irrelevant context, or missing the exact piece the question needed. The chunk boundaries were cutting across the units people ask about.
3. **Bucket and count.** How many failures are boundary damage, how many are noise from oversized chunks. Turn the disagreement into numbers both sides accept.
4. **Decide on the end answer, not the metric.** The team reverted to section-based splitting, following the document's own structure, and kept the semantic approach behind an experiment flag.
5. **Change the process, not just the code.** From then on, any chunking or retrieval change needed a human check on end answers before it shipped, not retrieval metrics alone.

</details>

---
