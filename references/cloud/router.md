# Cloud, Container, Kubernetes, And SaaS Operations


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
| [Establish Context](cloud-container-01-establish-context.md) | Load on entry to establish position, prerequisites, and the bounded question. | Return evidence, capability changes, affected paths, and the next decision. |
| [Build The Surface — Practical First Steps](cloud-container-02-build-the-surface-practical-first-steps.md) | Load on entry to establish position, prerequisites, and the bounded question. | Return evidence, capability changes, affected paths, and the next decision. |
| [Attack Primitives: Metadata Service](cloud-container-03-attack-primitives-metadata-service.md) | Load only when current evidence supports the Attack Primitives: Metadata Service route or its prerequisite must be tested. | Return evidence, capability changes, affected paths, and the next decision. |
| [Attack Primitives: IAM Privilege Escalation](cloud-container-04-attack-primitives-iam-privilege-escalation.md) | Load only when current evidence supports the Attack Primitives: IAM Privilege Escalation route or its prerequisite must be tested. | Return evidence, capability changes, affected paths, and the next decision. |
| [Attack Primitives: Storage & Data Exposure](cloud-container-05-attack-primitives-storage-data-exposure.md) | Load only when current evidence supports the Attack Primitives: Storage & Data Exposure route or its prerequisite must be tested. | Return evidence, capability changes, affected paths, and the next decision. |
| [Attack Primitives: Container Security](cloud-container-06-attack-primitives-container-security.md) | Load only when current evidence supports the Attack Primitives: Container Security route or its prerequisite must be tested. | Return evidence, capability changes, affected paths, and the next decision. |
| [Attack Primitives: Serverless](cloud-container-07-attack-primitives-serverless.md) | Load only when current evidence supports the Attack Primitives: Serverless route or its prerequisite must be tested. | Return evidence, capability changes, affected paths, and the next decision. |
| [Interpret Results](cloud-container-08-interpret-results.md) | Load after a material result to classify evidence and impact. | Return evidence, capability changes, affected paths, and the next decision. |
| [Domain Transitions](cloud-container-09-domain-transitions.md) | Load when evidence changes domain, identity boundary, execution surface, or network position. | Return evidence, capability changes, affected paths, and the next decision. |
| [Recollect When](cloud-container-10-recollect-when.md) | Load after gaining a new identity, privilege, asset, role, trust edge, or network position. | Return evidence, capability changes, affected paths, and the next decision. |
