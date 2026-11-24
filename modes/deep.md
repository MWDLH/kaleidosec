# DEEP mode

Load this card when: cross-domain, multi-identity, long horizon, or an engagement chain that must
survive new privileges and network positions. This is the full operating form.

## Control loop

Follow `references/core-workflow.md` as an iterative loop, not a waterfall:

```text
initialize/resume -> inspect capability -> collect -> check coverage -> model surface
-> generate and rank paths -> validate/execute -> interpret evidence -> update state
-> replan -> prove impact -> review coverage -> clean up -> report
```

Re-enter focused collection after gaining a new identity, privilege, host, application role, trust
relationship, cloud account, or network position. Do not restart collection from zero.

## Path states

Every path is in exactly one state, and every state change is recorded:

- `active` — currently being worked.
- `deep_dive` — deliberately investing; must state what investment buys.
- `parked` — paused; **must** carry a reactivation condition and a value estimate.
- `closed` — finished; **must** carry a completion or abandonment reason.

`rejected` is an observation class, not a path status. Never stop solely because of a retry count:
continue while an attempt changes a meaningful variable or can yield new information; stop mechanical
repetition with no new hypothesis. For path operations read `references/decision-and-paths.md`. For a
complete cross-domain call/return example read `references/example-full-chain.md`; treat its evidence
as illustrative, never as inherited target facts.

## Module stack and cross-domain return

Apply `references/module-continuity.md` before entering any domain card, supporting domain, or
cross-cutting capability. Keep `.pentest_session.json` as the single source of truth; its schema and
evidence rules are in `references/state-and-evidence.md`.

Before entering a domain card, supporting domain, or cross-cutting capability, record a frame with:
parent path, bounded question, inherited evidence, authorization profile, expected deliverable, and
return target.

On return: merge the result into shared evidence, record capability changes, re-rank affected paths,
and only then pop the frame. Keep one primary domain plus explicit supporting domains — do not replace
the engagement when the surface changes.

## Subagents

If the host supports subagents, emit work packets for independent, parallel-safe questions only;
otherwise run them serially — same protocol, different executor. A packet carries: one discriminating
question, scope, action limit, expected evidence format, return budget. Subagents return evidence and
capability changes; they never own or edit the path graph. You merge returns and re-rank. Use subagents
only at this depth; QUICK and STANDARD run serially.

## Execute and diagnose

Select tools by capability, not popularity. Read `references/tool-card-schema.md` before selecting a
tool. Before a command, confirm target and operator OS,
architecture, effective privilege, tool availability and version, network position, proxy/egress
constraints, interpreter, and output capture. Bind every command to current evidence; annotate
placeholders with their evidence source. Do not assume a tool is installed.

After a failure, classify it as execution, environment, access, reachability, method, prerequisite,
hypothesis, or route value. Read `references/failure-recovery.md` before retrying an ambiguous or
stalled action. Do not answer a tool error by cycling same-capability alternatives.

For a PoC or helper script: state purpose, environment, dependencies, risk, test status, evidence
output, and cleanup; check syntax and dependencies locally when possible; mark unverified
target-specific assumptions; preserve exact evidence without embedding live secrets.

## Resume

Validate the schema before inheriting state. Preserve history — mark superseded items instead of
rewriting. Ignore or archive mismatched state; never silently delete it. After resume, recheck scope,
authorization, access, tools, time window, target state, domain context, and active module frames.

Checkpoint after a material action, finding, identity or privilege change, new network position,
asset class, path status change, approval, persistent change, module call or return, and before any
long-running step.

## Close and report

Review active and parked paths, reconcile evidence with actions, list persistent changes and rollback
status, identify retained sensitive artifacts, and save a final checkpoint and handoff. Use
`references/report-template.md`. Report confirmed facts, tested scope, attack chains, business
impact, uncertainty, untested surfaces, and remediation. Do not hide incomplete coverage.
