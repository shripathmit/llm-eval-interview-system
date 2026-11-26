# 13 - Regression and CI Gating

> Models, prompts, and data all change under you. Regression eval is how a change proves it did not break what already worked.

---

## 🏗️ The Setup: Components & Signals

### Flow

```
[Change proposed: model, prompt, data, code]
Change → Run frozen regression set → Score vs baseline
                                          │
                                          ▼
                    Compare: total, per segment, per failure bucket
                                          │
                                          ▼
                    Gate: pass, warn, or block → Ship or send back
```

### Key Components

| Component | Responsibility |
|---|---|
| Frozen Regression Set | The same items, scored the same way, on every change; changes only through review |
| Baseline | The accepted scores of the current production version, stored with the set version |
| Gate | The rule that turns score deltas into a ship or block decision |
| Dip Process | The agreed steps when a score drops: what gets checked, by whom, in what order |
| Flake Control | Retries, judge settings, and variance tracking that keep the eval itself stable |

### Signals & Tools

| Category | Example Signals & Tools |
|---|---|
| Gate signals | Score delta vs baseline, per segment deltas, new failure buckets |
| Stability signals | Score variance across repeated runs, judge agreement drift |
| Tooling | CI pipelines, eval runners, promptfoo, DeepEval, in-house harnesses |

---

## Q1. What belongs in a regression set, and what does not? `[Basic]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Past failures belong, permanently.** Every production failure, every beta correction, every red team hit. The set is the memory of everything that ever broke.
2. **Representative traffic belongs.** A stratified slice of real usage, so the set measures the system users actually meet.
3. **Edge cases with high cost belong.** Rare inputs whose failure is expensive earn a permanent seat.
4. **Tuning items do not belong.** Anything you actively tune against will be gamed by your own process. Keep a separate held-out set for honest measurement.
5. **Stale items get reviewed, not silently kept.** If the product no longer does what an item tests, retire it through the same review that adds items. A set full of dead items produces a confident number about a system that no longer exists.

</details>

---

## Q2. How do you set gating thresholds? `[Intermediate]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Gate on deltas, not absolutes.** The question a gate answers is: did this change make things worse than the accepted baseline? Compare against baseline scores on the identical set.
2. **Set the threshold outside the noise band.** Measure your eval's run to run variance first. A gate tighter than your own variance blocks good changes at random and teaches the team to ignore it.
3. **Gate per segment, not just on the total.** A change that gains 2 points overall and loses 8 in one locale should block. Totals forgive; segments do not.
4. **Tier the gate by change risk.** A prompt wording tweak gets the standard gate. A model version change gets the full set, the held-out set, and human review of the delta.
5. **Write the gate down before the first run.** Thresholds negotiated after seeing a failing score are not thresholds.

</details>

---

## Q3. Walk me through the dip process: a gated score drops below the bar. What happens, step by step? `[Intermediate]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Confirm it is real.** Re-run the eval. Check judge and infrastructure health. Rule out a broken eval before anyone touches the model.
2. **Localize it.** Which segment, which failure bucket, which items flipped from pass to fail? A dip with no location is not actionable.
3. **Read the flipped items.** A human reads a sample of newly failing outputs. Half of all dips are rubric or label problems, and you want to know that before rolling anything back.
4. **Decide: block, roll back, or accept with a reason.** Block the change if the regression is real and priced above the gain. Roll back if it is already live. Accept only with a written reason and an owner.
5. **Close the loop.** New failures join the regression set. The dip, its cause, and its decision go in the log. The next dip starts from this one's lessons.

</details>

---

