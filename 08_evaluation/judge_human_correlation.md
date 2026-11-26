# Judge to Human Correlation: Proving the Judge Tracks People

> An LLM judge is a measurement instrument. You would not ship a scale you never calibrated; do not ship a judge you never compared against humans.

---

## What You Are Measuring

Judge quality is not "the judge is smart". It is agreement: on items humans have labeled, how often does the judge land where the humans landed. Measure it three ways, because each catches a different failure.

| Method | Use it when | What it catches |
|---|---|---|
| Percent agreement | Pass/fail or categorical labels | Raw mismatch rate; the number stakeholders understand |
| Cohen's kappa | Two raters, categorical labels | Agreement beyond chance; punishes a judge that passes everything |
| Spearman correlation | Scored rubrics (0 to 5, 1 to 10) | Whether the judge ranks outputs the way humans rank them, even if the absolute scores differ |

For pairwise judges, add a fourth: **win rate agreement**. Show the judge and the humans the same pairs, in both orders, and measure how often they pick the same winner.

---

## The Validation Process

1. **Build the validation slice.** 100 to 300 items, human labeled, sampled from real production distribution, stratified by segment. This slice is spent on judge validation only; never tune the system on it.
2. **Freeze the human labels.** Two raters per item where the budget allows, disagreements adjudicated. Record human to human agreement first. That number is the ceiling: a judge cannot meaningfully agree with humans more than humans agree with each other.
3. **Run the judge blind.** Same items, same rubric text the humans used, no access to the human labels.
4. **Compare, then slice.** Overall agreement first, then agreement by category, segment, and failure type. A judge at 85% overall can be at 50% on the one category that matters.
5. **Read the disagreements.** Classify each: judge missed a fact, judge rewarded style, rubric rule unstated, human error. The fix depends on the class, not the count.
6. **Re-validate on a schedule.** Every judge model change, every prompt change, and at a fixed cadence (monthly is common), because both the judge and your product drift.

---

## Acceptance Thresholds

Thresholds are starting points, not laws. Tighten them as the stakes rise.

| Signal | Minimum to iterate with the judge | Minimum to gate launches on the judge |
|---|---|---|
| Judge to human percent agreement | Within 10 points of human to human agreement | Within 5 points of human to human agreement |
| Cohen's kappa (judge vs human majority) | 0.4 | 0.6 |
| Spearman correlation on scored rubrics | 0.6 | 0.8 |
| Pairwise win rate agreement | 70% | 80% |
| Worst segment agreement | Within 15 points of overall | Within 10 points of overall |

Two rules sit underneath the table:

- **Relative, not absolute.** Judge quality is judged against the human to human ceiling on the same items. A kappa of 0.55 is excellent on a task where humans reach 0.6, and poor on a task where humans reach 0.9.
- **The dangerous direction counts double.** A judge that passes what humans fail is worse than a judge that fails what humans pass. Track the false pass rate separately, and set its threshold tighter than overall agreement.

---

## When the Judge Fails Validation

- **Narrow its job.** Use the judge only on the categories and segments where it agrees with humans; route the rest to people.
- **Add structure.** Evidence quoting, per-criterion scores instead of one holistic score, and a grounding pre-check all raise agreement more reliably than a longer prompt.
- **Escalate the model.** Judging is a capability task. The cheapest model that drafts your answers rarely judges them well.
- **Fall back to humans for decisions.** A judge that cannot validate is still useful for triage and ranking during development. It just does not get a vote on launches.
