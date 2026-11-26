# 10 - Task Success Eval

> A unit test tells you the parts work. Task success tells you the user got what they came for.

---

## 🏗️ The Setup: Components & Signals

### Flow

```
[User session]
Session → Task start (goal stated or inferred) → Steps and tool calls
                                                      │
                                                      ▼
                        Outcome check: goal achieved, partial, or failed
                                                      │
                                                      ▼
                        Score by level → Failure buckets → Bar check
```

### Key Components

| Component | Responsibility |
|---|---|
| Goal Definition | States what success means for the task, in the user's terms, before any scoring |
| Level Design | Splits success into levels, from raw perception up to goal completion |
| Blind Scoring | Human or judge scoring where the scorer does not know which system or variant produced the session |
| Cohort | A known group of users doing real tasks, so scores tie back to real usage |
| The Bar | The success rate a release must clear, set from the cost of failure |

### Signals & Tools

| Category | Example Signals & Tools |
|---|---|
| Outcome signals | Task completion, re-dos, escalations, abandonment, time to complete |
| Human scoring | Blind annotator panels, pairwise session comparisons |
| Instrumentation | Session tracing, funnel analytics, task tagging |

---

## Q1. What is task success eval, and how is it different from unit level eval? `[Basic]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Unit eval scores a component.** Did the model transcribe the words right? Did retrieval return the right chunk? Each part gets its own number.
2. **Task success scores the whole job.** The user started with a goal. Either they achieved it or they did not. That is the only score the user experiences.
3. **The two disagree often.** Every component can pass while the task fails, because errors compound across steps and because components are graded on proxies.
4. **You need both, for different decisions.** Unit eval tells you what to fix. Task success tells you whether to ship.
5. **Report task success first.** It is the number leadership and users actually live with.

</details>

---

## Q2. How do you design the levels of a task success eval? `[Intermediate]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

Real case, a voice shopping product in India, scored at three levels:

1. **Speech success rate.** Did the system hear the words right? Measured out of 100 sampled sessions.
2. **NLP success rate.** Did it get the meaning right: the intent, the product, the constraints?
3. **Goal success rate.** Did the user achieve what they came to do? This is the headline number.

Design rules that generalize:

1. **Order levels from perception to outcome.** Each level assumes the one below it. A goal failure with clean lower levels points at planning or flow, not at the model.
2. **Score each level separately.** One blended score hides which layer is broken.
3. **Weight the top level most.** A system at 95 on perception and 60 on goals is a failing product with good hearing.

</details>

---

## Q3. How do you set the bar for task success? `[Intermediate]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Start from the cost of a failed task.** A failed shopping task costs a retry. A failed task in a workflow people depend on costs trust and manual fallback. Higher cost, higher bar.
2. **Anchor to the current baseline.** Measure the existing system or the manual process first. The bar must beat the thing it replaces, by a margin users can feel.
3. **Set one number and publish it.** In the India voice case the bar was 85 out of 100 on goal success. Anything below 85 was not good enough to ship, and everyone knew it before scores arrived.
4. **Set bars per level, not just the top.** A release can clear the goal bar while one level rots. Per level bars catch that early.
5. **Never lower the bar to make a date.** Move the date, narrow the scope, or ship to a smaller cohort. A lowered bar teaches the whole org that bars are negotiable.

</details>

---

## Q4. Why blind testing, and how do you run it? `[Intermediate]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Annotators who know the variant play favorites.** They score the new system generously because they want it to win, or harshly because they liked the old one. Blind scoring removes the label, not the bias source.
2. **Strip identifying information.** Remove system names, timestamps that reveal the variant, and formatting tells.
3. **Randomize order.** Mix sessions from all variants in one queue so no scorer sees a block of one system.
4. **Double-score a slice.** Two annotators on the same sessions, agreement reported. Disagreement means the rubric needs work before the scores mean anything.
5. **Unblind only at analysis.** Scores are locked before anyone learns which system produced which session.

</details>

---

## Q5. How do you design a beta cohort for task success measurement? `[Basic]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Use a known cohort.** You know exactly who the participants are, so every session ties back to a real user with a real context.
2. **Give weekly tasked utterances or tasks.** Assigned tasks guarantee coverage of the flows you need to measure, not just the easy ones users pick on their own.
3. **Mix tasked and free use.** Tasked sessions measure the flows you chose. Free sessions show you the tasks you forgot to include.
4. **Keep the cohort stable across releases.** The same users, the same task set, scored the same way: that is what makes scores comparable over time.
5. **Rotate a slice each cycle.** A permanent cohort learns your system and stops behaving like new users. Fresh members keep the signal honest.

</details>

---

## Q6. A session fails. How do you attribute the failure to a level? `[Advanced]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Walk the session top down from the goal.** The goal failed. Now check each level below it, in order.
2. **Find the first level that broke.** If the words were heard wrong, stop there: it is a perception failure, and everything downstream is a consequence, not a cause.
3. **Bucket by first broken level.** A session gets one bucket: the earliest level that failed. Counting it in three buckets triple-counts one root cause.
4. **Separate system failure from user abandonment.** A user who got a phone call and walked away is not a failed task. Tag sessions where the user left for reasons outside the system.
5. **Rank buckets by frequency times cost.** The biggest bucket is the next fix, same loop as everywhere: score, bucket, fix, re-score.

</details>

---

## Q7. How many sessions do you need to score before a task success number means anything? `[Advanced]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Match the sample to the decision.** A tuning signal needs a few hundred sessions. A ship or no-ship call near the bar needs far more, because the margin matters.
2. **Know your noise band.** At 200 sessions, a score of 85 carries a swing of roughly plus or minus 5 points. If your bar is 85 and your score is 86, you have not cleared anything yet.
3. **Stratify before you scale.** Sample across locales, task types, and user segments first. 1,000 sessions from one segment tell you less than 300 spread across five.
4. **Oversample expensive failures.** Rare tasks with high failure cost deserve sample share above their traffic share.
5. **Freeze the task set for comparisons.** Same tasks, same scoring, every release. Changing the test and the system at once makes both numbers meaningless.

</details>

---

## Q8. Scenario: goal success is 82, the bar is 85, and the launch date is next week. What do you do? `[Scenario]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Do not ship wide and do not move the bar.** Both options spend credibility: one with users, one with your own team.
2. **Bucket the failures first.** If the missing 3 points sit in one fixable bucket, you have a targeted fix and a real timeline. If they are spread thin, you do not.
3. **Narrow the launch.** Ship the task types that clear the bar, hold the ones that do not. A partial launch with honest scope beats a full launch at 82.
4. **Or ship to a limited cohort.** Real users, stated accuracy, corrections captured as data. The cohort grows the sample and the failure list at the same time.
5. **Publish the number and the plan.** "We are at 82, the bar is 85, here is the bucket we are fixing and the date we re-score." Leadership accepts a held launch from a team that shows its work. They stop trusting a team that ships quietly and gets found out.

</details>
