# 14 - Online Eval, A/B and Shadow

> Offline eval tells you what a change scores. Online eval tells you what it does to real users. You need both, in that order.

---

## 🏗️ The Setup: Components & Signals

### Flow

```
[Change clears offline gate]
Change → Shadow mode: scores live traffic, serves nothing
              │
              ▼
        Staged rollout: small % of users, guardrails watched
              │
              ▼
        A/B read: task success and guardrails, treatment vs control
              │
              ▼
        Ship wide, keep a holdout → Measure long tail effects
```

### Key Components

| Component | Responsibility |
|---|---|
| Shadow Mode | Runs the new version on live inputs and logs its outputs, while users still get the old version |
| Experiment Design | Splits users, picks primary and guardrail metrics, sets duration and sample size |
| Guardrail Metrics | The numbers that stop a rollout: errors, escalations, unsafe rate, cost, latency |
| Holdout | A slice of users kept on the old version after launch, to measure long term effects |
| Rollback Path | The tested switch that returns users to the old version in minutes |

### Signals & Tools

| Category | Example Signals & Tools |
|---|---|
| Primary signals | Task success rate, goal completion, user corrections, retention |
| Guardrail signals | Escalation rate, unsafe output rate, latency, cost per task |
| Tooling | Feature flags, experiment platforms, session tracing |

---

## Q1. How is an A/B test for an LLM feature different from a classic product A/B test? `[Intermediate]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **The output is not deterministic.** The same user can get a great answer and a bad one from the same variant. You are comparing distributions, not experiences.
2. **Quality needs a judge in the loop.** Clicks and conversions do not tell you the answers got better. You need sampled human or judge scoring running inside the experiment, on both arms.
3. **Novelty effects are stronger.** Users poke at new AI behavior, then settle. A three day test measures curiosity, not value.
4. **Contamination is easier.** Users share outputs, switch devices, and hit both arms through different surfaces. Unit of randomization needs thought: user, account, or session.
5. **Cost is a variable, not a constant.** The treatment may cost three times more per task. A winning variant you cannot afford to run is not a winner.

</details>

---

## Q2. What is shadow mode, and what does it buy you that offline eval does not? `[Basic]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **The new version runs on real inputs.** Live traffic, real user phrasing, real data mess. Offline sets are always cleaner than this.
2. **Users see nothing new.** The old version serves. The new version's outputs are logged and scored, so the risk of the measurement is zero.
3. **It catches distribution surprises before users do.** The segment you never sampled, the input shape you never imagined: shadow mode meets them first.
4. **It gives you a paired comparison.** Same input, both versions, scored side by side. That is a cleaner read than any across-cohort comparison.
5. **Its limit is outcomes.** Shadow mode cannot measure what users would have done with the new output. For behavior, you need real exposure. Shadow first, then a small live slice.

</details>

---

## Q3. What are guardrail metrics, and how do you pick them? `[Basic]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Guardrails are the metrics allowed to stop the rollout.** Primary metrics decide if the change is good. Guardrails decide if it is safe to keep learning.
2. **Pick from the ways this change can hurt.** Error and escalation rates, unsafe output rate, latency, cost per task, and the success rate of your most vulnerable segment.
3. **Set thresholds before launch.** Each guardrail gets a line and an owner. Crossing the line pauses the rollout automatically, not after a meeting.
4. **Watch them in near real time.** A guardrail reviewed weekly is a postmortem input, not a guardrail.
5. **Keep the list short.** Five guardrails get watched. Twenty get ignored.

</details>

---

## Q4. What is interleaving, and when does it beat an A/B test? `[Advanced]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Interleaving mixes both versions into one experience.** Classic case: results from two rankers alternate in one list, and clicks attribute credit to each. For LLM outputs, variants alternate across comparable tasks or turns for the same user.
2. **It needs far fewer users.** Each user generates paired comparisons, so signal arrives with a fraction of the traffic an A/B test needs.
3. **It measures preference, not outcomes.** Users picking output A over B tells you which they prefer in the moment, not which completes their task or retains them.
4. **Use it early, for ranking close variants.** Prompt versions, model swaps, retrieval settings: fast preference reads to pick a finalist.
5. **Confirm the finalist with an A/B test.** Preference winners still need an outcome test before they own the traffic.

