# Agent Evaluation: Grade the Trajectory, Not Just the Destination

> An agent can reach the right answer by a reckless path, or fail one step from the goal - agent eval scores the path and the outcome separately.

---

## What Agent Evaluation Measures

A single-turn system produces an output. An agent produces a **trajectory**: a sequence of decisions, tool calls, and intermediate states that ends in an outcome. Eval has to cover three layers:

- **Outcome:** Did the agent complete the task, within its constraints (budget, time, permissions, side effects allowed)?
- **Trajectory:** Were the steps sensible? Right tools, right arguments, no loops, no unnecessary or risky actions on the way?
- **Components:** Per-step accuracy: tool selection, argument extraction, retrieval quality, plan quality.

Outcome-only eval misses agents that succeed by luck or by taking unacceptable risks. Step-only eval misses agents whose steps all look fine and whose result is still wrong. Report both, and know which one gates a launch: the outcome, with trajectory constraints as hard limits (no forbidden actions, no budget blowouts) rather than averages.

---

## Step Level vs Outcome Level

| Question | Step level | Outcome level |
|---|---|---|
| What it catches | Wrong tool, malformed arguments, loops, wasted calls | Task completed or not, whatever the path |
| What it misses | Whether the steps added up to success | Dangerous or lucky paths that happened to land |
| Cost to label | High: a human reads the whole trace | Low: often a programmatic check |
| Best use | Debugging, comparing planners, training signal | Launch bars, regression gates, production monitoring |

A practical rule: gate on outcome, alert on trajectory. If outcome holds but trajectory quality degrades (more steps, more retries, more cost per success), the outcome number will follow it down soon.

---

## Method Catalog: 5 Approaches

### 1. Programmatic Outcome Checks

**Mechanism:** The task defines a verifiable end state: the record exists, the tests pass, the booking is confirmed, the file contains the required sections. A checker script scores it, no judgment involved.

**Pros:** Deterministic, free, runs on every run; the gold standard where it is available
**Cons:** Only works for tasks with checkable end states; agents learn to satisfy the checker rather than the intent
**When to use:** Always, as the first tier, wherever the task allows it

### 2. Tool Call Accuracy Scoring

**Mechanism:** Compare each step against an expected action or a rubric: right tool, right arguments, right order. Score per step and per trajectory.

**Pros:** Precise diagnosis of where agents break; comparable across model versions
**Cons:** Many tasks have several valid paths; strict matching punishes legitimate variation
**When to use:** Fixed-workflow agents (support, data entry, ops runbooks) where the path really is specified

### 3. Trace Review by Humans or Judges

**Mechanism:** A reviewer reads the full trace and rates trajectory quality: efficiency, safety, recovery from errors. LLM judges can pre-screen; humans audit a sample.

**Pros:** Catches the reckless-but-successful paths that outcome checks reward
**Cons:** Trace review is the most expensive labeling there is; judge models struggle with long traces
**When to use:** Safety review before launch, and auditing a sample of production traces on a schedule

### 4. Simulation and Sandbox Eval

**Mechanism:** Run the agent against simulated users, tools, and environments: mocked APIs, scripted counterparties, seeded world state.

**Pros:** Safe to fail; reproducible; can generate rare and adversarial situations on demand
**Cons:** The simulator is a model of the world, and agents exploit its gaps; passing simulation is evidence, not proof
**When to use:** Pre-launch gating, regression suites, dangerous-action testing that production cannot host

### 5. Production Trace Monitoring

**Mechanism:** Score live traces with cheap signals: success events, step counts, retry rates, cost per task, human takeover rate. Sample traces for human review.

**Pros:** Real distribution, real stakes; catches the failures simulation never imagined
**Cons:** Labels are proxies; risky failures may happen before monitoring notices them
**When to use:** Always, once live; the takeover rate is often the single most honest agent metric

---

## Simulation vs Production: What Each Misses

Simulation misses real-world mess: ambiguous users, broken third-party data, tasks nobody scripted. Production misses the counterfactual: you cannot let an unproven agent loose on real users to see what happens, and rare catastrophic paths may not appear in a month of traffic. The standard stack is both: simulation as the gate, production monitoring as the truth, and a sampled trace review connecting them.

Recovery deserves its own line in any agent eval. Most trajectories include a mistake. Score whether the agent notices and recovers, not just whether it errs. An agent with a higher first-step error rate and strong recovery often beats a brittle agent that is perfect until it is lost.
