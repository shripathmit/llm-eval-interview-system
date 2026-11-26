# 06 - Rules and Heuristic Eval

> If a rule can check it, a model should not grade it. Deterministic checks are the cheapest, fastest, most honest layer of any eval.

---

## 🏗️ The Setup: Components & Signals

### Flow

```
[System outputs]
Outputs → Schema check → Format rules → Consistency rules
                                                  │
                                                  ▼
                              Pass, or fail with a named reason code
                                                  │
                                                  ▼
                              Failures → Buckets → Model and human tiers handle the rest
```

### Key Components

| Component | Responsibility |
|---|---|
| Schema Validation | Required fields present, types correct, structure intact |
| Format Rules | Regexes and parsers that check dates, IDs, citations, units, and shapes |
| Consistency Checks | Arithmetic and cross-field logic: totals sum, dates order, references resolve |
| Reason Codes | Every failure gets a named cause, so failures bucket without human reading |
| Rule Tests | A labeled slice each rule is scored against, like any other model |

### Signals & Tools

| Category | Example Signals & Tools |
|---|---|
| Rule quality | Per-rule precision: false pass rate, false fail rate on labeled data |
| Coverage | Percentage of outputs fully checked by rules alone |
| Tooling | JSON Schema, Pydantic, Great Expectations, plain unit tests |
| Alerting | New reason code spikes after a release |

---

## Q1. Which checks belong in rules, and which need a model or a human? `[Basic]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Rules own anything with a decidable right answer:** schema, required fields, formats, ranges, arithmetic consistency, forbidden patterns.
2. **Models and humans own meaning:** relevance, faithfulness, tone, whether the answer actually helps.
3. **The test is agreement.** If two engineers reading the spec would always reach the same pass or fail verdict, it is a rule. If they would argue, it is a judgment, and judgments need judges.
4. **Order matters.** Rules run first because they are nearly free, and because a structurally broken output should never reach the expensive tiers.
5. **Every failure a rule can name is a failure your judge never has to guess at.** That shrinks the judge's job to the part only it can do.

</details>

---

## Q2. What do schema and format validation actually catch? `[Basic]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Missing or extra fields,** wrong types, nulls where the contract forbids them.
2. **Malformed structure:** broken JSON, tables with shifted columns, citations pointing at nothing.
3. **Out-of-range values:** dates in the wrong century, percentages above 100, negative quantities.
4. **Why it matters:** these are the failures that crash downstream systems and corrupt reports. A judge scoring prose quality will often rate a malformed output as fine, because it reads well.
5. **They are also the cheapest signal you own.** A schema check costs microseconds and never has an off day.

</details>

---

## Q3. How do you keep a rule set from becoming a maintenance swamp? `[Intermediate]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **One owner.** A rule set everyone can edit is a rule set nobody maintains.
2. **Every rule carries a reason code and a test case.** A rule nobody can explain gets deleted, not debated.
3. **Version rules with the eval.** When a score changes, you should be able to say whether the system changed or the ruler did.
4. **Prune on evidence.** Rules that never fire are dead weight. Rules that always fire are measuring the wrong thing. Both go.
5. **Prefer a parser over a pile of regexes** the moment structure matters. Regexes accrete; parsers state the grammar once.
6. **Review rules when the product spec changes,** not when someone complains about a blocked output.

</details>

---

## Q4. Where do rules beat models outright? `[Intermediate]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Exactness.** A total either sums or it does not. There is no partial credit and no interpretation.
2. **Cost and latency.** A rule runs in microseconds with no API call. A judge call costs money and seconds, per output, forever.
3. **Auditability.** A rule gives the same verdict on the same input every time, which is what regulated settings and postmortems need.
4. **Determinism in gates.** A merge gate or release check that flips verdicts between runs teaches engineers to ignore it. Rules never flip.
5. **The one-liner version:** a judge is a sample from a distribution. A rule is a fact. Build your floor out of facts.

</details>

---

## Q5. How do you evaluate the rules themselves? `[Intermediate]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Run every rule against a human-labeled slice,** the same way you would validate a judge.
2. **Measure both error directions.** False passes: bad output the rule waved through. False fails: good output the rule blocked.
3. **Weight by failure cost.** A rule with a 2% false pass rate on a cosmetic field may be fine. The same rate on a totals check disqualifies it as a gate.
4. **Track per-rule precision over time.** Rules rot as the product changes; the labeled slice tells you when.
5. **Treat a rule as a model with one feature.** It earns its place in the pipeline with measured performance, not with seniority.

</details>

---

## Q6. A rule fails an output that the judge scores highly. Who wins? `[Advanced]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **If the rule guards a hard constraint,** the rule wins. Schema, safety patterns, arithmetic: a high judge score does not repair a broken total.
2. **If the rule is a heuristic proxy,** the disagreement goes to a human sample. The loser gets fixed: the rule, the judge prompt, or the rubric.
3. **Log every disagreement with its type.** One disagreement is noise. A recurring disagreement type is a diagnosis.
4. **Never resolve it by averaging.** A failed hard check plus a happy judge is a failed output with good PR.
5. **Review the pattern monthly.** Persistent rule and judge conflict usually means the spec changed and one of them was not told.

</details>

---

## Q7. Design a tiered eval pipeline. What runs where, and why? `[Advanced]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Tier 1, rules, on 100% of outputs.** Schema, format, consistency. Nearly free, fully deterministic, every failure named.
2. **Tier 2, judge, on a sample plus every borderline case.** All rule failures get a second look only if the failure is a proxy; hard failures stop at tier 1.
3. **Tier 3, humans, on a small stratified sample:** judge disagreements, new segments, and the outputs whose errors cost the most.
4. **Each tier calibrates the one below it.** Human labels validate the judge. Judge and human data together validate the rules.
5. **The budget shape:** coverage comes from the rule tier, scale from the judge tier, truth from the human tier. Total cost is set almost entirely by how much human truth you buy.

</details>

---

## Q8. Scenario: an extractor feeds tables into reports that other teams act on. Which checks must be deterministic before any model score matters? `[Advanced]` `[Scenario]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Required fields present,** in every row, with the right types. A missing value in a report is not a quality issue; it is a wrong report.
2. **Table structure intact:** row and column counts reconcile with the source, headers match the expected schema, no shifted columns.
3. **Numeric totals reconcile.** Column sums and cross-footed totals either match or the output does not ship.
4. **Ranges are sane:** dates inside the reporting period, quantities non-negative, percentages bounded.
5. **No silent truncation.** If the source table has 400 rows, the output says 400 rows, or it fails loudly.
6. **Every failure blocks with a reason code,** instead of lowering a score. Downstream teams act on these reports; a structural error that merely dents an average will eventually be acted on as if it were true.
7. **Only after this floor holds** does model grading earn its place, on the semantic residue: did the extractor read the right table, label it correctly, and map it to the right field.

</details>

---
