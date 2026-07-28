# Internal Network, Host, And Identity Operations: ACL Abuse Primitives

> Apply [../module-continuity.md](../module-continuity.md). Inherit the engagement, parent path, current capability, evidence, authorization profile, and module stack. Do not initialize a separate workflow. Checkpoint material results and return them to the parent path before leaving this card.

## ACL Abuse Primitives

Active Directory ACLs control delegation of permissions. Abuse means: a principal you control has a dangerous right over a higher-privileged object.

### Quick Reference: Dangerous ACLs and Their Exploitation

| ACE Right | On What Object | Exploitation Method | Effective Permission Gained |
|---|---|---|---|
| **GenericAll / FullControl** | User | Reset password, or perform Targeted Kerberoasting (set SPN + kerberoast) | That user's identity |
| **GenericAll / FullControl** | Group | Add yourself to the group | Group membership |
| **GenericAll / FullControl** | Computer | RBCD attack (write msDS-AllowedToActOnBehalfOfOtherIdentity) | SYSTEM on that computer |
| **GenericWrite** | User | Write to userAccountControl (disable pre-auth for AS-REP) or write logonScript path | Code execution when user logs in |
| **GenericWrite** | Group | Write to `member` attribute | Group membership |
| **GenericWrite** | Computer | RBCD (write msDS-AllowedToActOnBehalfOfOtherIdentity) | SYSTEM on that computer |
| **WriteDacl** | Any object | Grant yourself GenericAll over the object | Full control over target |
| **WriteOwner** | Any object | Take ownership, then modify DACL to grant GenericAll | Full control over target |
| **ForceChangePassword** | User | Reset user's password without knowing current one | That user's identity |
| **Self (Self-Membership)** | Group | Add yourself to the group | Group membership |
| **AddMember** | Group | Add a principal to group (specific to ms-DS-Group-ManagedServiceAccount) | Group membership |
| **WriteProperty (member)** | Group | Modify group membership | Group membership |
| **WriteProperty (servicePrincipalName)** | User | Set SPN on user account, then Kerberoast it | User's password hash (offline crack) |
| **WriteProperty (scriptPath)** | User | Set logon script path to attacker-controlled SMB share | Code execution at user logon |
| **WriteProperty (msDS-KeyCredentialLink)** | User/Computer | Shadow Credentials — add alternative key for PKINIT authentication | Authenticate as that principal |
| **ExtendedRight (User-Force-Change-Password)** | User | Reset password | That user's identity |
| **ExtendedRight (DS-Replication-Get-Changes)** | Domain | DCSync — replicate credentials from DC | All domain hashes |

### Using BloodHound

BloodHound is a graph analysis tool, not a scanner. It's only useful when collection is complete and edge data is accurate.

```powershell
# SharpHound collector (choose ONE; don't run all)
SharpHound.exe -c All                        # Full collection — highest noise
SharpHound.exe -c DCOnly                     # DC-only — lowest noise, essential edges
SharpHound.exe -c Session,LoggedOn           # Session/LoggedOn — moderate noise
SharpHound.exe -c Group,Domain,Trusts,ACL    # Structural data — low noise
```

**Interpreting BloodHound edges**:
- `CanRDP`/`CanPSRemote`/`ExecuteDCOM` → Lateral movement edges
- `HasSession`/`AdminTo` → Where privileged sessions exist or admin access is possible
- `GenericAll`/`WriteDacl`/`WriteOwner` → ACL abuse paths
- `MemberOf` → Group membership path to higher privilege
- `TrustedBy` → Cross-domain/forest attack paths
- `AllowedToDelegate` → Delegation-based privilege escalation

**Cypher queries for common analysis**:
```
// Shortest path to Domain Admins from owned principals
MATCH p=shortestPath((n)-[*1..]->(m:Group {name:'DOMAIN ADMINS@DOMAIN.LOCAL'})) WHERE n.owned RETURN p

// All computers where Domain Admins have sessions
MATCH (u:User)-[:MemberOf*1..]->(g:Group {name:'DOMAIN ADMINS@DOMAIN.LOCAL'}) WITH u
MATCH (c:Computer) WHERE c.HasSession CONTAINS u.name RETURN c.name, u.name

// All Kerberoastable users (users with SPN)
MATCH (u:User {hasspn:true}) RETURN u.name

// All unconstrained delegation computers
MATCH (c:Computer {unconstraineddelegation:true}) RETURN c.name

// Users with path to Domain Admins via ACL abuse (not group membership)
MATCH p=shortestPath((n:User)-[{isacl:true}*1..]->(m:Group {name:'DOMAIN ADMINS@DOMAIN.LOCAL'})) RETURN p
```

---


## Card Exit

Classify the result, update evidence and attempted methods, record capability or risk changes, identify affected paths, and apply the return contract in [../module-continuity.md](../module-continuity.md).
