# Judge Biases: The Ways a Model Grading Models Goes Systematically Wrong

> Judge bias is not random error - it is error with a direction, which means it silently favors some systems over others.

---

## Why Bias Is Worse Than Noise

A noisy judge makes scores jump around, and the jumps are visible. A biased judge makes scores consistently wrong in one direction: longer answers score higher, the judge's own model's outputs score higher, whichever answer appears first scores higher. The eval still looks precise. It is precisely wrong, and it will steer real decisions, usually toward whatever the bias rewards.

Every mitigation below follows the same pattern: name the bias, measure it on a human-labeled slice, then design it out or correct for it. A bias you have not measured is a bias you have.

---

## Bias Catalog: 4 Core Biases

### 1. Position Bias

**Mechanism:** In pairwise judging, the judge favors the answer in one position (commonly the first) independent of quality.

**How it shows up:** Swap the order of the same two answers and the winner changes more often than quality differences can explain.
**Mitigation:** Always judge both orders and count a win only when the same answer wins both, or average the two runs. Report the swap-inconsistency rate as a health metric for the judge itself.
**Residual risk:** Low, if both-orders judging is enforced. This is the easiest bias to kill and the most embarrassing to ship with.

### 2. Verbosity Bias

**Mechanism:** The judge rewards length: longer answers score higher even when the extra text adds nothing, and concise correct answers are punished.

**How it shows up:** Score correlates with token count after controlling for human grades; tuning against the judge makes outputs longer month over month.
**Mitigation:** State the length rule explicitly in the rubric ("length is not a dimension; a complete short answer outranks a padded long one"), include a padded mediocre answer among the few-shot failures, and track score-versus-length correlation as a standing check.
**Residual risk:** Real. The bias is baked into preference data judges were trained on. Rubric language reduces it; measurement catches what remains.

### 3. Self-Preference Bias

**Mechanism:** A judge rates outputs from its own model family higher than equivalent outputs from other models. Style familiarity reads as quality.

**How it shows up:** The judge's win rate for its own family's outputs exceeds the human win rate for the same pairs.
**Mitigation:** Do not let a model judge its own outputs for any decision that matters. Use a judge from a different family, or a panel, and validate on human labels sliced by which system produced the output.
**Residual risk:** Moderate. Cross-family judging helps, but shared training fashions mean biases correlate across judges more than teams expect.

### 4. Style Bias

**Mechanism:** The judge rewards surface form: confident tone, markdown structure, bullet lists, and fluent phrasing, independent of correctness. A wrong answer in a clean format beats a right answer in a rough one.

**How it shows up:** Formatting-only changes move scores; hedged but correct answers ("the source does not specify") score below confident fabrications.
**Mitigation:** Anchor the rubric on consequences, not form ("a material error caps correctness at 2 regardless of presentation"), add few-shot examples where the polished answer is the failure, and for factual tasks prefer reference-based judging, which grades agreement with a source instead of vibes.
**Residual risk:** The deepest of the four, because fluency genuinely correlates with quality in the judge's training data. Reference-based grading is the strongest defense.

---

## The Standing Defense: A Bias Audit Slice

Biases are not fixed once. Judge models get upgraded, prompts get edited, the system under test changes style as it is tuned. Keep a frozen audit slice: a few hundred items with trusted human labels, covering winners and losers from every system you compare. On every judge change, re-run the audit slice and report:

| Check | What it catches |
|---|---|
| Overall agreement with humans | Whether the judge still tracks human judgment at all |
| Agreement sliced by output source | Self-preference |
| Agreement sliced by output length | Verbosity bias |
| Swap inconsistency (pairwise) | Position bias |
| Score on polished-wrong few-shots | Style bias |

If a check regresses, the judge changed, not the system. Roll back the judge change or recalibrate before trusting any score it produced. The eval system needs its own regression discipline, and this slice is it.
