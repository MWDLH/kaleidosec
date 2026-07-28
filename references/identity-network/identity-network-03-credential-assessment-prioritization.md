# Identity, Credential, Trust, And Network Capability: Credential Assessment — Prioritization

> Apply [../module-continuity.md](../module-continuity.md). Inherit the engagement, parent path, current capability, evidence, authorization profile, and module stack. Do not initialize a separate workflow. Checkpoint material results and return them to the parent path before leaving this card.

## Credential Assessment — Prioritization

When you have multiple credentials, prioritize by effective value:

```yaml
rank_by:
  1_changes_identity_boundary: "Does this credential cross a trust boundary (user→admin, one tenant→another, external→internal, cloud account→workload, low_privilege→high_privilege)?"
  2_unlocks_new_assets: "Does it grant access to a previously unreachable asset class (database, source code, cloud console, DC, CI/CD, file share)?"
  3_chain_leverage: "Does it enable a path that unlocks other higher-value paths?"
  4_durability: "How long is it valid? Password (indefinite until changed) > NTLM hash (until password change) > Kerberos TGT (10h) > OAuth token (1h) > AWS STS (15min-1h)"
  5_detection_risk: "Is using this credential likely to trigger alerts? (Admin reconfigure actions > lateral movement > enumerating shares > read-only API calls)"
```

---


## Card Exit

Classify the result, update evidence and attempted methods, record capability or risk changes, identify affected paths, and apply the return contract in [../module-continuity.md](../module-continuity.md).
