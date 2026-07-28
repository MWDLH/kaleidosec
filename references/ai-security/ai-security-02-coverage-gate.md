# AI Application, LLM, Agent, And RAG Operations: Coverage Gate

> Apply [../module-continuity.md](../module-continuity.md). Inherit the engagement, parent path, current capability, evidence, authorization profile, and module stack. Do not initialize a separate workflow. Checkpoint material results and return them to the parent path before leaving this card.

## Coverage Gate

Before AI-specific testing, understand:

| Layer | Key Questions |
|---|---|
| **User & tenant isolation** | Can User A's prompt context or conversation history be accessed by User B? Are vector store documents scoped per-tenant? |
| **System prompt** | What's in the system prompt? Does it contain secrets, internal URLs, tool API keys, or logic that can be extracted? |
| **Tools & plugins** | What tools does the agent have? (API calls, code execution, file read/write, database queries, email send) What identity does each tool run as? |
| **Retrieval pipeline** | Where does RAG pull documents from? (Confluence, SharePoint, internal wiki, customer data) Is retrieval access-controlled per-user? |
| **File/URL ingestion** | Can users upload files or provide URLs for the model to process? What file types? What processing pipeline? |
| **Memory & context** | How long is conversation history retained? Is memory shared across users? Can prior conversations be retrieved? |
| **Output handling** | Is model output rendered as HTML? (XSS) Used in SQL queries? (SQLi) Passed to a shell? (command injection) |
| **Human approval** | Which actions require human approval? Can approval be bypassed by prompt injection? |
| **Model supply chain** | Which model? (OpenAI, Anthropic, open-source, fine-tuned) Custom adapters? Downloaded from where? |

---


## Card Exit

Classify the result, update evidence and attempted methods, record capability or risk changes, identify affected paths, and apply the return contract in [../module-continuity.md](../module-continuity.md).
