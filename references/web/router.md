# Web And API Operations


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
| [Build The Surface](web-api-01-build-the-surface.md) | Load on entry to establish position, prerequisites, and the bounded question. | Return evidence, capability changes, affected paths, and the next decision. |
| [Attack Primitives: Traditional Web Vulnerabilities](web-api-02-attack-primitives-traditional-web-vulnerabilities.md) | Load only when current evidence supports the Attack Primitives: Traditional Web Vulnerabilities route or its prerequisite must be tested. | Return evidence, capability changes, affected paths, and the next decision. |
| [Attack Primitives: Authentication & Session](web-api-03-attack-primitives-authentication-session.md) | Load only when current evidence supports the Attack Primitives: Authentication & Session route or its prerequisite must be tested. | Return evidence, capability changes, affected paths, and the next decision. |
| [Attack Primitives: Authorization](web-api-04-attack-primitives-authorization.md) | Load only when current evidence supports the Attack Primitives: Authorization route or its prerequisite must be tested. | Return evidence, capability changes, affected paths, and the next decision. |
| [Attack Primitives: Injection & Input Processing](web-api-05-attack-primitives-injection-input-processing.md) | Load only when current evidence supports the Attack Primitives: Injection & Input Processing route or its prerequisite must be tested. | Return evidence, capability changes, affected paths, and the next decision. |
| [Attack Primitives: Business Logic & Race Conditions](web-api-06-attack-primitives-business-logic-race-conditions.md) | Load only when current evidence supports the Attack Primitives: Business Logic & Race Conditions route or its prerequisite must be tested. | Return evidence, capability changes, affected paths, and the next decision. |
| [Interpret Results](web-api-07-interpret-results.md) | Load after a material result to classify evidence and impact. | Return evidence, capability changes, affected paths, and the next decision. |
| [Domain Transitions](web-api-08-domain-transitions.md) | Load when evidence changes domain, identity boundary, execution surface, or network position. | Return evidence, capability changes, affected paths, and the next decision. |
| [Recollect When](web-api-09-recollect-when.md) | Load after gaining a new identity, privilege, asset, role, trust edge, or network position. | Return evidence, capability changes, affected paths, and the next decision. |
