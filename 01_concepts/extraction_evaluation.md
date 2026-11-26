# Extraction Evaluation: The Level You Measure At Changes the Number You Get

> The same parser can score 95% or 60% depending on the level you grade at - pick the level before you quote the number.

---

## What Extraction Evaluation Measures

Extraction eval scores structured output pulled from unstructured input: fields from forms, rows from tables, entities from text. The central design decision is the **unit of grading**. For a table, you can grade at three levels:

- **Cell level:** Each cell is one item. A table with 200 cells contributes 200 scores.
- **Row level:** A row is correct only if every cell in it is correct.
- **Table level:** A table is correct only if every row and cell is correct, in the right structure.

These are not three views of the same number. They are three different numbers with three different meanings, and they diverge fast. A parser with 98% cell accuracy and 10 cells per row lands near 82% row accuracy if errors spread evenly, and far lower at table level. None of the three is lying. Each answers a different question.

---

## Which Level Answers Which Question

| Level | What it tells you | Who cares |
|---|---|---|
| Cell | How good is the raw extraction engine? | The team tuning the parser |
| Row | How much human cleanup does one record need? | Operations planning review effort |
| Table | How often is a document usable with zero touch? | The business deciding whether to trust automation |

Quote the level with the number, every time. "Accuracy is 88%" with no level attached is how a parser that needs review on every table gets sold as production-ready.

---

## Scoring Decisions That Move the Number

**Exact match vs normalized match.** Is "1,000" equal to "1000"? Is a date in a different format wrong? Define normalization rules before scoring, and version them with the eval. Silent normalization changes are silent score changes.

**Partial credit.** A row with 9 of 10 cells right can score 0 (strict row level) or 0.9 (cell credit within the row). Partial credit is more informative for tuning. Strict scoring is more honest for launch decisions. Use both, label both.

**Missing vs wrong.** An empty cell where the source had a value, and a filled cell with a wrong value, are different failures. Wrong values that look plausible are the dangerous ones. Score them separately.

**Structure errors.** A value extracted correctly but placed in the wrong column is a cell error, a row error, and a usability error all at once. Count it once, in the bucket that owns the fix: structure, not content.

---

## Method Catalog: 4 Approaches

### 1. Golden Document Set

**Mechanism:** A fixed set of documents with human-verified extractions at all three levels. Score every parser version against it.

**Pros:** Comparable across versions; catches regressions precisely; the set is an asset that compounds
**Cons:** Expensive to build well; documents must cover the real distribution, including the ugly ones
**When to use:** The backbone of extraction eval; build it from real failures, not clean samples

### 2. Field-Level Sampling in Production

**Mechanism:** Sample extracted records from live traffic. Humans verify a sample of fields. Report accuracy per field type, not just overall.

**Pros:** Measures the real distribution; per-field scores show which fields are safe to automate
**Cons:** Sampling misses rare document types unless stratified; verification cost per record
**When to use:** Deciding field by field what ships without review and what keeps a human in the loop

### 3. Downstream Task Scoring

**Mechanism:** Score the extraction by whether the system that consumes it succeeds: the record loads, the report generates, the values reconcile with a second source.

**Pros:** Measures what the business actually feels; catches errors that look fine cell by cell
**Cons:** Failures are hard to attribute back to a specific extraction step
**When to use:** As a complement to level scoring, especially before removing human review

### 4. Confidence Calibration

**Mechanism:** The parser emits a confidence per field. Measure whether confidence predicts correctness: of fields scored above 0.95 confidence, what fraction are actually right?

**Pros:** Turns accuracy into a routing decision: high confidence auto-accepts, low confidence goes to review
**Cons:** Many parsers emit confidence that is decorative, not calibrated; needs labeled data to verify
**When to use:** Any pipeline where review capacity is the bottleneck and you must choose what humans look at

---

## Worked Example: 80% Meant Three Different Things

A document parser reported about 80% accuracy on table recognition. The number turned out to be cell level: four out of five cells extracted correctly. At row level the same parser was far lower, because most rows had at least one bad cell, and at table level almost nothing came through untouched. Business users did not experience cell accuracy. They experienced tables that always needed fixing.

The team stopped quoting one number. They reported all three levels, set the launch bar at row level because that matched the review workflow, and ran a limited beta. User corrections, verified, became the ground truth. Tuning against real failed rows took accuracy from 80% to 86-88% at the level that mattered, and the three-level report stayed as the permanent format, so no future version could hide behind the friendliest level.
