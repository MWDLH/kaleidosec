# Identity, Credential, Trust, And Network Capability: Model Identity

> Apply [../module-continuity.md](../module-continuity.md). Inherit the engagement, parent path, current capability, evidence, authorization profile, and module stack. Do not initialize a separate workflow. Checkpoint material results and return them to the parent path before leaving this card.

## Model Identity

Record principal, identity provider, credential/token type, issuer, audience, scope, lifetime, device/session binding, delegation, effective roles, trust relationships, and where authorization is enforced.

**The single most important question: "What can this identity actually do, and where?"** A credential that looks powerful (Domain Admin hash!) is useless if it's for a domain you've already fully compromised. A credential that looks mundane (service account with one SPN) may be the key to the next trust boundary.

### Credential Type Reference

| Credential Type | How to Use | How to Validate | Restrictions |
|---|---|---|---|
| **Cleartext password** | Direct login: SMB, WinRM, RDP, SSH, web login, database login | Try the lowest-impact authenticated request possible | May trigger MFA, logon hour restrictions, workstation restrictions |
| **NTLM hash** | Pass-the-Hash (SMB, WMI, WinRM with Basic), Overpass-the-Hash (get TGT) | `crackmapexec smb <target> -u <user> -H <hash>` — check ACCESS GRANTED or ACCESS DENIED | NTLM-only protocols. Cannot use for Kerberos-only services, RDP without Restricted Admin |
| **AES Kerberos key (AES256-CTS-HMAC-SHA1-96)** | Overpass-the-Hash (request TGT with AES key) | Request TGT → use TGT to request service ticket → access service | Works for Kerberos authentication. More modern environments require AES over RC4 |
| **Kerberos TGT** (.kirbi or base64) | Pass-the-Ticket (inject into session) | `klist` after injection → if TGT present → request service ticket | TGT lifetime: 10h default. After expiration, need new TGT |
| **Kerberos TGS** (service ticket) | PTT for that specific service only | Try accessing the service after injection | Limited to that service and that SPN |
| **NetNTLMv2 hash** (from Responder/relay) | Crack offline (hashcat mode 5600), or relay to unsigned SMB/LDAP host | Cracking: hashcat -m 5600 hash.txt wordlist.txt | Cannot PTH with NetNTLM (challenge-response hash, not NTLM hash) |
| **JWT (Bearer token)** | Add to HTTP Authorization header | Decode, check `exp`, try against API | Expires (check `exp` claim). May be audience-restricted (`aud` claim). May be bound to IP/session |
| **OAuth access token** | Use against resource server (API) | Call a protected endpoint with the token | Typically short-lived (1h). Use refresh_token to extend |
| **OAuth refresh token** | Exchange for new access token at token endpoint | Send to token endpoint, check if new access_token returned | May require client_secret. May be single-use |
| **AWS access key + secret** | `aws configure` then `aws sts get-caller-identity` | `aws sts get-caller-identity` — returns ARN of current principal | May have session policy restriction. May be expired |
| **AWS session token (STS)** | Must include session token with access key | Same as above, with `aws_session_token` in credentials | Temporary: 15min-36h. Bound to specific role session |
| **Azure access token (JWT from IMDS)** | `Authorization: Bearer <token>` against Azure Resource Manager | `curl -H "Authorization: Bearer <token>" https://management.azure.com/subscriptions?api-version=2021-04-01` | Typically 8h. Resource-scoped |
| **GCP OAuth 2.0 token** | `Authorization: Bearer <token>` against GCP APIs | `curl -H "Authorization: Bearer <token>" https://www.googleapis.com/oauth2/v1/tokeninfo` | Typically 1h. Scope-restricted |
| **SSH private key** | `ssh -i <key> user@host` | Try `ssh -o BatchMode=yes -o ConnectTimeout=5 user@host` | May have passphrase. May be restricted to specific source IP in authorized_keys |
| **Cookie (session)** | Add to HTTP requests | Replay against the application | Cookie flags: HttpOnly, Secure, SameSite. May expire. May be IP-bound or user-agent-bound |
| **API key (in config/code)** | Add to HTTP header or query parameter as specified by API | Call the API with the key | May be IP-restricted, rate-limited, or scope-limited |

### Credential Validation — Minimal Impact Method

For each credential, find the cheapest live validation:

```
1. Cleartext password → try logging into the web portal (if exists) before trying lateral movement
2. NTLM hash → crackmapexec with --shares (lists shares, minimal impact) before --exec-method
3. Kerberos ticket → klist to check if valid, then try against one low-value target
4. AWS key → `aws sts get-caller-identity` as a read-only identity check; assume cloud, identity, proxy, or surrounding controls may log the call
5. JWT → decode locally, then try against a read-only API endpoint
6. SSH key → ssh -o BatchMode=yes <host> "whoami; hostname" (just check who it logs in as)
```

**Do not**: immediately run secretsdump against a DC, launch a shell, or start enumerating S3 buckets. First confirm the credential works, then plan its use strategically.

---


## Card Exit

Classify the result, update evidence and attempted methods, record capability or risk changes, identify affected paths, and apply the return contract in [../module-continuity.md](../module-continuity.md).

