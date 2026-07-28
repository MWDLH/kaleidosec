# CI/CD And Software Supply-Chain Operations


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
| [Build The Delivery Graph](supply-chain-01-build-the-delivery-graph.md) | Load on entry to establish position, prerequisites, and the bounded question. | Return evidence, capability changes, affected paths, and the next decision. |
| [Build The Surface — Practical Enumeration](supply-chain-02-build-the-surface-practical-enumeration.md) | Load on entry to establish position, prerequisites, and the bounded question. | Return evidence, capability changes, affected paths, and the next decision. |
| [Attack Primitives: CI/CD Pipeline Attacks](supply-chain-03-attack-primitives-ci-cd-pipeline-attacks.md) | Load only when current evidence supports the Attack Primitives: CI/CD Pipeline Attacks route or its prerequisite must be tested. | Return evidence, capability changes, affected paths, and the next decision. |
| [Attack Primitives: Registry & Deployment Attacks](supply-chain-04-attack-primitives-registry-deployment-attacks.md) | Load only when current evidence supports the Attack Primitives: Registry & Deployment Attacks route or its prerequisite must be tested. | Return evidence, capability changes, affected paths, and the next decision. |
| [Interpret Results](supply-chain-05-interpret-results.md) | Load after a material result to classify evidence and impact. | Return evidence, capability changes, affected paths, and the next decision. |
| [Domain Transitions](supply-chain-06-domain-transitions.md) | Load when evidence changes domain, identity boundary, execution surface, or network position. | Return evidence, capability changes, affected paths, and the next decision. |
| [Recollect When](supply-chain-07-recollect-when.md) | Load after gaining a new identity, privilege, asset, role, trust edge, or network position. | Return evidence, capability changes, affected paths, and the next decision. |
