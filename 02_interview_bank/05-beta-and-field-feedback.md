# 05 - Beta and Field Feedback

> A beta is not a soft launch. Run it right and it is a factory for ground truth.

---

## 🏗️ The Setup: Components & Signals

### Flow

```
[Known cohort, honest accuracy stated]
Users → Real work + assigned tasks → Corrections captured with original output
                                                    │
                                                    ▼
                              Expert verification → Promote to golden / regression set
                                                    │
                                                    ▼
                              Users see what their feedback fixed → Loop repeats
```

### Key Components

| Component | Responsibility |
|---|---|
| Cohort | Known users doing real work, who know it is a beta and know the current accuracy |
| Tasking | Assigned tasks that force coverage of segments real usage would miss |
| Instrumentation | Every correction, rejection, and re-do captured with the original output attached |
| Verification | Expert review that separates true corrections from preference and noise |
| Promotion | Verified feedback becomes the tuning set now and the regression set later |
| Loop Closure | Users hear what their feedback fixed; that is what keeps the feedback coming |

### Signals & Tools

| Category | Example Signals & Tools |
|---|---|
| Feedback volume | Corrections per user per week, silent-user rate |
| Quality | Percentage of corrections that survive verification |
| Coverage | Segments and task types exercised versus the launch checklist |
| Tracing | LangSmith, Braintrust, in-house feedback queues |

---

## Q1. Why run a beta as an evaluation tool instead of launching and watching the metrics? `[Basic]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Launch metrics tell you usage, not correctness.** Users can adopt a system that is quietly wrong.
2. **A beta produces corrections on real work,** from known users you can follow up with. That is ground truth forming in front of you.
3. **The blast radius is small** while the accuracy number is still low and still moving.
4. **Feedback quality is higher** when users know it is a beta and know the honest current accuracy. They correct like collaborators instead of complaining like customers.
5. **You get a failure list, not just a score.** The buckets from beta failures become the tuning plan.

</details>

---

## Q2. How do you pick a beta cohort? `[Basic]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Real users with real work** in the segments you plan to launch. Synthetic users produce synthetic feedback.
2. **Cover the segments that behave differently:** locales, document types, experience levels. A cohort from one segment validates one segment.
3. **Small enough to support, large enough for signal.** You should be able to name the users and read everything they send.
4. **Known identities.** Feedback tied to a user and a task can be followed up, verified, and measured week over week.
5. **Beware the friendly cohort.** Only power users and internal fans will tell you the system is ready months before it is.

Real case: a voice product beta ran with a cohort the team knew exactly, down to customer IDs. Because every utterance tied back to a real user, the same measurements could be repeated weekly and trusted.

</details>

---

## Q3. Raw user feedback is messy. How do you turn it into ground truth? `[Intermediate]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Capture the original output with every correction.** A correction without the thing it corrected is an anecdote.
2. **Separate correctness from preference.** "This extraction is wrong" is a label. "I like shorter answers" is a product signal. They go to different places.
3. **Verify before you promote.** Experts review corrections, all of them in high-stakes domains, a sample elsewhere. Users are sometimes wrong with great confidence.
4. **Label the failure type at capture time,** while the user still remembers what they were trying to do.
5. **Promote only verified corrections into sets.** Real case: a document parser beta turned verified user corrections into the tuning set that took table recognition from 80% to 86-88%, and the same set became the regression set afterward.

</details>

---

## Q4. What are tasked utterances, and when do you assign tasks to beta users? `[Intermediate]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **The gap:** beta users only do their own work, so whole segments and edge cases get no traffic and no feedback.
2. **Tasking fills the gap.** Users get assigned exercises: specific utterances, documents, or workflows to run each week.
3. **It buys controlled coverage.** The same tasked items, repeated weekly, produce comparable measurements over time.
4. **Real case:** a voice product in India gave its known beta cohort weekly homework of tasked utterances. Speech, NLP, and goal success could then be measured the same way every week, against an 85 bar, instead of waiting for organic traffic to cover the cases.
5. **Tasking supplements real usage; it never replaces it.** Tasked data is cleaner and less natural. Report the two separately.

</details>

---

## Q5. Your beta users are not your real users. How do you handle the bias? `[Intermediate]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Name the skew out loud:** early adopters, experts, one region, one company, unusually patient people. An unnamed bias gets quoted as a result.
2. **Stratify everything by segment.** Report scores per segment, so the segment the beta cannot see is visibly absent rather than silently averaged in.
3. **Never quote a beta score as a production score.** The beta buys ground truth, failure buckets, and a tuning set. It does not buy a launch guarantee.
4. **Widen in stages and re-measure at each stage.** Each wider ring is a new measurement, not a formality.
5. **Keep a skeptic on the team** whose job is to say which launch risks the beta structurally cannot answer.

</details>

---

## Q6. How do you keep beta users giving high-quality feedback for months? `[Advanced]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Be honest about the number.** Tell users the current accuracy and what is improving. In the parser beta, users stayed engaged for months because the number was honest and visibly moving.
2. **Close the loop visibly.** "Your correction fixed this failure type" is the payment users actually value.
3. **Keep the ask small and structured.** One-tap corrections and short tasked exercises beat open-ended surveys.
4. **Rotate the tasked work** so the same users are not drilled on the same cases until they memorize them.
5. **Retire silent or gaming users.** Dead weight in the cohort dilutes the set and flatters the scores.

</details>

---

## Q7. When does a beta end, and what happens to its data? `[Advanced]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **End it on evidence:** the release bar is met on verified data, or the failure list has stopped changing for several cycles.
2. **Promote before you close.** The verified correction set becomes the regression set first, while the people who built it are still around to explain it.
3. **Archive the raw feedback with cohort metadata.** Future teams need to know exactly who produced this data and how they were skewed.
4. **Publish the final beta report:** starting score, ending score, top failure buckets, and what remains open. No quiet endings.
5. **The beta ends; the set it built should outlive it.** In the parser case, the beta's ground truth kept guarding every release long after the beta cohort went back to their day jobs.

</details>

---

## Q8. Scenario: you are launching a voice feature for a mixed-language market, and no training or evaluation data exists for how people actually speak. How do you get the data without delaying the launch? `[Advanced]` `[Scenario]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

This is a real case, solved with beta launch parties:

1. **Recruit a known cohort** of real users in the market, with consent to record and measure.
2. **Put test devices in front of them in real settings.** Invite people, hand them a device, let them play with it on tasks they care about. Natural mixed-language speech only shows up when people stop performing for a lab.
3. **Collect the data in the open.** The team went to where the users were, in person, repeatedly, instead of waiting for data to arrive.
4. **Fill coverage gaps with tasked exercises** between events, assigned weekly, so rare cases get exercised on schedule.
5. **Measure from day one:** speech success, NLP success, and goal success, scored by blind human annotators against an 85 bar.
6. **Run collection in parallel with the launch decision.** The experiment and the data pipeline moved together, so solving the data gap never became the reason the launch slipped.

</details>

---
