# Module Continuity Protocol

Use one engagement state and one attack-path graph across every domain router, technical card, and cross-cutting capability. Splitting reference files must never split the engagement.

## Source Of Truth

Treat `.pentest_session.json` as the only persistent source of truth. A module may add evidence, actions, paths, or transitions, but it must not create a private parallel state or silently replace inherited facts.

Always inherit the engagement objective and scope; authorization profile; current identity, privilege, role, execution channel, and network position; evidence classes; findings and credential references; attack paths and parent-child relationships; actions, artifacts, blockers, persistent changes, approvals, and cleanup obligations.

## Call Contract

Before invoking a domain, card, or capability, record:

~~~yaml
module_call:
  module_id: stable module or card name
  engagement_id: inherited engagement identifier
  parent_path: attack path that owns the question
  current_objective: bounded question this module must answer
  current_position:
    identity: effective principal and role
    privilege: effective privilege or authorization level
    network_position: current reachability and trust boundary
    execution_channel: available interface or runtime
  inherited_evidence: decision-changing evidence references
  critical_unknowns: unknowns that may change the route
  authorization_profile: autonomous levels, exclusions, limits, and stop conditions
  expected_deliverable: evidence or decision required by the parent path
  return_condition: condition that ends this module invocation
~~~

Do not invoke a module with an open-ended objective such as "test everything" or "reverse the application." Narrow the call to the current decision while preserving the wider parent path.

## Return Contract

Before leaving a module, return:

~~~yaml
module_return:
  result_class: confirmed, contradicted, partial, ambiguous, execution_failure, or no_material_change
  confirmed_observations: new facts with evidence references
  inferences_and_hypotheses: updated interpretations kept separate from facts
  disproved_assumptions: assumptions invalidated by the result
  unresolved_unknowns: material questions still open
  capability_changes: new identity, privilege, asset, role, trust edge, or network position
  affected_paths: paths to activate, deepen, park, close, or rerank
  suggested_transitions: evidence-supported domain or capability transitions
  actions_and_artifacts: action and evidence identifiers created by the module
  persistent_changes: changes and rollback obligations
  next_decision: recommended parent-path action after return
~~~

Merge the return into shared state before choosing another module. A tool error or empty result must not erase the parent hypothesis unless it actually tested and contradicted a prerequisite.

## Domain And Card Stack

Maintain `domain_context` and `module_stack`:

- `primary_domain` owns the current decision and report context.
- `supporting_domains` contribute evidence without replacing the primary domain.
- `module_stack` records caller, callee, parent path, objective, and return target.
- Push a frame before invoking a card or capability; checkpoint before a material domain transition.
- Pop the frame only after merging the return contract and reranking affected paths.

Keep the same parent path for sequential scenes in one chain. Create a child path only when the new route has a distinct outcome, prerequisites, or independent value. Create an independent path only when it can progress without the current parent.

## Cross-Domain Transitions

Transition when evidence changes the actual operating surface, not merely because another reference contains a relevant command. For each transition:

1. checkpoint current evidence and path status;
2. record the transition reason and evidence reference;
3. preserve the originating path as parent or explicit related path;
4. set the destination as primary or supporting domain;
5. define a bounded question and return target;
6. recollect for the new identity, privilege, reachability, trust, and controls;
7. merge the result and rerank the whole attack-path graph.

Carry only decision-relevant context: the triggering evidence; exact asset, endpoint, identity, privilege, role, token or credential reference, network position, and execution channel involved; the capability already proved; unresolved assumptions; the bounded question for the destination; authorization constraints; and the return condition. The destination domain must inherit these facts, collect only its missing prerequisites, and return results to the originating path rather than starting a parallel engagement.

## Loading Discipline

Load the domain router first. Load entry and coverage cards when establishing or materially changing position. Load a technical card only when evidence supports its prerequisites or when it is the cheapest discriminating check. Load interpretation and transition cards after material results.

Do not load every card in a domain as a checklist. Do not restart collection from zero after switching cards. Reuse inherited evidence, then collect only the missing information that could change the current route.
