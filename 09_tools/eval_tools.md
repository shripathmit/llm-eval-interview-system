# Eval Tools: What Exists and What to Watch

> Tools do not give you an eval strategy. They make a strategy cheaper to run. Pick the strategy first (see 10_decision_system), then pick tools that fit it.

---

## Annotation

Where human labels get made. The tool matters less than the workflow it supports: rubric display, calibration rounds, disagreement review.

| Tool | What it does | Watch out for |
|---|---|---|
| Label Studio | Open source labeling for text, audio, images; custom interfaces, multi-rater workflows | You own hosting and user management; rubric versioning is a process you build, not a feature you get |
| Argilla | Labeling and feedback collection aimed at LLM workflows; good for curating datasets from production logs | Smaller ecosystem; check its export formats against your pipeline before committing |
| Prodigy | Scriptable, active learning driven labeling; the model picks the most useful items to label next | Single annotator heritage; multi-rater calibration workflows take extra setup |

---

## Eval Frameworks

Where scoring runs: judges, metrics, and test harnesses.

| Tool | What it does | Watch out for |
|---|---|---|
| Ragas | RAG focused metrics: faithfulness, answer relevance, context precision and recall, mostly judge based | Judge based scores inherit judge bias; validate against humans before quoting them |
| DeepEval | Pytest style eval for LLM apps; many built-in metrics, red teaming module | Metric count is not metric quality; pick the few that map to your failure buckets |
| promptfoo | Prompt and model comparison, assertions, CI friendly; good for regression across prompt versions | Assertion heavy tests catch format, not judgment; pair it with a judged or human layer |
| OpenAI Evals | Framework and registry for running evals against models, with templates for common tasks | Templates grade generic tasks; your production failures still need custom graders |
| TruLens | Instrumentation and feedback functions for LLM apps, with dashboards over runs | Feedback functions are judges under the hood; same calibration duties apply |

---

## Tracing and Observability

Where production behavior becomes eval material: sampled traffic, traces, and user feedback in one place.

| Tool | What it does | Watch out for |
|---|---|---|
| LangSmith | Tracing, datasets, and eval runs for LLM apps; strong debugging view of single traces | Cost grows with trace volume; sample deliberately instead of tracing everything forever |
| Braintrust | Eval scoring, logging, and experiment comparison aimed at product teams | Works best when the team commits to its dataset model; half adoption gives half the value |
| Arize Phoenix | Open source tracing and eval notebooks, OpenTelemetry based; good for local and self-hosted setups | Notebook driven analysis is powerful and easy to leave unshared; publish results back to the team |
| Langfuse | Open source LLM observability: traces, scores, prompt management, self-hostable | Self-hosting means you own upgrades and storage; budget the maintenance, not just the install |

---

## Benchmark Suites

Public benchmarks measure public tasks. They rank models; they do not grade your product.

| Benchmark | What it actually measures | Watch out for |
|---|---|---|
| MMLU | Multiple choice knowledge and reasoning across 57 subjects, from elementary to professional level | Saturated at the frontier and present in training data; a high score says little about your use case |
| HumanEval | Function level code generation from docstrings, scored by unit tests (pass at k) | 164 hand written problems; measures short self-contained coding, not repo level work |
| SWE-bench | Resolving real GitHub issues in real repositories, scored by the project's own tests | The honest one of the three for engineering agents, and the hardest to run cleanly; environment setup dominates the work |

The rule for all three: use benchmarks to shortlist models, then decide on your own golden set. A model that wins MMLU and fails your extraction set loses, every time, for your product.
