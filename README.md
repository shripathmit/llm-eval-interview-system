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

The map before the territory. The taxonomy classifies every eval type along four axes. The learning path sequences the reading. The design principles are the five rules that decide whether an eval system survives production.

### Concepts (`01_concepts/`)

One file per building block: ground truth, setting the bar, sampling, rubrics, human evaluation, annotator calibration, LLM judges, judge biases, golden sets, failure bucketing, retrieval and generation metrics, drift, and eval cost. Read these before the interview bank.

### Interview Bank (`02_interview_bank/`)

One file per eval type, 18 types. Each file has fundamentals, applied questions, production scenarios, and leadership questions, with difficulty tags and collapsible answers.

### Failure Modes (`03_failure_modes/`)

How evals lie: judge gaming, benchmark contamination, annotator drift, measuring at the wrong level, teaching to the test, green evals with silent production drift. Senior interviews live here.

### Patterns (`04_patterns/`)

The reusable designs: the eval loop, beta as ground truth, tiered eval, risk-tiered bars, shadow eval, and golden set governance.

### Labs (`06_labs_py/`)

Runnable Python. Build a golden set from logs, calibrate two annotators, run an LLM judge with bias checks, bucket failures, wire a regression gate into CI.

### Simulator (`07_simulator/`)

Timed practice sets by eval type, plus scenarios: a score dropped, a judge disagrees with humans, a launch decision with no ground truth.

### Evaluating the Evals (`08_evaluation/`)

Meta-evaluation. Judge and human correlation, agreement metrics, and coverage audits: what fraction of production failures would your current eval have caught?

### Tools (`09_tools/`)

Annotation tools, judge and eval frameworks, tracing and observability, and benchmark suites with what each one actually measures.

### Decision System (`10_decision_system/`)

Which eval when: ground truth available or not, risk level, budget, and stage. Plus a decision tree for setting the bar.

---

## 🤝 Contributing

PRs welcome. Add a question, fix an answer, or share a production failure mode. Keep answers plain, practical, and grounded in how evals behave in production, not in theory.
