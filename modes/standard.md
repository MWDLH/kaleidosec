# STANDARD mode

Load this card when: one target with several surfaces, or one identity/privilege change. A 3–5 entry
path table is enough. Do not build the full path graph yet.

## Path table

Keep a live table with one row per candidate path:

| id | title | status | target outcome | key evidence | main unknown | next action | value |
|---|---|---|---|---|---|---|---|

Re-rank after every material result. A path that cannot change the decision is not worth a row.

## Evidence bookkeeping

Maintain separate records — never collapse them:

- **fact** — directly observed, reproducible, tied to an artifact.
- **inference** — derived from facts; state the derivation.
- **hypothesis** — worth testing; state the test that would falsify it.
- **unknown** — decision-changing gap; record what would fill it.
- **rejected** — tested or ruled out; record why, so it is not retried blindly.

Never convert a tool error into proof that a vulnerability is absent. Only a result that tests the
hypothesis can falsify it.

## Decision contract (7 fields)

For each material action:

```yaml
judgment: what the evidence currently supports
key_evidence: facts that drive the decision
unknowns: missing facts that could change the route
next_action: the next bounded action
why_now: why it outranks alternatives
expected_signal: success, failure, partial, or ambiguous signals to watch for
failure_branch: what to inspect or change before another attempt
```

## Loading cards

Read the domain router first, then only the single card its trigger conditions support. Never walk
all cards of a domain as a checklist — that is the main source of wasted budget at this depth.

Supporting references, load only when the condition fires:

- `references/field-decision-examples.md` — operator behavior is ambiguous, or a path risks becoming
  tool-driven.
- `references/anti-patterns.md` — the engagement feels stuck, repetitive, or is falling into common
  mistakes.
- `references/decision-and-paths.md` — generating, ranking, deepening, parking, reactivating, or
  closing paths.

## Leaving STANDARD

Upgrade to DEEP on a new identity, a new trust boundary, evidence self-contradiction, or a goal that
needs a cross-domain chain. Close or park after two consecutive actions with no information gain.
