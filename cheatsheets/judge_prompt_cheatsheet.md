# Judge Prompt Cheatsheet: Skeleton, Rubric, and Bias Controls

> A judge prompt is a rubric with instructions attached. Steal the skeleton, write your own criteria, and run the bias checklist before you trust a single score.

---

## Prompt Skeleton

```
You are evaluating an AI system output. Score only what the rubric
defines. Do not reward length, confidence, or formatting.

TASK:
{the task the system was given}

SOURCE (the only facts the output may use):
{source text}

OUTPUT TO SCORE:
{system output}

RUBRIC:
{rubric, one criterion per line, with what each score means}

INSTRUCTIONS:
1. For each criterion, quote the part of the output you are scoring
   before you assign the score.
2. Check every number and named entity in the output against the
   SOURCE. A value the source does not contain fails Grounding,
   whatever the rest of the answer does.
3. Score each criterion separately. Then give the overall verdict:
   PASS only if every criterion passes.
4. If the output is empty, a refusal, or off task, say so plainly.

OUTPUT FORMAT (JSON):
{
  "evidence": {"<criterion>": "<quoted text or 'none found'>"},
  "scores": {"<criterion>": 0},
  "verdict": "PASS or FAIL",
  "reason": "<one sentence naming the deciding criterion>"
}
```

Why the skeleton is shaped this way: evidence before scores forces the judge to read before it grades. Per-criterion scores make failures bucketable. JSON makes the result parseable by the regression gate.

---

## Rubric Snippet (0 to 2 per criterion)

```
Grounding:
  2 = every fact and number in the output appears in the SOURCE
  1 = one minor unsupported detail, nothing a user would act on
  0 = any invented number, name, or claim a user could act on

Completeness:
  2 = all parts of the TASK are answered
  1 = one part missing, the rest usable
  0 = the main ask is missing or the output refuses a task the
      SOURCE can answer

Format:
  2 = matches the required structure exactly
  1 = readable but off structure
  0 = structure missing or broken
```

Write the 0 line first. The failing case is the one raters and judges actually disagree about, so define it before the passing cases blur together.

---

## Bias Control Checklist

Run every item before the judge's scores feed any decision:

- [ ] **Order swap.** In pairwise mode, present both orders and average, or count flips. Flip rate above roughly 10% means order is deciding.
- [ ] **Blind identity.** The judge never sees which model or version produced the output. Names leak reputations into scores.
- [ ] **Length control.** Check score versus length correlation on a sample. If longer wins with the same facts, add an explicit instruction and re-check.
- [ ] **Evidence required.** No score without a quote. Judges that must cite drift less and hallucinate fewer justifications.
- [ ] **Human validation slice.** The judge has been compared against human labels on 100 plus items, and the agreement number is written next to every score it produces.
- [ ] **Self judging flagged.** If the judge and the system share a model family, expect self preference. Validate harder or pick a different judge.
- [ ] **Rubric parity.** The judge prompt carries the same rubric text the human raters use. Two rubrics means two evals.
- [ ] **Version pinned.** Judge model, prompt, and rubric are versioned together. A silent change in any one invalidates comparisons with older runs.

---

## Failure Lines to Add Verbatim

Two sentences that fix the most common judge failures when added to the instructions:

- "A longer answer is not a better answer. Score the facts, not the word count."
- "If you cannot find evidence for a claim in the SOURCE, the claim fails Grounding, even if it sounds plausible or is probably true."
