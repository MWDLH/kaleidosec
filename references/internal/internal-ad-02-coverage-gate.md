# Internal Network, Host, And Identity Operations: Coverage Gate

> Apply [../module-continuity.md](../module-continuity.md). Inherit the engagement, parent path, current capability, evidence, authorization profile, and module stack. Do not initialize a separate workflow. Checkpoint material results and return them to the parent path before leaving this card.

## Coverage Gate

Before privilege escalation or lateral movement, confirm:

| Knowledge | Required Detail | Why It Matters |
|---|---|---|
| Current privilege | Local admin? Domain user? Domain admin? Service account? SYSTEM? | Determines available attack techniques |
| Domain membership | Domain name, forest, functional level, trust relationships | Defines scope of movement |
| Reachable management protocols | SMB (445), WinRM (5985/5986), RDP (3389), SSH (22), WMI (135+dynamic), LDAP (389/636) | Each protocol enables different lateral techniques |
| Critical trust edges | Domain admins group members, high-value groups, privileged service accounts | Prioritizes targets |
| Defensive controls | AV/EDR present, PowerShell logging, AMSI, AppLocker, network segmentation | Determines tool and technique selection |
| Credential availability | Any known passwords, hashes, tickets, or keys — validated or unvalidated | Enables or blocks many techniques |

**A credential that failed to authenticate is not necessarily invalid.** Separate: wrong protocol (NTLM vs Kerberos), account restrictions (logon hours, workstation restriction, smart card required), target policy (local account vs domain, admin approval mode), and network filtering.

---


## Card Exit

Classify the result, update evidence and attempted methods, record capability or risk changes, identify affected paths, and apply the return contract in [../module-continuity.md](../module-continuity.md).
