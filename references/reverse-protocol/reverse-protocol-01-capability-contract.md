# Reverse Engineering And Protocol Capability: Capability Contract

> Apply [../module-continuity.md](../module-continuity.md). Inherit the engagement, parent path, current capability, evidence, authorization profile, and module stack. Do not initialize a separate workflow. Checkpoint material results and return them to the parent path before leaving this card.

## Capability Contract

Record parent_path, capability_question, artifact identity and hash (SHA256), platform and architecture, expected deliverable, and return condition. Preserve the original artifact.

**Example of a well-scoped reverse engineering task**:
```
Parent path: mobile-backend-authorization
Capability question: How does the native library libsign.so construct the X-Signature header?
Artifact: libsign.so, SHA256: abc123..., platform: Android ARM64
Expected deliverable: The signing algorithm (or pseudo-code), key material source, whether key is extractable
Return condition: Enough information to test whether the backend trusts client-controlled signing parameters
```

This is NOT an open-ended "reverse this APK." This is "answer this specific question so the mobile path can continue."

---


## Card Exit

Classify the result, update evidence and attempted methods, record capability or risk changes, identify affected paths, and apply the return contract in [../module-continuity.md](../module-continuity.md).
