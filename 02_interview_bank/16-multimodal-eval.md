# 16 - Multimodal Eval

> A model that reads images fails in ways a text eval never sees. You grade what it perceived, what it extracted, and what it answered, separately.

---

## 🏗️ The Setup: Components & Signals

### Flow

```
[Image or document input]
Input → Perception check: what is actually in the image?
              │
              ▼
        Extraction check: text, tables, values pulled correctly?
              │
              ▼
        Answer check: response correct, grounded in the image?
              │
              ▼
        Score per stage → Failure buckets → Bar check
```

### Key Components

| Component | Responsibility |
|---|---|
| Perception Grading | Scores whether the system identified the right objects, regions, and layout |
| OCR and Extraction Scoring | Compares extracted text and values against ground truth at the right level: character, field, table |
| Visual QA Grading | Scores answers about charts, tables, and diagrams against what the image shows |
| Ground Truth Sets | Human verified images and documents with known content, including hard cases |
| Degradation Sets | Blurred, rotated, skewed, low light, and photographed inputs that match real usage |

### Signals & Tools

| Category | Example Signals & Tools |
|---|---|
| Accuracy signals | Character error rate, field accuracy, table structure accuracy, answer correctness |
| Robustness signals | Score drop from clean scan to phone photo of the same document |
| Tooling | Annotation tools with region marking, document benchmarks, OCR scorers |

---

## Q1. How does multimodal eval differ from text eval? `[Basic]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **There is a perception layer.** Before reasoning starts, the system has to see: read the text, find the table, parse the chart. Text eval starts after this layer. Multimodal eval has to grade it.
2. **Ground truth is richer and pricier.** Labeling an image means marking regions, transcribing tables, and verifying values. A text label is a sentence; an image label is an afternoon.
3. **Input quality varies wildly.** The same document arrives as a clean scan, a skewed photo, and a fax of a fax. Scores must be reported per input condition, not blended.
4. **Failures hide in grounding.** The answer can be fluent, confident, and about a number that is not in the image. Faithfulness checks matter more, not less.
5. **Stage your scoring.** Perception, extraction, answer. A single end score cannot tell you which stage to fix.

</details>

---

## Q2. How do you measure OCR accuracy for a document pipeline? `[Intermediate]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Character and word error rate for the raw layer.** Edit distance between OCR output and verified transcription, over total characters. Good for comparing engines and settings.
2. **Field level accuracy for the product layer.** Nobody downstream consumes raw characters. They consume names, dates, totals. Score the percentage of fields extracted exactly right.
3. **Reading order and structure.** Text in the wrong order or detached from its heading scores fine on error rate and fails in use. Add a structure check on multi column and headed documents.
4. **Report by document type and condition.** Clean scans, photos, and degraded copies get separate numbers. One blended OCR score describes none of them.
5. **Weight errors by cost.** A wrong digit in a total is not equal to a wrong letter in a name. For high cost fields, score exact match and report those fields individually.

</details>

---

## Q3. How do you evaluate table extraction from documents? `[Intermediate]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

Score at three levels, because each level tells a different story:

1. **Cell level.** Percentage of cells whose content is exactly right. Sensitive, and punishing: one merged cell can fail many cells at once.
2. **Row level.** Percentage of rows fully correct. This matches how records are consumed: a row with one wrong value is a wrong record.
3. **Table level.** Percentage of tables extracted completely correctly. The strictest number, and the one that matches a no human review workflow.

Production rules:

1. **Pick the level that matches the consumer.** If rows feed a database, row level is your headline. If a human reviews every table, cell level plus review cost may be the honest pair.
2. **Grade structure separately from content.** Right values in wrong columns is a structure failure with a content pass. Conflating them hides the fix.
3. **Include the tables that break extractors.** Merged cells, multi-line cells, borderless tables, totals rows, and tables split across pages. A test set of clean grid tables certifies a system for a world that does not exist.

</details>

---

