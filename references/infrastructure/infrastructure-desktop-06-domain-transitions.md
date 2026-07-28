# Infrastructure, VPN, Middleware, And Desktop Operations: Domain Transitions

> Apply [../module-continuity.md](../module-continuity.md). Inherit the engagement, parent path, current capability, evidence, authorization profile, and module stack. Do not initialize a separate workflow. Checkpoint material results and return them to the parent path before leaving this card.

## Domain Transitions

- **→ reverse-protocol**: Custom protocols (S7 for Siemens, Modbus for ICS, bacnet for building management) that need binary analysis
- **→ code-audit**: For recovered firmware, Java/.NET thick client decompilation, configuration scripts
- **→ internal/AD**: If the infrastructure sits on a domain-joined network or uses AD authentication
- **→ Web/API**: For management web interfaces, REST APIs on appliances, and SSLVPN portals
- **→ evasion**: When attempting to bypass NAC, 802.1X, or network access control to reach restricted segments


## Main Attack Chain

1. **Product and version evidence**: Establish what the target is (vendor, product, version, build) from banners, SNMP, management interfaces, or firmware. A version fingerprint is the starting point — not the finding.
2. **Management plane and authentication boundary**: Identify how the device or application is managed (web, SSH, proprietary protocol, SNMP write). Test default credentials, unauthenticated access, and weak authentication.
3. **Minimal capability validation**: For an unauthenticated service (Redis, MongoDB, Elasticsearch), confirm data access with a single read. For an authenticated surface, confirm privilege with a single bounded command. Do not expand beyond the minimal proof at this stage.
4. **Transition to the exploited capability's primary domain**: Infrastructure findings almost always enable a downstream domain. Web management → Web/API. Custom protocol → Reverse/protocol. Domain-joined host → Internal/AD. Network segmentation bypass → re-enter from new position. Thick client backend → Web/API (test the API the client calls).

## Transition Handoff

Carry the product, version, device or host, management interface and protocol, network segment, identity or session context, exposed capability, topology and control observations, captured artifact references, and the exact protocol, code, Web, or identity question.

## Card Exit

Classify the result, update evidence and attempted methods, record capability or risk changes, identify affected paths, and apply the return contract in [../module-continuity.md](../module-continuity.md).
