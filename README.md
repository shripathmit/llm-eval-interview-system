# LLM Evaluation Interview Questions & Answers (2026) - LLM Eval Interview Prep

![Questions](https://img.shields.io/badge/Questions-144-blue)
![Eval Types](https://img.shields.io/badge/Eval%20Types-18-green)
![Concepts](https://img.shields.io/badge/Concepts-23-orange)
![Labs](https://img.shields.io/badge/Python%20Labs-7-purple)

**144 interview questions and answers on LLM evaluation for AI engineers, ML engineers, and GenAI/LLM developers. Covers all 18 eval types, system design scenarios, LLM judges, human evaluation, golden sets, and the production failure modes that come up in real LLM engineering interviews.**

⭐ **Star this repo** if it helps your interview prep - it keeps the project growing.

## 🚀 Start Here

| Link | Use it for |
|---|---|
| 🧾 [Cheatsheet](cheatsheets/metrics_cheatsheet.md) | Every core eval metric compared in one table - best for a phone screen the same day |
| 🗺️ [Learning Path](00_overview/learning_path.md) | Structured curriculum if you have more than a few days to prepare |
| 🧭 [Eval Taxonomy](00_overview/eval_taxonomy.md) | All 18 eval types mapped by ground truth, judge, timing, and what they measure |
| 🧪 [Lab 01: Build a Golden Set](06_labs_py/build_a_golden_set.py) | Turn raw production logs into a labeled set you can score against, no setup beyond Python |

---

## 📂 What Is Inside

### Overview (`00_overview/`)

| File | What it covers |
|---|---|
| [Eval Taxonomy](00_overview/eval_taxonomy.md) | All 18 eval types mapped by ground truth source, who judges, when it runs, and production fit |
| [Learning Path](00_overview/learning_path.md) | A sequenced curriculum, from your first golden set to production drift monitoring |
| [Eval Design Principles](00_overview/eval_design_principles.md) | Five rules that decide whether an eval survives production |

### Concepts (`01_concepts/`)

| File | What it covers |
|---|---|
| [What Eval Is](01_concepts/what_eval_is.md) | Eval as a decision system, not a testing phase |
| [Ground Truth](01_concepts/ground_truth.md) | Where labels come from, and what your scores mean because of it |
| [Setting the Bar](01_concepts/setting_the_bar.md) | The number a version must clear before it ships |
| [Sampling Strategies](01_concepts/sampling_strategies.md) | Choosing the sample that represents traffic you cannot label |
| [Human Evaluation](01_concepts/human_evaluation.md) | The slowest scorer, and still the reference standard |
| [Annotator Calibration](01_concepts/annotator_calibration.md) | Tuning human scorers like a measurement instrument |
| [Rubrics](01_concepts/rubrics.md) | The written standard that turns opinion into a score |
| [LLM as Judge](01_concepts/llm_as_judge.md) | Volume and speed at the price of trust |
| [Judge Biases](01_concepts/judge_biases.md) | Position, verbosity, self-preference, and style bias |
| [Golden Sets](01_concepts/golden_sets.md) | The fixed benchmark every version must face |
| [Failure Bucketing](01_concepts/failure_bucketing.md) | Turning a score into a fix list |
| [Retrieval Evaluation](01_concepts/retrieval_evaluation.md) | Grading the evidence before you grade the answer |
| [Generation Evaluation](01_concepts/generation_evaluation.md) | Right, grounded, and responsive, measured separately |
| [Extraction Evaluation](01_concepts/extraction_evaluation.md) | Cell, row, and table level: the level changes the number |
| [Task Success Evaluation](01_concepts/task_success_evaluation.md) | Grading the outcome the user came for |
| [Agent Evaluation](01_concepts/agent_evaluation.md) | Scoring the trajectory, not just the destination |
| [Offline vs Online](01_concepts/offline_vs_online.md) | Gates before launch, truth after launch |
| [Regression and Dips](01_concepts/regression_and_dips.md) | What happens when the score falls below the bar |
| [Drift Monitoring](01_concepts/drift_monitoring.md) | Catching quality erosion segment by segment |
| [Eval Statistics](01_concepts/eval_statistics.md) | Sample sizes, confidence intervals, and when a gap is real |
| [Eval Cost and Latency](01_concepts/eval_cost_and_latency.md) | Signal per dollar, not scores per run |
| [Safety Evaluation](01_concepts/safety_evaluation.md) | Refusing what it must, helping where it should |
| [Audit and Traceability](01_concepts/audit_and_traceability.md) | Reproducing any score from its data, rubric, and judge versions |

### Interview Bank (`02_interview_bank/`)

One file per eval type. Each file has fundamentals, applied questions, production scenarios, and leadership questions, with difficulty tags and collapsible answers. 144 questions in total.

| # | Eval type | Focus |
|---|---|---|
| 01 | [No-Ground-Truth Eval](02_interview_bank/01-no-ground-truth-eval.md) | Measuring quality when nothing is labeled yet |
| 02 | [Human Evaluation](02_interview_bank/02-human-evaluation.md) | The only judge whose scores define truth |
| 03 | [LLM as Judge](02_interview_bank/03-llm-as-judge.md) | An eval you now have to evaluate |
| 04 | [Golden Sets and Benchmarks](02_interview_bank/04-golden-set-and-benchmarks.md) | What good means, frozen, versioned, and defended |
| 05 | [Beta and Field Feedback](02_interview_bank/05-beta-and-field-feedback.md) | A beta run right is a factory for ground truth |
| 06 | [Rules and Heuristic Eval](02_interview_bank/06-rules-and-heuristic-eval.md) | If a rule can check it, a model should not grade it |
| 07 | [Retrieval Eval](02_interview_bank/07-retrieval-eval.md) | Grade the handoff before you grade the answer |
| 08 | [Generation and Faithfulness Eval](02_interview_bank/08-generation-and-faithfulness-eval.md) | Faithfulness is the floor, not a nice-to-have |
| 09 | [Extraction Eval](02_interview_bank/09-extraction-eval.md) | Cell, row, and table level scores tell three different stories |
| 10 | [Task Success Eval](02_interview_bank/10-task-success-eval.md) | Whether the user got what they came for |
| 11 | [Agent Eval](02_interview_bank/11-agent-eval.md) | Grading the path, the calls, and the outcome, separately |
| 12 | [Safety and Red Team Eval](02_interview_bank/12-safety-and-red-team-eval.md) | What the system does when someone tries to make it fail |
| 13 | [Regression and CI Gating](02_interview_bank/13-regression-and-ci-gating.md) | Proving a change did not break what already worked |
| 14 | [Online Eval, A/B and Shadow](02_interview_bank/14-online-eval-ab-and-shadow.md) | What a change does to real users, not just what it scores |
| 15 | [Drift and Monitoring](02_interview_bank/15-drift-and-monitoring.md) | Scores after launch day, as the world moves |
| 16 | [Multimodal Eval](02_interview_bank/16-multimodal-eval.md) | Grading what the model perceived, extracted, and answered |
| 17 | [Conversational Eval](02_interview_bank/17-conversational-eval.md) | Judging the whole session, not five independent turns |
| 18 | [Eval Platform System Design](02_interview_bank/18-eval-platform-system-design.md) | Eval as a platform serving ten teams, every release |

### Failure Modes (`03_failure_modes/`)

| File | What it covers |
|---|---|
| [Judge Gaming](03_failure_modes/judge_gaming.md) | The model learns the judge, not the task |
| [Benchmark Contamination](03_failure_modes/benchmark_contamination.md) | The test was in the training data |
| [Annotator Drift](03_failure_modes/annotator_drift.md) | Your raters slowly change the rubric |
| [Wrong Level Measurement](03_failure_modes/wrong_level_measurement.md) | A precise answer to a question nobody asked |
| [Teaching to the Test](03_failure_modes/teaching_to_the_test.md) | Optimizing to the eval until the eval lies |
| [Green Eval, Silent Drift](03_failure_modes/green_eval_silent_drift.md) | Passed offline, degraded in production |
| [Unrepresentative Beta](03_failure_modes/unrepresentative_beta.md) | Feedback from the wrong users |
| [Proxy Failure](03_failure_modes/proxy_failure.md) | The metric went up and the users got unhappier |
| [Ceiling Effects](03_failure_modes/ceiling_effects.md) | An eval too easy to tell systems apart |
| [No Dip Process](03_failure_modes/no_dip_process.md) | A bar with nothing behind it |

### Patterns (`04_patterns/`)

| File | What it covers |
|---|---|
| [The Eval Loop](04_patterns/the_eval_loop.md) | Score, bucket, fix the biggest bucket, re-score |
| [Beta as Ground Truth](04_patterns/beta_as_ground_truth.md) | Buy your labels with a limited launch |
| [Tiered Eval](04_patterns/tiered_eval.md) | Cheap checks first, humans last |
| [Risk-Tiered Bars](04_patterns/risk_tiered_bars.md) | One framework, different bars per use case |
| [Shadow Eval](04_patterns/shadow_eval.md) | Score live traffic before users see the change |
| [Golden Set Governance](04_patterns/golden_set_governance.md) | Who can change the ruler, and how |

### Graphs (`05_graphs/`)

| File | What it covers |
|---|---|
| [The Eval Loop](05_graphs/eval_loop.md) | The loop as a diagram: score, bucket, fix, re-score, gate |
| [Eval Platform Architecture](05_graphs/eval_platform_architecture.md) | The platform pieces, and what each one earns |

### Labs (`06_labs_py/`)

Runnable Python, standard library only. Every lab runs as-is on small sample data.

| Lab | What it teaches |
|---|---|
| [Build a Golden Set](06_labs_py/build_a_golden_set.py) | Turn raw production logs into a labeled set |
| [Calibrate Annotators](06_labs_py/calibrate_annotators.py) | Percent agreement and Cohen's kappa from scratch |
| [LLM Judge With Bias Checks](06_labs_py/llm_judge_with_bias_checks.py) | Position bias and verbosity bias checks for a judge |
| [Failure Bucketing](06_labs_py/failure_bucketing.py) | Ranked failure buckets from a scored set |
| [Regression Gate](06_labs_py/regression_gate.py) | A CI gate that fails the build on a score drop |
| [Retrieval Eval Harness](06_labs_py/retrieval_eval_harness.py) | Recall at k and MRR on a miniature corpus |
| [Extraction Accuracy](06_labs_py/extraction_accuracy.py) | Cell, row, and table level scoring side by side |

### Simulator (`07_simulator/`)

| File | What it covers |
|---|---|
| [Timed Practice Sets](07_simulator/practice_sets.md) | Drill the bank like an interview: 25 minute and 60 minute sets |
| [Worked Scenarios](07_simulator/scenarios.md) | Eval decisions under pressure, walked step by step |

### Evaluating the Evals (`08_evaluation/`)

| File | What it covers |
|---|---|
| [Judge to Human Correlation](08_evaluation/judge_human_correlation.md) | Proving the judge tracks people before you trust it |
| [Agreement Metrics](08_evaluation/agreement_metrics.md) | Percent agreement, Cohen's kappa, and Krippendorff's alpha |
| [Eval Coverage Audit](08_evaluation/eval_coverage_audit.md) | What fraction of production failures your eval would have caught |

### Tools (`09_tools/`)

| File | What it covers |
|---|---|
| [Eval Tools](09_tools/eval_tools.md) | Annotation tools, eval frameworks, tracing, and benchmark suites, with what each actually measures |

### Decision System (`10_decision_system/`)

| File | What it covers |
|---|---|
| [Which Eval When](10_decision_system/which_eval_when.md) | Choosing the eval stack from ground truth, risk, budget, and stage |
| [Bar Setting Decision Tree](10_decision_system/bar_setting_decision_tree.md) | Setting a number you can defend in the room |

### Cheatsheets (`cheatsheets/`)

| File | What it covers |
|---|---|
| [Metrics Cheatsheet](cheatsheets/metrics_cheatsheet.md) | Every core metric on one page, with the watch-out column |
| [Judge Prompt Cheatsheet](cheatsheets/judge_prompt_cheatsheet.md) | Judge prompt skeleton, rubric snippet, and bias control checklist |
| [Bar Setting Cheatsheet](cheatsheets/bar_setting_cheatsheet.md) | The bar and the dip process on one page |

---

## 🤝 Contributing

PRs welcome. Add a question, fix an answer, or share a production failure mode. Keep answers plain, practical, and grounded in how evals behave in production, not in theory.
