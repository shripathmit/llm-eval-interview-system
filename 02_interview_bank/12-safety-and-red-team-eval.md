# 12 - Safety and Red Team Eval

> Quality eval asks if the system works. Safety eval asks what it does when someone tries to make it fail, or harm.

---

## 🏗️ The Setup: Components & Signals

### Flow

```
[Attack and risk design]
Risk list → Attack set (prompts, scenarios, jailbreaks) → System runs
                                                              │
                                                              ▼
                        Grade: unsafe output, correct refusal, over-refusal
                                                              │
                                                              ▼
                        Unsafe rate by category → Bar by risk tier → Gate
```

### Key Components

| Component | Responsibility |
|---|---|
| Risk Taxonomy | Lists the harm categories that matter for this product, in this context |
| Attack Set | Prompts and scenarios designed to trigger each category, refreshed as attacks evolve |
| Graders | Rules, classifiers, judges, and humans that label outputs unsafe, safe, or wrongly refused |
| Refusal Grading | Scores refusals for correctness and quality, not just presence |
| Risk Tiering | Assigns each use case a tier, so bars and gates scale with blast radius |

### Signals & Tools

| Category | Example Signals & Tools |
|---|---|
| Safety signals | Unsafe output rate by category, jailbreak success rate, over-refusal rate |
| Human signals | Red team findings, trust and safety escalations, abuse reports |
| Tooling | Classifier suites, curated harm benchmarks, internal attack libraries |

---

## Q1. How do you design a red team program for an LLM feature? `[Intermediate]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Start from a risk list, not from prompts.** Name the harms this product could enable or produce, in its real context. The list drives everything else.
2. **Build an attack set per harm.** Direct requests, indirect requests, multi-turn setups, encoded and obfuscated variants, and attacks through connected tools and data.
3. **Mix scripted and human red teaming.** Scripted sets give you repeatable rates. Human red teamers find the creative attacks scripts miss.
4. **Grade every run.** Unsafe output, correct refusal, or over-refusal. Ungraded red teaming produces stories, not measurements.
5. **Feed findings into the regression set.** Every successful attack becomes a permanent test. A fixed vulnerability that can return silently will.

</details>

---

## Q2. What is refusal quality, and why is refusing everything not a safety strategy? `[Basic]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **A refusal has three grades.** Correct refusal of a harmful request. Correct answer to a safe request. Wrong refusal of a safe request. Only the first two are good.
2. **Over-refusal is a product failure.** A system that refuses to explain chemistry to a student because the topic is adjacent to harm is safe on paper and useless in practice.
3. **Quality inside a refusal matters.** A good refusal is short, does not lecture, does not repeat the harmful content back, and offers the nearest safe help where one exists.
4. **Measure both rates.** Unsafe output rate and over-refusal rate, side by side. Optimizing one while blind to the other just moves the failure.
5. **Grade refusals with the rubric, not by keyword.** The word "cannot" in an output tells you nothing about whether the refusal was right.

</details>

---

## Q3. How do you measure an unsafe output rate you can trust? `[Intermediate]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Define unsafe per category, in writing.** Raters and classifiers cannot grade against a vibe. Each harm category needs examples of in and out.
2. **Use layered grading.** Deterministic rules and classifiers for volume, a judge for judgment calls, humans for the borderline slice and for calibration.
3. **Report per category, never one blended number.** A 0.5% overall rate can hide a 9% rate in the one category that matters.
4. **State the denominator and the attack set version.** An unsafe rate is only meaningful against the attacks actually run. A rate against last year's attacks is last year's number.
5. **Double-grade a slice with humans.** Classifier and judge drift is real. The human slice tells you whether your rate is a measurement or an artifact.

</details>

---

## Q4. How should safety bars differ across use cases? `[Intermediate]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

Use a per-use-case risk framework. Score each use case before you set its bar:

1. **Blast radius.** Who is affected if this output is wrong or harmful: one user, a team, the public, a regulated process?
2. **Reversibility.** Can the output be caught and undone, or does it act in the world the moment it ships?
3. **Audience vulnerability.** Adults choosing to use a tool, or children, patients, and people in crisis in the audience?
4. **Autonomy.** Does a human review the output before it acts, or does the system act on its own?

Then set the bar from the score. A summarizer with human review gets a standard bar. An autonomous agent writing to external systems gets the highest bar, mandatory human approval on irreversible actions, and a near zero tolerance in its worst category. Same framework, different bars: that is what makes the bars defensible when launch pressure arrives.

</details>

---

## Q5. How do you keep a red team attack set from going stale? `[Advanced]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Add every production incident.** Any unsafe output found by users, support, or monitoring becomes an attack case within days, not quarters.
2. **Track public jailbreaks.** New attack patterns appear in the open. Assign someone to pull them in on a cadence.
3. **Rotate human red teamers.** The same people run out of new ideas against the same system. Fresh attackers, including people from outside the team, find fresh holes.
4. **Retire attacks that no longer discriminate.** If every model version passes an attack for a year, keep it in regression but stop counting it in your headline rate. Rates should reflect current risk, not historical wins.
5. **Version the set and say which version a score used.** A safety number without its attack set version cannot be compared to anything.

</details>

---

## Q6. How do you evaluate safety when the model is connected to tools and data? `[Advanced]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **The attack surface moves.** Harm no longer needs to come from the user. It can sit in a retrieved document, a tool result, or a web page the agent reads: indirect prompt injection.
2. **Test poisoned inputs.** Plant instructions in documents and tool outputs and grade whether the system follows them, leaks them, or acts on them.
3. **Grade actions, not just text.** An agent that produces a safe answer while quietly calling a forbidden tool has failed. Safety grading must cover the trajectory.
4. **Test data boundaries.** Can one user's data surface in another user's session through retrieval or memory? Cross-user leakage is a safety category of its own.
5. **Set permission bars separately.** The eval should verify the system refuses actions outside its authority even when the text of the request looks harmless.

</details>

---

## Q7. Who should grade safety evals, and how do you protect the graders? `[Basic]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Machines grade volume, humans grade judgment.** Classifiers and judges handle the bulk. Humans take the borderline slice, new categories, and calibration samples.
2. **Write the rubric with policy owners.** Engineers alone should not define harm for a product. Trust and safety, legal, and domain experts own the category definitions.
3. **Limit human exposure.** Rotate graders through harmful content in short shifts, blur or truncate the worst material where grading allows, and make opting out costless.
4. **Measure grader agreement like anywhere else.** Safety categories with low human agreement are undefined categories. Fix the definition before trusting any rate built on it.
5. **Never let the team that ships grade its own launch gate alone.** Independent grading of the release decision is what makes the gate real.

</details>

---

## Q8. Scenario: your system passes the safety eval, and a week after launch a user posts a working jailbreak publicly. What happens next? `[Scenario]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Reproduce it immediately.** Confirm the jailbreak against the production configuration, not a staging approximation.
2. **Price the harm.** Which category, how severe, how repeatable, and does it scale or need a skilled attacker? Severity sets the response clock.
3. **Mitigate at the fastest layer.** A blocklist or classifier rule today, a system prompt or routing fix this week, a model level fix on the normal cycle. Layered fixes, fastest first.
4. **Add it to the attack set the same day.** The exact jailbreak and variants become permanent regression cases before the fix ships.
5. **Ask what the eval missed.** One jailbreak is an incident. The gap that let it through is the real finding: a missing category, a missing attack style, or a grading blind spot. Fix the gap, re-run the full set, and publish the updated unsafe rate with its new attack set version.

</details>
