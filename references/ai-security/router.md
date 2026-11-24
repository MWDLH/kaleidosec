# AI Application, LLM, Agent, And RAG Operations


## Continuity And Loading Rules

Read [../module-continuity.md](../module-continuity.md) before invoking a card. Keep one engagement state and one attack-path graph across all cards and domains.

1. Load entry and coverage cards first when they exist.
2. Load only the technical card supported by current evidence; do not enumerate cards as a checklist.
3. Keep the current parent path unless evidence creates a genuinely independent path.
4. Checkpoint before a domain transition and after a card returns material evidence.
5. When multiple domains cooperate, keep one primary domain and record supporting domains in state.

## Card Router

| Card | Load when evidence shows (field / response signature) | Must answer after loading |
|---|---|---|
| [Model The System](ai-security-01-model-the-system.md) | Entry: model, tools, retrieval and trust boundaries not yet mapped. | Which data flows cross the model, and where is trust assumed? |
| [Coverage Gate](ai-security-02-coverage-gate.md) | Before the first material validation, and after any capability or position change. | Which surfaces are covered, which are not, and is the next action justified anyway? |
| [Attack Primitives: Prompt Injection](ai-security-03-attack-primitives-prompt-injection.md) | User input reaches model context and model output influences tools, data or decisions. | Does injected instruction change behavior, and what observable proves it? |
| [Attack Primitives: Tool/Function Calling Abuse](ai-security-04-attack-primitives-tool-function-calling-abuse.md) | Model can invoke tools or functions whose parameters derive from input or retrieved content. | Which tool call can be steered, and what is the least harmful proof? |
| [Attack Primitives: RAG / Knowledge Base Attacks](ai-security-05-attack-primitives-rag-knowledge-base-attacks.md) | Retrieval source is writable, shared across tenants, or of unknown provenance. | Can poisoned or cross-tenant content reach the answer, and what proves it? |
| [Attack Primitives: File/URL Processing](ai-security-06-attack-primitives-file-url-processing.md) | Input triggers file parsing or URL fetching (upload, link preview, fetch tool). | Which parser or fetcher is reachable (SSRF/XXE/deserialization), and what bounds it? |
| [Interpret Results](ai-security-07-interpret-results.md) | After any material result, positive or negative. | What does this prove, and does it change the path ranking? |
| [Domain Transitions](ai-security-08-domain-transitions.md) | Evidence implies a different domain, identity boundary, execution surface or network position. | Where are we now, what authority do we hold, and what is the return target? |
| [Recollect When](ai-security-09-recollect-when.md) | New identity, privilege, asset, role, trust edge or network position. | What must be re-collected, and what evidence can be safely reused? |
