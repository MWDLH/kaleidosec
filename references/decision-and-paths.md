# Decision And Attack-Path Management

## Build Paths

Turn observations into paths connecting current capability to a useful security outcome. Do not create a path from a scanner label alone. State prerequisites, falsifiers, and the observable result that would advance it.

## Rank Paths

Compare objective contribution, business impact, reachability, prerequisite coverage, evidence strength, feasibility, information gain, chain leverage, time cost, operational risk, noise, and reversibility.

Do not reduce ranking to CVSS. A medium issue that unlocks a critical trust boundary can outrank an isolated high-severity issue.

When the user provides a testing window, remaining time, or deadline, include it in reranking. Favor paths that can produce high-value evidence within the available window and reserve necessary time for evidence capture and cleanup. Without an explicit time constraint, do not invent a hard budget or abandon a valuable path because of elapsed time alone.

## Control Depth

Continue when the next attempt changes a meaningful variable, tests an independent branch, resolves material ambiguity, or has strong expected information gain.

Use deep_dive when value is high and evidence is strengthening, even if several distinct attempts are required.

Park when a path lacks a prerequisite, stalls without new information, is dominated by a stronger route, or costs more than its current contribution. Record a reactivation condition.

Close only when completed, sufficiently disproved, out of scope, superseded with no value, or irrelevant.

## Avoid Mechanical Repetition

Before retrying, state what changed: method, parameters, identity, privilege, network position, entry point, protocol, environment assumption, defensive-control hypothesis, or evidence source. Without a change or supported transient failure, do not repeat.

Re-rank when access, identity, privilege, network position, target value, controls, scope, evidence, or path status changes.
