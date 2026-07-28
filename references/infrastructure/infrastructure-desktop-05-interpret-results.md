# Infrastructure, VPN, Middleware, And Desktop Operations: Interpret Results

> Apply [../module-continuity.md](../module-continuity.md). Inherit the engagement, parent path, current capability, evidence, authorization profile, and module stack. Do not initialize a separate workflow. Checkpoint material results and return them to the parent path before leaving this card.

## Interpret Results

- **Service unavailability**: Timeout could be firewall blocking, not the service being down. Check from multiple network positions.
- **Protocol negotiation mismatch**: TLS version/cipher mismatch between client and server — not a vulnerability unless the server supports weak ciphers.
- **Certificate failure**: Self-signed cert? Expired? Wrong hostname? Common in internal networks — note it but severity depends on context.
- **Default credentials used**: Always a finding. Always report.
- **Unauthenticated access to data service**: Always a finding. Always report.

---


## Card Exit

Classify the result, update evidence and attempted methods, record capability or risk changes, identify affected paths, and apply the return contract in [../module-continuity.md](../module-continuity.md).
