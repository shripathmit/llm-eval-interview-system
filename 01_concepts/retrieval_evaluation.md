# Retrieval Evaluation: Grade the Evidence Before You Grade the Answer

> In a RAG system, most wrong answers are retrieval failures wearing a generation costume - retrieval eval is how you tell them apart.

---

## What is Retrieval Evaluation?

Retrieval evaluation measures whether the retriever returns the content the answer needs: all of it, ranked usefully, without drowning it in irrelevant text. It is a unit eval, run on the retrieval layer alone, with queries whose relevant documents are known.

It matters because of attribution. When an end-to-end answer fails, there are two suspects: the retriever never fetched the evidence, or the model ignored good evidence. The fixes are completely different, and retrieval metrics are how you separate them before spending a week tuning the wrong layer.

---

## The Core Metrics

Setup: for a query, the retriever returns a ranked list of k chunks. A labeled set says which chunks are relevant.

**Recall at k:** of all the relevant chunks that exist, what fraction appear in the top k?

```
Recall@k = (relevant chunks in top k) / (all relevant chunks)
```

The ceiling metric. If recall is low, no prompt or model upgrade can save the answer, because the evidence never arrives.

**Precision at k:** of the k chunks returned, what fraction are relevant?

```
Precision@k = (relevant chunks in top k) / k
```

The noise metric. Low precision means the model reads mostly junk, which costs tokens, latency, and answer quality.

**MRR (mean reciprocal rank):** for each query, take 1 divided by the rank of the first relevant chunk, then average across queries. A first relevant hit at rank 1 scores 1.0, at rank 4 scores 0.25.

The ranking metric for single-answer tasks, where one good chunk is enough and its position decides whether the model uses it.

**nDCG (normalized discounted cumulative gain):** like MRR but handles graded relevance (highly relevant, partially relevant) and rewards putting the best chunks highest across the whole list.

The ranking metric for multi-document tasks, where several chunks matter and their order shapes the answer.

**Context relevance:** the fraction of the retrieved context that is actually on-topic for the query, judged per chunk or per token. Where precision at k counts chunks, context relevance counts content: one long chunk that is 90% filler scores badly here even if it counts as "relevant" for precision.

| Metric | Question it answers | Watch it when |
|---|---|---|
| Recall at k | Did the evidence arrive at all? | Answers fail with "not enough information" |
| Precision at k | How much junk came with it? | Costs rise, answers ramble or contradict |
| MRR | Is the best evidence near the top? | Single-fact questions underperform |
| nDCG | Is the full ranking well ordered? | Multi-document synthesis is weak |
| Context relevance | Is the returned text itself on-topic? | Chunks are long or documents are dense |

---

## Offline vs Online Retrieval Quality

Offline eval uses a frozen query set with labeled relevance. It is reproducible and comparable across versions, and it is the only way to gate a retriever change. Its blind spot: the labeled queries age, and relevance labels are usually binary where real relevance is graded.

Online signals measure retrieval as users experience it: answer acceptance, follow-up rephrasing (users re-ask when retrieval failed them), citation clicks, abandonment. They are noisy and confounded, but they catch the failures the frozen set never imagined.

Run both. Gate changes offline, where you can attribute them. Watch online for drift and for new query types that belong in the offline set.

---

## Worked Example: When Human Eval Overruled the Retrieval Design

A knowledge base over regulated documents needed a chunking strategy. The team tried LLM-based semantic chunking: a model drew the boundaries where topics seemed to shift. It looked principled, and offline similarity checks did not object.

Human evaluation did. Evaluators reading retrieved chunks against real questions found the failure: answers came back stuffed with irrelevant context, or missing the exact section the question needed. The semantic boundaries did not line up with the units people actually ask about, and traceability back to the source section broke.

The team reverted to section-based splitting, following the document's own structure: the boring option. Retrieval behavior fixed itself, because chunks now matched the units of the questions. The lessons generalize:

- **Retrieval quality is defined by the questions, not by the text.** A boundary that looks semantic to a model can still split a question from its answer.
- **Automated similarity metrics did not catch it; human reading did.** Keep a human-eval pass in the loop for retrieval changes, especially chunking changes, where failure is about fit rather than scores.
- **Traceability is a retrieval requirement.** If a chunk cannot point back to its exact source section, the answer built on it cannot be audited, and in regulated settings that ends the discussion.
