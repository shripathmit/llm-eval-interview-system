# Timed Practice Sets: Drill the Bank Like an Interview

> Interviews are timed. Practice should be too. Pick a set, start the clock, answer out loud, then check.

---

## How a Practice Set Works

Every set follows the same rules:

1. **Answer cold.** No notes, no opening the file first. Say the answer out loud, the way you would in the room.
2. **One question, one timer.** When the time for a question ends, move on, even mid-sentence. Interviews do not wait.
3. **Check after, not during.** Open the collapsible answers only when the whole set is done.
4. **Score yourself honestly.** For each question: could you state the mechanism, one trade-off, and one production example? Missing any of the three means the question goes back in the pile.

---

## The 25 Minute Set

Use this on a weekday, or the morning of a phone screen.

| Step | Time | What to do |
|---|---|---|
| Pick | 0 min | Choose one bank file from the table below |
| Q1 to Q3 | 15 min | Answer the first three questions, 5 minutes each, out loud |
| Scenario | 7 min | Answer one scenario question from the same file |
| Review | 3 min | Open the answers, mark the gaps, write one line per gap |

Good first sets:

| Eval type | Bank file | Start with |
|---|---|---|
| No ground truth | [01-no-ground-truth-eval.md](../02_interview_bank/01-no-ground-truth-eval.md) | Q1: setting a bar with no labels |
| Human evaluation | [02-human-evaluation.md](../02_interview_bank/02-human-evaluation.md) | Rubric design and calibration |
| LLM as judge | [03-llm-as-judge.md](../02_interview_bank/03-llm-as-judge.md) | Bias checks |
| Golden sets | [04-golden-set-and-benchmarks.md](../02_interview_bank/04-golden-set-and-benchmarks.md) | Building and versioning the set |

---

## The 60 Minute Set

Use this on a weekend, or the day before an onsite. It simulates a full eval round: fundamentals, depth, system design, and a scenario back to back.

| Step | Time | What to do |
|---|---|---|
| Fundamentals | 15 min | Q1 to Q3 from one bank file, 5 minutes each |
| Depth | 20 min | Two advanced questions from the same file, 10 minutes each; expect follow-ups, so keep answering "why" until you run out |
| System design | 15 min | [18-eval-platform-system-design.md](../02_interview_bank/18-eval-platform-system-design.md): design the eval platform for the system in the prompt |
| Scenario | 10 min | One scenario from [scenarios.md](scenarios.md), stated as a decision, not a description |

Rotate the bank file each session. Across two weeks of 60 minute sets you can cover the core types:

| Session | Bank file |
|---|---|
| 1 | [05-beta-and-field-feedback.md](../02_interview_bank/05-beta-and-field-feedback.md) |
| 2 | [07-retrieval-eval.md](../02_interview_bank/07-retrieval-eval.md) |
| 3 | [09-extraction-eval.md](../02_interview_bank/09-extraction-eval.md) |
| 4 | [11-agent-eval.md](../02_interview_bank/11-agent-eval.md) |
| 5 | [13-regression-and-ci-gating.md](../02_interview_bank/13-regression-and-ci-gating.md) |
| 6 | [15-drift-and-monitoring.md](../02_interview_bank/15-drift-and-monitoring.md) |

---

## Rules That Make Practice Transfer

- **Out loud, always.** Reading an answer feels like knowing it. Saying it shows you whether you do.
- **Numbers ready.** Every answer should carry one number: a bar, a sample size, a cost, a drop threshold. Vague answers fail senior rounds.
- **End with the failure mode.** Close each answer with what breaks first in production. Interviewers probe there anyway; get there first.
- **Log the misses.** Keep a list of questions you could not answer cold. That list is your study plan for the next session.
