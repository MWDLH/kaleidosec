# Infrastructure, VPN, Middleware, And Desktop Operations


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
| [Build The Surface](infrastructure-desktop-01-build-the-surface.md) | Entry: exposed hosts, ports or appliances not yet fingerprinted. | Which infrastructure surfaces and fingerprints matter, and what is the bounded question? |
| [Attack Primitives: Unauthenticated/Default Credential Services](infrastructure-desktop-02-attack-primitives-unauthenticated-default-credential-services.md) | Management ports open (SSH/RDP/DB/middleware consoles) and service banners respond. | Which service admits unauthenticated or default access, and what bounds the test? |
| [Attack Primitives: Desktop & Thick Client](infrastructure-desktop-03-attack-primitives-desktop-thick-client.md) | Desktop client, local service or update channel discovered. | Which client-side weakness yields data or execution, and what proves it? |
| [Attack Primitives: VPN & Network Appliances](infrastructure-desktop-04-attack-primitives-vpn-network-appliances.md) | VPN, firewall, load balancer or bastion fingerprint identified. | Which appliance weakness is reachable, and what is its blast radius? |
| [Interpret Results](infrastructure-desktop-05-interpret-results.md) | After any material result, positive or negative. | What does this prove, and does it change the path ranking? |
| [Domain Transitions](infrastructure-desktop-06-domain-transitions.md) | Evidence implies a different domain, identity boundary, execution surface or network position. | Where are we now, what authority do we hold, and what is the return target? |
| [Recollect When](infrastructure-desktop-07-recollect-when.md) | New identity, privilege, asset, role, trust edge or network position. | What must be re-collected, and what evidence can be safely reused? |
