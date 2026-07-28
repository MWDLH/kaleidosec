# Mobile Operations: Domain Transitions

> Apply [../module-continuity.md](../module-continuity.md). Inherit the engagement, parent path, current capability, evidence, authorization profile, and module stack. Do not initialize a separate workflow. Checkpoint material results and return them to the parent path before leaving this card.

## Domain Transitions

- **→ Web/API**: Backend testing is always higher priority than purely local attacks. Carry the discovered endpoints, auth tokens, and API structure.
- **→ reverse-protocol**: For native library analysis, custom protocol reverse engineering, or cryptographic key extraction from binary.
- **→ code-audit**: For recovered source code or JS bundles that contain server-side logic hints.
- **→ cloud**: For mobile backends hosted on cloud platforms (Firebase, AWS Amplify, Azure Mobile Apps).


## Transition Handoff

Carry the package, build, platform, and device context; discovered endpoints and API versions; user, tenant, token, and device-binding state; request signing or cryptographic fields; relevant runtime or pinning observations; and the exact backend or reverse-engineering question.

## Card Exit

Classify the result, update evidence and attempted methods, record capability or risk changes, identify affected paths, and apply the return contract in [../module-continuity.md](../module-continuity.md).
