# 01 - No-Ground-Truth Eval

> No labeled set, no benchmark, no problem: how to measure quality when nothing is labeled yet.

---

## 🏗️ The Setup: Components & Signals

### Flow

```
[Live or staging outputs]
Outputs → Sampler (random, stratified) → Scored sample
                                              │
Rubric ───────────────────────────────────────┤
                                              ▼
                        Human / judge / beta feedback scores
                                              │
                                              ▼
                        Failure buckets → Fix biggest bucket → Re-score → Bar check
```

### Key Components

| Component | Responsibility |
|---|---|
| Sampling | Pulls a representative slice of real outputs; random, stratified by segment |
| Rubric | Defines good and bad in writing, at the level being scored |
| Judge or Beta Cohort | Produces the signal: human scores, judge scores, or user corrections |
| Failure Bucketing | Groups failures by cause, so fixes target the biggest bucket first |
| The Bar | The threshold that decides ship, hold, or roll back; set before scores arrive |

### Signals & Tools

| Category | Example Signals & Tools |
|---|---|
| Human signals | Corrections, ratings, task completion, escalation rate |
| Annotation | Label Studio, Argilla, in-house review queues |
| Judge frameworks | Ragas, DeepEval, promptfoo, OpenAI Evals |
| Tracing | LangSmith, Braintrust |

---

## Q1. You have no labeled data. How do you set a quality bar for an LLM feature? `[Intermediate]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Write the rubric first.** Define good and bad output in words before any number exists. The bar is meaningless until two people can score the same output the same way.
2. **Sample real outputs.** Pull a random slice of what the system actually produces, across segments. 100-300 items is enough for a first signal.
3. **Label a small seed set by hand.** Expert labels on that sample give you a baseline score and, more important, a failure list.
4. **Set the bar from the cost of errors, not from today's score.** If a wrong output costs a user an hour, the bar is high. If it costs a shrug, the bar is lower. Never set the bar at whatever the model happens to hit.
5. **Mark the bar provisional.** Publish it with its sample size, and re-baseline it after the first real labeling round.

A bar set from risk survives launch pressure. A bar set from a deadline does not.

</details>

---

## Q2. How does running a beta buy you ground truth? `[Basic]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Pick a small cohort** of real users who know they are on a beta and know the current accuracy, stated honestly.
2. **Give them real tasks**, not test scripts. Ground truth only forms around work people actually need done.
3. **Instrument corrections as data.** Every edit, rejection, and re-do is captured with the original output attached.
4. **Verify corrections before they become labels.** A sample of corrections gets expert review; bad corrections stay out of the set.
5. **Promote the verified set.** It becomes the tuning set now and the regression set later.

Real case: a document parser at 80% on table recognition had no labeled set. A limited beta turned user corrections into ground truth, tuning took it to 86-88%, and the set outlived the beta.

</details>

---

## Q3. How do you know your eval itself is trustworthy? `[Advanced]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Measure annotator agreement.** Double-label a slice. If two trained annotators cannot agree, the rubric is broken, and every score downstream is noise.
2. **Check the judge against humans.** Score a human-labeled slice with your judge or rules. Report agreement per failure type, not just overall.
3. **Run known probes.** Feed outputs you already know are good and already know are bad. An eval that passes the bad ones is not measuring what you think.
4. **Audit coverage against production failures.** Take last quarter's real incidents and ask: would this eval have caught them? The misses define your blind spots.
5. **Test stability.** Re-score the same frozen set twice. If the score moves on its own, fix the eval before you touch the model.

</details>

---

## Q4. How do you sample outputs for evaluation, and how many do you need? `[Intermediate]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Sample randomly from real traffic.** Cherry-picked examples produce scores that describe your examples, not your system.
2. **Stratify by segments that behave differently:** locale, document type, input length, model version. Averages hide the segment that is failing.
3. **Size the sample to the decision.** 100-200 items gives a rough signal for tuning. A launch or rollback decision needs a tighter margin, so it needs more.
4. **Oversample rare and expensive failures.** A failure type that is 1% of traffic and 90% of the cost deserves more than 1% of your sample.
5. **Freeze the sample.** The same items, re-scored on every change, become your regression set.

</details>

---

## Q5. What is failure bucketing, and why does it beat watching the headline score? `[Basic]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

A headline score tells you the system got worse or better. It never tells you what to fix. Failure bucketing turns a score into a work list:

1. **Score** the sample against the rubric.
2. **Bucket every failure by cause:** retrieval missed, wrong field extracted, format broken, reasoning error, rubric unclear.
3. **Rank buckets** by frequency times cost. The top bucket is your next fix.
4. **Fix the biggest bucket only.** Resist fixing five things at once; you will not know which one worked.
5. **Re-score and confirm** the total moved and no other bucket regressed.

The loop is: score, bucket, fix, re-score. Run it until the top bucket is eval error rather than system error.

</details>

---

## Q6. When do you stop tuning against an eval? `[Advanced]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

Stop, or change the eval, when any of these show up:

1. **Gains fall inside the noise.** Your improvements are smaller than the eval's own variance between runs.
2. **The top failure bucket is eval error.** Annotators disagree with the labels more than the model does. You are now tuning against mistakes.
3. **Scores rise while spot checks stay flat.** The system is learning the test, not the task. That is teaching to the test, and production will expose it.
4. **The remaining failures cost less than the next fix.** Eval work competes with every other engineering investment.
5. **A held-out check disagrees.** Tune on one set, confirm on a set the tuning never touched. When the two diverge, believe the held-out set.

</details>

---

## Q7. What are the risks of synthetic labels? `[Intermediate]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Shared blind spots.** The model generating labels fails on the same inputs as the model being graded, so the hardest cases get labeled wrong with confidence.
2. **Style bias.** Synthetic labels prefer outputs that read like model output. Human phrasing gets scored down for style, not correctness.
3. **Too-clean distribution.** Generated test cases are tidier than production traffic. Scores on them overstate production quality.
4. **Compounding errors.** When synthetic labels train the system and grade the system, a wrong label is both teacher and examiner.
5. **The mitigation is structural:** use synthetic labels for volume and coverage, humans for truth. Validate every synthetic pipeline on a human-labeled slice, and re-validate when either model changes.

</details>

---

## Q8. Scenario: your parser is at 80% accuracy and leadership wants to ship it to all users this quarter. Ship, or wait? `[Advanced]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

Neither option as posed. The production answer is a third option: a limited beta with the bar set in advance.

1. **Price the errors first.** Ask what the failing 20% does downstream. If wrong output flows into reports people act on, a full launch spends user trust you cannot buy back.
2. **Refuse to argue fidelity without measurement.** With no ground truth, "80%" is an estimate, and nobody knows which 20% fails. Make the missing ground truth the problem to solve first.
3. **Ship to a limited cohort instead.** Real users, real documents, the accuracy number stated honestly. A beta is shipping, not delaying: leadership still gets a deliverable this quarter.
4. **Convert feedback into ground truth.** Verified corrections become the tuning set and then the regression set.
5. **Set the full-release bar before the beta starts**, from the cost of errors, and ship wide when the system meets it.

In the real case this took accuracy from 80% to 86-88%, kept users engaged because the number was honest, and gave leadership its quarterly deliverable without betting the team's credibility.

</details>
