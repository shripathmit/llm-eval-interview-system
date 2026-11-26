# Golden Set Governance: Who Can Change the Ruler

> If anyone can edit the test, every score is negotiable.

---

## Problem

The golden set is the ruler every quality decision gets measured with. In most teams it is also a shared folder anyone can edit. Items get added after embarrassing failures, removed when they keep failing, and re-labeled when a release needs a better number. None of it is malicious. All of it destroys the set's one job: being a stable reference that scores can be compared against over time.

---

## The pattern

Treat the golden set as production infrastructure with change control, not as a document. One owner, versioned changes, reviewed diffs, and a fixed refresh cadence. The governance is deliberately boring. Boring is the point: excitement around the ruler means the measurements are moving.

---

## How it works

1. **Name an owner.** One person or small group owns the set. Ownership means reviewing changes, not writing every item.
2. **Version the set like code.** Every change is a reviewed diff with a reason attached: new failure class, retired scenario, corrected label. Scores always cite the set version they were measured against.
3. **Separate the working set from the decision set.** Teams tune against a working set that can change freely. The decision set used for launch gates changes slowly, through review, and nobody tunes against it directly.
4. **Review label changes hardest.** Adding an item is low risk. Changing an existing label moves every historical comparison, so it needs evidence: the old label, the new label, and why the old one was wrong.
5. **Schedule refresh, forbid edits in anger.** New production failures enter through the regular refresh cycle, not in the middle of a launch dispute. An item added during an argument about a score is a conflict of interest with a file name.
6. **Audit access.** The set stays out of training and tuning pipelines, and access is logged. Contamination is usually a process failure, not a person failure.

---

## When to use it

- Any eval whose scores get compared across releases, teams, or vendors
- Launch gates and contractual quality bars, where a moved ruler has legal and business consequences
- Regulated settings, where an auditor will ask who changed the standard and when

---

## Signs governance is missing

- Two teams quote different scores for the same release, measured on different set versions
- Nobody can say who added the item that a launch is currently failing on
- The set's edit history spikes in the week before every launch decision
- Historical scores get restated quietly instead of versioned loudly

Any one of these means the ruler is being negotiated, and every score downstream of it is suspect.

---

## Failure mode it prevents

- **Benchmark contamination**, by keeping the set out of tuning pipelines and under access control
- **Teaching to the test**, because the decision set is separated from the set teams optimize against
- Score disputes that cannot be settled because nobody knows which version of the truth was used
