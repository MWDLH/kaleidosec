# PoC, Debugging, And Tool Engineering Capability


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
| [Build For A Decision](poc-tooling-01-build-for-a-decision.md) | Load on entry to establish position, prerequisites, and the bounded question. | Return evidence, capability changes, affected paths, and the next decision. |
| [PoC Patterns By Vulnerability Class](poc-tooling-02-poc-patterns-by-vulnerability-class.md) | Load only when current evidence supports the PoC Patterns By Vulnerability Class route or its prerequisite must be tested. | Return evidence, capability changes, affected paths, and the next decision. |
| [Debugging Unstable Techniques](poc-tooling-03-debugging-unstable-techniques.md) | Load only when current evidence supports the Debugging Unstable Techniques route or its prerequisite must be tested. | Return evidence, capability changes, affected paths, and the next decision. |
| [Tool Engineering: When to Write vs When to Use Existing](poc-tooling-04-tool-engineering-when-to-write-vs-when-to-use-existing.md) | Load only when current evidence supports the Tool Engineering: When to Write vs When to Use Existing route or its prerequisite must be tested. | Return evidence, capability changes, affected paths, and the next decision. |
| [Return To Parent Path](poc-tooling-05-return-to-parent-path.md) | Load before returning capability results to the parent attack path. | Return evidence, capability changes, affected paths, and the next decision. |
