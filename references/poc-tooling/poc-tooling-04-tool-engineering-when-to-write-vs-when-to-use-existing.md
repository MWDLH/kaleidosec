# PoC, Debugging, And Tool Engineering Capability: Tool Engineering: When to Write vs When to Use Existing

> Apply [../module-continuity.md](../module-continuity.md). Inherit the engagement, parent path, current capability, evidence, authorization profile, and module stack. Do not initialize a separate workflow. Checkpoint material results and return them to the parent path before leaving this card.

## Tool Engineering: When to Write vs When to Use Existing

| Scenario | Recommendation |
|---|---|
| Standard protocol (HTTP, SMB, LDAP) | Use existing tool. Write a wrapper script if automation is needed. |
| Custom protocol | Write a minimal client/server. Start with Python sockets + struct, not a full framework. |
| Payload generator | Write a small script. Python's `struct` and `bytes` are sufficient for most binary payloads. |
| Scanner/fuzzer | Use existing (ffuf, dirsearch, wfuzz) unless the target requires custom auth/encoding that existing tools can't handle. |
| Post-exploitation agent | Use existing C2 framework. Write custom modules only for target-specific operations. |

---


## Card Exit

Classify the result, update evidence and attempted methods, record capability or risk changes, identify affected paths, and apply the return contract in [../module-continuity.md](../module-continuity.md).
