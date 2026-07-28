# Infrastructure, VPN, Middleware, And Desktop Operations


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
| [Build The Surface](infrastructure-desktop-01-build-the-surface.md) | Load on entry to establish position, prerequisites, and the bounded question. | Return evidence, capability changes, affected paths, and the next decision. |
| [Attack Primitives: Unauthenticated/Default Credential Services](infrastructure-desktop-02-attack-primitives-unauthenticated-default-credential-services.md) | Load only when current evidence supports the Attack Primitives: Unauthenticated/Default Credential Services route or its prerequisite must be tested. | Return evidence, capability changes, affected paths, and the next decision. |
| [Attack Primitives: Desktop & Thick Client](infrastructure-desktop-03-attack-primitives-desktop-thick-client.md) | Load only when current evidence supports the Attack Primitives: Desktop & Thick Client route or its prerequisite must be tested. | Return evidence, capability changes, affected paths, and the next decision. |
| [Attack Primitives: VPN & Network Appliances](infrastructure-desktop-04-attack-primitives-vpn-network-appliances.md) | Load only when current evidence supports the Attack Primitives: VPN & Network Appliances route or its prerequisite must be tested. | Return evidence, capability changes, affected paths, and the next decision. |
| [Interpret Results](infrastructure-desktop-05-interpret-results.md) | Load after a material result to classify evidence and impact. | Return evidence, capability changes, affected paths, and the next decision. |
| [Domain Transitions](infrastructure-desktop-06-domain-transitions.md) | Load when evidence changes domain, identity boundary, execution surface, or network position. | Return evidence, capability changes, affected paths, and the next decision. |
| [Recollect When](infrastructure-desktop-07-recollect-when.md) | Load after gaining a new identity, privilege, asset, role, trust edge, or network position. | Return evidence, capability changes, affected paths, and the next decision. |
