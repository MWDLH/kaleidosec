# Web And API Operations: Domain Transitions

> Apply [../module-continuity.md](../module-continuity.md). Inherit the engagement, parent path, current capability, evidence, authorization profile, and module stack. Do not initialize a separate workflow. Checkpoint material results and return them to the parent path before leaving this card.

## Domain Transitions

If code, package artifacts, mobile clients, cloud metadata, internal services, or custom protocols become important, invoke the matching capability or domain while preserving the Web path:

- **→ code-audit**: When source code, decompiled client, or JS bundle reveals server-side logic that needs tracing
- **→ reverse-protocol**: When custom serialization, binary protocol, or non-HTTP RPC is discovered
- **→ cloud**: When SSRF reveals cloud metadata, or application uses cloud services extensively
- **→ mobile**: When testing reveals a mobile-specific API version or authentication path
- **→ internal-ad**: When SSRF or file operations reach internal services
- **→ supply-chain**: When JS dependencies, CI/CD exposure, or build artifacts are discovered
- **→ business-logic**: When a multi-step business process handles value actions (payment, order, transfer, redemption, approval) and the server may trust client-supplied business data, state, or sequence

Carry forward: the specific endpoint/function/parameter being investigated, the identity context, and the security question to answer.


## Transition Handoff

Carry the exact URL, method, parameter or function; application, user, role, tenant, and session context; decisive request and response evidence; the primitive already proved; backend, internal, cloud, client, or build clues; and the specific question the destination must answer.

## Card Exit

Classify the result, update evidence and attempted methods, record capability or risk changes, identify affected paths, and apply the return contract in [../module-continuity.md](../module-continuity.md).
