# LLM as Judge: A Model Grades the Model

> A judge buys you volume and speed at the price of trust - the craft is knowing exactly how much trust you spent.

---

## What is LLM as Judge?

LLM as judge means using a language model to grade the outputs of a language model: scoring answers, picking winners, checking criteria. It exists because human labeling does not scale to the iteration speed of LLM development. You can judge 10,000 outputs overnight. You cannot label them overnight.

A judge is a proxy for human judgment. Like every proxy, it is useful exactly to the extent that its agreement with humans has been measured, on your task, with your rubric. An unvalidated judge produces numbers. A validated judge produces evidence.

---

## Approach Catalog: 4 Configurations

### 1. Single Judge, Absolute Scoring

**Mechanism:** One judge model scores one output against the rubric, typically 1 to 5 per dimension, with a short written rationale.

**Pros:** Directly comparable across versions and time; produces per-dimension diagnostics; simplest to run
**Cons:** Judge calibration to the scale drifts with model versions; scores cluster and compress at the top
**When to use:** Tracking a bar over time, regression checks, any trend you report

### 2. Pairwise Judging

**Mechanism:** The judge sees two outputs for the same input and picks the better one, or calls a tie. Run both orders (A-B and B-A) to cancel position bias.

**Pros:** Matches how models are actually compared; relative judgment is more reliable than absolute scoring for judges and humans alike
**Cons:** Produces a win rate, not a quality level; both outputs can be bad and the judge still crowns one
**When to use:** Version comparisons, model selection, prompt A/B decisions

### 3. Panel of Judges

**Mechanism:** Several judges, different models or different rubric emphases, grade independently. Scores are averaged, or disagreements are escalated to a human.

**Pros:** Cancels individual model quirks; disagreement itself is a signal that flags hard or ambiguous items
**Cons:** Cost multiplies; panel members share more bias than their diversity suggests; someone still owns the tie-breaking rule
**When to use:** High-stakes gates, calibration studies, auditing a single judge before trusting it

### 4. Reference-Based Judging

**Mechanism:** The judge compares the output against a reference answer or source documents, grading agreement, coverage, and contradiction rather than free-floating quality.

**Pros:** Grounds the judgment in something checkable; far more reliable for factual tasks; contradiction detection is a concrete job judges do well
**Cons:** Needs references, which are ground truth by another name; a correct answer phrased differently from the reference can be unfairly punished
**When to use:** Extraction, summarization with sources, RAG answers, any task where a source of truth exists

---

## Prompt Structure That Works

A judge prompt is a rubric wearing a costume. The parts that matter:

```
1. The task        What the original system was asked to do
2. The input       The user input and any source material
3. The output      The answer being graded, nothing else
4. The rubric      Dimensions, anchored scale, edge rules
5. The format      Score first or rationale first (pick one, keep it
                   fixed), then a machine-readable score
6. The few-shots   Two or three graded examples, including a failure
```

Two operational rules. Keep the prompt frozen per eval run and version it with the scores, because a judge prompt edit is a rubric change. And never let the system under test and the judge share a model without a human-labeled audit slice; the failure mode is documented in judge_biases.md.

---

## Scoring vs Ranking

| | Scoring (absolute) | Ranking (pairwise) |
|---|---|---|
| Output | A level: "this is a 4" | An order: "this beats that" |
| Answers | Is it good enough? (bar decisions) | Which is better? (selection decisions) |
| Weakness | Scale calibration | No absolute floor |
| Cost | One call per output | Two calls per pair (both orders) |

Serious eval stacks run both: pairwise for fast iteration between versions, absolute scoring against the bar for the ship decision. Confusing the two produces the classic error of shipping a version that beats the old one and still sits below the bar.
