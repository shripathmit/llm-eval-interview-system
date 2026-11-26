# Bar Setting Decision Tree: A Number You Can Defend

> A bar is a promise: below this number, we do not ship. A defensible bar comes from the cost of being wrong, the baseline you are replacing, and the noise in your own measurement, in that order.

---

## The Tree

```
START: What happens when the system is wrong?
|
|-- A wrong answer can cause harm, legal exposure,
|   or a regulatory finding
|       |
|       +--> Bar anchors to the harm case. Set the bar per use
|            case, at the strictest level users consume (often
|            table or record level). Humans keep the launch vote.
|            Typical shape: very high bar, small tolerance, zero
|            tolerance categories named explicitly.
|
|-- A wrong answer costs money or rework, but is reversible
|       |
|       +--> Bar anchors to the economics. The system must beat
|            the current process (human or legacy) by enough to
|            pay for its own error rate. Typical shape: accuracy
|            bar plus a cost per error budget.
|
|-- A wrong answer is an annoyance (drafts, suggestions,
    internal summaries)
        |
        +--> Bar anchors to adoption. If users stop trusting it,
             they stop using it, and the feature dies. Typical
             shape: a quality bar users can feel, plus a usage
             metric watched alongside.
```

After the anchor, two checks apply to every branch:

```
CHECK 1: Does the bar beat the baseline?
    The system replaces something: a human process, a legacy
    tool, doing nothing. The bar must clear that baseline by a
    margin worth the switching cost, or the honest decision is
    not to ship.

CHECK 2: Is the bar outside your measurement noise?
    On a set of n items, a score wobbles. Roughly, the standard
    error of a proportion is sqrt(p x (1 - p) / n). At 200 items
    and 85%, that is about 2.5 points. A bar 1 point above your
    current score is a coin flip, not a standard. Grow the set
    or widen the gap.
```

---

## Setting the Bar, Step by Step

1. **Name the cost of one wrong answer.** In money, time, trust, or harm. If you cannot name it, you are not ready to set the bar.
2. **Measure the baseline.** Score the current process on the same items. Bars set without a baseline are wishes.
3. **Pick the level.** Cell, row, table; per answer or per task completed. The level is the level users consume. See the extraction lab (06_labs_py/extraction_accuracy.py) for how much the level moves the number.
4. **Set the bar above the baseline plus the noise.** Write the set size next to the bar, always: "85% on 400 items" is a standard; "85%" alone is a slogan.
5. **Name the zero tolerance categories.** Some failures fail the release at any score: safety content, fabricated numbers in regulated output, leaked data. List them before the run, not after.
6. **Attach the dip process before you need it.** Who gets paged, what gets checked first, who can hold a release. A bar without a process is a poster. See cheatsheets/bar_setting_cheatsheet.md.

---

## Worked Example

A voice product measured goal success: did the user complete what they came to do. The baseline was the previous system. The team set the bar at 85 out of 100, measured by blind human annotators on sampled real tasks, because below that level users visibly struggled and support contacts climbed. Three levels were tracked (speech, understanding, goal completion) so a dip named its own layer. The bar worked because it was tied to a user-visible effect, measured by people who did not know which system produced the output, and checked on a set large enough that 85 meant something.

---

## Defending the Bar in the Room

- "Why this number?" The cost of error, the baseline, and the noise, in that order. If your answer starts with "industry standard", you do not have a bar, you have a citation.
- "Can we ship 2 points under, just this once?" That is a scope decision, not a bar decision: shrink what ships (one segment, one document type, behind a flag) instead of lowering the number. The bar survives; the launch gets smaller.
- "The competitor ships at a lower bar." Their error costs are not yours, and their users are not your users. Measure your own baseline.
