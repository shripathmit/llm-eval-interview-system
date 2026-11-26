# Human Evaluation: The Slowest Scorer and Still the Reference Standard

> Every cheaper scorer is an approximation of human judgment - human eval is where you find out how good the approximation is.

---

## What is Human Evaluation?

Human evaluation means people grade model outputs: rating quality, choosing the better of two answers, or marking pass/fail against defined criteria. It is slow, expensive, and inconsistent in ways that need managing. It is also the only method that directly measures what users will experience, because users are humans making the same judgments.

Every other scorer in the stack, rules, judges, metrics, is validated against human labels. That makes human eval the foundation even when it scores only a small slice of traffic.

---

## Method Catalog: 4 Approaches

### 1. Absolute Scoring With a Rubric

**Mechanism:** An annotator scores one output against a written rubric, typically 1 to 5 per dimension (correctness, completeness, tone) or a single overall grade.

**Pros:** Produces scores that compare across time and versions; each output stands on its own
**Cons:** Annotators calibrate differently to the scale; scores drift as annotators learn or tire
**When to use:** Tracking a bar over time, launch gates, any number you report as a trend

### 2. Pairwise Comparison

**Mechanism:** An annotator sees two outputs for the same input, blind to which system produced which, and picks the better one (ties allowed).

**Pros:** Much easier for humans than absolute scoring; agreement between annotators is higher; directly answers "is the new version better"
**Cons:** Gives a ranking, not a level; cannot tell you whether both outputs are bad; no absolute bar
**When to use:** Version-versus-version decisions, model selection, prompt comparisons

### 3. Likert-Scale Rating

**Mechanism:** Annotators rate agreement or quality on a fixed scale (strongly disagree to strongly agree, or 1 to 7) for statements like "this answer fully addresses the question."

**Pros:** Captures degrees, not just pass/fail; standard in research, so results compare with published work
**Cons:** The middle of the scale becomes a dumping ground; scale meaning varies by annotator without anchors
**When to use:** User-satisfaction style measurement, research-grade studies, subjective dimensions like helpfulness

### 4. Blind Testing

**Mechanism:** Annotators score outputs without knowing which model, version, or condition produced them. Often combined with any method above.

**Pros:** Removes brand and expectation bias; the only way to trust a comparison when annotators know the systems involved
**Cons:** Operational overhead; annotators sometimes guess the source from style anyway
**When to use:** Any comparison where the result will be contested, which includes every launch decision

---

## Worked Example: Blind Human Eval at Launch Scale

A voice product launching in India needed launch decisions for three models across locales, with no appetite for opinion-based calls. The setup:

- A known beta cohort got weekly homework: tasked utterances to speak to the device, so the same kinds of tasks were measured the same way every week.
- Human annotators scored sampled interactions blind: they did not know which model or locale they were judging.
- Scores were kept at three levels: speech success, NLP success, goal success, each out of 100, against a bar of 85.

Because the annotators were blind and the tasks were fixed, a score movement meant the system changed, not the measurement. The language launch decision (which model ships for which locale) was made from those numbers, not from demos.

---

## When Humans Beat Judges

Use humans, and pay the cost, when:

- **The launch is high-stakes.** A judge model is a proxy. Proxies are for iteration speed; the final call deserves the real measurement.
- **The quality is taste-shaped.** Tone, helpfulness, and trust are human judgments. A judge can rank them, but only humans define them.
- **You are calibrating the judge.** Judge scores mean nothing until they are checked against human labels on the same items.
- **The failure mode is new.** Annotators surface failures nobody wrote a check for. Judges mostly find the failures they were prompted to find.

Use judges and rules for volume and speed. Use humans for truth. A healthy eval stack is explicit about which is which.
