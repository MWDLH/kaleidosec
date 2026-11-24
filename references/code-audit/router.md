# Code Audit Capability


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
| [Capability Contract](code-audit-01-capability-contract.md) | Entry: source code or repository available and a code question identified. | What decision will this audit serve, and what is out of scope? |
| [Language-Specific Sink Patterns](code-audit-02-language-specific-sink-patterns.md) | Language and framework confirmed; candidate sinks not yet located. | Which sinks in this language/framework are reachable from untrusted input? |
| [Audit Workflow By Codebase Type](code-audit-03-audit-workflow-by-codebase-type.md) | Codebase type identified (monolith, microservice, frontend, mobile). | Which audit workflow fits this codebase, and what order covers the most risk? |
| [Return To Parent Path](code-audit-04-return-to-parent-path.md) | Before returning results to the parent attack path. | What changed, and which parent paths must be re-ranked? |
