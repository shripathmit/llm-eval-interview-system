# 17 - Conversational Eval

> A conversation is not five independent turns. Users judge the whole session, and your eval has to as well.

---

## 🏗️ The Setup: Components & Signals

### Flow

```
[Conversation]
Turns 1..n → Turn scoring: each response in its context
                  │
                  ▼
        Session scoring: goal reached? context carried? recovery?
                  │
                  ▼
        Rubric scores per dimension → Failure buckets → Bar check
```

### Key Components

| Component | Responsibility |
|---|---|
| Turn Scorer | Grades each response against the conversation so far, not in isolation |
| Session Scorer | Grades the whole conversation: goal completion, efficiency, recovery, tone |
| Context Probes | Scripted conversations that plant facts early and test them late |
| Conversation Rubric | The dimensions of a good session, defined in writing: correctness, memory, recovery, concision, tone |
| Persona Scripts | Repeatable user simulations with a goal, a style, and a patience limit |

### Signals & Tools

| Category | Example Signals & Tools |
|---|---|
| Session signals | Goal completion, turns to completion, user corrections, restarts, abandonment point |
| Quality signals | Context carryover rate, contradiction rate, recovery success rate |
| Tooling | Conversation simulators, transcript graders, session replay tools |

---

## Q1. Why is per turn eval not enough for conversational systems? `[Basic]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Turns are not independent.** A response that looks fine alone can contradict turn two, repeat a question the user already answered, or forget the constraint set in turn one.
2. **Users experience sessions.** Nobody rates a conversation one message at a time. They rate whether the thing understood them across the whole exchange.
3. **Failures compound.** A small misunderstanding in turn two, uncorrected, steers the next eight turns. Per turn scores record eight mediocre turns and miss the single cause.
4. **Recovery only exists at session level.** Catching and fixing a misunderstanding mid conversation is a core skill, and it is invisible to isolated turn grading.
5. **Grade both levels.** Turn scores diagnose. Session scores decide.

</details>

---

## Q2. How do you evaluate context carryover? `[Intermediate]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Build probe conversations.** Script sessions that plant a fact early: a name, a budget, a date, a constraint. Ask about it several turns later, after distracting turns in between.
2. **Vary the distance.** Test carryover at two turns, five turns, and twenty. Memory that works at two and fails at ten has a measurable cliff, and you want its location.
3. **Test updates, not just recall.** The user corrects the fact mid conversation. The system must use the new value and stop using the old one. Stale memory is worse than no memory.
4. **Test what should not carry.** Facts from a different user, a different session, or a hypothetical the user floated and rejected. Carryover has a boundary, and crossing it is a failure, not a feature.
5. **Score it as a rate.** Carryover success over the probe set, reported by distance. One number per distance band beats one blended memory score.

</details>

---

## Q3. What does a good conversation rubric contain? `[Intermediate]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

Score each dimension separately. A single session grade hides every tradeoff:

1. **Correctness.** Were the facts and the final answer right?
2. **Goal completion.** Did the user get what they came for, in this session?
3. **Memory.** Did the system use what the user already said, and respect updates?
4. **Recovery.** When something went wrong, did the system notice, clarify, and repair it?
5. **Efficiency.** How many turns did it take? Did the user have to repeat themselves?
6. **Tone and clarity.** Was it understandable, appropriately brief, and free of lecturing or filler?

Each dimension gets behavioral anchors: what a 1, a 3, and a 5 look like, with example turns. Anchors are what let two annotators score the same transcript the same way.

</details>

---

## Q4. How do you measure session level success? `[Basic]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Define the session goal.** From the user's first request or a task tag. No goal, no success measure, only vibes.
2. **Grade the outcome at session end.** Goal achieved, partially achieved, or failed, plus who ended it: user satisfied, user gave up, or session timed out.
3. **Add efficiency.** Turns to completion and user repeats. Two sessions can both succeed; the one that took nine turns and three corrections is the worse product.
4. **Count abandonment honestly.** A user who leaves mid task is a failed session unless you have evidence they left satisfied. Marking abandonments as neutral is how success rates inflate.
5. **Report success with its distribution.** Success rate by task type, by session length, by new versus returning users. The blended rate is the headline; the distribution is the information.

