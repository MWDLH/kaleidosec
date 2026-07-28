# Code Audit Capability: Return To Parent Path

> Apply [../module-continuity.md](../module-continuity.md). Inherit the engagement, parent path, current capability, evidence, authorization profile, and module stack. Do not initialize a separate workflow. Checkpoint material results and return them to the parent path before leaving this card.

## Return To Parent Path

Return:
1. **Confirmed vulnerabilities**: Entry point, data flow, sink, impact, confidence level, validation method
2. **Suspicious but unverified**: Requires runtime testing, requires specific environment, requires dependency chain verification
3. **Safe areas**: Functions/data flows that were audited and found not exploitable
4. **Not audited**: Code areas that exist but weren't in scope of this capability invocation

A dangerous function IS NOT a vulnerability by itself. Always verify: input source, data path, validation/transformation applied, prerequisite conditions, and exploitability.

## Card Exit

Classify the result, update evidence and attempted methods, record capability or risk changes, identify affected paths, and apply the return contract in [../module-continuity.md](../module-continuity.md).
