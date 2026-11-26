# Risk-Tiered Bars: One Framework, Different Bars Per Use Case

> The right bar for a draft summary is the wrong bar for a safety document. Set both on purpose.

---

## Problem

A single quality bar across every use case fails in both directions. Set it for the highest-stakes case and low-risk use cases never ship, strangled by a standard they do not need. Set it for the average case and the high-stakes case ships at a quality its consequences cannot afford. Teams then negotiate exceptions case by case, which means the bar is really set by whoever argues best.

---

## The pattern

Score every use case on one shared risk framework, and let the framework assign the bar, the eval depth, and the level of automation allowed. One framework, applied consistently, with different numbers coming out the other end. The argument moves from the individual launch to the framework itself, where it belongs.

---

## How it works

1. **Define the risk dimensions.** Cost of a wrong answer, reversibility, who is affected, whether a human reviews the output before it acts, regulatory exposure.
2. **Score each use case on the same dimensions.** The people who own the use case and the people who own the platform score together, so neither side can inflate or deflate alone.
3. **Map tiers to requirements.** Each tier carries a bar, an eval stack, and an automation rule. Example shape: low risk ships at a judge-verified bar with sampling audits; high risk requires human-labeled golden sets, a higher bar, and a human in the loop.
4. **Publish the mapping.** Anyone can look up what their use case must clear before anyone argues about a date.
5. **Review on change.** A use case that gains users, autonomy, or consequences gets re-scored and moves tiers. Movement is normal, not an admission of error.

---

## When to use it

- A platform serving many use cases with different stakes, which is most internal AI platforms
- Any setting where one team's launch standard is blocking another team's safe use case
- Regulated environments, where the framework doubles as audit evidence that standards were applied consistently

In a regulated document platform, two camps fought over exactly this: one side wanted no AI anywhere near the documents, the other wanted AI everywhere. A risk framework built from the one objective both sides shared, do not harm the end user, scored each use case on what level of AI it could carry. Both camps co-authored the framework. The conflict ended because the decision rule was shared, even where the answers differed by use case.

---

## Example tier mapping

| Tier | Bar | Eval required | Automation allowed |
|---|---|---|---|
| Low | Judge-verified threshold | Rules plus judge sampling | Full, with audit samples |
| Medium | Higher threshold, held-out set | Golden set plus judge trends | Full, with human review of failures |
| High | Highest threshold, dip process in place | Human-labeled golden set, shadow run | Assistive only, human decides |

Your numbers will differ. The shape should not: as risk rises, the bar, the evidence, and the human involvement all rise together.

---

## Failure mode it prevents

- **No dip process**, because each tier defines its bar and its response before launch
- Readiness arguments settled by seniority instead of by stated criteria
- Quiet over-automation of high-stakes cases that inherited a low-stakes bar
