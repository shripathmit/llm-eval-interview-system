# 11 - Agent Eval

> A single-turn score cannot grade a ten-step agent. You grade the path, the calls, and the outcome, separately.

---

## 🏗️ The Setup: Components & Signals

### Flow

```
[Task given to agent]
Task → Trajectory (reasoning, tool calls, observations) → Final state
                                                              │
                                                              ▼
                    Outcome check: goal reached in final state?
                                                              │
                                                              ▼
              Step scoring: each call right tool, right args, right time?
                                                              │
                                                              ▼
                        Failure attribution → Buckets → Bar check
```

### Key Components

| Component | Responsibility |
|---|---|
| Trajectory Capture | Records every step: inputs, tool calls, arguments, results, final state |
| Outcome Checker | Verifies the end state against the goal, ideally with code, not vibes |
| Step Scorer | Grades each tool call: right tool, right arguments, necessary at all |
| Simulator | A controlled environment where the agent can run tasks safely and repeatably |
| Attribution | Assigns each failure to the step where the run actually went wrong |

### Signals & Tools

| Category | Example Signals & Tools |
|---|---|
| Outcome signals | Task completion rate, final state correctness, human task rating |
| Trajectory signals | Tool call accuracy, redundant steps, loops, recovery after errors |
| Environments | Sandboxed APIs, recorded tool responses, digital twin environments |

---

## Q1. What is the difference between trajectory eval and outcome eval for agents? `[Basic]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Outcome eval grades the destination.** Did the agent book the right flight, update the right record, produce the right answer? Final state only.
2. **Trajectory eval grades the path.** Which tools it called, with what arguments, in what order, and whether it recovered when something failed.
3. **Outcome alone hides lucky runs.** An agent that reaches the right state through wrong steps will fail the same task tomorrow with slightly different inputs.
4. **Trajectory alone hides pointlessness.** A clean, efficient path to the wrong outcome is still a failed task.
5. **Score both, report both.** Outcome is the headline. Trajectory is the diagnostic.

</details>

---

## Q2. How do you measure tool call accuracy? `[Intermediate]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

Break it into three separate scores. One blended number hides which skill is missing:

1. **Selection accuracy.** Of all steps where a tool was needed, how often did the agent pick the right one? Include the steps where it should have called a tool and did not, and where it called one it did not need.
2. **Argument accuracy.** Given the right tool, were the arguments right? Score required fields, formats, and values separately. A right tool with a wrong date is a failed call.
3. **Sequencing accuracy.** Were calls made in an order that respects dependencies? Reading a record after updating it is a sequencing failure even if both calls are individually correct.
4. **Score against gold trajectories on fixed tasks.** A curated set of tasks with known correct call sequences gives you a regression set for every model or prompt change.

</details>

---

## Q3. How do you build an eval environment for an agent without letting it damage real systems? `[Intermediate]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Sandbox the tools.** Point the agent at copies of the real APIs with realistic data and no production write access.
2. **Record and replay tool responses.** For a fixed task set, frozen responses make runs repeatable. The same task should test the agent, not the weather in your downstream services.
3. **Reset state between runs.** Every task starts from the same initial state, or scores across runs are not comparable.
4. **Include failure injection.** Make tools return errors, timeouts, and empty results on purpose. Recovery behavior is half of what you are grading.
5. **Keep a path to realism.** Periodically run the same tasks against live-like sandboxes with fresh data. A frozen environment slowly becomes a test the agent has memorized.

</details>

---

## Q4. A multi-step task fails. How do you find the step that caused it? `[Advanced]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Replay the trajectory.** Read the run step by step with the tool results the agent actually saw, not the results it should have seen.
2. **Find the first wrong step.** The earliest step where the action diverged from a correct path. Later errors are usually consequences.
3. **Classify the first wrong step:** wrong tool, wrong arguments, misread observation, bad plan, or a correct step built on an earlier silent error.
4. **Check for silent corruption.** The most dangerous step is one that looks fine and poisons the state: a wrong record fetched and trusted for six more steps.
5. **Bucket across many runs.** One failure is an anecdote. Fifty failures with the same first wrong step is your next fix. Score, bucket, fix the biggest bucket, re-score.

</details>

---

## Q5. How do you verify an agent's outcome when the outcome is not a simple string match? `[Intermediate]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Check state, not text.** If the task was to update a record, query the record. Agent self-reports of success are claims, not evidence.
2. **Write programmatic checkers where you can.** Dates in range, totals that add up, required fields present, no forbidden side effects. Code checkers are cheap, fast, and consistent.
3. **Use a rubric and a judge for the rest.** Quality of a drafted email or a research summary needs judgment. Define the rubric at the level of the deliverable, and validate the judge against human scores on a slice.
4. **Check for side effects separately.** An agent can hit the goal and still send the wrong email on the way. Outcome checkers should include a "did nothing forbidden" pass.
5. **Sample human review on top.** Even with checkers, blind human scoring on a random slice catches the failure class your checkers were never written to see.

</details>

---

## Q6. How do you set a bar for an agent before launch? `[Intermediate]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Set the bar on outcomes, per task risk.** A wrong answer in a draft is cheap. A wrong action in a system of record is not. One bar for both is wrong in both directions.
2. **Add trajectory guardrails.** Even at a passing outcome rate, cap acceptable loops, redundant calls, and cost per task. An agent that succeeds at ten times the budget has not succeeded.
3. **Require recovery performance.** On injected failures, the agent must recover or fail loudly some set fraction of the time. Silent wrong completion is the one outcome you price highest.
4. **Use a per-use-case risk framework.** Score each use case on blast radius and reversibility, and set its bar from that score. Read only research agent: lower bar. Agent that writes to production systems: highest bar, plus human approval on irreversible steps.
5. **Publish the bar before the eval runs.** A bar written after seeing scores is a rationalization, not a bar.

</details>

---

## Q7. Why do agent eval scores drop when you move from your test set to production? `[Advanced]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Test tasks are cleaner than real tasks.** Curated tasks have clear goals and complete information. Real users give agents ambiguous goals and missing inputs.
2. **Frozen tool responses are kinder than live ones.** Real APIs time out, paginate oddly, and return partial data. Agents graded in a quiet room meet a loud world.
3. **Long tail of state.** Production data has the weird record, the duplicate name, the legacy format. Test sets under-sample exactly these.
4. **Distribution of task length.** Your set averages five steps. Production includes the forty step task where per step accuracy compounds against you: 98% per step is 45% over forty steps.
5. **The fix is sampling from production.** Mine real tasks, sanitize them, and rebuild the test set from what users actually ask. Keep the curated set for regression, trust the production set for launch decisions.

</details>

---

## Q8. Scenario: your agent passes 92% of outcome eval, but users report it feels unreliable. How do you reconcile that? `[Scenario]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Believe the users first.** A passing eval with unhappy users means the eval is measuring the wrong thing, not that users are wrong.
2. **Audit the passing runs.** Sample successes and grade the trajectories. You will usually find ugly wins: loops, retries, near misses, and correct answers reached for wrong reasons. Users feel those even when the outcome lands.
3. **Check what your outcome checker misses.** Partial credit counted as pass, side effects uncounted, slow runs counted the same as fast ones. Feelings of unreliability often track latency and visible thrashing.
4. **Compare eval tasks to real tasks.** If the eval set is shorter, cleaner, and friendlier than production work, the 92% is a score about your test set.
5. **Add the missing measures and re-baseline.** Trajectory quality, cost and time per task, and a human rating on real sessions. Report the new, lower, honest number and the plan to raise it.

</details>
