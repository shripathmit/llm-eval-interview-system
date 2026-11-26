# Eval Design Principles: Five Rules That Decide Whether an Eval Survives Production

> Principles first, tools second. Every eval failure in production traces back to one of these five rules being skipped.

---

### **1. Build the measurement plan on day one**

Decide how quality will be measured before you build the system, not after it works in a demo. The plan names the metric, the level it is measured at, who labels, and what score blocks a release. Retrofitting measurement onto a finished system costs more than building it in, because the outputs you needed to keep are already gone.

**Example:** A document parsing team spent weeks arguing whether output quality was good enough to ship. Nobody had defined how quality would be measured before building started, so every review meeting was opinion against opinion. The argument ended only when a measurement plan existed: a rubric, a sample, and a bar.

### **2. The bar is set by risk, not by the ship date**

A threshold is a risk decision. Set it from the cost of a wrong output reaching a user, then check whether the date is still realistic. A bar negotiated down to fit a deadline is not a bar; it is a date with a number attached.

**Example:** A document parser sat at 80% accuracy on table recognition, and leadership wanted it shipped to all business users in Q3 at that fidelity. Wrong cells in a regulated report are not a cosmetic bug; they flow into documents people make decisions from. The bar came from that risk, and the launch plan changed instead of the bar.

### **3. Be honest about the number**

Report the score you have, with its sample size and its weak segments, not the score you wish you had. Users and executives forgive a low number they can watch improving. They do not forgive a good number that turns out to be wrong, because every later number you report gets discounted.

**Example:** The same parser went to its first users with the number stated plainly: this is where it is, this is what is improving. Users stayed engaged, kept using it, and kept sending corrections, because progress they could see was worth more than a promise.

### **4. Measure at the level that matters**

A system can pass at every unit level and fail the user. Measure the level the user experiences: the completed task, not just the components under it. Lower levels are for debugging. The top level is for decisions.

**Example:** A voice product launching in India was evaluated at three levels: speech success (did it hear the words), NLP success (did it get the meaning), and goal success (did the user finish what they came to do). The bar was 85, judged by blind human annotators who did not know which model they were scoring. Launch decisions were made on goal success, because that is the level the user lives at.

### **5. A beta is the cheapest way to buy ground truth**

When no labeled set exists, a small honest beta creates one. Real users on real tasks produce corrections, and verified corrections become labels. That set then does double duty: it tunes the system and becomes the regression set that protects it.

**Example:** The parser at 80% had no ground truth to tune against. Instead of a full low-fidelity launch, it went to a limited beta. User feedback became the ground truth, accuracy climbed from 80% to 86-88%, and the team got a labeled set it could score every future change against.
