# Failure Bucketing: The Loop That Turns a Score Into a Fix List

> A score tells you that you are failing - buckets tell you where, and the biggest bucket tells you what to do on Monday.

---

## What is Failure Bucketing?

Failure bucketing is the practice of sorting every failed eval case into a named category of failure, counting the buckets, and fixing the largest one first. It is the middle step of the eval loop, and it is the step teams skip when they tune by vibes: change a prompt, watch the score wiggle, change it again.

The full loop:

```
Score  ->  Bucket the failures  ->  Fix the biggest bucket
  ^                                            |
  |                                            v
Confirm no slip  <-  Re-score the full set  <-+
```

Each pass through the loop is one unit of real progress: a named failure class, measurably reduced, with the rest of the system verified intact.

---

## Step by Step

### 1. Score

Run the full eval set with the current version. Keep every failed case with its input, output, score, and scorer rationale. A failure you cannot inspect is a failure you cannot bucket.

### 2. Bucket the Failures

Read the failures and sort them into a taxonomy. Start from the failures, not from imagination: cluster what you actually see, name the clusters plainly, and write a one-line test for membership in each bucket.

A taxonomy from a document-processing system, as an example shape:

| Bucket | Membership test |
|---|---|
| Retrieval miss | The needed content never reached the model |
| Wrong level | Scored per cell, the error lived at row level |
| Format break | Content right, structure unusable downstream |
| Unsupported claim | Answer asserts what the sources do not say |
| Refusal error | System declined a case it should have answered |

Rules for a taxonomy that stays useful: buckets are mutually exclusive by primary cause (pick the earliest failure in the chain), an "other" bucket above about 10% means the taxonomy is stale, and bucket definitions are written down with examples, versioned with the eval set.

### 3. Fix the Biggest Bucket

Rank buckets by count weighted by cost. Fix the top one. Only the top one. Fixing three buckets at once destroys attribution: the score moves and nobody knows which change did it, or which change quietly broke something else.

The biggest bucket is also a management tool. "Retrieval misses are 40% of failures" ends prioritization arguments that "overall quality" never could.

### 4. Re-Score the Full Set

Not the bucket. The full set. A fix aimed at one bucket routinely damages another: tighter retrieval raises precision and strands recall; stricter grounding cuts unsupported claims and raises refusal errors. Re-scoring only the fixed bucket reports a victory that the full set would contradict.

### 5. Confirm the Number Does Not Slip

Compare against the previous version on the same set version: headline score, per-bucket counts, and the held-out slice if the change was large. A fix that trades one failure for another at equal total is not progress; it is rearrangement, and the bucket counts are how you catch it.

---

## Worked Example: The Parser Beta Loop

A document parser sat at about 80% accuracy on table recognition, with no labeled set to tune against. A limited beta produced verified user corrections: real failures, labeled. The loop ran on them:

- **Score:** accuracy measured against the verified corrections, at table level.
- **Bucket:** failures clustered on a few table shapes and extraction levels, not spread evenly. The biggest bucket was specific enough to fix.
- **Fix:** targeted work on that bucket, not a general "make the parser better" effort.
- **Re-score:** the full verified set, not just the fixed cases.
- **Confirm:** accuracy climbed from 80% to 86-88% across successive passes, and the verified set became the standing regression set, so later changes had to prove they did not slip the number back.

The loop is why the number moved. Tuning without buckets spends the same effort spread across every failure at once, and the score barely moves.

---

## Anti-Patterns

- **Score-watching:** re-running the eval after every small change and reacting to noise inside the margin of error.
- **Bucket-free tuning:** prompt edits justified by a handful of anecdotes.
- **Vanity buckets:** categories so broad ("quality issues") that no fix can target them.
- **Silent taxonomy edits:** redefining buckets mid-comparison, which manufactures improvement. Version the taxonomy like the set.
