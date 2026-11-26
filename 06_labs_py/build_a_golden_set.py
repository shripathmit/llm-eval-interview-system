"""Lab: Build a golden set from production logs.

What this teaches: a golden set starts as raw production traffic. You
dedupe it, sample it stratified by segment so no segment goes missing,
and export a labeling template that annotators can fill in.

How to run: python3 build_a_golden_set.py
Writes golden_set_template.csv and golden_set_template.json in the
current directory and prints a summary.
"""

import csv
import json
import random
from collections import defaultdict

# Sample production log lines, the way you would pull them from a log
# store. Each line is one interaction, tagged with its segment.
PRODUCTION_LOGS = [
    {"id": "p001", "segment": "invoice", "input": "Extract the total from invoice 1042.", "output": "Total: 1250.00"},
    {"id": "p002", "segment": "invoice", "input": "Extract the total from invoice 1043.", "output": "Total: 89.99"},
    {"id": "p003", "segment": "invoice", "input": "Who is the vendor on invoice 1044?", "output": "Vendor: Acme Supplies"},
    {"id": "p004", "segment": "invoice", "input": "Extract the total from invoice 1042.", "output": "Total: 1250.00"},
    {"id": "p005", "segment": "invoice", "input": "What is the due date on invoice 1045?", "output": "Due date: 2026-02-01"},
    {"id": "p006", "segment": "invoice", "input": "Extract the tax amount from invoice 1046.", "output": "Tax: 102.50"},
    {"id": "p007", "segment": "contract", "input": "What is the renewal term in the Acme contract?", "output": "Renewal: 12 months"},
    {"id": "p008", "segment": "contract", "input": "What is the liability cap in the Beta contract?", "output": "Cap: 500000"},
    {"id": "p009", "segment": "contract", "input": "When does the Gamma contract expire?", "output": "Expiry: 2027-06-30"},
    {"id": "p010", "segment": "contract", "input": "What is the renewal term in the Acme contract?", "output": "Renewal: 12 months"},
    {"id": "p011", "segment": "contract", "input": "Which law governs the Delta contract?", "output": "Governing law: Delaware"},
    {"id": "p012", "segment": "report", "input": "Summarize the Q3 stability report.", "output": "Summary: all batches within limits."},
    {"id": "p013", "segment": "report", "input": "Summarize the Q4 stability report.", "output": "Summary: one batch flagged for review."},
    {"id": "p014", "segment": "report", "input": "List the out-of-spec results in the May report.", "output": "Out of spec: none"},
    {"id": "p015", "segment": "report", "input": "Summarize the Q3 stability report.", "output": "Summary: all batches within limits."},
    {"id": "p016", "segment": "report", "input": "What changed in the June report versus May?", "output": "Change: two new sites added."},
]


def normalize(text):
    """Lowercase and collapse whitespace so near-identical inputs match."""
    return " ".join(text.lower().split())


def dedupe(logs):
    """Drop later lines whose normalized input was already seen."""
    seen = set()
    unique = []
    for line in logs:
        key = normalize(line["input"])
        if key in seen:
            continue
        seen.add(key)
        unique.append(line)
    return unique


def stratified_sample(items, total_n, seed=42):
    """Sample total_n items, allocated across segments by their share.

    Every segment with at least one item gets at least one slot, so a
    small segment is never silently absent from the golden set.
    """
    by_segment = defaultdict(list)
    for item in items:
        by_segment[item["segment"]].append(item)

    rng = random.Random(seed)
    total = len(items)
    sample = []
    for segment, group in sorted(by_segment.items()):
        share = round(total_n * len(group) / total)
        take = max(1, min(share, len(group)))
        sample.extend(rng.sample(group, take))
    return sample


def write_templates(sample, csv_path, json_path):
    """Write the labeling template: item fields plus empty label fields."""
    rows = [
        {
            "id": item["id"],
            "segment": item["segment"],
            "input": item["input"],
            "output": item["output"],
            "label": "",
            "notes": "",
        }
        for item in sample
    ]
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "segment", "input", "output", "label", "notes"])
        writer.writeheader()
        writer.writerows(rows)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2)


def main():
    unique = dedupe(PRODUCTION_LOGS)
    sample = stratified_sample(unique, total_n=9)

    write_templates(sample, "golden_set_template.csv", "golden_set_template.json")

    per_segment = defaultdict(int)
    for item in sample:
        per_segment[item["segment"]] += 1

    print(f"Raw log lines:        {len(PRODUCTION_LOGS)}")
    print(f"After dedupe:         {len(unique)}")
    print(f"Sampled for labeling: {len(sample)}")
    for segment in sorted(per_segment):
        print(f"  {segment}: {per_segment[segment]}")
    print("Wrote golden_set_template.csv and golden_set_template.json")
    print("Next step: annotators fill the label column. That filled file is the golden set.")


if __name__ == "__main__":
    main()
