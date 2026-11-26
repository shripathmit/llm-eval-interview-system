# No Dip Process: A Bar With Nothing Behind It

> A threshold nobody acts on is a decoration, not a bar.

---

## What it is

Many teams set an eval bar: the score the system must hold before and after release. Fewer teams define what happens when the score falls below it. Who gets paged, what gets checked first, who can hold a release, and what evidence reopens the gate. Without that process, a dip produces a meeting, not a response, and the bar quietly stops meaning anything.

---

## How it shows up

- A score drops and the first response is debating whether the drop is real
- Releases ship during dips because no one holds explicit authority to stop them
- The same dip gets explained differently by different teams
- After the incident, nobody can reconstruct what was decided or why

---

## Why it happens

Setting a number feels like finishing the work. In one voice product eval, the bar was explicit: below 85 on goal success was not good enough to ship. The number was the easy part. The harder design work was the standing process around it: track scores by locale over time so a dip is visible early, keep annotators calibrated so a dip is not a labeling artifact, hold out a set for local speech patterns, and agree in advance what gets checked first and who decides on holding a release.

---

## How to detect it

| Check | What it tells you |
|---|---|
| Ask who can stop a release on a dip, by name | Whether the authority exists or is assumed |
| Read the last dip's timeline | How long detection to decision actually took |
| Check whether dip criteria are written anywhere | Whether the process survives the people who remember it |

---

## How to fix it

- Write the dip playbook before the first dip: detection, first checks, decision owner, release authority
- Rule out measurement first: annotator drift, a bad sample, a set change, then investigate the system
- Define recovery evidence in advance: what score, on what set, over what window, reopens the gate
- Log every dip and its decision, so the bar builds a track record instead of a folklore