</details>

---

## Q5. How do you decide sample size and duration for an LLM A/B test? `[Intermediate]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Start from the smallest effect worth shipping.** If a 1 point gain in task success would not change your decision, do not power the test to detect 1 point.
2. **Use your baseline variance.** Task success on human scored samples is noisy. Your offline scoring history tells you the variance; the sample size follows from it.
3. **Score a sample, not every session.** Human and judge scoring on a stratified sample of sessions in each arm usually beats shallow signals on all sessions.
4. **Run at least one full usage cycle.** Weekly products have weekday and weekend users. A test that misses a cycle measures a slice of your population.
5. **Pre-commit the stopping rule.** Fixed horizon or a stated sequential method. Peeking daily and stopping on the first green day manufactures false wins.

</details>

---

## Q6. A/B testing is impossible because the change is safety critical and you cannot expose users to the weaker arm. What replaces it? `[Advanced]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

Some changes you never randomize: a safety fix, a compliance change, a model handling a regulated workflow. The replacement stack:

1. **Offline gate first.** The change clears the regression set, the held-out set, and the red team set. No live exposure until the offline case is strong.
2. **Shadow mode.** Run it on live traffic, serve nothing, compare outputs paired against production. You learn the distribution with zero user risk.
3. **Staged rollout with guardrails.** 1%, then 5%, then 25%, with guardrail thresholds and a tested rollback at each step. Exposure grows only while every guardrail holds.
4. **Pre and post with a holdout.** Keep a small holdout on the old version where that is safe, or compare against matched historical cohorts. Weaker than randomization, so say so in the read.
5. **Heightened monitoring as the price.** The segments and failure types the change touches get human review sampling well above normal rates for the first weeks.

You give up causal cleanliness. You buy safety. State the tradeoff in the launch doc instead of pretending the read is an A/B read.

</details>

---

## Q7. Your A/B test shows task success up 3 points and cost up 40%. How do you make the call? `[Intermediate]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Price the success gain.** What is a completed task worth: support cost avoided, retention, revenue, time saved? Three points of success has a number.
2. **Price the cost honestly.** Cost per task at full traffic, not at test traffic, including judge and infrastructure costs that scale with it.
3. **Check where the gain lives.** If the 3 points concentrate in cheap tasks and the cost concentrates in expensive ones, routing may capture the gain without the bill: send hard tasks to the strong setup, easy tasks to the cheap one.
4. **Check the guardrails before the celebration.** Latency, escalations, vulnerable segments. A win with a guardrail dent is a negotiation, not a launch.
5. **Decide with the tradeoff stated.** "We pay 40% more per task for 3 points of success, worth roughly X per month at current volume." Leaders can sign that sentence. They should not be asked to sign "engagement improved."

</details>

---

## Q8. Scenario: the A/B test is flat on task success, but the treatment arm's human scored quality is clearly higher. Leadership wants to kill the change. What do you do? `[Scenario]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Check whether task success can even see the difference.** If tasks are easy, both arms complete them and quality differences hide under a ceiling. A flat success rate with a quality gap often means the task metric is saturated, not that the change is worthless.
2. **Verify the quality read.** Sample size, blind scoring, annotator agreement. A "clear" quality gap on 40 unblinded sessions is an opinion with a chart.
3. **Look for the outcome quality should move.** Fewer corrections, fewer re-dos, less follow-up contact, higher trust on hard tasks. Measure the hard task slice separately.
4. **Run the deciding slice longer or bigger.** Power a follow-up on the segment where quality differs, with re-dos and corrections as primary metrics.
5. **Make the honest case either way.** If no outcome moves anywhere, quality that users cannot feel is not worth cost and risk, and killing the change is right. If hard tasks show fewer re-dos, you have your ship case with numbers attached.

</details>
