# What Eval Is: The Trust Mechanism, Not a QA Step

> Eval is how a team decides whether an AI system deserves users - it is a decision system, not a testing phase.

---

## What is Eval?

Evaluation is the measurement system that tells you whether an LLM system is good enough to ship, what to fix next, and whether a change made things better or worse. It is not the last step of development. It runs before launch, during tuning, and for as long as the system is in production.

A test suite asks: does the code do what the code says? Eval asks a harder question: does the output deserve trust? For deterministic software those two questions are the same. For a model that generates language, they are not even close.

---

## Eval Decides Ship or No-Ship

Every eval system exists to feed three decisions:

```
Ship decision     Is this version good enough to put in front of users?
Fix decision      Which failure is costing us the most, and what do we fix next?
Change decision   Did this prompt, model, or pipeline change help or hurt?
```

If a score cannot change one of these decisions, it is decoration. Teams drown in dashboards full of numbers nobody acts on. A working eval produces a small number of scores, each wired to a decision and a threshold: above the bar, ship; below the bar, do not.

This is why eval is a leadership surface, not just an engineering one. The bar is a promise to users. Setting it, defending it under deadline pressure, and holding it when a launch date slips are judgment calls, and they are exactly what interviewers probe.

---

## Unit Eval vs End-to-End Eval

Eval happens at two levels, and confusing them is a common failure.

| Level | What it measures | Example | Blind spot |
|---|---|---|---|
| Unit / component | One piece in isolation | Did retrieval return the right chunk? Did the parser read the table correctly? | A system of passing units can still fail the user |
| End-to-end / task | The whole job the user came to do | Did the user get a correct, usable answer and finish the task? | Slow and expensive; hard to attribute a failure to one component |

You need both. Unit evals tell you where to fix. End-to-end evals tell you whether the fix mattered.

A voice product launch used three levels explicitly: speech success (did the system hear the words right), NLP success (did it get the meaning), and goal success (did the user achieve what they came to do). The first two are unit-level diagnostics. The third is the only one the user experiences. When the levels disagree, the end-to-end number wins the argument.

---

## The Four Parts of Every Eval

Whatever the system, an eval has the same four parts:

1. **A set of cases:** inputs that represent real use, including the hard and embarrassing ones.
2. **A scorer:** a human, a judge model, a rule, or a mix, that grades each output.
3. **A bar:** the score a version must clear, set by the cost of being wrong.
4. **A loop:** score, bucket the failures, fix the biggest bucket, re-score, and confirm the number does not slip.

Remove any one part and the eval stops working. Cases without a bar produce trivia. A bar without a loop produces a launch-day surprise. A scorer nobody trusts produces arguments instead of decisions.

---

## Where Eval Sits in the Lifecycle

| Stage | Eval's job |
|---|---|
| Development | Compare approaches cheaply before committing to one |
| Pre-launch | Gate the release: clear the bar or do not ship |
| Beta | Buy ground truth from real users on real tasks |
| Production | Watch for drift, regressions, and failures the test set never imagined |

The mistake is treating eval as the second row only. Teams that build the measurement plan on day one argue about data. Teams that build it at the end argue about opinions, usually in the launch meeting.
