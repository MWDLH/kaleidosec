# PoC, Debugging, And Tool Engineering Capability


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
| [Build For A Decision](poc-tooling-01-build-for-a-decision.md) | Entry: a script or PoC is needed to answer one specific question. | Which decision depends on this artifact, and what is the smallest thing that answers it? |
| [PoC Patterns By Vulnerability Class](poc-tooling-02-poc-patterns-by-vulnerability-class.md) | Vulnerability class identified; a validation artifact must be constructed. | Which pattern fits this class, and what would falsify it? |
| [Debugging Unstable Techniques](poc-tooling-03-debugging-unstable-techniques.md) | Intermittent success, environment-dependent behavior or inconsistent results. | Which variable differs between runs, and how do we isolate it? |
| [Tool Engineering: When to Write vs When to Use Existing](poc-tooling-04-tool-engineering-when-to-write-vs-when-to-use-existing.md) | Existing tooling is missing, blocked or unsuitable for the bounded question. | Is writing justified by the gap, and what is the maintenance cost? |
| [Return To Parent Path](poc-tooling-05-return-to-parent-path.md) | Before returning results to the parent attack path. | What changed, and which parent paths must be re-ranked? |
