"""Lab: Bucket failures so you fix the biggest one first.

What this teaches: an average score hides the work. Bucketing splits
failures by cause, ranks the buckets, and turns "accuracy is 78%"
into "most failures are one fixable thing". Score, bucket, fix the
biggest bucket, re-score. That loop is the eval flywheel.

The stub scorer below applies weak rules (format, grounding,
completeness, refusal). Swap in your judge or human labels and keep
the bucketing.

How to run: python3 failure_bucketing.py
"""

from collections import Counter, defaultdict

PASS_BAR = 1.0  # an item passes only if every check passes

# Sample outputs. Each has the source it should stay grounded in and
# the facts a complete answer must carry.
ITEMS = [
    {"id": "e01", "source": "Total due is 1250. Tax is 102.", "required": ["1250", "102"],
     "output": "Answer: The total is 1250 and the tax is 102."},
    {"id": "e02", "source": "Total due is 89. Tax is 7.", "required": ["89", "7"],
     "output": "The total is 89 and the tax is 7."},
    {"id": "e03", "source": "Total due is 430. Tax is 35.", "required": ["430", "35"],
     "output": "Answer: The total is 430."},
    {"id": "e04", "source": "Total due is 512. Tax is 41.", "required": ["512", "41"],
     "output": "Answer: The total is 512 and the tax is 44."},
    {"id": "e05", "source": "Renewal term is 12 months. Cap is 500000.", "required": ["12", "500000"],
     "output": "Answer: The renewal term is 12 months and the cap is 500000."},
    {"id": "e06", "source": "Renewal term is 24 months. Cap is 250000.", "required": ["24", "250000"],
     "output": "I cannot answer that from the given document."},
    {"id": "e07", "source": "Expiry is 2027-06-30. Law is Delaware.", "required": ["2027", "Delaware"],
     "output": "Answer: Expiry is 2027-06-30 and the law is Delaware."},
    {"id": "e08", "source": "Expiry is 2028-01-15. Law is Ohio.", "required": ["2028", "Ohio"],
     "output": "Expiry is 2028-01-15 and the law is Ohio."},
    {"id": "e09", "source": "Total due is 77. Tax is 6.", "required": ["77", "6"],
     "output": "Answer: The total is 77 and the tax is 9."},
    {"id": "e10", "source": "Total due is 910. Tax is 74.", "required": ["910", "74"],
     "output": "Answer: The total is 910."},
    {"id": "e11", "source": "Cap is 100000. Term is 36 months.", "required": ["100000", "36"],
     "output": "Answer: The cap is 100000 and the term is 36 months."},
    {"id": "e12", "source": "Cap is 75000. Term is 6 months.", "required": ["75000", "6"],
     "output": "Answer: The cap is 75000."},
]


def stub_scorer(item):
    """Return (score, failure_category). Checks run in a fixed order;
    the first failed check names the bucket, so buckets stay stable
    across runs and comparable week to week."""
    output = item["output"]

    if output.startswith("I cannot answer"):
        return 0.0, "refusal"

    if not output.startswith("Answer:"):
        return 0.0, "format"

    # Grounding: every required fact in the output must appear in the
    # source. A required fact that is present but altered (a wrong
    # number) shows up as a different token, so check the exact
    # required values against the source text.
    stated = [fact for fact in item["required"] if fact in output]
    for fact in stated:
        if fact not in item["source"]:
            return 0.0, "grounding"

    # Grounding, second form: a number in the output that the source
    # never stated is an invented value.
    source_numbers = {tok.strip(".,") for tok in item["source"].split() if any(c.isdigit() for c in tok)}
    output_numbers = {tok.strip(".,") for tok in output.split() if any(c.isdigit() for c in tok)}
    if output_numbers - source_numbers:
        return 0.0, "grounding"

    if len(stated) < len(item["required"]):
        return 0.0, "completeness"

    return 1.0, "pass"


def bucket_failures(items):
    buckets = defaultdict(list)
    passed = 0
    for item in items:
        score, category = stub_scorer(item)
        if score >= PASS_BAR:
            passed += 1
        else:
            buckets[category].append(item["id"])
    return buckets, passed


def main():
    buckets, passed = bucket_failures(ITEMS)
    total = len(ITEMS)
    failures = total - passed

    print(f"Items: {total}   Passed: {passed}   Failed: {failures}   Score: {passed / total:.0%}")
    print()
    print("Failure buckets, biggest first:")
    ranked = sorted(buckets.items(), key=lambda kv: len(kv[1]), reverse=True)
    for category, ids in ranked:
        share = len(ids) / failures if failures else 0
        print(f"  {category:<14} {len(ids):>2} failures  {share:>4.0%} of all failures   e.g. {ids[0]}")
    print()
    if ranked:
        print(f"Fix '{ranked[0][0]}' first. It is the largest bucket, so one fix")
        print("moves the score more than any other single change. Then re-score")
        print("the same set and confirm the bucket shrank and nothing else grew.")


if __name__ == "__main__":
    main()
