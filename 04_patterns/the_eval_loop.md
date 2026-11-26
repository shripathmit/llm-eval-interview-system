# The Eval Loop: Score, Bucket, Fix the Biggest Bucket, Re-Score

> Quality improves one failure class at a time, not one failure at a time.

---

## Problem

A single eval score tells you the system is at 83%. It does not tell you what to do next. Teams without a loop either chase individual bad outputs at random or run broad rewrites that move ten things at once and teach them nothing. Effort goes in, the number wobbles, and nobody can say which change helped.

---

## The pattern

Run eval as a flywheel, not an event. Score the system, group the failures into buckets, fix the biggest bucket, re-score, and confirm the number moved without slipping anywhere else. Each turn of the loop converts one vague quality problem into one concrete engineering task.

---

## How it works

1. **Score.** Run the current system against the golden set and a fresh production sample. Record scores by segment, not just the headline.
2. **Bucket.** Read the failures and group them by cause, not by surface shape. Wrong retrieval, misread table structure, and tone failures are different buckets even when the outputs look similar.
3. **Rank.** Order buckets by frequency times user impact. The biggest bucket is the next task. Everything else waits.
4. **Fix.** Change one thing aimed at that bucket: a rule, a prompt, a chunking boundary, a retrieval parameter. One change per turn, so the result is attributable.
5. **Re-score.** Run the same sets. The target bucket should shrink and the headline should move.
6. **Confirm no slip.** Check the other buckets and the held-out set. A fix that grows a different bucket is not a fix; it is a trade, and it gets made deliberately or not at all.
7. **Refill.** Add the newly found failure types to the set, so the next turn starts from what production looks like now.

---

## When to use it

- Any system in active tuning, where quality work competes for the same engineers as feature work
- When leadership asks what the next quality investment buys; the ranked buckets are the answer
- When a score has stalled and nobody knows why; the bucket distribution usually says it plainly

In a document parsing project, this loop ran on human-evaluated chunks: score the retrieval, bucket the failures, and the biggest bucket turned out to be a chunking strategy that looked smart and read wrong. The fix was a simpler rule, found because the loop forced a ranking instead of an argument.

---

## What each turn produces

- A ranked bucket list, with the top bucket converted into an owned engineering task
- A score history that attributes movement to specific changes
- A growing eval set that tracks production instead of the team's memory of it

Keep the cadence fixed: a turn per release, or per week on fast-moving systems. A loop that runs only when someone worries is a postmortem habit, not a quality system.

---

## Failure mode it prevents

- **Teaching to the test**, when fixes target failure classes and get verified on held-out items
- **Proxy failure**, because bucket reviews force the team to read raw outputs, not just the number
- Random-walk tuning, where effort is spent and nothing is learned
