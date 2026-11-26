# 09 - Extraction Eval

> Extraction accuracy is not one number. Cell, row, and table level scores tell three different stories, and they fail for different reasons.

---

## 🏗️ The Setup: Components & Signals

### Flow

```
[Documents + field schema]
Docs → Extractor → Predicted tables
                        │
                        ▼
        Align to labeled truth → Score cells
                        │
                        ▼
        Roll up: rows intact → Tables structurally sound
                        │
                        ▼
        Error taxonomy counts → Fix biggest bucket → Re-score
```

### Key Components

| Component | Responsibility |
|---|---|
| Field Schema | Defines what a correct extraction is: fields, types, and where each lives in the table |
| Cell Scoring | Value-level accuracy, exact or normalized match per cell |
| Row Scoring | Whether a full record survives intact; one bad cell usually kills the row |
| Structure Scoring | Headers, row and column counts, merged cells, multi-page table joins |
| Partial Credit Policy | Written rules for near misses, decided before scoring starts |
| Error Taxonomy | Failures bucketed by cause, ranked by frequency times downstream cost |

### Signals & Tools

| Category | Example Signals & Tools |
|---|---|
| Accuracy | Cell accuracy, row accuracy, table accuracy, reported separately |
| Structure | Header match rate, row count reconciliation, shifted-column rate |
| Tooling | Labeled document sets, diff viewers, in-house scoring harnesses |
| Downstream | Report rejection rate from the teams consuming the extraction |

---

## Q1. Why score extraction at cell, row, and table level separately? `[Basic]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Cell level** shows raw reading accuracy: of all the values, how many came out right.
2. **Row level** shows whether records survive. Most downstream systems consume rows, and one bad cell usually makes the whole row unusable.
3. **Table level** shows structural success: the right table, complete, with headers where they belong.
4. **The levels diverge hard.** A parser at 95% cell accuracy can sit near 60% row accuracy on wide tables, because every row multiplies the per-cell risk.
5. **Each level points at a different fix:** reading errors, alignment errors, or structure errors. One blended number points at nothing.

</details>

---

## Q2. What is partial credit, and when do you grant it? `[Basic]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Grant it for near misses that preserve meaning:** formatting differences, a trailing unit, minor character noise in a name the reader can still resolve.
2. **Refuse it where the value drives a decision:** numbers, dates, identifiers, codes. A nearly right amount is a wrong amount.
3. **Write the policy before scoring starts.** Partial credit decided case by case, mid-scoring, is score inflation with paperwork.
4. **Report scores with and without partial credit** when the audience is deciding whether to trust the system. The gap between them is information.
5. **Keep the policy in the eval repo,** versioned with the scorer, so two teams' 90% means the same thing.

</details>

---

## Q3. What are table structure errors, and why do they cost more than cell errors? `[Intermediate]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **The shapes:** merged or split rows and columns, headers attached to the wrong column, a table broken across pages and never rejoined, a totals row read as data.
2. **They multiply.** One shifted column corrupts every cell under it, and the values land in the wrong fields, plausible and wrong.
3. **Cell errors are visible and local.** A garbled value looks garbled. Structure errors are quiet: every value is clean text, filed under the wrong meaning.
4. **Downstream cost follows the quiet errors.** Reports built on shifted columns get acted on before anyone notices.
5. **So score structure separately and weight it heavily.** A parser that reads every cell perfectly and misplaces one column in ten is not a 90% parser for any purpose that matters.

</details>

---

## Q4. How do you build an error taxonomy for extraction failures? `[Intermediate]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Start from scored failures, not imagination.** Take a few hundred real failures and sort them before naming anything.
2. **Bucket by cause:** structure broken, text missed, wrong value read, normalization mismatch, content hallucinated that was never in the document.
3. **Rank buckets by frequency times downstream cost.** A rare bucket that corrupts financial tables outranks a common cosmetic one.
4. **Map each bucket to its fix class:** parser rules, model change, document triage, or schema clarification. A bucket with no fix class is a complaint, not a category.
5. **Let the taxonomy become the report.** Every eval run publishes bucket counts, and progress means the top bucket shrinks.
6. **Retire empty buckets.** A taxonomy that only grows becomes a museum.

</details>

---

## Q5. Exact match or normalized match: what normalization is fair? `[Intermediate]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Normalize what the downstream system treats as equal:** whitespace, case in names, date formats, thousand separators, unit spellings.
2. **Never normalize what changes meaning:** rounding money, dropping a negation, merging distinct codes, resolving an ambiguous date the convenient way.
3. **The test is the consumer.** If the report reader cannot tell the two forms apart, they are equal. If they can, they are not.
4. **Publish the normalization rules with every score.** An accuracy number without them cannot be reproduced, challenged, or compared.
5. **Expect the argument.** Most extraction score disputes are normalization disputes wearing a costume. Settle them in the rules, once, in writing.

</details>

---

## Q6. Someone reports a parser at "80% accuracy." What do you ask before believing it? `[Advanced]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **80% of what?** Cells, rows, tables, or documents. These numbers differ by tens of points on the same system.
2. **On whose documents?** Clean born-digital PDFs and scanned, skewed, multi-page tables are different sports.
3. **Who labeled the truth,** and did anyone measure their agreement?
4. **Exact or normalized match,** under which written rules?
5. **What was excluded from the test set?** The document types left out are usually the ones that fail.

Real case: a document parser sat at about 80% on table recognition, and the number turned out to be an estimate with no ground truth behind it at all. The first job was not arguing about the 80. It was building the measurement that could say what the number actually was.

</details>

---

## Q7. How do you set the release bar for an extractor whose output feeds other teams' reports? `[Advanced]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Price the errors by level.** A wrong cell in a lookup table is cheap. A shifted column in a table people act on is not.
2. **Set separate bars per level,** structure highest, then row, then cell, because the blast radius runs in that order.
3. **Set the bar on your documents,** measured with your labels, never on a demo set.
4. **Add a hold rule:** below the bar, output ships with human review attached, not silently. The bar decides the workflow, not just the launch.
5. **Revisit the bar when the consumers change.** A new downstream team acting on the data reprices every error type.

</details>

---

## Q8. Scenario: a vendor claims 95% accuracy on their benchmark and wants a contract. Design your acceptance eval. `[Advanced]` `[Scenario]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Your documents, not theirs.** Sample across every type you actually process, including the scanned, skewed, and multi-page ones vendors leave out.
2. **Your labels.** Your experts label the truth, with a double-labeled slice so agreement is measured, not assumed.
3. **Score at three levels:** cell, row, and table, with your normalization rules published to the vendor before the run.
4. **Report by document type,** not just overall. The average is where a failing document type goes to hide.
5. **Write the acceptance bar into the contract,** per level and per major document type, with the eval set named as the standard.
6. **Re-run the same set on every vendor model update.** An update is a new system until your set says otherwise.
7. **The principle:** vendor benchmarks measure the vendor's documents under the vendor's rules. Contracts should measure yours.

</details>

---
