# Authorized Control-Evasion And Environment Adaptation

Use this capability only when a defensive control blocks a necessary bounded validation or the engagement objective explicitly includes control effectiveness. Do not make evasion a default stage — it's a tactical adaptation, not a goal.

**Before attempting any evasion, ask**: "Is there a lower-noise, native method, different path, or smaller proof that can answer the same question without bypassing this control?" Process-local, temporary adaptation requires L2 pre-authorization; central logging, policy, or security-control mutation is L3 and requires explicit approval.

---


## Continuity And Loading Rules

Read [../module-continuity.md](../module-continuity.md) before invoking a card. Keep one engagement state and one attack-path graph across all cards and domains.

1. Load entry and coverage cards first when they exist.
2. Load only the technical card supported by current evidence; do not enumerate cards as a checklist.
3. Keep the current parent path unless evidence creates a genuinely independent path.
4. Checkpoint before a domain transition and after a card returns material evidence.
5. When multiple domains cooperate, keep one primary domain and record supporting domains in state.

## Card Router

| Card | Load condition | Required return |
|---|---|---|
| [Diagnose The Control Layer](evasion-testing-01-diagnose-the-control-layer.md) | Load on entry to establish position, prerequisites, and the bounded question. | Return evidence, capability changes, affected paths, and the next decision. |
| [Evasion Techniques By Control Layer](evasion-testing-02-evasion-techniques-by-control-layer.md) | Load only when current evidence supports the Evasion Techniques By Control Layer route or its prerequisite must be tested. | Return evidence, capability changes, affected paths, and the next decision. |
| [Evasion Decision Flow](evasion-testing-03-evasion-decision-flow.md) | Load only when current evidence supports the Evasion Decision Flow route or its prerequisite must be tested. | Return evidence, capability changes, affected paths, and the next decision. |
| [Return](evasion-testing-04-return.md) | Load before returning capability results to the parent attack path. | Return evidence, capability changes, affected paths, and the next decision. |

