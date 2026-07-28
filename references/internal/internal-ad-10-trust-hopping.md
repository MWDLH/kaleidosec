# Internal Network, Host, And Identity Operations: Trust Hopping

> Apply [../module-continuity.md](../module-continuity.md). Inherit the engagement, parent path, current capability, evidence, authorization profile, and module stack. Do not initialize a separate workflow. Checkpoint material results and return them to the parent path before leaving this card.

## Trust Hopping

### Recognizing Trust Relationships

```cmd
nltest /domain_trusts                     # list all trusts
nltest /domain_trusts /all_trusts /v      # detailed trust info
Get-ADTrust -Filter *                     # PowerShell AD module
```

### Trust Attack Paths

| Trust Type | Attack | Prerequisites |
|---|---|---|
| **Parent-Child** (default within forest) | Child DC → Parent domain via SID History (Golden Ticket with Enterprise Admins SID) | KRBTGT hash of child domain |
| **Two-way forest** | PTH/PTT across forest if same account exists in both forests and SID filtering is disabled | Credentials valid across trust; SID filtering disabled (rare in modern environments) |
| **External/Realm** | PTH/PTT to trusted domain with outbound trust direction | Credentials from trusting domain; may need to cross trust boundary |
| **Forest (selective authentication)** | Enumerate allowed authenticating principals; target those | Knowledge of which principals are allowed |

**SID History attack (cross-forest)**: When you have KRBTGT hash of any child domain in a forest, create a Golden Ticket with Enterprise Admins SID (S-1-5-21-<root-domain>-519) to gain Enterprise Admin in the entire forest. This works because SID History is trusted within a forest.

---


## Card Exit

Classify the result, update evidence and attempted methods, record capability or risk changes, identify affected paths, and apply the return contract in [../module-continuity.md](../module-continuity.md).
