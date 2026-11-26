# 15 - Drift and Monitoring

> Launch day is the best your eval scores will ever describe the system. After that, the world moves and the system quietly follows it down.

---

## 🏗️ The Setup: Components & Signals

### Flow

```
[Production traffic]
Live sessions → Sampler (by segment, by locale) → Scored samples
                                                      │
                                                      ▼
                    Trend lines vs baseline: total, segment, bucket
                                                      │
                                                      ▼
                    Alert on breach → Dip process → Fix or roll back
```

### Key Components

| Component | Responsibility |
|---|---|
| Continuous Sampling | Pulls scored samples from live traffic on a fixed cadence, stratified by segment and locale |
| Baseline | The score profile at launch: totals, per segment scores, failure bucket mix |
| Trend Tracking | Watches scores over time, so slow declines show up before they become incidents |
| Alerting | Fires when a segment or metric crosses its line, routed to an owner, not a channel nobody reads |
| Monitoring Budget | The scoring capacity allocated per segment, reviewed like any other budget |

### Signals & Tools

| Category | Example Signals & Tools |
|---|---|
| Quality signals | Task success trend, judge scores on live samples, correction rate |
| Input signals | Input length, language mix, topic mix, new input shapes |
| Tooling | Tracing platforms, dashboards, scheduled eval jobs, alerting systems |

---

## Q1. What is drift in an LLM system, and what are its main sources? `[Basic]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **User drift.** Users change what they ask, how they phrase it, and what they expect. A new user population is a new distribution.
2. **Data drift.** The documents, records, and world facts the system works on change. Retrieval quality decays as content ages or grows.
3. **Provider drift.** The model behind an API gets updated, sometimes silently. Your system changes because someone else's did.
4. **Product drift.** New features route new kinds of traffic into the system. The eval set from launch describes a product that no longer exists.
5. **Adversarial drift.** Users learn the system's edges and start asking at them. Safety and quality both feel this one.

Drift is not a defect. It is the default. Monitoring is the decision to watch it happen on purpose.

</details>

---

## Q2. Why track scores by segment and locale instead of one global number? `[Basic]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

Real case: a voice product in India ran three locales, with a different model behind each: a US base model adapted for Indian English, a pure Hindi model, and a Hinglish model built for dynamic switching.

1. **Averages forgive.** The global number can sit flat while one locale falls apart, as long as the others carry it.
2. **Segments fail for different reasons.** A locale drops because of a data gap in that language. A document type drops because a new template arrived. The fix lives at the segment level, so the measurement must too.
3. **Segments have different bars and different costs.** A failing segment serving a regulated workflow matters more than its traffic share suggests.
4. **Routing hides problems.** When users select a locale or a surface, each path is effectively its own product. Score it like one.
5. **Segment trends are your early warning.** The global number moves last. By the time it drops, the segment has been down for weeks.

</details>

---

## Q3. What does a production monitoring setup actually sample and score? `[Intermediate]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **A fixed random slice of live sessions**, scored on the production rubric by judge or rules, on a daily or weekly cadence. This is your trend line.
2. **Stratified oversamples of risky segments.** New locales, new features, high cost failure areas. Random sampling alone under-covers exactly where drift starts.
3. **User signal streams.** Corrections, re-dos, escalations, thumbs, abandonment. Cheap, continuous, and biased, which is why they sit next to scored samples, not instead of them.
4. **Input distribution stats.** Length, language, topic, and shape of incoming requests. Inputs often drift before outputs do, and input stats cost almost nothing to track.
5. **A small human scored slice.** Judges drift too. A modest human sample, scored blind on the same rubric, is the calibration that keeps the whole setup honest.

</details>

---

## Q4. How do you set alert thresholds for quality monitoring? `[Intermediate]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Measure normal variance first.** Run the monitoring for a few weeks before alerting on it. A threshold inside the normal swing pages the team weekly and gets muted within a month.
2. **Alert on sustained movement, not single points.** Two or three consecutive periods beyond the line, or a trend slope over a window. Quality data is noisy; persistence is the signal.
3. **Set per segment thresholds.** A 3 point drop in a stable segment is an event. The same drop in a volatile new segment is Tuesday.
4. **Tier the response.** A soft breach opens an investigation ticket. A hard breach, or a guardrail metric like unsafe rate, pages an owner and starts the dip process.
5. **Review thresholds quarterly.** As segments stabilize or products change, lines move. A threshold nobody has re-examined in a year is decoration.

