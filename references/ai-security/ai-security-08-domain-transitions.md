# AI Application, LLM, Agent, And RAG Operations: Domain Transitions

> Apply [../module-continuity.md](../module-continuity.md). Inherit the engagement, parent path, current capability, evidence, authorization profile, and module stack. Do not initialize a separate workflow. Checkpoint material results and return them to the parent path before leaving this card.

## Domain Transitions

- **→ Web/API**: For application controls (auth, rate limiting, HTML rendering of output), backend APIs, and traditional web testing of the chat/file upload interface
- **→ cloud**: For hosted model endpoints, vector databases (Pinecone, Weaviate, pgvector), and storage buckets for uploaded files
- **→ code-audit**: For agent orchestration code, tool implementations, custom adapters, and RAG pipelines
- **→ supply-chain**: For model supply chain (HuggingFace models, fine-tuning datasets, custom adapters, plugin registries)


## Main Attack Chain

1. **Map input surface**: Identify which user inputs reach the model (chat, file upload, URL fetch, email processing, API parameters) and which tools/functions the model can call.
2. **Establish baseline**: Normal model behavior, refusal patterns, tool call conditions, and approval gates under benign inputs.
3. **Controlled injection**: Test direct, indirect, and tool-response injection against the identified input surface with controlled, non-destructive objectives (read a test document, call a read-only tool).
4. **Observe boundary crossing**: Does the injection cause a tool call, data access, or output that crosses a security boundary? A model saying "I'll help you hack" is not a finding; a model calling `send_email(to=attacker, body=admin_data)` is.
5. **Verify backend authorization**: The model calling a tool is one step. Verify that the tool's backend actually executed the action and returned protected data — a model claiming it called a tool is not evidence unless the tool's effect is independently observed.
6. **Prove minimal impact**: Use the smallest proof that demonstrates the boundary violation — a single unauthorized data retrieval, a single tool call with elevated scope, a single document retrieved from another tenant.
7. **Return to parent domain**: AI findings almost always chain into another domain. Tool access → Web/API or Cloud. RAG poisoning → Web/API (upload endpoints). Model supply chain → Supply-chain. Hosted model endpoint → Cloud. Agent identity → Identity-network.

## Transition Handoff

Carry the model and provider, application session and identity, prompt or file entry point, tool or function schema, RAG source and retrieval evidence, observed model or tool behavior, hosting clues, trust boundary, and the exact destination question.

## Card Exit

Classify the result, update evidence and attempted methods, record capability or risk changes, identify affected paths, and apply the return contract in [../module-continuity.md](../module-continuity.md).
