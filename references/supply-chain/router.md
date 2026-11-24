# CI/CD And Software Supply-Chain Operations


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
| [Build The Delivery Graph](supply-chain-01-build-the-delivery-graph.md) | Entry: code-to-production path not yet mapped (repo, CI, registry, deploy). | What is the delivery graph, and which node is the cheapest leverage point? |
| [Build The Surface — Practical Enumeration](supply-chain-02-build-the-surface-practical-enumeration.md) | Repository, CI configuration or artifact location obtained. | Which build and artifact surfaces are reachable, and what is the first probe? |
| [Attack Primitives: CI/CD Pipeline Attacks](supply-chain-03-attack-primitives-ci-cd-pipeline-attacks.md) | Pipeline config, runner registration, secrets references or PR-triggered workflows visible. | Which pipeline weakness yields code execution or secret access, and what proves it? |
| [Attack Primitives: Registry & Deployment Attacks](supply-chain-04-attack-primitives-registry-deployment-attacks.md) | Private registry, unsigned artifacts or deployment credentials/paths discovered. | Which registry or deployment weakness is exploitable, and what is the blast radius? |
| [Interpret Results](supply-chain-05-interpret-results.md) | After any material result, positive or negative. | What does this prove, and does it change the path ranking? |
| [Domain Transitions](supply-chain-06-domain-transitions.md) | Evidence implies a different domain, identity boundary, execution surface or network position. | Where are we now, what authority do we hold, and what is the return target? |
| [Recollect When](supply-chain-07-recollect-when.md) | New identity, privilege, asset, role, trust edge or network position. | What must be re-collected, and what evidence can be safely reused? |
