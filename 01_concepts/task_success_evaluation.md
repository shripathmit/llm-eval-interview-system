# Task Success Evaluation: Grade the Outcome the User Came For

> Users do not care that each step scored well if the task failed - measure the levels, but ship or hold on the goal.

---

## What Task Success Evaluation Measures

Unit evals score components: the retriever found the right chunk, the classifier picked the right intent, the reply was fluent. Task success eval scores the whole job: did the user achieve the goal they started with?

Both matter, and they answer different questions. Unit metrics tell you where to fix. Task success tells you whether to ship. A pipeline where every unit scores 95% can still fail one task in three, because task success multiplies across steps and because users do things the unit tests never imagined.

The practical design is a **level stack**: measure each level of the system separately, from raw input handling up to goal completion, and report every level. The top level is the bar. The lower levels are the diagnosis.

---

## The Level Stack

```
Level 3   Goal success       Did the user complete what they came to do?
Level 2   Understanding      Did the system get the meaning right?
Level 1   Input handling     Did the system perceive the input correctly?
```

Rules for reading a level stack:

- **The bar lives at the top.** Launch and regression decisions use goal success.
- **Diagnosis flows down.** When goal success drops, check level 2, then level 1, to find which layer broke.
- **Levels can move in opposite directions.** Better input handling can expose understanding errors that were previously masked by input failures. A level improving while the goal drops is a real pattern, not a bug in your eval.
- **Never average the levels into one score.** The stack is the report.

---

## Method Catalog: 4 Approaches

### 1. Human Goal Rating on Sampled Sessions

**Mechanism:** Sample real sessions. Annotators see the full session and one question: did the user achieve their goal? Blind to system version and model internals.

**Pros:** The most direct read of the thing you care about; blind rating removes version bias
**Cons:** Goals are sometimes ambiguous even to a human reader; session review is slow
**When to use:** The primary bar for launches and major changes; the calibration target for every automated proxy

### 2. Outcome Signals From the Product

**Mechanism:** Use completion events as labels: task finished without retry, no escalation, no reformulated repeat request, purchase or submission completed.

**Pros:** Available on 100% of traffic, in near real time; no annotation cost
**Cons:** Proxies lie at the edges: a user who gives up also stops retrying; silent failures look like completions
**When to use:** Continuous monitoring between human rating rounds; validate the signals against human ratings regularly

### 3. Tasked Beta Cohorts

**Mechanism:** A known cohort of users gets assigned tasks on a schedule. Because the task is known, success is unambiguous, and results are comparable week over week.

**Pros:** Clean labels; controlled difficulty; catches cold-start problems before launch
**Cons:** Assigned tasks are not natural behavior; cohort users learn the system and get unrepresentatively good at it
**When to use:** Pre-launch measurement and cold-start data collection, when natural traffic does not exist yet

### 4. Scenario Suites

**Mechanism:** A fixed set of scripted tasks covering the important goals, run against every version. Score completion per scenario.

**Pros:** Perfectly comparable across versions; covers rare but critical tasks that sampling misses
**Cons:** Scripted tasks drift from real usage; teams learn to pass the suite
**When to use:** Regression gating; pair with sampled human rating so the suite cannot quietly become the product

---

## Worked Example: Three Levels and an 85 Bar

A voice shopping product launching in India was evaluated at three levels, each scored out of 100:

- **Speech success:** Did the system hear the words right?
- **NLP success:** Did it understand the meaning, across three language setups: English with local vocabulary, Hindi, and a code-switched mix of both?
- **Goal success:** Did the user complete the purchase task they started?

The bar was 85, at every level, and anything below 85 was not shippable. Scores came from random sampling scored by human annotators who were blind to which model and locale they were judging, so no setup got graded by its friends.

The stack earned its keep in diagnosis. When goal success dipped for the code-switched setup, the level split showed speech success holding while NLP success fell: the system heard the mixed-language input fine and misunderstood it. That pointed the fix at language understanding, not at the speech layer, and saved weeks of tuning the wrong component. A single end-to-end score would have shown a dip and nothing else.
