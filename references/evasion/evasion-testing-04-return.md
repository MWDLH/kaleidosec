# Authorized Control-Evasion And Environment Adaptation: Return

> Apply [../module-continuity.md](../module-continuity.md). Inherit the engagement, parent path, current capability, evidence, authorization profile, and module stack. Do not initialize a separate workflow. Checkpoint material results and return them to the parent path before leaving this card.

## Return

Return:
1. **Control layer identified**: What was blocking, evidence it was the cause
2. **Evasion attempted**: Method, result, any detection alerts triggered
3. **Residual risk**: Did the evasion leave artifacts? Disable protections? Create a detection gap?
4. **Cleanup status**: Reverted? (AMSI patch → process exit reverts it. AppLocker bypass → temporary.)
5. **Parent path continuation**: Can the parent path now proceed? With what limitations?

**Never**: Disable logging, clear event logs, remove security agents, or modify group policy to make evasion easier. These actions are outside the scope of authorized testing.

## Card Exit

Classify the result, update evidence and attempted methods, record capability or risk changes, identify affected paths, and apply the return contract in [../module-continuity.md](../module-continuity.md).
