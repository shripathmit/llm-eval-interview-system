# 03 - LLM as Judge

> A judge model is not a shortcut around evaluation. It is an eval you now have to evaluate.

---

## 🏗️ The Setup: Components & Signals

### Flow

```
[System outputs + rubric]
Outputs → Judge prompt (rubric encoded) → Scores with evidence
                                                  │
Human-labeled slice ──────────────────────────────┤
                                                  ▼
                        Agreement report → Trust, fix, or fall back to humans
```

### Key Components

| Component | Responsibility |
|---|---|
| Judge Model | Scores outputs against the rubric; version pinned, never silently upgraded |
| Judge Prompt | The rubric encoded as instructions, with level definitions and examples |
| Reference Answer | Optional gold answer the judge compares against; helps on factual tasks |
| Bias Controls | Order swapping, evidence-first scoring, claim checks that keep style from winning |
| Validation Set | A human-labeled slice the judge must match before its scores are trusted |

### Signals & Tools

| Category | Example Signals & Tools |
|---|---|
| Agreement | Judge and human agreement, overall and per failure type |
| Stability | Same set scored twice, score movement with no system change |
| Judge frameworks | Ragas, DeepEval, promptfoo, OpenAI Evals |
| Tracing | LangSmith, Braintrust |

---

## Q1. What is LLM as judge, and when does it work? `[Basic]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **The pattern:** a model scores another model's outputs against a written rubric, at a volume and speed humans cannot match.
2. **It works when the rubric is explicit** and the judgment is checkable: faithfulness to a provided context, coverage of required points, format and constraint compliance.
3. **It works when you validate it** against human labels on your data, not on a benchmark's data.
4. **It struggles with taste,** with quality dimensions nobody has defined yet, and with cases where the judge shares the generator's blind spots, because then both are wrong together and the score looks clean.
5. **Treat the judge as a measurement instrument.** Instruments get calibrated. Nobody ships readings from an uncalibrated one.

</details>

---

## Q2. Single-answer scoring or pairwise judging: which do you pick? `[Basic]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Single-answer scoring** grades one output against the rubric and returns an absolute score. That supports bars, trends, and release gates.
2. **Pairwise judging** shows the judge two outputs and asks which is better. Per comparison it is usually more reliable, because relative judgment is easier than absolute judgment.
3. **Pairwise gives a ranking, not a bar.** It cannot tell you both outputs fail.
4. **Pairwise carries position bias.** The judge favors the first or the longer answer unless you swap the order and average both runs.
5. **Pick by decision:** single scoring for gates and monitoring, pairwise for model selection and A/B comparisons.

</details>

---

## Q3. How do you write a judge prompt that produces stable scores? `[Intermediate]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Encode the rubric verbatim.** Same level definitions and examples the human raters use. Two rubrics means two evals.
2. **Demand evidence before the score.** The judge quotes the part of the output it is scoring, then scores it. Scores without evidence drift toward fluent-sounding outputs.
3. **One dimension per call.** A judge asked to score accuracy, tone, and format in one pass blends them into a vibe.
4. **Fix the output schema.** A strict format, a score field, a reason field. Free-text verdicts cannot be trended.
5. **Keep temperature low and few-shot examples adjudicated.** Examples pulled from real disagreements teach more than invented ones.
6. **Version the prompt like code.** Every score in your store should name the judge model and prompt version that produced it.

</details>

---

## Q4. What biases do judge models have, and how do you control each one? `[Intermediate]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Position bias:** in pairwise judging, the judge favors one slot. Control: run both orders, count a win only when the judge is consistent, treat flips as ties.
2. **Verbosity bias:** longer answers score higher regardless of content. Control: score claim by claim, put "padding adds no credit" in the rubric with an example, and check score against length on your validation set.
3. **Self-preference:** a judge rates outputs from its own model family higher. Control: never let a judge gate releases for its own family without extra human validation on top.
4. **Style bias:** polished phrasing beats correct but plain answers. Control: evidence-first scoring, and rubric items that separate correctness from presentation.
5. **Measure each bias on your validation set.** Generic lists of biases are trivia. Your judge, on your data, with numbers, is engineering.

</details>

---

## Q5. How do you validate a judge against human labels before trusting its scores? `[Intermediate]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Build a validation slice:** a few hundred outputs, human-labeled, stratified across segments, and deliberately rich in failures. A slice of easy passes validates nothing.
2. **Report agreement overall and per failure type.** 90% overall agreement can hide 40% agreement on the one failure type that costs you users.
3. **Read the judge's misses.** Ask not just how often it is wrong, but whether the errors it misses are the expensive ones.
4. **Set a minimum agreement bar** before the judge is allowed to gate anything, and write the bar down.
5. **Re-validate on every change:** judge model, judge prompt, rubric, or a generator upgrade. Validation expires.

</details>

---

## Q6. When is a panel of judges worth the cost? `[Advanced]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **What a panel buys:** several judges from different model families score the same output. Variance drops, and disagreement becomes a signal instead of noise.
2. **Route the disagreements to humans.** The panel's real value is triage: it finds the items humans should spend time on.
3. **Worth it for high-cost decisions:** release gates, judge validation, and scoring the sets other evals will be built from.
4. **Not worth it for bulk scoring** where a single judge already shows proven agreement with humans. You are paying three times for the same number.
5. **Know the limit:** a panel reduces individual variance. It does not fix a blind spot every judge shares.

</details>

---

## Q7. Judge scores jump right after you upgrade the generator model. Real improvement, or judge artifact? `[Advanced]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Freeze the comparison.** Keep a set of outputs from the old generator. Score old and new outputs in the same run, with the same judge and prompt.
2. **Re-score the old outputs.** If the old outputs also score higher than they did last month, your judge moved, not your product.
3. **Check the boring causes first:** judge model version, prompt edits, rubric edits, sampling changes. Most phantom improvements live there.
4. **Check self-preference.** If the new generator is now the judge's own family, suspect the jump until a human slice confirms it.
5. **Confirm on the human-labeled slice.** Only claim the improvement when humans, or a validated held-out check, agree with the judge.

</details>

---

## Q8. Scenario: your team wants to drop human evaluation entirely and gate releases on a judge, to cut cost. What do you require first? `[Advanced]` `[Scenario]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **A validation report, on your data:** judge and human agreement overall and per failure type, with the expensive failure types named.
2. **A permanent human sample.** Small, stratified, scored every release. This is the drift control that tells you when the judge has quietly stopped matching reality.
3. **A pinned judge.** Model and prompt versioned, changes treated as eval changes that need re-validation, never as routine upgrades.
4. **An escalation path.** When the judge and human spot checks disagree past a set margin, humans decide and the judge goes back for diagnosis.
5. **The honest cost math:** the judge removes most of the scoring cost. The small human sample is the cheapest insurance in the whole system, and it is the part that keeps every other number believable.

The position to defend: judges scale the scoring. Humans keep the judge honest. Cutting the second part makes the first part worthless on a delay.

</details>

---
