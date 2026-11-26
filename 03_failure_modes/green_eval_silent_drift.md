# Green Eval, Silent Drift: Passed Offline, Degraded in Production

> The eval said fine. The users said otherwise. Both were describing their own data honestly.

---

## What it is

Silent drift means the system passes every offline eval while real-world quality degrades. The eval set froze at some point in the past. Production did not. New inputs, new users, new edge cases arrive in traffic that the set never contained, and the first sign of trouble is user complaints instead of a red dashboard.

---

## How it shows up

- Offline scores flat and green while support tickets and retries climb
- Failures concentrate in segments the eval set barely covers: a new locale, a new document type, a new user group
- The failing inputs look different from anything in the test set
- Nobody can say when it started, because nothing was watching production quality directly

---

## Why it happens

Eval sets are built from what the system faced at build time. Production keeps moving. In one voice product, usage spanned multiple locales with different speech patterns, and a set built on one population said little about another. The same shape appears in document pipelines when a new document type enters the flow: the parser scores fine on the old types while the new type fails in ways the set cannot see.

---

## How to detect it

| Check | What it tells you |
|---|---|
| Scored samples of live production traffic | The real current score, not the frozen one |
| Score breakdowns by segment, locale, and input type | Where the drift is hiding inside a healthy average |
| Outcome signals: retries, abandonment, escalations | Proxy alarms between formal eval cycles |
| Input distribution comparison, set versus live traffic | How far the set has drifted from reality |

---

## How to fix it

- Score a random sample of production traffic on a fixed cadence, with the same rubric as the offline set
- Feed production failures back into the eval set every cycle, so the set ages with the traffic
- Break every headline score down by segment before calling it green
- Treat a gap between offline and production scores as a defect in the eval, and fix the eval first
