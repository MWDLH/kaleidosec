# Internal Network, Host, And Identity Operations


## Continuity And Loading Rules

Read [../module-continuity.md](../module-continuity.md) before invoking a card. Keep one engagement state and one attack-path graph across all cards and domains.

1. Load entry and coverage cards first when they exist.
2. Load only the technical card supported by current evidence; do not enumerate cards as a checklist.
3. Keep the current parent path unless evidence creates a genuinely independent path.
4. Checkpoint before a domain transition and after a card returns material evidence.
5. When multiple domains cooperate, keep one primary domain and record supporting domains in state.

## Card Router

| Card | Load condition | Required return |
|---|---|---|
| [Establish Current Position](internal-ad-01-establish-current-position.md) | Load on entry to establish position, prerequisites, and the bounded question. | Return evidence, capability changes, affected paths, and the next decision. |
| [Coverage Gate](internal-ad-02-coverage-gate.md) | Load before the first material validation and after a capability or position change. | Return evidence, capability changes, affected paths, and the next decision. |
| [Kerberos Route Selection](internal-ad-03-kerberos-attack-primitives.md) | Load only when current evidence supports the Kerberos Attack Primitives route or its prerequisite must be tested. | Return evidence, capability changes, affected paths, and the next decision. |
| [Basic Internal Network Attacks](internal-ad-04-basic-internal-network-attacks.md) | Load only when current evidence supports the Basic Internal Network Attacks route or its prerequisite must be tested. | Return evidence, capability changes, affected paths, and the next decision. |
| [ACL Abuse Primitives](internal-ad-05-acl-abuse-primitives.md) | Load only when current evidence supports the ACL Abuse Primitives route or its prerequisite must be tested. | Return evidence, capability changes, affected paths, and the next decision. |
| [Active Directory Certificate Services (AD CS) Attack Primitives](internal-ad-06-active-directory-certificate-services-ad-cs-attack-primitives.md) | Load only when current evidence supports the Active Directory Certificate Services (AD CS) Attack Primitives route or its prerequisite must be tested. | Return evidence, capability changes, affected paths, and the next decision. |
| [Lateral Movement Decision Tree](internal-ad-07-lateral-movement-decision-tree.md) | Load only when current evidence supports the Lateral Movement Decision Tree route or its prerequisite must be tested. | Return evidence, capability changes, affected paths, and the next decision. |
| [Credential Dumping Decision Matrix](internal-ad-08-credential-dumping-decision-matrix.md) | Load only when current evidence supports the Credential Dumping Decision Matrix route or its prerequisite must be tested. | Return evidence, capability changes, affected paths, and the next decision. |
| [LOLBin & Living Off The Land](internal-ad-09-lolbin-living-off-the-land.md) | Load only when current evidence supports the LOLBin & Living Off The Land route or its prerequisite must be tested. | Return evidence, capability changes, affected paths, and the next decision. |
| [Trust Hopping](internal-ad-10-trust-hopping.md) | Load only when current evidence supports the Trust Hopping route or its prerequisite must be tested. | Return evidence, capability changes, affected paths, and the next decision. |
| [Post-Exploitation Cleanup Tracking](internal-ad-11-post-exploitation-cleanup-tracking.md) | Load only when current evidence supports the Post-Exploitation Cleanup Tracking route or its prerequisite must be tested. | Return evidence, capability changes, affected paths, and the next decision. |
| [Domain Transitions](internal-ad-12-domain-transitions.md) | Load when evidence changes domain, identity boundary, execution surface, or network position. | Return evidence, capability changes, affected paths, and the next decision. |
| [Recollect When](internal-ad-13-recollect-when.md) | Load after gaining a new identity, privilege, asset, role, trust edge, or network position. | Return evidence, capability changes, affected paths, and the next decision. |

