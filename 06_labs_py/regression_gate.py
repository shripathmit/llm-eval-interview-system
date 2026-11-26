"""Lab: A regression gate you can drop into CI.

What this teaches: an eval score that nobody gates on is a report,
not a control. The gate compares current metrics to a stored
baseline and fails the build when any metric drops more than the
allowed threshold. Small drops are noise; drops past the threshold
stop the release until a human looks.

How to run:
  Demo with sample data:  python3 regression_gate.py
  Real CI use:            python3 regression_gate.py --baseline baseline.json --current current.json --threshold 0.02

Both JSON files are flat objects: {"metric_name": score, ...}.
Exit code is 0 when the gate passes, 1 when it blocks.
"""

import argparse
import json
import sys

DEFAULT_THRESHOLD = 0.02

# Sample run results, as an eval job would emit them.
SAMPLE_BASELINE = {"accuracy": 0.86, "groundedness": 0.92, "format_valid": 0.99}
SAMPLE_CURRENT = {"accuracy": 0.85, "groundedness": 0.88, "format_valid": 0.99}


def compare(baseline, current, threshold):
    """Return a list of (metric, baseline, current, drop) for every
    metric that dropped more than the threshold."""
    failures = []
    for metric, base_value in baseline.items():
        if metric not in current:
            failures.append((metric, base_value, None, None))
            continue
        drop = base_value - current[metric]
        if drop > threshold:
            failures.append((metric, base_value, current[metric], drop))
    return failures


def report(baseline, current, failures, threshold):
    print(f"{'Metric':<16} {'Baseline':>9} {'Current':>9} {'Drop':>7}")
    failed_names = {f[0] for f in failures}
    for metric, base_value in baseline.items():
        cur = current.get(metric)
        cur_text = f"{cur:.2f}" if cur is not None else "missing"
        drop = base_value - cur if cur is not None else 0.0
        mark = "  BLOCK" if metric in failed_names else ""
        print(f"{metric:<16} {base_value:>9.2f} {cur_text:>9} {drop:>7.2f}{mark}")
    print()
    if failures:
        print(f"Gate: BLOCKED. {len(failures)} metric(s) dropped more than {threshold:.2f}.")
        print("A human reviews the failing items before this ships. The gate")
        print("does not argue; it stops the line and shows the numbers.")
    else:
        print(f"Gate: PASSED. No metric dropped more than {threshold:.2f}.")


def run_gate(baseline, current, threshold):
    failures = compare(baseline, current, threshold)
    report(baseline, current, failures, threshold)
    return 1 if failures else 0


def demo():
    print("Demo mode: sample baseline versus sample current run.")
    print("(In CI, pass --baseline and --current JSON files instead.)")
    print()
    code = run_gate(SAMPLE_BASELINE, SAMPLE_CURRENT, DEFAULT_THRESHOLD)
    print()
    print(f"The gate would exit with code {code}.")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Block a release when eval metrics regress.")
    parser.add_argument("--baseline", help="Path to baseline metrics JSON")
    parser.add_argument("--current", help="Path to current metrics JSON")
    parser.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD,
                        help="Largest allowed drop per metric (default 0.02)")
    args = parser.parse_args(argv)

    if not args.baseline and not args.current:
        demo()
        return 0
    if not args.baseline or not args.current:
        parser.error("Pass both --baseline and --current, or neither for the demo.")

    with open(args.baseline, encoding="utf-8") as f:
        baseline = json.load(f)
    with open(args.current, encoding="utf-8") as f:
        current = json.load(f)
    return run_gate(baseline, current, args.threshold)


if __name__ == "__main__":
    sys.exit(main())
