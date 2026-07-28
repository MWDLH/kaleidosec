# State And Evidence Protocol

Persist state in `.pentest_session.json`. Use `scripts/session_state.py` for initialization, validation, authorization updates, module-stack transitions, summaries, and checkpoints.

## Required Structure

~~~json
{
  "schema_version": "2.0",
  "engagement_id": "project-or-generated-id",
  "objective": "current measurable objective",
  "scope": {"status": "confirmed", "assets": [], "exclusions": [], "constraints": []},
  "authorization_profile": {
    "autonomous_levels": ["L0", "L1"],
    "approved_action_classes": [],
    "excluded_actions": [],
    "scale_limits": {},
    "stop_conditions": [],
    "approvals": []
  },
  "context": {"domain": "web-api", "phase": "collection", "current_access": [], "network_position": [], "controls": []},
  "domain_context": {"primary_domain": "web-api", "supporting_domains": [], "transition_reason": "", "return_target": ""},
  "module_stack": [],
  "observations": {"facts": [], "inferences": [], "hypotheses": [], "unknowns": [], "rejected": []},
  "assets": [],
  "credential_refs": [],
  "findings": [],
  "attack_paths": [],
  "actions": [],
  "blockers": [],
  "persistent_changes": [],
  "artifacts": [],
  "next_decision": {},
  "last_updated": "ISO-8601 timestamp"
}
~~~

## Authorization Profile

Apply [action-safety-gates.md](action-safety-gates.md). `autonomous_levels` may contain L0, L1, and explicitly pre-authorized L2. Record specifically approved action classes, exclusions, scale limits, stop conditions, and L3 approval records. An authorization update never expands target scope by itself.

## Evidence Records

A decision-changing record contains an identifier, statement, source or artifact reference, observation time, confidence, and affected assets. Keep raw evidence separate from interpretation.

Use `confirmed` for direct reproducible evidence, `high` for multiple consistent observations, `medium` for plausible inference with incomplete prerequisites, and `low` for weak or unverified signals.

## Attack Paths

Record identifier, title, parent path, status, target outcome, prerequisites, supporting and opposing evidence, unknowns, attempted methods, remaining independent branches, value, blockers, next action, close reason, and reactivation condition. Allowed statuses are `active`, `deep_dive`, `parked`, and `closed`.

`rejected` is an observation class, not a path status. Represent a completed path as `closed` with an explicit completion reason.

## Domain And Module Continuity

Apply [module-continuity.md](module-continuity.md). `domain_context` identifies the primary domain, supporting domains, transition reason, and return target. `module_stack` stores active call frames so a card or capability cannot detach from its parent path.

Push a frame before invoking a technical card or supporting capability. Pop it only after the return contract is merged into shared evidence and affected paths are reranked.

## Credential References

Never persist live secrets by default. Record a reference identifier, type, source, principal, applicable scope, validation status, storage location, and sensitivity. Redact secrets from summaries and reports.

## Resume Rules

- Resume only when engagement identity and objective are compatible.
- Validate the schema before inheriting state.
- Preserve history; mark superseded items instead of rewriting it.
- Ignore or archive mismatched state. Never silently delete it.
- Recheck scope, authorization, access, tools, time window, target state, domain context, and active module frames after resume.

Checkpoint after a material action, finding, identity or privilege change, new network position, asset class, path status change, approval, persistent change, module call or return, or before a long-running step.

A valid empty example is available at [state-example.json](state-example.json).
