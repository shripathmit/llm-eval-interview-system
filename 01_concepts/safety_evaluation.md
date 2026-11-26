# Safety Evaluation: Proving the System Refuses What It Must and Helps Where It Should

> Safety eval has two failure directions: the system does something harmful, or it refuses something harmless - measure both, because fixing one blindly creates the other.

---

## What Safety Evaluation Measures

Three quantities, reported separately, always:

- **Unsafe output rate:** Of the outputs sampled, what share violate policy: harmful instructions, leaked private data, dangerous errors presented as fact.
- **Refusal quality:** When the system refuses, is the refusal correct, clear, and proportionate? A refusal that lectures a legitimate user is a product failure wearing a safety costume.
- **Over-refusal rate:** Of benign requests, what share got refused or degraded? This is the number teams forget to measure, and the one users experience as "the product got worse and dumber."

Safety bars are not one number. They are set per use case, by risk tier, because the same model behavior is acceptable in one context and disqualifying in another.

---

## Risk Tiers Set the Bar

A per-use-case risk framework scores each use case on what the output can affect, and the eval bar follows the tier:

| Tier | Example shape | Safety bar |
|---|---|---|
| Low | Internal drafts, summaries a human edits before use | Unsafe rate monitored; over-refusal weighted heavily |
| Medium | Customer-facing answers with citations and review paths | Unsafe rate capped; refusal quality reviewed by humans |
| High | Outputs that act on the world, or inform regulated decisions | Near-zero tolerance on defined harm categories; hard gates; human audit of samples mandatory |

Two properties make the framework work. The tier is assigned before launch, by the framework, not negotiated per release. And moving a use case up a tier automatically tightens its eval: bigger samples, human review, adversarial coverage. The bar is a property of the risk, not of the team's schedule.

---

## Method Catalog: 4 Approaches

### 1. Red Teaming

**Mechanism:** People (and automated generators) actively try to make the system fail: jailbreaks, indirect prompt injection through retrieved content, edge-case phrasing, multi-turn manipulation.

**Pros:** Finds failures that no benign test set contains; tests the system as an adversary will meet it
**Cons:** Coverage is unbounded; a clean red team round proves effort, not safety; findings skew to the testers' imagination
**When to use:** Before every launch at medium tier and above, after any model or prompt change, and on a schedule against the live system

### 2. Adversarial Test Sets

**Mechanism:** Red team findings, production incidents, and known attack patterns become fixed test cases in a safety regression set, run in CI like any other gate.

**Pros:** Yesterday's attack becomes today's permanent test; comparable across versions
**Cons:** Only covers known attacks; sets leak and get trained against if handled carelessly
**When to use:** Always, as a hard gate: safety set failures block release, no threshold negotiation

### 3. Refusal Audits

**Mechanism:** Sample refused requests from production. Humans classify each: correct refusal, over-refusal, or wrong-reason refusal (refused, but on a mistaken basis that will misfire elsewhere).

**Pros:** The only way to see the over-refusal problem, which never appears in attack testing
**Cons:** Requires policy judgment from annotators; borderline cases generate real disagreement that must be resolved into rubric updates
**When to use:** Continuously at any tier where users can be refused; the wrong-reason category is the most valuable output

### 4. Harm Category Scoring

**Mechanism:** Define the specific harm categories for the product (not generic lists): the wrong dose, the leaked record, the fabricated citation. Score sampled outputs per category with judges pre-screening and humans deciding.

**Pros:** Ties eval directly to the product's actual risk register; gives leadership a per-category number instead of a vibe
**Cons:** Category definitions need legal and domain input; rare categories need huge samples to measure directly
**When to use:** Medium and high tiers; combine with red teaming, which finds the categories you forgot to define

---

## The Trap: One-Directional Pressure

Every safety incident pushes the system toward refusing more. Every over-refusal complaint pushes toward refusing less. Without both rates on the same dashboard, the system oscillates: tightened after an incident until users revolt, loosened until the next incident. The eval design that prevents this is boring and absolute: unsafe rate and over-refusal rate, same report, same review, neither allowed to improve by quietly worsening the other.
