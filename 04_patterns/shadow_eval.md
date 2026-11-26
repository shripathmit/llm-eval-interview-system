# Shadow Eval: Score the New System on Live Traffic Before Users See It

> The safest production test is the one users never notice.

---

## Problem

Offline evals run on yesterday's data. The moment a new model, prompt, or pipeline version meets live traffic, it meets inputs the test set never contained: new phrasings, new segments, new failure shapes. A full launch finds those on day one, in front of everyone. A cautious launch to a small percentage still exposes real users to an unproven system.

---

## The pattern

Run the candidate system in shadow mode. It receives the same live inputs as the production system and produces outputs that are logged, scored, and compared, but never shown to users. You get production-distribution evidence with zero user exposure, and the launch decision becomes a comparison instead of a bet.

---

## How it works

1. **Mirror the traffic.** Send the candidate the same inputs production gets, at the same time, with the same context. Sampled mirroring is fine if volume forces it; keep the sample random.
2. **Log both outputs.** Store production and candidate outputs side by side with the input, so every comparison is reproducible.
3. **Score both.** Run the same eval stack on both: deterministic checks on everything, judges on samples, humans on disagreements and high-stakes segments.
4. **Compare at the level users feel.** Task success and top-level quality first, diagnostics second. A candidate that wins on style and loses on goal completion loses.
5. **Set the promotion rule in advance.** The candidate ships when it beats or matches production on the gated metrics over an agreed window and volume. Write the rule before the data arrives.
6. **Watch the cost.** Shadow doubles inference spend on mirrored traffic. Budget for it as the price of evidence, and time-box the run.

---

## When to use it

- Model or prompt changes to a system already live, where regression risk is real
- High-stakes segments where even a small exposed beta is not acceptable
- Any launch decision where two camps disagree and live data can settle it

The pattern pairs with beta as ground truth: shadow tells you how the candidate compares on real traffic, and the beta that follows tells you how users respond when the outputs become real.

---

## What shadow cannot tell you

- User behavior change. People respond differently to outputs they can act on; shadow measures output quality, not interaction effects.
- True serving behavior under user load patterns, session state, and multi-turn context built on real answers.
- Long-horizon outcomes. Shadow windows are days to weeks; slow-burning quality problems need the beta and production monitoring that follow.

Treat shadow as the gate before exposure, not a replacement for watching the system after it ships.

---

## Failure mode it prevents

- **Green eval, silent drift**, because the candidate is measured on today's traffic, not a frozen set
- Launch-day surprises in segments the test set never covered
- Rollback scrambles, since a candidate that fails in shadow never needs one