</details>

---

## Q5. How do you use simulated users in conversational eval, and where do they lie to you? `[Advanced]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Give the simulator a persona, a goal, and a patience budget.** It pursues the goal like a user would, answers questions, and gives up after a set number of bad turns.
2. **Use simulation for coverage and regression.** Hundreds of scripted conversations per change, probing carryover, recovery, and edge flows that human testing cannot afford to repeat.
3. **Know the lies.** Simulated users are more coherent, more patient, and more literal than real users. They do not typo, change their mind mid sentence, or paste a wall of text. Scores on simulation overstate production quality.
4. **Calibrate against real transcripts.** Score a set of real sessions with the same rubric. The gap between simulated and real scores is your simulation discount, and it should be published next to any simulated number.
5. **Never gate a launch on simulation alone.** Simulation picks finalists and catches regressions. Humans on real conversations make the launch call.

</details>

---

## Q6. How do you evaluate recovery from misunderstandings? `[Intermediate]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Inject misunderstandings on purpose.** Ambiguous requests, misheard values, contradictory instructions, a user who changes the goal mid session. Recovery cannot be graded on conversations where nothing goes wrong.
2. **Score the detection.** Did the system notice the ambiguity and clarify, or did it guess confidently? Asking one clarifying question beats three wrong turns.
3. **Score the repair.** After the user corrects it, does the system fix the whole thread: the answer, the stored facts, and anything already produced from the wrong value?
4. **Score the cost.** Turns spent recovering, and whether the user had to repeat information the system already had. Recovery that costs the user more than starting over is not recovery.
5. **Track recovery rate as its own metric.** Systems improve it deliberately once it is measured: clarification policies, confirmation on high cost actions, and summaries that let users catch errors early.

</details>

---

## Q7. How do multi-turn evals change when the conversation is long? `[Advanced]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Context pressure becomes the test.** Long sessions stress summarization and memory selection. Probe what survives compression: early constraints, corrections, and decisions, not just recent turns.
2. **Contradiction risk grows.** The system has said more, so it has more to contradict. Add a consistency pass: extract the system's stated facts across the session and check them against each other.
3. **Score in windows and as a whole.** Window scores localize where quality decays. The session score captures whether the user still got served at turn forty.
4. **Watch efficiency decay.** Late turns get slower, more repetitive, and more hedged in many systems. Turns to completion by session position shows it.
5. **Sample long sessions deliberately.** Random sampling under-represents them. Oversample the long tail, because that is where your most invested users live.

</details>

---

## Q8. Scenario: per turn scores are 94 and glowing, but session success is 71 and users say the assistant is frustrating. Reconcile it. `[Scenario]`

<details>
<summary>💡 Show Answer</summary>

**Answer:**

1. **Start by believing the session number.** Users live at session level. A 94 per turn average that produces 71 successful sessions means the turn rubric measures something users do not care about, or misses what they do.
2. **Read failing sessions end to end.** Not samples of turns: whole transcripts. Look for the patterns turn scoring cannot see: repeated questions, forgotten constraints, unrecovered misunderstandings, answers that are individually fine and jointly useless.
3. **Check the compounding math.** If each turn has a small chance of a context error, a ten turn session collects them. Per turn quality and session success are related by multiplication, not by average.
4. **Fix the rubric.** Add the missing dimensions: memory, recovery, repetition. Re-score the same transcripts. If the new rubric reproduces the 71, it is measuring the right thing now.
5. **Report both numbers with the explanation.** Leadership keeps the per turn score for diagnosis and the session score for decisions. A team that hides the 71 behind the 94 will meet it again in churn.

</details>
