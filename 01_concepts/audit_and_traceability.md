# Audit and Traceability: An Eval Score You Cannot Reproduce Is an Opinion

> In regulated settings, "the model scored 88%" is not evidence - evidence is the data version, rubric version, and judge version that produced the 88%.

---

## What Traceability Means for Eval

Every eval score is the output of a pipeline with versioned inputs:

```
Score  =  Eval(data version, system version, rubric version, judge version, code version)
```

If any input is unrecorded, the score cannot be reproduced, compared, or defended. In unregulated products that is a quality problem. In regulated ones (health, finance, aviation, anything with auditors) it is a compliance problem: a launch decision justified by an irreproducible number is, to an auditor, an unjustified launch decision.

Traceability has three concrete requirements:

- **Lineage:** Every scored item records where it came from: which production slice, which document, which user task, when.
- **Versioning:** Data sets, rubrics, judge models, prompts, and scoring code all carry versions, and every run records the full set.
- **Retention:** Raw outputs and labels are kept for the retention period the domain requires, so a score from six months ago can be re-derived and re-examined.

---

## What Gets Versioned

| Artifact | Version trigger | Why it matters |
|---|---|---|
| Eval data set | Any item added, removed, or relabeled | Score changes may be data changes |
| Rubric | Any wording change to criteria or scale | The same output scores differently under a new rubric |
| Judge model and prompt | Model swap, prompt edit, temperature change | Judge drift masquerades as system change |
| System under test | Model, prompt, retrieval, or config change | The thing actually being decided on |
| Scoring code | Any change to aggregation or normalization | Silent math changes are silent score changes |

The discipline that makes this cheap: versions are recorded automatically by the harness on every run, in a run manifest. The moment versioning depends on a human remembering to write it down, it stops happening exactly when the launch pressure is highest.

```json
{
  "run_id": "eval-2026-03-14-0042",
  "system_version": "parser-v2.4.1",
  "data_version": "golden-tables-v17",
  "rubric_version": "extraction-rubric-v6",
  "judge": {"model": "judge-model-x", "prompt_version": "jp-11", "temperature": 0},
  "scoring_code": "eval-harness@1.9.0",
  "score": {"cell": 0.93, "row": 0.88, "table": 0.81}
}
```

---

## Change Control for Evals

Eval artifacts are production code for decisions, and regulated settings treat them that way:

- **Changes are reviewed.** A rubric edit or a data set change goes through the same review as a model change, because it can move scores as much as one.
- **Changes are announced with expected impact.** "We are removing 40 mislabeled items from the golden set; scores will rise about half a point with no system change." Stated before the run, not explained after.
- **Old versions stay runnable.** When a score is challenged, you re-run the exact manifest. If the environment cannot reproduce it, that is a finding in itself.
- **Held-out sets have access control.** Who can see the golden set, who can edit it, and who labeled what is logged. A benchmark everyone can browse is a benchmark the system will be tuned to, deliberately or not.

---

## The Audit Questions, Asked in Advance

Design the eval system so these have one-line answers:

1. This launch decision cited a score. Which run produced it?
2. What data was in that run, and where did each item come from?
3. Who labeled it, under which rubric version, with what agreement rate?
4. What changed between this run and the previous one: system, data, rubric, judge, or code?
5. Can you re-run it today and get the same number?

If any answer requires archaeology, the traceability work is not done. The practical test: hand the manifest to someone who was not on the team and ask them to reproduce the score. Their success is the audit passing before the auditor arrives.

---

## Worked Example: A Score Increase That Was Really a Rubric Change

A team's extraction accuracy rose two points between releases, and the release notes credited a parser improvement. The run manifests told a different story: the rubric had been revised in the same window, clarifying that dates in any standard format counted as correct. Re-running the old parser under the new rubric recovered most of the gain; re-running the new parser under the old rubric removed it.

Nothing dishonest had happened; two legitimate changes landed together and the score credited the wrong one. With manifests, the disentangling took an afternoon. Without them, the team would have shipped a parser change that did nothing, learned a false lesson about what improves extraction, and been unable to explain the number to anyone who asked later. In a regulated review, that explanation is the product.
