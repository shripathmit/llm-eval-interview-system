# 18 - Eval Platform System Design

> Every team starts with a spreadsheet and a judge prompt. A platform is what that becomes when eval has to serve ten teams, every release, without breaking.

---

## 🏗️ The Setup: Architecture & Components

### Flow

```
[Production systems]
Traffic → Sampler → Sample store ──────────────┐
                                                ▼
                          Labeling workflow (humans, judges)
                                                │
                                                ▼
                        Scoring engine → Score store (versioned)
                                                │
                                                ▼
              Regression gates ← Baselines   Dashboards → Teams
```

### Key Components

| Component | Responsibility |
|---|---|
| Ingestion and Sampling | Pulls production outputs into the platform, stratified, deduplicated, privacy filtered |
| Labeling Workflow | Queues, rubric delivery, annotator assignment, agreement tracking, adjudication |
| Judge Orchestration | Runs judge models at scale: batching, retries, version pinning, cost tracking |
| Score Store | Every score with its set, rubric, judge, and model versions; nothing overwritten |
| Gates and Dashboards | Regression comparisons, release gates, per team and per segment views |

---

## Q1. Design an LLM evaluation platform for a company with ten product teams. `[Advanced]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

Walk it in layers:

1. **Ingestion.** A sampling service taps production logs from every team: inputs, outputs, context, model and prompt versions, user signals. Stratified sampling by team, segment, and surface, with privacy filtering and retention rules applied at the door.
2. **Storage.** Raw samples in object storage, indexed metadata in a queryable store. Every sample carries its source, timestamp, and version stamps.
3. **Labeling.** A queue service routes samples to human annotators, judges, or rules based on each team's eval config. Rubrics are versioned documents the platform delivers with each task. Agreement tracking and adjudication are built in, not bolted on.
4. **Scoring.** A scoring engine runs eval jobs: full sets, regression sets, ad hoc slices. Judges are orchestrated as batch jobs with pinned versions, retries, and per job cost accounting.
5. **Serving results.** A versioned score store feeds dashboards per team and per segment, a comparison view for any two runs, and a gate API that CI calls to ask: did this change regress?
6. **Governance.** Set and rubric changes go through review in the platform. Baselines are promoted deliberately. Access control respects that samples are production data.

The design principle: eval is a shared pipeline with per team configuration, not ten private spreadsheets with an API.

</details>

---

## Q2. How do you design the sampling and ingestion layer? `[Intermediate]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Sample at the source with config per team.** Rates, segments, and filters differ per product. Central config, distributed collection.
2. **Stratify, do not just randomize.** Guarantee coverage of locales, surfaces, and high cost flows. Pure random sampling starves exactly the segments that fail first.
3. **Filter privacy before storage.** Strip or tokenize personal data at ingestion. An eval platform full of raw user data becomes the company's biggest liability with a dashboard on top.
4. **Deduplicate and cap floods.** A broken client retrying can fill your sample with one user's bad afternoon. Cap per user, per session, per input hash.
5. **Stamp everything.** Model version, prompt version, retrieval index version, timestamp, segment. A sample without its versions cannot be scored meaningfully later.
6. **Keep a raw replay path.** Store enough context to re-run the sample through a new model version. That replay ability is what powers regression and shadow eval.

</details>

---

## Q3. Design the labeling workflow: humans and judges in one system. `[Intermediate]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **One queue, three worker types.** Rules and deterministic checks take the mechanical items. Judges take the judgment items at volume. Humans take the borderline, the new, and the calibration slices.
2. **Routing is config, not code.** Each eval defines what fraction gets double labeled, what goes to humans, and what a judge may decide alone. Teams tune it without platform changes.
3. **Blind by default.** Annotators do not see model versions, other scores, or whether an item is a calibration probe. The platform enforces it.
4. **Agreement is a first class output.** Every queue reports inter annotator agreement and judge versus human agreement continuously. Falling agreement pauses scaling and triggers rubric review.
5. **Adjudication closes disagreements.** A senior annotator resolves split items, and the resolution feeds back into rubric examples. Disagreement is rubric maintenance data.
6. **Calibration probes flow constantly.** Known answer items mixed into every queue. A worker, human or judge, drifting on probes gets flagged before their scores pollute a release decision.

</details>

---

