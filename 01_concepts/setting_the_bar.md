# Setting the Bar: The Number a Version Must Clear Before It Ships

> A bar is a promise: below it, the system does not ship, no matter what the calendar says.

---

## What is a Bar?

A bar is the minimum score a system must reach on a defined eval before it goes to users. Not a target to aim at, not an average to hope for: a threshold with a decision attached. Above the bar, ship. Below the bar, fix or hold.

A bar has three parts, and a bar missing any of them is a wish:

1. **The metric:** what is measured, at what level (cell, row, task, session).
2. **The number:** the threshold, stated before the results come in.
3. **The process:** what happens when a version lands below it.

---

## The Bar Is Set by Risk, Not by the Ship Date

The cost of a wrong answer decides the bar. A wrong answer in a low-stakes summary costs a shrug. A wrong value extracted into a regulated report costs an audit finding, or worse.

This is why one org ran a per-use-case risk framework: every use case was scored on how much AI it may carry, derived from one shared objective, do not harm. Low-risk use cases shipped with lighter eval and lower bars. High-risk use cases needed higher bars, human review, and staged rollouts. Same team, same models, different bars, because the risk was different.

```
Risk tier        Bar              Release shape
Low              Moderate         Ship, monitor
Medium           High             Beta first, then ship
High             Highest + human  Staged rollout, human in the loop
                 review
```

The failure mode to avoid: negotiating the bar down in the launch meeting because the date is fixed. When that happens, the bar was never a bar. It was a decoration on a decision already made.

---

## Worked Example: The 85 Bar

A voice product launching in India was evaluated at three levels: speech success, NLP success, and goal success, each measured out of 100 by blind human annotators on sampled interactions. Before launch, the team set the bar: anything below 85 is not good.

The number did three jobs:

- **It ended arguments.** A model variant was not "pretty good" or "probably fine." It was above 85 or below it.
- **It made the launch decision delegable.** Anyone could look at the score and know the call, without escalating.
- **It protected trust.** The bar was set from what users would accept, not from what the current model happened to score. Setting the bar at whatever the model already achieves is grading your own homework.

Note what the bar was not: it was not 100. Perfection was not available at any cost the project could pay. The bar was the level where the product worked for users, stated in advance, and held.

---

## What a Bar Needs Behind It: The Dip Process

Scores dip. A model update, a data change, a new user segment: something will push a live system below its bar eventually. A bar without a dip process is a launch gate that becomes a monitoring chart nobody acts on.

A working dip process answers four questions in advance:

| Question | Example answer |
|---|---|
| How do we notice? | Weekly scored sample from production, tracked by segment |
| Who decides? | The team that owns the bar, named, not "the team" in general |
| What do we check first? | Data drift, then pipeline changes, then model behavior |
| What is the remedy ladder? | Roll back, route to the safer path, hold the next release |

Write the dip process when you set the bar, while everyone is calm. Inventing it during an incident produces either panic rollbacks or quiet acceptance of a worse product.

---

## Common Ways Bars Go Wrong

- **Set after seeing the score.** The bar lands just under the current number. This is not a standard; it is a signature.
- **One bar for everything.** A chat summary and a regulated extraction held to the same threshold means one of them is wrong.
- **Bar with no owner.** Nobody is accountable for the hold decision, so the hold never happens.
- **Bar on the wrong level.** A 95% cell-level extraction score can hide row-level errors that change the meaning of a table. Measure at the level where errors hurt.
