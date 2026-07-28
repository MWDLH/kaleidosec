# Internal Network, Host, And Identity Operations: Domain Transitions

> Apply [../module-continuity.md](../module-continuity.md). Inherit the engagement, parent path, current capability, evidence, authorization profile, and module stack. Do not initialize a separate workflow. Checkpoint material results and return them to the parent path before leaving this card.

## Domain Transitions

- **→ cloud**: When hybrid identity (Azure AD Connect, AD FS) or cloud management (AWS Managed AD, Google Cloud Directory Sync) is discovered
- **→ code-audit**: When custom services, scripts in SYSVOL/NETLOGON, or GPO startup scripts need analysis
- **→ reverse-protocol**: When custom agents, appliances, or non-standard protocols are encountered
- **→ Web/API**: When management web interfaces (IIS admin, Exchange ECP, SharePoint) or internal APIs are found
- **→ evasion**: When defensive controls block necessary movement and a low-noise alternative is needed


## Transition Handoff

Carry the domain, forest, host, and network position; effective principal, group, privilege, ticket or credential references; reachable services, sessions, trust edges, and controls; the capability already proved; and the exact cloud, Web, code, or protocol question.

## Card Exit

Classify the result, update evidence and attempted methods, record capability or risk changes, identify affected paths, and apply the return contract in [../module-continuity.md](../module-continuity.md).
