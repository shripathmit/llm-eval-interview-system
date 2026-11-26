"""Lab: Calibrate annotators with agreement and Cohen's kappa.

What this teaches: before you trust a labeled set, you check whether
two raters apply the rubric the same way. Percent agreement is the
naive number. Cohen's kappa corrects it for the agreement you would
get by chance, and the disagreement list tells you what to fix in
the rubric.

How to run: python3 calibrate_annotators.py
"""

from collections import Counter

# Two raters labeled the same 20 outputs against a rubric.
# Labels: good, ok, bad.
ITEMS = [
    {"id": "i01", "rater_a": "good", "rater_b": "good"},
    {"id": "i02", "rater_a": "good", "rater_b": "ok"},
    {"id": "i03", "rater_a": "ok", "rater_b": "ok"},
    {"id": "i04", "rater_a": "bad", "rater_b": "bad"},
    {"id": "i05", "rater_a": "good", "rater_b": "good"},
    {"id": "i06", "rater_a": "ok", "rater_b": "bad"},
    {"id": "i07", "rater_a": "good", "rater_b": "good"},
    {"id": "i08", "rater_a": "ok", "rater_b": "ok"},
    {"id": "i09", "rater_a": "bad", "rater_b": "ok"},
    {"id": "i10", "rater_a": "good", "rater_b": "good"},
    {"id": "i11", "rater_a": "ok", "rater_b": "ok"},
    {"id": "i12", "rater_a": "good", "rater_b": "ok"},
    {"id": "i13", "rater_a": "bad", "rater_b": "bad"},
    {"id": "i14", "rater_a": "good", "rater_b": "good"},
    {"id": "i15", "rater_a": "ok", "rater_b": "ok"},
    {"id": "i16", "rater_a": "good", "rater_b": "good"},
    {"id": "i17", "rater_a": "bad", "rater_b": "bad"},
    {"id": "i18", "rater_a": "ok", "rater_b": "ok"},
    {"id": "i19", "rater_a": "good", "rater_b": "good"},
    {"id": "i20", "rater_a": "ok", "rater_b": "good"},
]


def percent_agreement(items):
    agree = sum(1 for it in items if it["rater_a"] == it["rater_b"])
    return agree / len(items)


def cohens_kappa(items):
    """Kappa from scratch: observed agreement minus chance agreement,
    divided by the room above chance."""
    labels = sorted({it["rater_a"] for it in items} | {it["rater_b"] for it in items})
    n = len(items)
    observed = percent_agreement(items)

    counts_a = Counter(it["rater_a"] for it in items)
    counts_b = Counter(it["rater_b"] for it in items)
    expected = sum((counts_a[l] / n) * (counts_b[l] / n) for l in labels)

    if expected == 1.0:
        return 1.0
    return (observed - expected) / (1 - expected)


def disagreements(items):
    return [it for it in items if it["rater_a"] != it["rater_b"]]


def interpret(kappa):
    if kappa < 0.20:
        return "slight: the rubric is not shared yet, rewrite it before labeling more"
    if kappa < 0.40:
        return "fair: usable for drafts, not for launch decisions"
    if kappa < 0.60:
        return "moderate: find the disagreement pattern and tighten the rubric"
    if kappa < 0.80:
        return "substantial: good enough for most golden sets"
    return "almost perfect: the raters apply the rubric the same way"


def main():
    pa = percent_agreement(ITEMS)
    kappa = cohens_kappa(ITEMS)
    rows = disagreements(ITEMS)

    print(f"Items labeled by both raters: {len(ITEMS)}")
    print(f"Percent agreement:             {pa:.0%}")
    print(f"Cohen's kappa:                 {kappa:.2f} ({interpret(kappa)})")
    print()
    print(f"Disagreements: {len(rows)}")
    for it in rows:
        print(f"  {it['id']}: rater A said {it['rater_a']}, rater B said {it['rater_b']}")
    print()
    print("Work the disagreement list, not the average. Each row is a rubric")
    print("sentence that two people read differently.")


if __name__ == "__main__":
    main()
