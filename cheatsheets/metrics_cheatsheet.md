# Metrics Cheatsheet: Every Core Metric on One Page

> One table, every metric you will be asked about. The watch-out column is the interview: anyone can define a metric, seniors know where it lies.

---

| Metric | Measures | Good range intuition | Watch out for |
|---|---|---|---|
| Accuracy | Fraction of items exactly right | Task dependent; compare to the baseline, never to 100% in the abstract | Hides class imbalance; 95% accuracy can mean 0% on the rare class that matters |
| Precision | Of what the system flagged or produced, how much was right | High when false alarms are expensive | Easy to raise by doing less; pair it with recall |
| Recall | Of what should have been found, how much was found | High when misses are expensive | Easy to raise by flagging everything; pair it with precision |
| F1 | Harmonic mean of precision and recall | Use when both error types cost roughly the same | Averages hide which side is failing; report the pair alongside |
| Percent agreement | How often two raters give the same label | Above 80% feels good; meaning depends on label balance | Inflates with skewed labels; never report it alone for launch grade labels |
| Cohen's kappa | Agreement corrected for chance, two raters | 0.6 to 0.8 is substantial; above 0.8 is rare on subjective tasks | Drops when labels are skewed even if raters behave identically; read it with percent agreement |
| Krippendorff's alpha | Agreement for any rater count, missing data, ordinal scales | Same bands as kappa; 0.67 is a common tentative floor | Harder to compute and explain; worth it for pooled annotation |
| Spearman correlation | Whether two scorers rank items the same way | 0.8 plus means a judge ranks like your humans | Says nothing about absolute scores; a judge can rank perfectly and grade generously |
| Recall at k | Whether the relevant docs appear in the top k retrieved | Depends on k and corpus; track the trend per change | Only as good as your relevance labels; unlabeled relevant docs count as misses |
| Precision at k | How much of the top k is relevant | Higher matters when the generator drowns in context | Conflicts with recall at k; report both, at the k your system actually uses |
| MRR | How high the first relevant doc ranks | Closer to 1 means the good doc is near the top | Ignores everything after the first hit; wrong metric for multi-doc answers |
| nDCG | Ranking quality with graded relevance | Use when relevance has degrees, not just yes or no | Needs graded labels, which cost more to produce |
| Faithfulness / groundedness | Whether every claim in the answer is supported by the source | As high as you can measure honestly; zero tolerance categories sit here | Usually judge scored, so it inherits judge bias; validate the judge first |
| Pass at k | Whether any of k sampled generations passes the tests | Standard for code; report k and temperature with it | Rewards sampling luck; pass at 1 is the honest production number |
| Refusal rate | How often the system declines to answer | Healthy systems refuse the unanswerable and nothing else | Both directions fail: refusing answerable questions is a completeness bug |
| False pass rate | Items the judge or gate passed that humans fail | The metric to watch on any automated gate; keep it near zero | Averages hide it inside overall agreement; always slice it out |
| BLEU / ROUGE | N-gram overlap with a reference text | Legacy metrics; useful for rough regression on fixed tasks | Overlap is not correctness; a fluent wrong answer can outscore a terse right one |
| Latency (p50 / p95) | How long eval or the system takes, typical and tail | Eval latency decides what can run in CI versus nightly | Averages hide the tail; report p95 next to every quality number |
| Cost per eval run | What one full scoring pass costs in labels and judge calls | Must fit the cadence: a run you cannot afford weekly will not happen weekly | Cheap tiers first; spend human labels only where they change decisions |

---

## The Three Pairings to Memorize

- **Precision with recall.** Quoting one without the other is a choice about what to hide.
- **Agreement with the ceiling.** Judge to human agreement means nothing until you place human to human agreement next to it.
- **Quality with cost and latency.** A score that takes a week and a budget to produce will be produced twice, then never again.
