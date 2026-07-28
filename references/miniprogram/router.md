# Mini-Program Operations


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
| [Build The Surface](miniprogram-01-build-the-surface.md) | Load on entry to establish position, prerequisites, and the bounded question. | Return evidence, capability changes, affected paths, and the next decision. |
| [Coverage Gate](miniprogram-02-coverage-gate.md) | Load before the first material validation and after a capability or position change. | Return evidence, capability changes, affected paths, and the next decision. |
| [Attack Primitives: Core Vulnerability Classes](miniprogram-03-attack-primitives-core-vulnerability-classes.md) | Load only when current evidence supports the Attack Primitives: Core Vulnerability Classes route or its prerequisite must be tested. | Return evidence, capability changes, affected paths, and the next decision. |
| [Platform-Specific: WeChat Mini-Program WebView](miniprogram-04-platform-specific-wechat-mini-program-webview.md) | Load only when current evidence supports the Platform-Specific: WeChat Mini-Program WebView route or its prerequisite must be tested. | Return evidence, capability changes, affected paths, and the next decision. |
| [Platform-Specific: Other Mini-Program Platforms](miniprogram-05-platform-specific-other-mini-program-platforms.md) | Load only when current evidence supports the Platform-Specific: Other Mini-Program Platforms route or its prerequisite must be tested. | Return evidence, capability changes, affected paths, and the next decision. |
| [Interpret Results](miniprogram-06-interpret-results.md) | Load after a material result to classify evidence and impact. | Return evidence, capability changes, affected paths, and the next decision. |
| [Domain Transitions](miniprogram-07-domain-transitions.md) | Load when evidence changes domain, identity boundary, execution surface, or network position. | Return evidence, capability changes, affected paths, and the next decision. |
| [Recollect When](miniprogram-08-recollect-when.md) | Load after gaining a new identity, privilege, asset, role, trust edge, or network position. | Return evidence, capability changes, affected paths, and the next decision. |
