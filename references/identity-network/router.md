# Identity, Credential, Trust, And Network Capability


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
| [Model Identity](identity-network-01-model-identity.md) | Entry: accounts, tokens or credentials held but their authority is unclear. | What does this identity actually authorize, and where does it fail? |
| [Model Network Position](identity-network-02-model-network-position.md) | Reachability or proxy/jump position unclear, or egress constraints observed. | What is reachable from here, and what is the cheapest way to prove it? |
| [Credential Assessment — Prioritization](identity-network-03-credential-assessment-prioritization.md) | Multiple credentials, hashes or tickets available. | Which credential yields the most authority per unit of risk? |
| [Return To Parent Path](identity-network-04-return-to-parent-path.md) | Before returning results to the parent attack path. | What changed, and which parent paths must be re-ranked? |
