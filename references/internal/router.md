# Internal Network, Host, And Identity Operations


## Continuity And Loading Rules

Read [../module-continuity.md](../module-continuity.md) before invoking a card. Keep one engagement state and one attack-path graph across all cards and domains.

1. Load entry and coverage cards first when they exist.
2. Load only the technical card supported by current evidence; do not enumerate cards as a checklist.
3. Keep the current parent path unless evidence creates a genuinely independent path.
4. Checkpoint before a domain transition and after a card returns material evidence.
5. When multiple domains cooperate, keep one primary domain and record supporting domains in state.

## Card Router

| Card | Load when evidence shows (field / response signature) | Must answer after loading |
|---|---|---|
| [Establish Current Position](internal-ad-01-establish-current-position.md) | Entry: no domain membership, network position or held-credential model yet. | What position and authority do we have, and what is the bounded question? |
| [Coverage Gate](internal-ad-02-coverage-gate.md) | Before the first material validation, and after any capability or position change. | Which surfaces are covered, which are not, and is the next action justified anyway? |
| [Kerberos Route Selection](internal-ad-03-kerberos-attack-primitives.md) | Kerberos services reachable (88/464), SPNs exposed, TGT/TGS traffic, clock skew, delegation flags. | Which Kerberos primitive fits this evidence, and what precondition is missing? |
| [Basic Internal Network Attacks](internal-ad-04-basic-internal-network-attacks.md) | Reachable SMB/LDAP/RDP/WinRM, NTLM relay surface, null sessions, anonymous binds. | Which unauthenticated or relay path is live, and what bounds the test? |
| [ACL Abuse Primitives](internal-ad-05-acl-abuse-primitives.md) | Domain user held and object ACLs readable; `GenericAll`, `WriteDACL`, `WriteOwner` or similar edges visible. | Which ACL edge yields the next privilege, and what is its blast radius? |
| [Active Directory Certificate Services (AD CS) Attack Primitives](internal-ad-06-active-directory-certificate-services-ad-cs-attack-primitives.md) | CA reachable (`/certsrv`), certificate templates enumerable, enrollment rights exposed. | Which template misconfiguration is exploitable, and what is the rollback? |
| [Lateral Movement Decision Tree](internal-ad-07-lateral-movement-decision-tree.md) | Usable credential, hash or ticket held; multiple reachable hosts. | Which target/method pair maximizes gain per unit of risk? |
| [Credential Dumping Decision Matrix](internal-ad-08-credential-dumping-decision-matrix.md) | Local admin or SYSTEM equivalent obtained on a host. | Which credential source is worth touching, and what is the approval class? |
| [LOLBin & Living Off The Land](internal-ad-09-lolbin-living-off-the-land.md) | Execution needed without dropping tools, or EDR blocks conventional binaries. | Which native binary performs the action, and what is logged? |
| [Trust Hopping](internal-ad-10-trust-hopping.md) | Domain trusts visible (`trustedDomain`), cross-domain SIDs, forest or external trust edges. | Which trust edge is traversable with current authority, and what proves it? |
| [Post-Exploitation Cleanup Tracking](internal-ad-11-post-exploitation-cleanup-tracking.md) | After any persistence, dropped file, account change or configuration change. | What must be rolled back, what remains, and who owns the handoff? |
| [Domain Transitions](internal-ad-12-domain-transitions.md) | Evidence implies a different domain, identity boundary, execution surface or network position. | Where are we now, what authority do we hold, and what is the return target? |
| [Recollect When](internal-ad-13-recollect-when.md) | New identity, privilege, asset, role, trust edge or network position. | What must be re-collected, and what evidence can be safely reused? |
