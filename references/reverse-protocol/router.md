# Reverse Engineering And Protocol Capability


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
| [Capability Contract](reverse-protocol-01-capability-contract.md) | Entry: binary, app or protocol sample available and a reverse decision identified. | What decision will reversing serve, and what is the minimum to answer it? |
| [Workflow By Target Type](reverse-protocol-02-workflow-by-target-type.md) | Target type confirmed (APK, SO, PE, Mach-O, firmware, custom protocol). | Which workflow fits this target type, and what toolchain does it require? |
| [Return To Parent Path](reverse-protocol-03-return-to-parent-path.md) | Before returning results to the parent attack path. | What changed, and which parent paths must be re-ranked? |
