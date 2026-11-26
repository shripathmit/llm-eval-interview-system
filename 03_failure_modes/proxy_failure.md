# Proxy Failure: The Metric Went Up and the Users Got Unhappier

> A proxy metric is a bet that one number moves with quality. Sometimes the bet loses.

---

## What it is

Proxy failure means the metric you optimize has come loose from the thing users care about. The metric improves, release after release, and user satisfaction, retention, or task success quietly degrades. The eval is not broken. It is measuring something real that stopped mattering.

---

## How it shows up

- Offline scores and user complaints rise at the same time
- The metric improves fastest exactly where users report the most pain
- Teams celebrate eval wins that support and success teams do not recognize
- Qualitative feedback describes a different product than the dashboard does

---

## Why it happens

Proxies are chosen for measurability, not meaning. Accuracy at the wrong level is the classic case: cell-level accuracy in a parser can rise while whole tables stay unusable. In a voice product, the team tracked speech success and NLP success, but treated goal success as the real metric, because a user whose words were heard perfectly and whose goal still failed had a bad product, whatever the lower levels said.

---

## How to detect it

| Check | What it tells you |
|---|---|
| Correlate the metric with task success or satisfaction over time | Whether the proxy still predicts what it stands for |
| Read raw failing outputs behind a rising score | What the number is not seeing |
| Segment users by satisfaction and compare metric scores | Whether happy and unhappy users even differ on the metric |

---

## How to fix it

- Anchor the eval stack to one outcome metric users feel, and demote everything else to diagnostics
- Re-check the proxy against the outcome on a schedule, not once at design time
- When proxy and outcome disagree, investigate the proxy first; it is cheaper to fix and more often wrong
- Keep a small set of raw, unscored user sessions in every review, so the team reads the product, not just its numbers
