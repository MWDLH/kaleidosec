# Internal Network, Host, And Identity Operations: Kerberos Route Selection

> Apply [../module-continuity.md](../module-continuity.md). Inherit the engagement, parent path, current capability, evidence, authorization profile, and module stack. Do not initialize a separate workflow. Checkpoint material results and return them to the parent path before leaving this card.

## Kerberos Route Selection

### Decision Tree: Which Kerberos Attack First?

```
Current access:
├─ Unauthenticated (no domain creds) → AS-REP Roasting (if pre-auth disabled)
├─ Domain user, no SPN knowledge → AS-REP Roasting scan, then enumerate SPNs
├─ Domain user, know SPN → Kerberoasting
│   └─ Got service ticket crackable hash → crack offline
│       └─ Cracked → service account access gained
├─ Domain user, have NTLM hash → Overpass-the-Hash (get TGT)
│   └─ Have TGT → Pass-the-Ticket to any service
├─ Local admin/SYSTEM on any domain host → dump LSASS (TGTs, NTLM hashes)
│   ├─ If domain admin TGT found → Pass-the-Ticket to DC
│   ├─ If service account hash → Overpass-the-Hash, then check capability
│   └─ If any hash → Overpass-the-Hash
├─ Domain admin hash/KRBTGT hash → Golden Ticket **[L3 — forges durable domain-wide authentication material]**
├─ Service account hash → Silver Ticket **[L3 — forges persistent service-specific ticket; requires explicit approval]**
└─ Have unconstrained delegation host → wait for high-value TGT or printer bug
```

### Ticket Type And Authorization Level

A cached ticket extracted from LSASS on a host you already own is using existing access (L2 when authorized). Forging a new ticket from key material creates durable impersonation capability — this is L3. The source of key material and the target identity's privilege both factor into the authorization level, not just the extraction method.

| Ticket Type | Source | Authorization |
|---|---|---|
| **TGT from LSASS dump** | Cached credential on owned host | Classify use by ticket identity, reachable services, source, and intended impact; a privileged TGT is not automatically L2 |
| **TGS from LSASS dump** | Cached service ticket on owned host | Classify use by ticket identity, target SPN, source, and intended impact |
| **Overpass-the-Hash (TGT from NTLM hash)** | Hash obtained from owned host (LSASS dump, SAM dump, credential hunting) | L2 when hash source is L2; L3 when hash source required L3 (DCSync of privileged accounts, NTDS.dit) |
| **Silver Ticket** | Forged from service account hash — the ticket itself expires (default 10h), but the forger retains the service account key and can re-forge | **L3** — creates persistent service-specific impersonation capability through key retention |
| **Golden Ticket** | Forged from KRBTGT hash — the forger may specify a long lifetime; actual acceptance is constrained by KDC validation, key rotation, and PAC validation | **L3** — domain-wide durable impersonation; forest-wide scope requires Enterprise Admins SID and cross-domain KRBTGT material |
| **DCSync** | Uses DS-Replication-Get-Changes right — extracts any account hash from DC without code execution on DC | Having this right is itself a domain-level privilege; constrained replication verification against a controlled test account may be L2 when explicitly authorized; extracting privileged accounts, KRBTGT, or bulk material is L3 |

### Prerequisites Boundary

Before executing a Kerberos attack, verify:
- The hash source: where did the NTLM hash or AES key come from? The source's authorization level propagates.
- The ticket scope: a TGS for `MSSQLSvc/sql-01` grants access only to that SPN on that host. A TGT grants TGS requests to any service.
- The key material: a cleartext password, NTLM hash, Kerberos AES key, TGT, and service key are different material. NTLM hashes support NTLM pass-the-hash and may act as an RC4 Kerberos key where allowed. An account AES key can request Kerberos tickets for that account; a service or KRBTGT key may also enable ticket forgery for its corresponding scope, which is L3. A TGT enables Kerberos ticket requests as its embedded identity until policy or expiry invalidates it.

### Failure Branches

| Failure | Likely Cause | Next Variable |
|---|---|---|
| Kerberoasting returns no TGS | SPN does not exist, account has no SPN set, or the requested encryption type is not offered | Enumerate SPNs first; request both AES (AES256-CTS-HMAC-SHA1-96) and RC4 encryption types; AES-encrypted TGS can also be cracked offline — the absence of RC4 does not block Kerberoasting |
| Overpass-the-Hash returns `KDC_ERR_ETYPE_NOSUPP` | DC enforces AES-only; RC4 hash not accepted for AS-REQ | Use AES key instead of NTLM hash; if only NTLM is available, PTH via NTLM protocols may still work |
| Pass-the-Ticket fails with `KRB_AP_ERR_MODIFIED` | The target service uses a key that does not match the ticket's encryption key — commonly caused by duplicate SPNs, service running under a different account than the SPN, or ticket encrypted for a different host's key | Verify the SPN maps to the correct service account; check for duplicate SPNs (`setspn -X`); verify the ticket's target host matches the actual destination host |
| Pass-the-Ticket fails with `KRB_AP_ERR_SKEW` | Clock skew between client and target exceeds the 5-minute default tolerance | Check clock sync with `net time \\DC` or `w32tm /query /status`; adjust client clock or use a ticket obtained closer in time |
| Golden/Silver Ticket creation attempted without L3 approval | Authorization profile blocks L3 | Stop and request approval; record the path, the missing key material, and expected impact for the approval request |


## Card Exit

Classify the result, update evidence and attempted methods, record capability or risk changes, identify affected paths, and apply the return contract in [../module-continuity.md](../module-continuity.md).
