# Eval Coverage Audit: What Would Your Eval Have Caught?

> Your eval set is a bet about how the system will fail. The audit settles the bet: take the failures production actually produced, and check how many your eval would have caught before they shipped.

---

## What the Audit Measures

The headline number is the **catch rate**: of the real production failures in the audit window, the fraction your current eval (set plus gates plus monitors) would have flagged before users saw them.

Report it two ways:

- **Overall catch rate.** One number for leadership. Useful, and easy to hide behind.
- **Catch rate by failure category.** The working number. A 90% overall rate with a 0% rate on the highest risk category is a failing audit wearing a good costume.

---

## The Audit Process

**Step 1: Collect real failures.**

Pick a window, usually the last 30 to 90 days. Pull failures from every channel that sees them:

| Source | What it gives you |
|---|---|
| Incident reports and postmortems | The severe failures, with root causes attached |
| User reports and support tickets | Failures users noticed and bothered to report |
| Thumbs down and in-product feedback | Volume signal, weak on detail |
| Escalations and account team flags | High value failures, commercially sensitive ones |
| Monitoring alerts | Failures the system noticed itself; note which ones paged a human |

**Step 2: Label and deduplicate.**

Classify each failure by category (grounding, format, completeness, refusal, safety, latency, other) and severity. Merge duplicates: one root cause behind 40 tickets is one failure for audit purposes, weighted by its blast radius.

**Step 3: Replay each failure against the eval.**

For every failure, ask one question: with the eval exactly as it stood when this shipped, would anything have flagged it?

- An item in the set covers this failure mode and scores it: **caught by the set**.
- No set item covers it, but a rule, gate, or monitor would have fired: **caught by a control**.
- Nothing would have fired: **missed**.

Be strict. "A human might have noticed in review" is a miss. The audit grades the system, not the hope.

**Step 4: Compute and slice.**

Catch rate per category, per severity, and per segment. Sort the misses by severity times frequency. That sorted list is your eval roadmap for the next cycle, in priority order, written by your users.

**Step 5: Convert misses into assets.**

Every missed failure becomes eval material: a set item, a rule, or a monitor, owned by a named person with a date. A miss that produces no asset will be missed again.

---

## Audit Report Template

| Category | Real failures | Caught by set | Caught by control | Missed | Catch rate |
|---|---|---|---|---|---|
| Grounding | 18 | 11 | 3 | 4 | 78% |
| Format | 9 | 8 | 1 | 0 | 100% |
| Completeness | 12 | 5 | 1 | 6 | 50% |
| Refusal | 4 | 1 | 0 | 3 | 25% |
| Safety | 2 | 2 | 0 | 0 | 100% |

Read the table by severity, not by volume. In the example, refusal and completeness are the work, even though grounding has the most failures.

---

## Cadence and Ownership

- **Run it quarterly**, and after any severe incident, whichever comes first.
- **The eval owner runs it**, not the team being audited. Self-graded audits drift generous.
- **Publish the misses.** An audit that only reports the catch rate teaches the org to hide failures. An audit that publishes the missed list teaches the org to report them early, which makes the next audit better.

The audit closes the loop the rest of this repo opens: the eval loop improves the system, and the coverage audit improves the eval.