## Q4. How do you orchestrate judges at scale without the bill eating the platform? `[Advanced]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Tier the judging.** Cheap checks first: deterministic rules and small models filter the obvious passes and fails. Expensive judges see only what survives. Most volume never reaches the top tier.
2. **Batch and cache.** Group judge calls into batches, cache by input and rubric hash. Re-scoring an unchanged item with an unchanged rubric should cost zero.
3. **Pin versions and record cost per job.** Every score stores judge model, prompt, and the job's total spend. Cost per eval set is a dashboard, not a surprise invoice.
4. **Budget per team with alerts.** Each team's eval config carries a budget. The platform warns at thresholds and degrades gracefully: smaller samples, cheaper tier, never silent overspend.
5. **Sample humans where they teach the most.** Human budget goes to calibration and borderline items, where one label improves thousands of judge calls. That is the highest leverage spend in the system.

</details>

---

## Q5. What does the score store need to record so scores stay comparable over time? `[Intermediate]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **The full version tuple.** Eval set version, rubric version, judge model and prompt version, system model and prompt version, retrieval index version. A score is meaningless without the tuple that produced it.
2. **Item level scores, not just aggregates.** Aggregates cannot be re-bucketed. Store per item scores with failure bucket labels so any historical run can be re-analyzed.
3. **Baselines as first class objects.** A baseline is a promoted run with an owner and a date. Comparisons always name both runs: candidate versus baseline, never candidate versus a number someone remembers.
4. **Immutability.** Scores are appended, never edited. Corrections are new runs. The moment a score can be quietly fixed, every gate built on scores becomes negotiable.
5. **Retention matched to decisions.** Release decisions get challenged months later. Keep item level data at least as long as the releases it gated are in production.

</details>

---

## Q6. How do regression gates plug into the platform and into CI? `[Intermediate]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **The platform exposes a gate API.** CI sends a candidate identifier: model version, prompt version, config hash. The platform runs or looks up the candidate's scores on the team's regression set.
2. **Comparison is computed by the platform.** Candidate versus the team's promoted baseline, total and per segment, against thresholds the team configured in advance.
3. **Three outcomes, not two.** Pass, block, and warn. Warn covers deltas inside an agreed gray zone and requires a human acknowledgment with a name attached. Binary gates force teams to argue with the tool; three state gates make them decide.
4. **Results land where developers live.** The gate result posts back to the pull request or release ticket with the flipped items linked. A gate that only exists on a dashboard gets routed around.
5. **Every gate decision is logged.** Who shipped, what the delta was, who acknowledged a warn. That log is the audit trail and the input to quarterly gate tuning.

</details>

---

## Q7. How does the platform support safe rollout and rollback of model changes? `[Advanced]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Experiment tracking ties versions to results.** Every model, prompt, and config version registers with its offline scores, its shadow results, and its rollout history in one record. When something breaks, you can see what changed and what it scored before shipping.
2. **Shadow evaluation is a platform job.** A candidate version replays recent production samples before any live exposure, and the platform diffs its outputs and scores against production.
3. **Rollout integrates with feature flags.** The platform supplies the guardrail metrics and thresholds; the flag system executes staged exposure. Guardrail breach triggers automatic halt, and rollback is a flag flip to the previous version, tested regularly, not invented during an incident.
4. **Validation continues after rollout.** Live sampling scores the new version by segment from the first hour. The platform compares against the pre rollout baseline and alerts on the dip process thresholds.
5. **Rollback restores the full version tuple.** Model, prompts, and config roll back together. Rolling back only the model while leaving a prompt written for the new model is a second incident wearing a fix's clothes.

</details>

---

## Q8. Scenario: three teams share your platform. One team's eval volume triples in a quarter, costs spike, and the other teams say their jobs now run slowly. What do you do? `[Scenario]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Find where the volume goes.** Per team, per eval, per tier. Tripling usually concentrates: one team scoring everything with the top tier judge, or a sampling config that quietly went to 100%.
2. **Fix the economics before the capacity.** Push the heavy team down the tiering: deterministic checks and small models first, top tier judge on the survivors. Add caching. Most volume spikes are config problems wearing a scale costume.
3. **Isolate the workloads.** Separate queues and quotas per team, with priority for gate jobs over exploratory jobs. One team's experiment should never delay another team's release gate.
4. **Charge back or budget cap.** Show the team its cost per eval and per release decision. Teams optimize what they can see. A cap with warnings makes the tradeoff theirs to make explicitly.
5. **Scale what is genuinely shared.** Judge orchestration and storage scale horizontally; add capacity there once the waste is out. Scaling before fixing config just rents a bigger version of the same problem.

</details>
