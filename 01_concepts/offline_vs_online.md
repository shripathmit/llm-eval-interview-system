# Offline vs Online Evaluation: Gates Before Launch, Truth After Launch

> Offline eval tells you whether a change is safe to ship; online eval tells you whether it worked - confusing the two is how teams ship regressions with confidence.

---

## The Two Jobs Are Different

**Offline eval** runs before release, on fixed data, under your control. Its job is a gate: is this version at or above the bar, with no regressions on the cases you already know about?

**Online eval** runs after release, on live traffic, in the real distribution. Its job is detection: is the system still performing, for real users, this week?

Each is blind where the other sees:

| | Offline | Online |
|---|---|---|
| Data | Fixed sets: golden, regression, scenario suites | Live traffic, sampled |
| Catches | Known failure modes, regressions on covered cases, unsafe behavior on adversarial sets | Drift, new user behavior, uncovered cases, real-world mess |
| Misses | Anything not in the set; distribution shift; emergent behavior at scale | Rare events in small samples; counterfactuals (what the old version would have done) |
| Speed | Minutes to hours, on demand | Hours to weeks for statistical confidence |
| Labels | Human or judge, built in advance | Proxies first, human rating on samples |
| Decision it owns | Ship or hold | Roll back, investigate, or accept |

---

## What Offline Eval Must Contain

- **The golden set:** Human-labeled, versioned, held out from tuning. The launch bar lives here.
- **The regression set:** Every production failure you have ever fixed, as a permanent test case. It only grows.
- **The adversarial set:** Safety cases, edge cases, malformed input, the inputs your angriest user will find.
- **Slices, not just totals:** Score by segment: locale, document type, user class, task type. Averages hide the segment that is on fire.

Offline eval fails quietly when the sets go stale. A golden set that no longer matches production traffic gives precise scores about a world that no longer exists. Refresh sets from production sampling on a schedule, and version every refresh.

---

## What Online Eval Must Contain

- **Outcome signals on all traffic:** Completion, retry, escalation, abandonment. Cheap, immediate, and the first place a regression shows.
- **Human rating on a rolling sample:** The calibration anchor. Proxies drift; a small weekly human-rated sample tells you whether the proxies still mean what they meant.
- **Segment dashboards:** The same slices as offline. Most production incidents are one segment breaking while the average holds.
- **A comparison story:** Shadow mode (score the new version on live traffic without serving it), canary releases (small traffic share first), or A/B tests where the product allows them. Without some comparison, online numbers describe the world, not your change.

---

## How the Two Connect: The Eval Loop

The loop that ties them together, run continuously:

1. **Score** the current version offline and online.
2. **Bucket the failures** by type and segment.
3. **Fix the biggest bucket** - and add its cases to the regression set before fixing, so the fix is provable.
4. **Re-score** offline: the bucket shrinks, nothing else slipped.
5. **Ship through the gate**, then confirm online that the number does not slip in the real distribution.

The regression set is the memory of this loop. Every online failure that gets fixed becomes an offline test, so the gate gets smarter every cycle. Teams that skip step 3's test-writing fix the same failure twice: once in production, once again six months later.

---

## Common Failure: One Without the Other

**Offline only:** Beautiful gate scores, then production teaches you about the traffic you never sampled. Symptom: "but it passed eval" becomes a team catchphrase.

**Online only:** No gate at all; every release is an experiment on users, and rollbacks replace judgment. Symptom: launch quality depends on how fast someone notices a dashboard.

**Both, unconnected:** Online failures never become offline tests, offline sets never refresh from online data. The two systems age into irrelevance at the same time.
