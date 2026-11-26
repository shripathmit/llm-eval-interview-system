# Rubrics: The Written Standard That Turns Opinion Into a Score

> A rubric is a contract: anyone applying it should land on the same score for the same output, or the rubric is not finished.

---

## What is a Rubric?

A rubric is the scoring guide for an eval: the dimensions being graded, the scale for each, and the descriptions that anchor each point on the scale. It is the document that converts "is this answer good?" from a matter of taste into a measurement two people can repeat.

Rubrics serve three audiences at once. Annotators apply them. Judge models are prompted from them. And when a score is disputed, the rubric is the arbiter: the argument becomes about what the rubric says, not about who is senior.

---

## Anatomy of a Working Rubric

1. **Dimensions:** the separate qualities being graded. Keep them few and non-overlapping. Correctness, completeness, and groundedness separate cleanly. "Quality" does not.
2. **Scale:** points with names, not just numbers. A 1 to 5 scale where 3 is undefined will be used as a 2-point scale with a junk drawer in the middle.
3. **Anchors:** a written description of what each score point looks like, per dimension.
4. **Examples:** at least one real output per score point on the hardest dimension, with the reasoning.
5. **Edge rules:** decisions for recurring hard cases, written as rules ("an answer that is correct but cites a source that does not support it scores at most 2 on groundedness").

---

## Anchored Scales Beat Bare Numbers

The difference between a rubric that works and one that produces noise is the anchors:

| Score | Bare version | Anchored version (correctness) |
|---|---|---|
| 5 | Excellent | Fully correct, no unsupported claims, nothing material missing |
| 4 | Good | Correct on the main point; one minor omission or imprecision |
| 3 | Okay | Partially correct; a real error that does not change the main conclusion |
| 2 | Poor | A material error: a user acting on this would do the wrong thing |
| 1 | Bad | Wrong, fabricated, or answers a different question entirely |

Notice the anchored version defines scores by consequences, not adjectives. "A user acting on this would do the wrong thing" is a line two annotators can apply the same way. "Poor" is not.

---

## Worked Example: Answer Quality Rubric

For a question-answering system over documents:

**Dimension 1: Correctness (1-5)**
Anchored as in the table above.

**Dimension 2: Groundedness (1-5)**
- 5: Every factual claim traces to the retrieved documents.
- 3: Most claims trace; one claim goes beyond the sources without changing the answer.
- 1: The answer asserts facts the sources contradict or never mention.

**Dimension 3: Completeness (1-5)**
- 5: Covers every part of the question, including the part users imply but do not state.
- 3: Answers the stated question, misses an implied part.
- 1: Answers a fraction of the question.

**Pass rule:** An answer passes only if correctness is 4 or above AND groundedness is 4 or above. Completeness is reported but does not gate. This encodes a judgment: a complete, fluent, wrong answer is worse than a partial right one, and the rubric should say so explicitly instead of averaging the sin away.

---

## Writing Rules That Survive Contact

- **Write from real failures.** Start the rubric after reading 50 real outputs, not before. The dimensions that matter are the ones the failures cluster on.
- **One dimension, one question.** If an annotator must hold two ideas to score one dimension, split it.
- **Test the rubric before scaling it.** Two annotators, 30 items, measure agreement. Below target, the rubric is the bug. Fix the words, not the people.
- **Version it like code.** Every score records the rubric version that produced it. When the rubric changes, old and new scores are different currencies; do not average across the change without noting it.
- **Let edge rules accumulate.** Every recalibration decision becomes a written rule. A rubric that never grows is a rubric nobody is using honestly.
