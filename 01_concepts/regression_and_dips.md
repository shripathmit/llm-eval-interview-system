# Regression and Dips: What Happens When the Score Falls Below the Bar

> A bar without a dip process is a decoration - the value of an eval system is decided in the hour after a score drops.

---

## Two Different Events, Two Different Responses

**Regression:** A change you made (model, prompt, retrieval, code) made a score worse on a fixed set. You caused it, you can find it, you can revert it.

**Dip:** A production score falls with no obvious change from you. The world moved: user behavior, input distribution, an upstream dependency, a judge model update. Diagnosis comes before any fix.

Treating a dip like a regression wastes days reverting innocent changes. Treating a regression like a dip wastes days investigating the world while your own change sits in the diff. The first step of the process is deciding which event you are in.

---

## The Regression Defense: Sets and Gates

**Regression sets.** Every fixed production failure becomes a permanent test case, added before the fix ships. The set only grows. A fix that does not come with its test is a rumor.

**CI gating.** Run the golden and regression sets on every change that can affect output: model version, prompt, retrieval config, chunking, tools. Gate rules that work:

- Hard fail on safety cases. No threshold, no exceptions.
- Hard fail on regression set cases that were previously fixed.
- Threshold fail on golden set score: below the bar, or down more than the noise band, blocks the merge.
- Warn-only on slices with small samples, where noise would block everything.

**The noise band matters.** A gate set tighter than the eval's own variance trains the team to override it. Measure your eval's run-to-run variance first, then set the gate outside it.

---

## The Dip Process: A Checklist That Starts Before Panic

When a production score falls below the bar, check in this order:

1. **Is the eval itself healthy?** Judge model version changed? Annotation vendor rotated? Pipeline dropped a field? More dips are measurement failures than product failures. Verify the ruler before measuring the room.
2. **Did the sample change?** Traffic mix shifts (a new locale, a big customer, a marketing launch) move averages without anything breaking. Compare like-for-like segments before comparing totals.
3. **Which segment fell?** Locale, document type, task type, user class. A total-score dip with one segment down is a segment bug. All segments down together points at a shared dependency.
4. **What changed, anywhere?** Your releases, model provider updates, upstream data changes, policy changes. Build the timeline before forming theories.
5. **Is it one failure bucket growing?** Bucket the recent failures. A dip is usually one known bucket getting bigger, or one new bucket appearing. Each has a different owner.
6. **How bad is the user impact, honestly?** Score dips and user harm are related, not identical. A 2-point dip in a proxy metric with flat outcome signals is an investigation. A dip with rising escalations is an incident.

---

## Who Decides on Holding a Release

Decide this in writing before the first dip, because mid-incident is the worst time to negotiate authority:

- **The bar owner** (usually the team that owns the eval) can hold any release that fails a hard gate. No meeting required.
- **Threshold failures** get a named decision-maker, typically the launch owner, who can accept the risk in writing with a rollback plan and a date to revisit.
- **Safety failures** cannot be accepted by the launch owner. They escalate to whoever owns the risk framework for the product.
- **In production**, the on-call for the eval system can trigger a rollback on a confirmed dip below the floor, without waiting for the full diagnosis. Diagnosis continues after users are safe.

Write the acceptance down: who accepted, what risk, what rollback trigger, what date it gets re-scored. Undocumented risk acceptance is how a one-time exception becomes the permanent bar.

---

## Worked Example: A Dip That Was Not a Regression

A parser's measured accuracy fell several points in one week. No parser change had shipped. Following the checklist: the eval was healthy, but the sample had changed - a new document type had entered production traffic, with denser tables than anything in the original sets, and it scored far below the established types. The total was honest arithmetic over a different mix.

The response was not a rollback. The new type got its own slice and its own bar, the golden set gained documents of the new type, and tuning work was scheduled against the bucket that was actually failing. The dip process turned a frightening number into a coverage gap with an owner.
