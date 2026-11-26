# Eval Taxonomy: Classification and Method Mapping

> All 18 eval types mapped by ground truth source, who judges, when it runs, and production fit.

---

## Classification Axes

Every eval setup can be classified along four independent dimensions. Understanding these axes helps you systematically answer "How does X eval work?" and "When do you choose Y over Z?"

**1. Ground Truth Source**
- **Human Labels**: People score outputs against a rubric (human evaluation, golden sets)
- **Field Feedback**: Real users correct, rate, or complete tasks in production (beta eval, online eval)
- **Reference Outputs**: A fixed set of expected answers (benchmarks, regression sets)
- **Synthetic**: A model generates the labels or the test cases (judge-labeled sets, generated benchmarks)
- **None (Reference-Free)**: Scoring uses the input and a rubric only, with no expected answer (no-ground-truth eval, most rubric judges)

**2. Who Judges**
- **Humans**: Most trusted, slowest, most expensive
- **LLM Judge**: Scales to any volume, but carries bias and drift
- **Code**: Deterministic checks - schema, format, exact rules
- **Users**: Implicit signals - completion, retry, abandonment, escalation
- **Hybrid**: Code first, judge second, humans on the disagreements

**3. When It Runs**
- **Offline**: Before release, on a fixed set
- **Launch**: Beta cohorts and gated rollouts
- **Online**: On live traffic, as an A/B test or in shadow mode
- **Continuous**: CI gates on every change, plus production monitoring

**4. What It Measures**
- **Retrieval**: Did the system find the right context?
- **Generation**: Is the answer correct, grounded, and complete?
- **Task**: Did the user get the outcome they came for?
- **Trajectory**: Did the agent take the right steps, not just reach the end?
- **Safety**: Did the system refuse, leak, or comply when it should not have?

Each axis maps to a different set of failure modes and trade-offs. Mastering these axes makes every LLM evaluation interview question answerable.

---

## The Full Taxonomy: All 18 Eval Types

| Eval Type | Ground Truth | Judge | Timing | Measures | Cost Class | Production Maturity |
|---|---|---|---|---|---|---|
| No-Ground-Truth Eval | None at start; built from field feedback | Human spot checks, beta users | Pre-launch, launch | Task quality without labels | Medium | Emerging (2023+) |
| Human Evaluation | Human labels | Trained annotators | Offline, pre-release | Quality, preference, safety | High | Stable (mature) |
| LLM as Judge | Reference answers or rubric | LLM | Offline, CI | Quality at scale | Medium | Emerging (2023+) |
| Golden Set and Benchmarks | Curated labeled set | Deterministic scoring, judges | Offline, CI | Regression, capability | Medium | Stable (mature) |
| Beta and Field Feedback | User corrections and behavior | Users | Launch, production | Real-world task success | Medium | Stable (growing) |
| Rules and Heuristic Eval | Hand-written rules | Code | Offline, CI, production | Format, schema, known errors | Low | Stable (mature) |
| Retrieval Eval | Labeled query-document pairs | Deterministic metrics | Offline | Recall, precision, ranking | Low | Stable (mature) |
| Generation and Faithfulness Eval | Source documents, references | Judges, NLI models, humans | Offline, production sampling | Groundedness, hallucination | Medium | Emerging (2023+) |
| Extraction Eval | Annotated documents | Deterministic field comparison | Offline, CI | Field, row, and table accuracy | Medium | Stable (growing) |
| Task Success Eval | Task outcomes | Humans, judges, product signals | Offline, production | Goal completion | Medium | Emerging (2023+) |
| Agent Eval | Trajectories, task outcomes | Judges, simulators, humans | Offline, shadow | Tool use, trajectory, outcome | High | Cutting-edge (2024+) |
| Safety and Red Team Eval | Attack sets, policy rubrics | Humans, classifier models | Pre-release, continuous | Unsafe output rate, refusal quality | High | Emerging (2023+) |
| Regression and CI Gating | Golden set | Automated scoring | CI, every change | Score movement vs. baseline | Low | Stable (growing) |
| Online Eval: A/B and Shadow | Live user outcomes | Product metrics, judges | Production | Causal impact | Medium | Stable (mature) |
| Drift and Monitoring | Production samples, re-labeled over time | Judges, humans on samples | Continuous | Score decay by segment | Medium | Emerging (2024+) |
| Multimodal Eval | Annotated multimodal sets | Humans, multimodal judges | Offline | Cross-modal correctness | High | Emerging (2024+) |
| Conversational Eval | Conversation transcripts | Judges, humans | Offline, production sampling | Multi-turn coherence, goal completion | Medium | Emerging (2023+) |
| Eval Platform System Design | All of the above | Platform | Always on | Coverage, eval cost, eval latency | High | Emerging (2024+) |

---

## How to Use This Table in an Interview

Name the axes before you name a method. "We have no labels, the judge is a hybrid, it runs at launch, and it measures task success" is a complete eval design in one sentence. Then pick the row that matches, and be ready to defend its cost class and its failure modes.
