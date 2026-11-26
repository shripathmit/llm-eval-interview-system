"""Lab: Check an LLM judge for position bias and verbosity bias.

What this teaches: a judge you have not bias-checked is a random
number generator with good grammar. Two cheap checks catch the most
common failures. Swap the order in pairwise mode and see if the
winner flips. Correlate the score with answer length and see if the
judge is grading words instead of content.

The stub judge below stands in for a real model judge. It carries a
small position bonus and a small length bonus on purpose, so the
checks have something to find. Replace stub_judge_score with a call
to your judge and keep the same checks.

How to run: python3 llm_judge_with_bias_checks.py
"""

import math

# Sample answers to one question, with the facts a correct answer needs.
QUESTION = "What does the regression gate do in an eval pipeline?"
REQUIRED_FACTS = ["compares", "baseline", "blocks", "drop"]

CANDIDATES = [
    "It compares current scores to a baseline and blocks the release when a metric drops.",
    "It compares scores against a baseline. If a metric shows a drop beyond the threshold, it blocks the release and reports which metric moved.",
    "It is a gate. It is in the pipeline. It runs after scoring. It has a threshold. It produces a report. It is automated. It compares current scores to a baseline and blocks the release when a metric drops beyond the threshold, and it also writes the result to the dashboard so the team can see the metric history over time.",
    "It compares to a baseline and blocks on a drop.",
    "The gate compares every metric with the stored baseline, blocks the release on a drop, and names the failing metric.",
]


def stub_judge_score(question, answer):
    """Score an answer 0 to 10. Stub: fact coverage plus small bonuses
    for length, the way real judges quietly reward longer answers."""
    text = answer.lower()
    facts_found = sum(1 for fact in REQUIRED_FACTS if fact in text)
    score = facts_found * 2.0
    score += min(len(answer.split()) / 40.0, 1.5)  # verbosity bonus, capped
    return min(score, 10.0)


def judge_pairwise(question, first, second):
    """Return 'first' or 'second'. The stub adds a small bonus to
    whichever answer is presented first, the way real judges do."""
    score_first = stub_judge_score(question, first) + 0.6  # position bonus
    score_second = stub_judge_score(question, second)
    return "first" if score_first >= score_second else "second"


def position_bias_check(question, candidates):
    """Run every pair in both orders. A flip means the order, not the
    content, decided the winner."""
    flips = 0
    total = 0
    for i in range(len(candidates)):
        for j in range(i + 1, len(candidates)):
            a, b = candidates[i], candidates[j]
            winner_ab = judge_pairwise(question, a, b)
            winner_ba = judge_pairwise(question, b, a)
            # In run one, 'first' means a won. In run two, 'first' means b won.
            a_won_first_run = winner_ab == "first"
            a_won_second_run = winner_ba == "second"
            total += 1
            if a_won_first_run != a_won_second_run:
                flips += 1
    return flips, total


def pearson(xs, ys):
    n = len(xs)
    mean_x = sum(xs) / n
    mean_y = sum(ys) / n
    num = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
    den = math.sqrt(sum((x - mean_x) ** 2 for x in xs) * sum((y - mean_y) ** 2 for y in ys))
    return num / den if den else 0.0


def verbosity_bias_check(question, candidates):
    lengths = [len(c.split()) for c in candidates]
    scores = [stub_judge_score(question, c) for c in candidates]
    return pearson(lengths, scores), lengths, scores


def main():
    flips, total = position_bias_check(QUESTION, CANDIDATES)
    print("Position bias check (pairwise, both orders)")
    print(f"  Pairs tested: {total}")
    print(f"  Winner flipped when order swapped: {flips} ({flips / total:.0%})")
    print("  A flip rate above roughly 10% means the judge is reading order,")
    print("  not content. Fix: score both orders and average, or use scoring")
    print("  mode instead of pairwise for this task.")
    print()

    corr, lengths, scores = verbosity_bias_check(QUESTION, CANDIDATES)
    print("Verbosity bias check (score versus answer length)")
    for length, score in zip(lengths, scores):
        print(f"  {length:>3} words -> score {score:.1f}")
    print(f"  Correlation between length and score: {corr:.2f}")
    print("  A strong positive correlation on answers with the same facts")
    print("  means the judge rewards length. Fix: cap the length you show")
    print("  the judge, or add an explicit 'do not reward length' rubric line")
    print("  and re-check.")


if __name__ == "__main__":
    main()
