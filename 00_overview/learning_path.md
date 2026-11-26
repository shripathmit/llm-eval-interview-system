# Learning Path: A Sequenced Curriculum for LLM Evaluation

> A sequenced curriculum for mastering LLM evaluation - from your first golden set to production drift monitoring.

---

## Three Learning Tracks

Choose your track based on your available time and interview target.

| Track | Time Budget | Recommended For | Where to Start |
|-------|-------------|-----------------|-----------------|
| **Breadth-First** | 1-2 weeks | Phone screens, quick prep, need to know all 18 types at high level | `00_overview/eval_taxonomy.md`, then each file in `02_interview_bank/` Q1-Q3 only |
| **Depth-First** | 4 weeks | Technical interviews, system design rounds, deep expertise on 3-4 types | `01_concepts/` in full, then `02_interview_bank/` 01-04 in depth |
| **Production-First** | 3 weeks | Senior/staff interviews, operations focus, drift and failure modes | `00_overview/eval_design_principles.md`, the `[Advanced]` production questions in each bank file, then `03_failure_modes/` |

---

## Week-by-Week Study Plan (4-Week Depth-First)

### Week 1: Foundations
**Goal:** Understand where scores come from: labels, bars, samples, rubrics.

| Day | Topic | Read | Questions to Answer |
|-----|-------|------|---------------------|
| 1-2 | Ground Truth | `01_concepts/ground_truth.md` full | Where do labels come from when none exist? What makes a label trustworthy? |
| 2-3 | Setting the Bar | `01_concepts/setting_the_bar.md` full | How do you pick a threshold? Who owns the bar, engineering or the business? |
| 4 | Sampling Strategies | `01_concepts/sampling_strategies.md` full | Random vs. stratified sampling? How many samples before a score means anything? |
| 5 | Rubrics | `01_concepts/rubrics.md` full | What makes two people score the same output the same way? |

**Code Exercise:** Take 100 outputs from any LLM app (your own logs, or generate them). Write a 3-point rubric, label all 100 yourself, and write down every case where the rubric was ambiguous. That list is your first rubric revision.

---

### Week 2: Humans and Judges
**Goal:** Master the two scoring engines every eval system runs on.

| Day | Topic | Read | Questions to Answer |
|-----|-------|------|---------------------|
| 1-2 | Human Evaluation | `01_concepts/human_evaluation.md` full | When do you use blind testing? Pairwise or absolute scoring, and why? |
| 2-3 | Annotator Calibration | `01_concepts/annotator_calibration.md` full | How do you measure agreement? What do you do when annotators drift apart? |
| 4 | LLM as Judge | `01_concepts/llm_as_judge.md` full | Single judge or pairwise? When does a judge need a reference answer? |
| 5 | Judge Biases + Practice | `01_concepts/judge_biases.md` full, then Q1-Q5 from `02_interview_bank/02-human-evaluation.md` and `03-llm-as-judge.md` | Name three judge biases and one mitigation for each. |

**Code Exercise:** Build a small LLM judge. Run it on your Week 1 labels and compute agreement. List every disagreement and classify it: judge error, rubric ambiguity, or your label was wrong.

---

### Week 3: Components, Tasks, and the Eval Loop
**Goal:** Evaluate pieces of the system, not just final answers, and run the fix loop.

| Day | Topic | Read | Questions to Answer |
|-----|-------|------|---------------------|
| 1 | Retrieval Evaluation | `01_concepts/retrieval_evaluation.md` full | What does recall at k miss? When is precision the metric that matters? |
| 2 | Generation and Extraction | `01_concepts/generation_evaluation.md`, `01_concepts/extraction_evaluation.md` | How do you detect an ungrounded answer? Why does cell vs. table level change the accuracy number? |
| 3 | Task Success Evaluation | `01_concepts/task_success_evaluation.md` full | Why measure goal success instead of answer quality? What are the levels below it? |
| 4 | Failure Bucketing + Golden Sets | `01_concepts/failure_bucketing.md`, `01_concepts/golden_sets.md` | How do you turn a score into a fix list? Who is allowed to change the golden set? |
| 5 | Practice Q&A | Q1-Q8 from `02_interview_bank/01-no-ground-truth-eval.md` and `05-beta-and-field-feedback.md` | Answer cold, out loud, in under three minutes each. |

**Code Exercise:** Score a set of outputs, bucket every failure by cause, rank the buckets by frequency, fix the biggest one, and re-score. Confirm the total moved and no other bucket got worse.

---

### Week 4: Production Evaluation
**Goal:** Keep the eval honest after launch: regression, drift, agents, safety, cost.

| Day | Topic | Read | Questions to Answer |
|-----|-------|------|---------------------|
| 1 | Offline vs. Online | `01_concepts/offline_vs_online.md` full | What can offline eval never tell you? When is shadow mode enough? |
| 2 | Regression, Dips, Drift | `01_concepts/regression_and_dips.md`, `01_concepts/drift_monitoring.md` | The score drops 4 points overnight. What do you check first, and who decides to roll back? |
| 3 | Agent and Safety Eval | `01_concepts/agent_evaluation.md`, `01_concepts/safety_evaluation.md` | How do you score a trajectory, not just an outcome? What makes a refusal good? |
| 4 | Cost, Statistics, Audit | `01_concepts/eval_cost_and_latency.md`, `01_concepts/eval_statistics.md`, `01_concepts/audit_and_traceability.md` | When is a 2-point gain real? How do you cut eval cost without cutting coverage? |
| 5 | Practice Q&A | Q1-Q8 from `02_interview_bank/13-regression-and-ci-gating.md`, `15-drift-and-monitoring.md`, `18-eval-platform-system-design.md` | Design answers out loud. Draw the platform before you describe it. |

**Code Exercise:** Wire a regression gate. A script scores a golden set, compares against the stored baseline, and fails if the score drops beyond a margin you set. Run it against a deliberately worse prompt and watch it block.