</details>

---

## Q5. What is silent degradation, and how do you catch it? `[Advanced]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

Silent degradation: quality falls while every dashboard the team watches stays green. It happens three ways:

1. **The monitored metric stops matching quality.** Users adapt to a worse system, complain less, and correct it themselves. Satisfaction proxies go flat while real quality sinks.
2. **The sample stops matching traffic.** Monitoring samples the traffic shape from launch. New traffic shapes flow past unscored.
3. **The judge degrades with the system.** A judge built on the same model family shares the system's blind spots. As one drifts, the other certifies it.

Catches:

1. **Periodic human audits on fresh traffic.** A blind human scored sample, drawn from today's distribution, compared against the trend line.
2. **Coverage audits.** What fraction of live traffic shapes does monitoring actually touch? Report the number.
3. **Incident backtesting.** Every real failure found by users gets one question: why did monitoring miss it? Each answer closes a hole.

</details>

---

## Q6. How do you budget monitoring across segments? `[Intermediate]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

Scoring costs money, judge calls, and human time. You cannot score everything, so allocate like a budget:

1. **Floor for every segment.** Each segment gets enough sample for a usable trend line. Below the floor you are not monitoring the segment, you are hoping.
2. **Weight by risk.** Failure cost times traffic change rate. Regulated, high cost, or fast changing segments get multiples of the floor.
3. **Weight by ignorance.** New segments get heavy sampling until their behavior is understood, then taper to the floor. Uncertainty is a budget line.
4. **Reserve a surge slice.** A standing allocation for investigating alerts and auditing incidents, so investigations do not cannibalize the trend samples.
5. **Rebalance on a cadence.** Quarterly, move budget from stable, well understood segments to new and drifting ones. A monitoring budget that never moves describes last year's product.

</details>

---

## Q7. How do you tell real drift from a broken monitor? `[Advanced]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Check the monitor's own vitals first.** Sample volumes, scoring completion rates, judge version, pipeline errors. A sampling bug looks exactly like a quality event.
2. **Re-score a frozen reference set.** Keep a fixed set of historical sessions with known scores. If the monitor's scores on the frozen set moved, the monitor changed. If they held, the world changed.
3. **Cross-check with an independent signal.** User corrections, escalations, a human spot sample. Real drift shows up in more than one place.
4. **Localize.** Broken monitors usually break uniformly or absurdly: all segments at once, impossible values. Real drift has a shape: one segment, one failure bucket, a start date.
5. **Only then start the dip process on the product.** Teams that roll back models because a dashboard broke learn to distrust both.

</details>

---

## Q8. Scenario: a locale's goal success slides from 87 to 81 over six weeks. No alert fired, no incident was reported, and users have not complained. Walk me through it. `[Scenario]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Verify the slide.** Re-score samples from the start and end of the window with the same rubric and judge. Confirm the trend is real and not a scoring change.
2. **Localize inside the locale.** Bucket the failures now versus six weeks ago. A slide driven by one growing bucket has a cause you can find: a data gap, a new phrase pattern, a content change.
3. **Check the inputs.** Did the locale's traffic mix change: new user cohort, new task types, a marketing push in a new region? Input drift explains most slow slides.
4. **Fix the alerting failure too.** Six weeks below trend with no alert means thresholds were set on the global number or set too loose. Per segment trend alerts exist for exactly this case. That gap gets fixed in the same pass.
5. **Decide the response by the bar.** The locale is at 81 against a bar of 85. That is a below bar product being served today. Options: targeted fix from the top bucket with a re-score date, added sampling to watch it closely, or scope reduction for the failing task types. What does not happen: nothing, because users have not complained yet. Silence from users is the weakest signal you own.

</details>
