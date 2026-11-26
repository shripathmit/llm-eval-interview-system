# Wrong Level Measurement: Cell, Row, or Table

> A score at the wrong level is a precise answer to a question nobody asked.

---

## What it is

Every output has levels. A parsed table has cells, rows, and the table as a whole. A voice interaction has the words heard, the meaning extracted, and the user's goal. Wrong level measurement means scoring one level while users live at another. The number is real. It just does not describe the experience you ship.

---

## How it shows up

- A parser reports 95% accuracy while users reject the output, because the 5% of wrong cells break whole tables
- A speech system scores well on word accuracy while task completion stays poor
- Teams argue about whether the system is good, each side holding a true number from a different level
- Tuning improves the measured level and leaves the user-facing level untouched

---

## Why it happens

Low levels are easy to score. Counting correct cells is mechanical; deciding whether a table is usable takes judgment. So teams measure what is countable and report it as quality. In one document parsing eval, the headline number sat around 80% on table recognition, and the first real work was agreeing on what that 80% even measured before anyone could argue about shipping. In a voice product, the team scored three levels separately, speech success, NLP success, and goal success, because the only level the user feels is the last one.

---

## How to detect it

| Check | What it tells you |
|---|---|
| Correlate each level's score with user acceptance | Which level actually predicts the experience |
| Error analysis at the top level | Whether low-level errors cluster into top-level failures |
| Score the same outputs at two levels | How far apart the story changes between levels |

---

## How to fix it

- Name the level every score refers to, in the metric name itself, never a bare percentage
- Set the release bar at the level users feel, and use lower levels for diagnosis only
- Track all levels, but gate on the top one
- When levels disagree, believe the top level and go find out why the lower one is lying
