# Internal Network, Host, And Identity Operations: Credential Dumping Decision Matrix

> Apply [../module-continuity.md](../module-continuity.md). Inherit the engagement, parent path, current capability, evidence, authorization profile, and module stack. Do not initialize a separate workflow. Checkpoint material results and return them to the parent path before leaving this card.

## Credential Dumping Decision Matrix

### Authorization Context

Extraction and use are two independent authorization decisions:

- **Permission enumeration and path modeling**: L1.
- **Constrained replication verification against a single controlled test account**: L2 only when the authorization profile explicitly includes this action.
- **Extraction of privileged accounts, KRBTGT, bulk user material, or domain-wide credential data**: L3 — classified by scale, sensitivity, and actual impact.
- **Modifying ACLs to obtain replication rights**: L3.

### LSASS Dumping — Tool vs EDR Evasion

LSASS access itself is a high-fidelity detection signal regardless of which tool or process performs it. Tool signature or LOLBin identity does not downgrade the behavioral detection profile.

| Method | Tool | Detection Risk | Authorization | Notes |
|---|---|---|---|---|
| Direct LSASS read | Mimikatz `sekurlsa::logonpasswords` | Extreme | L2 on owned host | Every major EDR catches in-memory Mimikatz |
| Process dump + offline | procdump → mimikatz offline | High | L2 on owned host | procdump.exe -accepteula -ma `<lsass_pid>` lsass.dmp; procdump is signed but LSASS access behavior is flagged regardless of tool signature |
| Task Manager dump | Task Manager → dump file | High — LSASS access behavior is the primary signal | L2 on owned host | Requires GUI or RDP session. Whether Task Manager can create an LSASS dump depends on privilege level, PPL status, Credential Guard configuration, OS version, and security product intervention. Using a system component does not guarantee lower detection or protection bypass. |
| Comsvcs.dll dump | `rundll32.exe C:\windows\System32\comsvcs.dll MiniDump <pid> lsass.dmp full` | High — LSASS access behavior remains the primary signal | L2 on owned host | LOLBin identity does not reduce behavioral detection; works on Win10+/Server2016+ |
| Custom tool/reflective | Custom DLL, Donut, process injection | Variable | L2 on owned host | Requires custom development; detection depends on injection method, tool signature, and behavioral indicators |
| SamDump | reg save SAM/SYSTEM + offline secretsdump | High | L2 on owned host | Requires admin + disk write for registry export; SAM contains local accounts only, not domain credentials |
| NTDS.dit dump | ntdsutil or vssadmin + diskshadow on a DC | Very High | **L3** — extracts entire domain credential database | Domain controller only; shadow copy creation is heavily monitored |
| DCSync | Mimikatz `lsadump::dcsync` or impacket-secretsdump | High | L2 only for constrained verification against a controlled test account when explicitly authorized; L3 for privileged accounts, KRBTGT, or bulk replication | Replication traffic may be logged as Event 4662 when the appropriate Directory Service Access audit policy and SACL are configured; the absence of 4662 does not prove replication did not occur |

### DCSync — Capability Evidence

DCSync of password material normally requires both DS-Replication-Get-Changes and DS-Replication-Get-Changes-All on the domain naming context; replication of attributes in the filtered set can additionally require DS-Replication-Get-Changes-In-Filtered-Set. Verify the effective ACEs and requested data instead of treating one replication right as sufficient.

```bash
# Impacket (Linux)
impacket-secretsdump <domain>/<user>:<password>@<dc_ip> -just-dc-user krbtgt
# Mimikatz (Windows)
mimikatz # lsadump::dcsync /domain:<domain> /user:krbtgt
```

**Detection context**: Event 4662 with GUID `1131f6ad-9c07-11d1-f79f-00c04fc2dcd2` requires the Directory Service Access audit subcategory and a SACL on the domain object. Without these, the event is not generated. Replication from an unexpected source is typically highly suspicious, but legitimate replication agents (Entra Connect, identity sync, migration tools, directory management components) may originate from non-DC IPs — compare against the authorized replication topology and network baseline.

**What DCSync gives you vs what it doesn't**: DCSync extracts password hashes and Kerberos keys for any principal. It does not grant that principal's group membership, session tokens, or access to resources requiring interactive logon. A KRBTGT hash from DCSync enables Golden Ticket forgery — L3, requires separate approval.

### Post-Extraction: Credential Material Lifecycle

| Material | Lifetime | What It Enables | Authorization |
|---|---|---|---|
| Cleartext password | Until user changes password | Full interactive and network logon | Depends on source and scale |
| NTLM hash | Until user changes password | NTLM pass-the-hash where supported, RC4-based Kerberos key use where permitted, and offline analysis | Highly sensitive but not technically equivalent to cleartext; it cannot satisfy every protocol or key derivation that requires the password |
| AES Kerberos key | Until user changes password or key rotation | Overpass-the-Hash (TGT request) | Same as the password |
| TGT | Domain-policy lifetime | Request TGS as the ticket identity | Classify by identity privilege, reachable scope, source, and intended use; extraction from an owned host does not automatically make use L2 |
| TGS | Ticket lifetime | Access the ticket's SPN as the ticket identity | Classify by service, identity privilege, source, and intended use; scope is narrower than a TGT but may still be high impact |
| KRBTGT hash | Until KRBTGT password change (twice for full invalidation) | Golden Ticket — the forger may specify a long lifetime; actual acceptance is constrained by KDC validation, key rotation, PAC validation, and security controls | **L3** — domain-wide, durable impersonation capability |


## Card Exit

Classify the result, update evidence and attempted methods, record capability or risk changes, identify affected paths, and apply the return contract in [../module-continuity.md](../module-continuity.md).
