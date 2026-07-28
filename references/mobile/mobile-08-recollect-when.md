# Mobile Operations: Recollect When

> Apply [../module-continuity.md](../module-continuity.md). Inherit the engagement, parent path, current capability, evidence, authorization profile, and module stack. Do not initialize a separate workflow. Checkpoint material results and return them to the parent path before leaving this card.

## Recollect When

Recollect after:
- Changing application role (regular user → admin, via backend authorization flaw)
- Finding a new backend environment (dev/staging/prod — token from one works on another?)
- Extracting credentials from local storage or binary
- Bypassing certificate pinning (you now have API visibility)
- Changing app version (old version may have unfixed issues, new version may have new attack surface)
- Finding a hidden/debug endpoint or feature flag in the binary

## Card Exit

Classify the result, update evidence and attempted methods, record capability or risk changes, identify affected paths, and apply the return contract in [../module-continuity.md](../module-continuity.md).