## Q4. Your eval is flaky: the same change passes and fails on different runs. How do you fix it? `[Advanced]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Find the variance source first.** Run the frozen set five times with nothing changed. If scores move, the flake is in the eval: judge sampling, temperature, ordering effects, or unstable infrastructure.
2. **Pin the judge.** Fixed model version, temperature at or near zero, fixed prompts. A judge that samples creatively grades creatively.
3. **Score items, not vibes.** Flakiness shrinks when items have deterministic checks where possible and narrow rubric questions where not.
4. **Average or majority vote on judge calls.** Three judge passes with a majority costs more and stabilizes borderline items, which is where flakes live.
5. **Quarantine genuinely unstable items.** Some items sit exactly on a decision boundary. Tag them, track them separately, and keep them out of the gate until the rubric or the item is fixed. A gate that cries wolf gets bypassed, and a bypassed gate is worse than none.

</details>

---

## Q5. How do you stop the regression set from being gamed or going stale? `[Advanced]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Separate tuning sets from gating sets.** The team tunes against one set and is gated on another they do not optimize directly. Overlap is where gaming starts.
2. **Hold out a sealed set.** Scored rarely, on major changes only, by a small group. When the working set and the sealed set disagree, believe the sealed set.
3. **Rotate fresh production samples in.** New real traffic, with its new failure shapes, joins the set on a cadence. A set frozen in time certifies a system for a world that moved on.
4. **Version everything.** Set version, rubric version, judge version, baseline version. A score without its versions cannot be compared to last month's score.
5. **Audit the set against incidents.** Every production failure gets one question: was this in the set, and if yes, why did it pass? The answers are your set's real report card.

</details>

---

## Q6. What should trigger a regression run: every commit, every prompt change, every model change? `[Basic]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Tier by blast radius.** Small, fast set on every pull request: a few hundred items, minutes to run, catches obvious breakage.
2. **Full set on the changes that can hurt.** Model version changes, prompt changes to production templates, retrieval or chunking changes, data pipeline changes. These run the full regression plus the held-out set.
3. **Scheduled runs catch what events miss.** A nightly run against the frozen set catches drift from dependencies you do not control: provider model updates, upstream data changes.
4. **Data changes are changes.** A refreshed index or a new document corpus can regress quality as surely as a model swap. It goes through the same gate.
5. **Match cost to risk.** Eval runs cost money and time. The tiering is the budget: cheap gates often, expensive gates where the risk is.

</details>

---

## Q7. How do you handle a regression in one segment when the total score improves? `[Intermediate]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **The gate fires on the segment.** That is what per segment gating is for. An improving total does not waive a segment loss.
2. **Price the segment loss honestly.** How many users, how costly are their failures, did they choose this system or get assigned it? A small segment with no alternative and high failure cost outranks a large segment's small gain.
3. **Look for the mechanism.** Segment regressions usually have a specific cause: a prompt tuned on majority patterns, a tokenizer edge, a data gap. Find it before deciding.
4. **Ship split if you can.** Route the improved change to segments that gain, hold the old version for the segment that loses. Version routing exists for exactly this.
5. **If you ship anyway, write it down.** The tradeoff, the owner, the fix plan, and the date it gets revisited. Silent acceptance is how a segment stays broken for a year.

</details>

---

## Q8. Scenario: a provider silently updates the model behind your API and your nightly regression drops 4 points. Walk me through your response. `[Scenario]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Confirm and localize.** Re-run to rule out flake, then bucket the drop: which segments, which failure types, which items flipped.
2. **Check whether you can pin or roll back.** If the provider offers version pinning, pin to the previous version while you evaluate. This is why the eval platform tracks model version as part of every score.
3. **Read flipped items with a human.** Decide whether the drop is real quality loss or a style shift your rubric over-penalizes. Both happen; the response differs.
4. **Quantify user impact before escalating.** Four points on which tasks, for which users, at what failure cost? That pricing is what turns a metric event into a business decision.
5. **Fix forward or stay pinned, with a date.** Either adapt prompts and re-gate until the new version clears the bar, or stay pinned and set a deadline for the decision. Then add the flipped items to the regression set and record the incident: silent provider changes are a permanent risk, and your nightly run just proved its value.

</details>
