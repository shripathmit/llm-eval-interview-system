# 07 - Retrieval Eval

> Generation can only use what retrieval hands it. Grade the handoff before you grade the answer.

---

## 🏗️ The Setup: Components & Signals

### Flow

```
[Query set + relevance labels]
Queries → Retriever → Ranked chunks
                            │
                            ▼
        Recall@k, precision@k, nDCG per query
                            │
                            ▼
        Segment breakdown → Failure buckets: missed, noisy, misranked
                            │
                            ▼
        Downstream check: end answers scored on the same queries
```

### Key Components

| Component | Responsibility |
|---|---|
| Query Set | Real queries from logs and beta tasks, frozen and versioned |
| Relevance Judgments | Graded labels per query and chunk: essential, useful, useless |
| Metrics | Recall@k and precision@k for set quality, nDCG for ranking quality |
| Segment Breakdown | Scores split by query type, locale, and document type, never just averaged |
| Downstream Check | End answers evaluated on the same queries, because retrieval serves the answer |

### Signals & Tools

| Category | Example Signals & Tools |
|---|---|
| Retrieval quality | Recall@k, precision@k, MRR, nDCG |
| Usefulness | Answer-bearing rate: does the top-k contain the fact the answer needs |
| Tooling | ranx, ir-measures, Ragas retrieval metrics, in-house harnesses |
| Failure signals | Zero-result rate, segment score gaps |

---

## Q1. Recall@k and precision@k: what does each one tell you? `[Basic]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Recall@k:** of all the chunks that could answer the query, how many made it into the top k. A miss here is unrecoverable; the generator cannot use what it never saw.
2. **Precision@k:** of the top k, how much is actually useful. Low precision dilutes the prompt with near-topic noise and invites confident wrong answers.
3. **They pull against each other.** Raising k lifts recall and taxes precision. The right k is a product decision, not a default.
4. **Report both, always.** A system can ace one and fail the other, and a single blended score hides which failure you have.
5. **Read them per segment.** The average usually describes your easiest queries.

</details>

---

## Q2. When do you need nDCG instead of set metrics like recall@k? `[Basic]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Set metrics ignore order.** Recall@k treats rank 1 and rank k as equals.
2. **Order matters in practice.** The generator reads the top chunks first, context windows truncate, and a key chunk at rank 9 often behaves like a miss.
3. **nDCG credits graded relevance by position:** essential chunks ranked high score well, essential chunks buried score poorly.
4. **Use nDCG when comparing rankers and rerankers,** or any change whose whole point is ordering.
5. **Use set metrics for coarse health:** is retrieval finding the material at all. Pick the metric that matches the decision in front of you.

</details>

---

## Q3. How do you build a retrieval eval set? `[Intermediate]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Sample real queries** from logs and beta tasks. Invented queries test the system you imagine, not the one users have.
2. **Build the candidate pool from multiple retrievers.** Judging only what one system returns biases the labels toward that system.
3. **Label with grades, not binary:** essential, useful, useless. Grades feed nDCG and make borderline calls visible.
4. **Include queries with no good answer in the corpus.** A retriever that always returns something looks fine until you measure what it does when the answer does not exist.
5. **Freeze and version the set** like any golden set, and grow it from production failures on a schedule.

</details>

---

## Q4. How do you evaluate a chunking change? `[Intermediate]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Hold everything else fixed.** Same queries, same relevance labels, same retriever, same generator. Chunking is the only variable.
2. **Compare the retrieval metrics:** recall@k, precision@k, nDCG, per segment.
3. **Then run the end-answer eval on the same queries.** Chunking changes what answers are even possible, and retrieval metrics alone cannot see that.
4. **Human-check a sample of the answers, blind.** Reviewers score answers without knowing which chunking produced them.
5. **Respect the downstream verdict.** Chunking changes have passed retrieval metrics and failed real answers. When the two disagree, the answer is the product, so the answer wins.

</details>

---

## Q5. Retrieved chunks are on-topic, but the answers still fail. What is your metric missing? `[Intermediate]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Relevance is topical. Usefulness is specific.** A chunk can be about the right subject and still not contain the fact the answer needs.
2. **Measure answer-bearing rate:** for each query, does at least one top-k chunk contain the piece the correct answer requires?
3. **Check boundary damage.** The right chunk was retrieved, but the key sentence sits cut in half at its edge, or landed in the neighboring chunk that ranked too low.
4. **Check contradiction load.** Top-k chunks that disagree with each other push the generator into picking one at random.
5. **Bucket these separately.** Missed, noisy, and boundary-damaged are three different fixes: retrieval, ranking, and chunking.

</details>

---

## Q6. Offline retrieval metrics improve, but end-task success does not move. Give the differential. `[Advanced]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **The generator ignores the context** and answers from its own weights. Retrieval improved; nothing downstream consumed the improvement.
2. **Prompt assembly drops the gains:** truncation, ordering, or formatting loses the chunks retrieval worked to find. Log what the generator actually received, not what retrieval returned.
3. **The gains landed on easy queries.** Hard queries drive task failure, and their recall did not move. Check the segment breakdown before celebrating.
4. **The labels reward topical chunks** that lack the answer-bearing piece, so the metric improved on a proxy.
5. **Task success has other bottlenecks:** tool errors, reasoning failures, bad instructions. Retrieval can be innocent. Instrument each stage and let the buckets argue.

</details>

---

## Q7. Your relevance labels cover only part of the corpus. How do you evaluate honestly? `[Advanced]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Say so, in the report.** Metrics computed on pooled judgments are estimates. Name the pooling method next to every number.
2. **Never compare two systems on different judged pools.** Same queries, same labels, same pool, or the comparison is fiction.
3. **Grow coverage deliberately:** a fresh batch of judged queries each cycle, aimed at the segments with the thinnest labels.
4. **Spot-check the blind spot.** Hand-judge a small sample of retrievals the pool never covered, to size how wrong the estimate could be.
5. **Watch for pool bias over time.** A pool built from one retriever's outputs systematically flatters that retriever's family of approaches.

</details>

---

## Q8. Scenario: your team wants to replace section-based splitting with LLM semantic chunking. Design the before and after eval. `[Advanced]` `[Scenario]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Freeze the harness first:** one query set, one set of relevance labels, one generator, one prompt. Nothing moves except the splitter.
2. **Baseline the current splitter** on recall@k, precision@k, and nDCG, then score end answers on the same queries.
3. **Run the semantic splitter through the identical harness** and compare per segment, not just overall.
4. **Add a blind human pass on end answers.** Reviewers must not know which splitter produced which answer; this is the check that decides.
5. **Decide on the end answers.** Retrieval metrics advise; the answer quality rules.

Real case: semantic chunking looked reasonable on offline numbers. Human eval found the answers stuffed with irrelevant context, or missing the exact piece the question needed, because model-drawn boundaries ignored how the documents were written and how people ask about them. The team reverted to section-based splitting. The eval design lesson: any retrieval change ships only after the downstream human check, never on retrieval metrics alone.

</details>

---
