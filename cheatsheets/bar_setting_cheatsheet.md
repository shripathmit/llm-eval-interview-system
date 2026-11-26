# Bar Setting Cheatsheet: The Bar and the Dip Process on One Page

> Set the bar from the cost of error, the baseline, and your measurement noise. Then write the dip process before the first dip, because the first dip always arrives two days before a launch.

---

## Setting the Bar in Six Steps

| Step | Action | Output |
|---|---|---|
| 1 | Name the cost of one wrong answer | A number or a harm statement, in writing |
| 2 | Score the current process on the same items | The baseline the bar must beat |
| 3 | Pick the level users consume | Cell, row, table; answer or completed task |
| 4 | Set the bar above baseline plus noise | "85% on 400 items", never "85%" alone |
| 5 | Name the zero tolerance categories | Failures that block at any overall score |
| 6 | Attach the dip process | The section below, agreed before the first run |

Noise reminder: the standard error of a proportion is roughly sqrt(p x (1 - p) / n). At 85% on 200 items, one standard error is about 2.5 points. Bars closer than that to your current score are coin flips.

---

## The Dip Process

When a score lands below the bar:

1. **Freeze.** No launch, no quiet re-runs until the number moves. Re-running until it passes is not debugging; it is shopping for a score.
2. **Verify the measurement.** Re-score the previous build on today's setup. If it also dropped, the eval moved: check judge version, prompt, rubric, and set version, in that order.
3. **Bucket the failures.** One bucket or many? One document type, one segment, one failure mode, or a spread? The shape of the drop decides the response.
4. **Read five failures.** A person, not a dashboard. Decide whether users would care about what broke.
5. **Choose the response:**
   - Narrow bucket, low user impact: ship the rest, flag or exclude the broken slice, fix scheduled.
   - Broad drop or high risk bucket: hold the release. Shrink scope before you ever lower the bar.
   - Eval was wrong, product is fine: fix the eval, document it, and re-run both builds to prove it.
6. **Bank the failures.** Every failing item joins the regression set the same day. A dip you do not bank is a dip you will have again.
7. **Write it down.** The drop, the cause, the decision, and who made it. Future you, mid-incident, will ask what past you was thinking.

---

## Lines That Hold in the Room

- "The bar is not the target. The bar is the floor we promised users."
- "We can shrink the launch or extend the timeline. The number does not move to fit the calendar."
- "Show me the bucket, not the average, and I will tell you if we can ship."
- "A score with no set size next to it is not a measurement."
