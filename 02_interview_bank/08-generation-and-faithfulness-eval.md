# 08 - Generation and Faithfulness Eval

> A fluent answer that invents facts is worse than no answer. Faithfulness is the floor, not a nice-to-have.

---

## 🏗️ The Setup: Components & Signals

### Flow

```
[Answer + source context]
Answer → Claim extraction → Support check per claim
                                    │
Citation check ─────────────────────┤
                                    ▼
              Verdict: unsupported claims listed by type
                                    │
                                    ▼
              Relevance score → Failure buckets → Fix, re-score
```

### Key Components

| Component | Responsibility |
|---|---|
| Claim Extraction | Breaks the answer into individual checkable statements |
| Support Check | Verifies each claim against the source context; supported or not |
| Citation Check | Confirms citations exist, point at real sources, and the cited span backs the claim |
| Answer Relevance | Scores whether the answer addresses the question that was actually asked |
| Refusal Check | Catches both failures: answering when it should decline, declining when it could answer |

### Signals & Tools

| Category | Example Signals & Tools |
|---|---|
| Faithfulness | Unsupported claim rate, claims per answer, support rate by segment |
| Relevance | Directness score, question coverage from the rubric |
| Tooling | Ragas faithfulness, DeepEval, NLI models, in-house claim checkers |
| Audit | Scheduled human audit of sampled production answers |

---

## Q1. Faithfulness and answer relevance: what is the difference, and why score both? `[Basic]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Faithfulness:** everything the answer claims is supported by the source it was given. Nothing invented, nothing smuggled in from the model's weights.
2. **Relevance:** the answer addresses the question the user actually asked.
3. **The failure modes are independent.** An answer can be faithful and useless: it quotes the context accurately and dodges the question. Or relevant and invented: it answers directly, with details it made up.
4. **Ship decisions need both numbers.** A faithfulness score alone will pass a bot that never actually answers anything.
5. **Report them side by side, per segment.** The segment where they diverge is where your product problem lives.

</details>

---

## Q2. How do you detect hallucination in a grounded answer? `[Basic]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Extract the answer's claims.** Hallucination hides inside fluent paragraphs; it cannot hide as a list of statements.
2. **Check each claim against the retrieved context.** In a grounded system, an unsupported claim is a hallucination by definition.
3. **Name the kinds you find:** invented facts, swapped numbers or dates, real facts attributed to the wrong source, and true-in-general claims the source never made.
4. **Human-verify a sample of the automated checks.** Support checkers miss subtle swaps, and a checker you never audit is a rumor.
5. **Track the unsupported claim rate,** by segment and claim type. That rate is a metric a team can drive down. "Hallucination" as a vibe is not.

</details>

---

## Q3. How do citation checks work, and what do they miss? `[Intermediate]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Existence:** the citation is present and points at a real source in the corpus.
2. **Span check:** the cited passage actually contains support for the claim attached to it. This is the step most implementations skip.
3. **Coverage:** every load-bearing claim carries a citation. Uncited claims are unchecked claims.
4. **What checks miss: citation laundering.** A real source, cited correctly, attached to a claim it does not support. The bracket renders, the user trusts it, and the claim is invented.
5. **Also missed:** the right claim cited to the wrong span, which passes existence checks and fails any reader who clicks.

A citation is evidence only when the span is verified. Otherwise it is decoration with a link.

</details>

---

## Q4. Why score at claim level instead of giving the whole answer one score? `[Intermediate]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **One score hides the crime scene.** Nine supported claims and one invented policy detail average out to "pretty good."
2. **Claim level produces a work list:** which claim, which source, what kind of unsupported. That feeds failure bucketing directly.
3. **Partial credit becomes principled.** An answer with 9 of 10 claims supported is a different problem from one with 5 of 10, and the fixes differ.
4. **It separates the generator's sins:** fabrication, misattribution, and stale facts look identical in a single score and nothing alike at claim level.
5. **It makes bars enforceable.** "No more than 2% unsupported claims on policy content" is a gate. "Answers should be high quality" is a wish.

</details>

---

## Q5. How do you evaluate answers when many different answers are acceptable? `[Intermediate]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Score properties, not strings.** Claims supported, question addressed, constraints obeyed, nothing forbidden added.
2. **Never use exact match** against one reference answer for open-ended output. It punishes correct answers for wording.
3. **Anchor raters with examples:** several acceptable answers at different quality levels, plus the classic failure shapes, all inside the rubric.
4. **Use humans or a validated judge** on a sample, with the property rubric, and measure their agreement like any other eval.
5. **Keep a disagreement log.** Cases where raters split on acceptability are where your rubric's definition of acceptable is still unwritten.

</details>

---

## Q6. Answers are faithful, but users say the bot is useless. What is the eval missing? `[Advanced]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Faithful copying is a dodge.** An answer that restates the context without resolving the question scores perfectly on faithfulness and helps nobody.
2. **Add a directness dimension,** scored against the question: did the answer commit to the thing the user asked, or orbit it?
3. **Check refusal behavior in both directions.** Declining answerable questions is a failure mode with the same cost as hallucinating, and most evals never score it.
4. **Measure task success end to end** on real tasks: did the user finish what they came to do. Per-answer properties are proxies for that, and proxies drift.
5. **Read twenty raw answers yourself.** When metrics and users disagree, the answers are the only witness that never lies.

</details>

---

## Q7. Where does judge-based faithfulness scoring break? `[Advanced]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Subtle swaps.** A changed number, date, or name reads plausibly, and the judge skims past it the way a tired human would.
2. **Long contexts.** The judge cannot hold the whole source in attention, so it checks the claims it can find support for and waves the rest through.
3. **Cross-span arithmetic.** Claims that require adding two numbers from different paragraphs defeat judges that verify by resemblance.
4. **Shared misreading.** When the judge and the generator misread the source the same way, the wrong claim looks supported to both.
5. **Mitigations:** claim-level judging with forced evidence quotes, deterministic checks for numbers and dates, and human audits concentrated on the claim types whose errors cost the most.

</details>

---

## Q8. Scenario: a support bot gets high helpfulness ratings, but a manual audit finds invented policy details in some answers. Design the fix in eval terms. `[Advanced]` `[Scenario]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Demote the helpfulness rating.** Fluency inflates it, and it just certified a bot that invents policy. It becomes a secondary signal, never the headline.
2. **Build a claim-level faithfulness eval** on sampled production answers, with the policy documents as the only source of truth.
3. **Bucket the unsupported claims by type:** invented policy, wrong number, stale rule, wrong product. The biggest bucket is the first fix.
4. **Set a release bar on the unsupported claim rate for policy content,** and gate releases on it. Policy invention is a trust failure, not a quality wobble.
5. **Move decidable claim types to deterministic checks:** prices, dates, eligibility numbers. Rules do not get charmed by fluent prose.
6. **Schedule the audit.** One audit is an anecdote. The same audit, monthly, on a fresh sample, is a rate, and a rate is something a team can be held to.

</details>

---
