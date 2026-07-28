# AI Application, LLM, Agent, And RAG Operations: Interpret Results

> Apply [../module-continuity.md](../module-continuity.md). Inherit the engagement, parent path, current capability, evidence, authorization profile, and module stack. Do not initialize a separate workflow. Checkpoint material results and return them to the parent path before leaving this card.

## Interpret Results

AI testing requires repeated trials. Model output is non-deterministic; a single success or failure is not conclusive.

- **Stochastic behavior**: Run each test at least 5 times with identical inputs (use temperature=0 if possible). Report success rate: "Prompt injection succeeded in 4/5 trials."
- **Model refusal vs application filtering**: The model may refuse a request while the application-level filter would also have blocked it. Test with both obfuscated and direct prompts to distinguish.
- **Tool authorization vs model behavior**: If the model attempts a tool call but the tool's backend rejects it (403 Forbidden) — the tool is secure, but the model's behavior is still worth noting.
- **Provider/model differences**: Note the exact model, provider, and configuration. A vulnerability in GPT-4o may not exist in Claude or Gemini, and vice versa.

---


## Card Exit

Classify the result, update evidence and attempted methods, record capability or risk changes, identify affected paths, and apply the return contract in [../module-continuity.md](../module-continuity.md).
