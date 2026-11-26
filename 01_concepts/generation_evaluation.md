# Generation Evaluation: Is the Answer Right, Grounded, and Actually Responsive?

> A fluent answer can be wrong, ungrounded, or beside the point - generation eval measures all three separately because they fail separately.

---

## What Generation Evaluation Measures

Generation eval scores what the model produced, not what it retrieved or extracted. Three properties matter, and each needs its own measurement because a system can pass one and fail the others:

- **Faithfulness:** Every claim in the answer is supported by the provided context. The model did not add, distort, or invent.
- **Groundedness:** The answer's claims trace back to specific source material you can point to. Faithfulness is about not contradicting or exceeding the context; groundedness is about attribution.
- **Answer relevance:** The answer addresses the question the user actually asked, at the scope they asked it.

A fourth property sits underneath all three: **hallucination**, the failure mode where the model produces confident content with no source at all. Hallucination detection is not one metric. It is a set of checks aimed at different ways fabrication happens.

---

## Why One Score Is Not Enough

A single quality score hides which property broke. When a user reports a bad answer, the fix depends on the failure type:

```
Faithfulness failure   The answer says something the context does not support
                       Fix: prompt constraints, citation requirements, decoding
Groundedness failure   The answer is right but cites nothing, or cites the wrong span
                       Fix: retrieval changes, attribution step, UI surfacing
Relevance failure      The answer is true, grounded, and answers a different question
                       Fix: query understanding, intent handling, clarification
Hallucination          The answer invents facts with no context behind them
                       Fix: abstention, retrieval coverage, escalation to a human
```

Score the properties separately, bucket failures by property, and the fix becomes obvious. Blend them into one number and every bad answer looks the same.

---

## Method Catalog: 5 Approaches

### 1. Claim Decomposition and Verification

**Mechanism:** Split the answer into atomic claims. Check each claim against the context with an entailment model or a judge model. Score is the fraction of claims supported.

**Pros:** Pinpoints the exact sentence that broke; works per claim, so partial credit is natural
**Cons:** Decomposition and checking cost multiplies with answer length; the checker has its own error rate
**When to use:** RAG answers, summaries, any output where a single invented sentence does real damage

### 2. Citation Checking

**Mechanism:** Require the model to cite sources per claim, then verify mechanically that each citation exists and that the cited span actually supports the claim.

**Pros:** The existence check is deterministic and free; forces the model to commit to sources at generation time
**Cons:** A real citation can still be a wrong citation; support checking still needs a model
**When to use:** Regulated or high-trust settings where a user or auditor must be able to verify the answer

### 3. LLM Judge With a Property Rubric

**Mechanism:** A judge model scores the answer on one property at a time against a written rubric, with the question, context, and answer all in the prompt.

**Pros:** Scales to full traffic samples; captures relevance and tone that rules cannot
**Cons:** Judge bias is real: position, verbosity, and self-preference; scores drift when the judge model changes
**When to use:** Broad coverage scoring, calibrated against a human-labeled slice before you trust it

### 4. Reference-Based Comparison

**Mechanism:** Compare the answer to a known-good reference answer: overlap metrics, semantic similarity, or a judge asked which answer is better.

**Pros:** Stable target; easy to explain; works well for regression
**Cons:** Many questions have several correct answers; a different correct answer scores low; references go stale
**When to use:** Tasks with constrained answer shapes: short factual answers, summaries of fixed documents, template outputs

### 5. Self-Consistency Probing

**Mechanism:** Ask the same question several times, or ask follow-up questions about the answer's own claims. Flag answers that contradict themselves across samples.

**Pros:** Needs no labels and no context; catches unstable, guessed answers
**Cons:** A model can be consistently wrong; costs multiple generations per item
**When to use:** A cheap hallucination smoke signal on traffic where you have no ground truth at all

---

## Worked Example: A Relevance Failure That Passed Every Other Check

A question-answering system over internal documents scored well on faithfulness: every sentence in its answers was supported by retrieved text. Users still complained. Failure bucketing showed why. The answers were grounded and true, but they answered the general topic instead of the specific question: asked for the retention period of one document class, the system returned a correct, cited paragraph about retention policy in general.

The fix was not in generation. It was in query understanding and in the eval itself: relevance had never been scored separately, so the failure class was invisible. Once relevance got its own rubric and its own bucket, the team could see the rate, fix the intent handling, and watch that one number move without disturbing the faithfulness score.