## Q4. How do you evaluate chart and diagram question answering? `[Intermediate]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Split questions by skill.** Value reading (what is the value in Q3), comparison (which bar is higher), trend (is it rising), and composition (what share is X). Report accuracy per skill; models fail these unequally.
2. **Vary the chart surface.** Same data as a bar chart, a line chart, and a table. A system that answers from the table and fails from the chart has a perception gap, and you want to know.
3. **Test axis and legend dependence.** Questions that require reading scales and units, not just spotting the tallest bar. Include charts with truncated axes and dual axes, where careless reading produces confident wrong answers.
4. **Grade the grounding.** Require the answer to be traceable to chart elements. Spot check answers against the underlying data table, which is your ground truth.
5. **Include unanswerable questions.** Charts that do not contain the answer. The correct behavior is to say so, and the eval should reward it instead of forcing a guess.

</details>

---

## Q5. How do you build a ground truth set for document understanding? `[Advanced]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Start from real documents.** Production samples across every document type, source, and condition. Synthetic documents are cleaner than the job.
2. **Transcribe and mark by hand.** Human verified text, field values, table structures, and regions. Double-label a slice and measure agreement; table structure is where annotators diverge first.
3. **Record the level of every label.** Each item states whether its truth is at character, field, row, or table level, so scoring never compares against the wrong grain.
4. **Freeze versions.** Documents get revised, templates change. A ground truth set without a version certifies against a past world.
5. **Grow it from failures.** Every production extraction failure, once verified, joins the set. The set becomes the memory of every way documents have beaten the system.

</details>

---

## Q6. How do you test robustness to real world image quality? `[Basic]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Build a degradation ladder.** Take clean documents and produce the versions users actually send: phone photo at an angle, low light, blur, shadow, creases, screenshots of scans.
2. **Score each rung separately.** The number you need is the drop from clean to realistic, per document type. That drop is your robustness budget.
3. **Set the bar on the realistic rung.** A system that clears the bar on clean scans and fails on photos is a demo, not a product.
4. **Feed failures back as training signal for preprocessing.** Deskewing, contrast fixes, and capture guidance in the product all get prioritized by which rung loses the most points.
5. **Keep some degradations held out.** If you tune against every degradation you test, you have taught to the test. Keep a surprise set for honest reads.

</details>

---

## Q7. A multimodal model gives a confident answer about an image. How do you eval hallucination specifically? `[Advanced]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Ask about things that are not there.** Include images missing the queried object, table, or value. Any specific answer is a hallucination by construction. This is your cleanest hallucination rate.
2. **Swap details between similar images.** Two invoices, two charts with different numbers. Answers that import values from the wrong image expose grounding failure.
3. **Score claims, not answers.** Break the response into individual claims and verify each against the image. A mostly right answer with one invented figure is a fail for high stakes use, and claim level scoring shows it.
4. **Use humans for the calibration slice.** Judges, especially judges from the same model family, miss the same visual details the system misses. Human verification on a sample keeps the hallucination number honest.
5. **Track hallucination rate as a guardrail metric.** It belongs next to unsafe rate in release decisions, with its own bar by use case risk.

</details>

---

## Q8. Scenario: leadership wants one accuracy number for the new document AI feature. The vendor reports 97%. What do you do before repeating that number? `[Scenario]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Ask: 97% of what, at what level?** Cell, field, row, or table. On whose documents, in what condition. A level-less accuracy number is marketing, not measurement.
2. **Ask for the test set.** If it is the vendor's set, it describes the vendor's documents. Your documents, your templates, your photo quality are the product's reality.
3. **Run your own sample.** A few hundred real documents from your traffic, human verified, scored at the level your workflow consumes. This takes days, not quarters, and it replaces an argument with a number.
4. **Report the honest structure.** Accuracy per document type, per condition, at the level that matters, with the sample size attached. If the real number is 89% at row level on photos, that is the number leadership plans around.
5. **Set the launch bar from error cost and re-score.** Then the vendor's next claim gets measured on your set, in your harness, like every other change.

</details>
