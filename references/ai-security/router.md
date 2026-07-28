# AI Application, LLM, Agent, And RAG Operations


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
| [Model The System](ai-security-01-model-the-system.md) | Load on entry to establish position, prerequisites, and the bounded question. | Return evidence, capability changes, affected paths, and the next decision. |
| [Coverage Gate](ai-security-02-coverage-gate.md) | Load before the first material validation and after a capability or position change. | Return evidence, capability changes, affected paths, and the next decision. |
| [Attack Primitives: Prompt Injection](ai-security-03-attack-primitives-prompt-injection.md) | Load only when current evidence supports the Attack Primitives: Prompt Injection route or its prerequisite must be tested. | Return evidence, capability changes, affected paths, and the next decision. |
| [Attack Primitives: Tool/Function Calling Abuse](ai-security-04-attack-primitives-tool-function-calling-abuse.md) | Load only when current evidence supports the Attack Primitives: Tool/Function Calling Abuse route or its prerequisite must be tested. | Return evidence, capability changes, affected paths, and the next decision. |
| [Attack Primitives: RAG / Knowledge Base Attacks](ai-security-05-attack-primitives-rag-knowledge-base-attacks.md) | Load only when current evidence supports the Attack Primitives: RAG / Knowledge Base Attacks route or its prerequisite must be tested. | Return evidence, capability changes, affected paths, and the next decision. |
| [Attack Primitives: File/URL Processing](ai-security-06-attack-primitives-file-url-processing.md) | Load only when current evidence supports the Attack Primitives: File/URL Processing route or its prerequisite must be tested. | Return evidence, capability changes, affected paths, and the next decision. |
| [Interpret Results](ai-security-07-interpret-results.md) | Load after a material result to classify evidence and impact. | Return evidence, capability changes, affected paths, and the next decision. |
| [Domain Transitions](ai-security-08-domain-transitions.md) | Load when evidence changes domain, identity boundary, execution surface, or network position. | Return evidence, capability changes, affected paths, and the next decision. |
| [Recollect When](ai-security-09-recollect-when.md) | Load after gaining a new identity, privilege, asset, role, trust edge, or network position. | Return evidence, capability changes, affected paths, and the next decision. |
