# Tiered Eval: Cheap Checks First, Humans Last

> Spend human judgment only where cheaper signals cannot decide.

---

## Problem

Human evaluation is the most trusted signal and the most expensive. Judge models are cheaper and less reliable. Rules are nearly free and narrow. Teams that pick one tier for everything either blow the budget on human review of trivial cases or trust a cheap signal with decisions it cannot make.

---

## The pattern

Stack the tiers so each output climbs only as far as it needs to. Deterministic checks run on everything. Judge models score what passes. Humans review what the judges find uncertain, borderline, or high stakes, plus a random audit sample of everything else.

---

## How it works

1. **Tier 1: deterministic checks.** Schema validity, format, required fields, banned content, numeric ranges. Runs on 100% of outputs, in CI and in production. Failures are facts, not opinions.
2. **Tier 2: automated judges.** Model judges score quality dimensions against a rubric on a large sample. Fast enough to run per release and per day in production.
3. **Tier 3: human judgment.** Reserved for calibration, launch gates, disputed cases, and a standing audit sample. Small volume, highest trust.
4. **Route by uncertainty.** Judge confidence low, judges disagreeing, or the segment flagged high risk: escalate to humans automatically.
5. **Calibrate downward.** Human labels from tier 3 continuously audit tier 2. When judge and human agreement drops, fix the judge or the rubric before trusting any tier 2 number.
6. **Gate at the right tier.** CI blocks on tier 1. Release decisions use tier 2 trends confirmed by tier 3 samples. No single tier decides alone.

---

## When to use it

- Any system with real traffic volume, where full human review is arithmetically impossible
- Production monitoring, where cost per check decides what can run daily
- Regulated or high-stakes outputs, where the human tier must exist but cannot scale

The same shape appears in document pipelines: deterministic rules first, because most checks are expressible as rules, and heavier methods only for what rules cannot catch. In one data quality project, rules expressed about 85% of the checks; the expensive methods earned their place on the remaining 15%.

---

## The cost shape

| Tier | Cost per output | Coverage | Decides |
|---|---|---|---|
| Deterministic checks | Near zero | 100% of outputs | Format and rule failures |
| Automated judges | Low, scales with sample size | Large samples, daily | Quality trends and release comparisons |
| Human judgment | High, minutes per item | Small samples only | Launch gates, calibration, disputes |

If a tier's cost surprises you, the routing is wrong: too much is climbing, or the cheap tiers are not catching what they should.

---

## Failure mode it prevents

- **Judge gaming**, because the human tier audits what the judge tier rewards
- **Annotator drift** going unnoticed, because tier 3 volume stays small enough to calibrate properly
- Eval budgets spent rating outputs a regex could have failed
