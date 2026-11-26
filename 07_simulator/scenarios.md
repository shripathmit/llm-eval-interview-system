# Worked Scenarios: Eval Decisions Under Pressure

> Scenario questions test judgment, not recall. Each scenario below walks the decision the way you should walk it in the room: facts first, then options, then the call, then the follow-through.

---

## Scenario 1: The Score Dropped Two Days Before Launch

**Situation.** Your golden set score was 88% last week. The release candidate just scored 83%. The bar is 85%. Launch is in two days, and the launch date was announced to customers.

**Step 1: Verify the drop is real before you react to it.**

- Re-run the eval on the previous build. If the old build also scores lower than 88% today, your eval moved, not the product. Check for judge model changes, prompt edits, and set changes first.
- Check the sample. Same set, same version, same scoring config? A silent change in any of the three manufactures drops.
- Look at the size of the drop against your noise floor. On a 200 item set, 5 points is about 10 items. That is a signal. On a 40 item set, it might be weather.

**Step 2: Bucket the failures.**

- Split the new failures by category. A drop concentrated in one bucket (one document type, one locale, one failure mode) is a targeted bug. A drop spread evenly is a systemic regression.
- Read five failing items yourself. Automated buckets tell you where; reading tells you whether users will care.

**Step 3: Decide with the bucket, not the average.**

- One narrow bucket, low user impact: ship with the bucket documented, a fix scheduled, and the affected segment monitored or feature-flagged.
- Broad drop, or a bucket that touches correctness on high-risk items: hold. A launch date is a cost. A wrong answer shipped to every user is a bigger one.
- Either way, the decision and the numbers go in writing to whoever owns the launch. Verbal approvals evaporate.

**Step 4: Follow through.**

- The failing items join the regression set the same day, so this exact failure can never pass silently again.
- After launch, re-score on production samples within the first week and compare against the golden set prediction.

**The call in this scenario.** The drop traces to one document type with malformed tables, 9 of the 10 lost items. Hold that document type behind a flag, ship the rest on time, fix the parser path, and unflag after the fix clears the full set. You protected the date and the bar at the same time, by shrinking the launch instead of lowering the standard.

---

## Scenario 2: The Judge Disagrees With Human Raters

**Situation.** Your LLM judge passes 92% of outputs. Human raters, on the same 150 items, pass 78%. The team wants to know which number to report.

**Step 1: Do not average the two numbers. Find where they disagree.**

- Build the disagreement set: items the judge passed and humans failed, and the reverse. The first group is the dangerous one; the judge is approving output your users would reject.
- Read 15 to 20 disagreement items. Classify each: judge missed a factual error, judge rewarded fluent but empty text, humans applied a rubric rule the judge prompt never stated, or humans were inconsistent.

**Step 2: Check the humans before you blame the judge.**

- Compute human to human agreement on the same items. If your raters only agree with each other 80% of the time, the judge at 78% agreement with the majority may be near the ceiling the rubric allows.
- If human agreement is high (kappa above 0.7) and judge agreement is low, the judge is the problem. If both are low, the rubric is the problem, and no judge fixes a rubric two people read differently.

**Step 3: Fix the layer that is actually broken.**

- Rubric rule missing from the judge prompt: add it, with two worked examples from the disagreement set, and re-run.
- Judge rewarding fluency: add a grounding check before the quality score, or require the judge to quote the evidence for each claim it credits.
- Judge model too weak for the domain: move judging to the stronger model for this eval, and keep the cheap judge only for the tiers where it agrees with humans.

**Step 4: Re-validate, then set the reporting rule.**

- Re-run the judge on the same human labeled set. Report judge to human agreement next to every judge score from now on.
- The reporting rule: judge scores are for iteration speed, human scores are for launch decisions, until the judge holds agreement above your threshold for several consecutive runs.

**The call in this scenario.** Most disagreements trace to one unstated rubric rule: answers must not state numbers the source does not contain. The judge prompt never said it. Add the rule plus a grounding pre-check, and judge to human agreement rises into the mid 80s. You report both numbers with the agreement rate attached, and launch decisions stay with humans until the judge proves itself over time.

---

## Scenario 3: A Launch Decision With No Ground Truth

**Situation.** A new document extraction feature is ready. There is no labeled set, no benchmark, and no time to build one before the quarter ends. Leadership asks: is it good enough to ship?

**Step 1: Refuse the framing, politely.**

- "Good enough" has no meaning without a measurement. The honest answer is: nobody knows yet, and here is the cheapest way to know.
- Propose buying ground truth instead of building it: a limited beta whose corrections become the labeled set.

**Step 2: Design the smallest measurement that supports a decision.**

- Pick a small cohort of real users on real work, with the current accuracy stated as unknown, not implied.
- Define the bar before the beta starts: the accuracy level, at the level users consume (cell, row, or table), that makes the feature worth its support cost.
- Instrument correction capture from day one. Every user fix is a label; if you cannot capture corrections, the beta produces opinions, not data.

**Step 3: Run it, then decide on evidence.**

- Score the beta corrections weekly. Bucket the failures. Tune against the biggest bucket.
- Decide at the pre-agreed bar: clear it and expand, miss it and extend the beta or narrow the scope. No renegotiating the bar after the number lands.

**Step 4: Keep the asset.**

- The verified corrections become the golden set. Every future change gets regression tested against the failures your first users actually hit.

**The call in this scenario.** This is the parser beta pattern: at roughly 80% accuracy with no ground truth, a limited beta turned user corrections into labels, tuning lifted accuracy to 86 to 88%, and the launch decision made itself. The alternative, shipping blind at an unknown number, spends user trust to save two weeks.
