# Identity, Credential, Trust, And Network Capability


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
| [Model Identity](identity-network-01-model-identity.md) | Load on entry to establish position, prerequisites, and the bounded question. | Return evidence, capability changes, affected paths, and the next decision. |
| [Model Network Position](identity-network-02-model-network-position.md) | Load on entry to establish position, prerequisites, and the bounded question. | Return evidence, capability changes, affected paths, and the next decision. |
| [Credential Assessment — Prioritization](identity-network-03-credential-assessment-prioritization.md) | Load only when current evidence supports the Credential Assessment — Prioritization route or its prerequisite must be tested. | Return evidence, capability changes, affected paths, and the next decision. |
| [Return To Parent Path](identity-network-04-return-to-parent-path.md) | Load before returning capability results to the parent attack path. | Return evidence, capability changes, affected paths, and the next decision. |
