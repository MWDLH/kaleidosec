# Web And API Operations: Attack Primitives: Traditional Web Vulnerabilities: Server-Side Request Forgery

> Apply [../module-continuity.md](../module-continuity.md). Keep the same engagement and parent path as the calling route. Load this scene only when current evidence supports its prerequisites.

### Server-Side Request Forgery — Trust Chain Analysis

SSRF is not one vulnerability. It is a **trust chain exploration**. The target server makes requests on your behalf — model the network map and test each hop.

### Decision Entry

Load this scene when:
- [FACT] A URL-fetch function exists (webhook, import, PDF/thumbnail generation, link preview, proxy endpoint, SSO callback test)
- [FACT] The parameter accepts a URL or host that you control
- [INFERENCE] The target server can reach internal services or cloud metadata that you cannot reach directly

Do not load for: client-side redirect, open redirect without server-side fetch, purely client-side CORS requests.

### Attack Progression Decision Tree

```
1. Confirm server-side fetch — distinguish function from vulnerability
   ├─ Point the parameter at your controlled server → observe the request
   │   ├─ Request received? → server-side fetch FUNCTION confirmed. Record: User-Agent, source IP, HTTP library
   │   ├─ No request → Check: URL format validation? Protocol restriction? DNS resolution? Firewall egress?
   │   └─ A successful callback only confirms the server CAN make outbound requests. It does NOT
   │       automatically mean the fetch is exploitable — the URL may be validated, the response may not
   │       be returned, or the function may only fetch allowlisted hosts. Continue to step 2 before
   │       concluding this is a vulnerability.
   └─ A single failed callback does not rule out SSRF — the target may resolve but not route to you

2. Map the network trust model (THE critical step — determines whether SSRF is exploitable)
   ├─ What network can the server reach? (same-host, same-subnet, internal ranges, cloud metadata)
   ├─ What protocols does the HTTP client support? → test http, https first; file:// protocol requires
   │   a URL scheme that the HTTP library supports (not all libraries implement file://)
   └─ Build a target list of internal services likely behind the trust boundary before probing any of them

3. Test protocol escalation (only against targets within authorized scope)
   ├─ file:///etc/passwd → local file read (Linux, if supported by the HTTP library)
   ├─ gopher:// → raw TCP socket, useful for text-based protocols (Redis, SMTP, FastCGI) — not for file read
   ├─ dict:// → service probe on a specific port
   └─ Protocol escalation beyond http/https requires the HTTP library to support non-HTTP schemes

4. Test cloud metadata → IF metadata endpoint is reachable and returns credentials,
   TRANSITION to [cloud domain](../cloud/router.md) for credential validation, permission enumeration,
   and IAM escalation path modeling. Do not maintain a second cloud testing workflow here.
   The SSRF card's role is to confirm reachability to the metadata endpoint — the cloud domain
   owns the exploitation steps.

5. Test internal service reachability (within authorized scope)
   ├─ Start with hosts and ports confirmed in scope — do not spray internal subnets
   ├─ Known internal endpoints (from source code, error messages, JS references)
   ├─ If probing adjacent hosts or undiscovered services → confirm authorization profile allows
   │   internal network discovery before expanding the target set
   └─ Unauthorized internal scanning is scope violation — stop at the first unauthorized boundary
```

### URL Bypass Matrix — When The Filter Blocks

Change one variable at a time. Do not cycle through bypasses blindly.

| Filter Type | Technique | When It Works |
|---|---|---|
| Hostname blocklist | Alternative IP representation: `http://2130706433/` (decimal), `http://0x7F.0.0.1/` (hex), `http://[::ffff:169.254.169.254]/` (IPv6-mapped) | IPv4 parsing differences between filter and HTTP client |
| Scheme allowlist (http/https only) | Redirect following: your server responds 302 → `file:///etc/passwd`; or test if scheme validated on initial URL only | HTTP client follows redirects across schemes |
| Domain allowlist | Open redirect on allowed domain; DNS rebinding (TTL-controlled IP switch); subdomain takeover on allowed domain | Allowed domain has redirect or name-resolution gap |
| IP blocklist (10.x, 192.168.x, 127.x) | DNS rebinding, domain A-record pointing to internal IP, IPv6 alternative, decimal/hex IP encoding | Filter blocks literal IP but allows DNS resolution |
| URL path filter | CRLF injection (`%0d%0a`), `@` host confusion (`http://safe.com@169.254.169.254/`), backslash as separator | URL parser mismatch between filter and fetcher |
| Response blocked | Blind SSRF — use timing (port scan via response time difference), error messages, or out-of-band confirmation | Cannot read response but can observe side effects |

### Failure Branches

| Failure Signal | Likely Cause | Next Variable |
|---|---|---|
| No callback received but URL format accepted | Egress firewall blocks outbound HTTP from the server; DNS resolution fails; the function validates URL reachability before fetching | Test DNS resolution independently (does the target resolve external hostnames?); test with a known-public IP instead of hostname; if the server cannot reach the internet at all, the SSRF is internal-only — shift to probing internal targets |
| Callback received from unexpected IP or with wrong User-Agent | The request comes from a different host (proxy, renderer service, queue worker) — the SSRF surface may be larger than expected | Map the actual source IP and service; the fetching service may have different network reachability than the web server |
| Connection refused / timeout on internal target | Target port not listening on that host; firewall between server and internal target drops the connection; the internal hostname resolves to a different IP than expected | Verify the internal hostname resolution from the server's perspective against the authorized target list. Do not expand probing to adjacent hosts without scope confirmation — the host may exist but the port is closed, and the next host may be out of authorized scope |
| Metadata endpoint returns 403/404 | IMDSv2 enforced (AWS); metadata header missing (Azure, GCP); not running on that cloud platform; the server runs in a container without metadata access | For AWS: test IMDSv2 PUT token flow (only if authorized); for Azure: add `Metadata: true` header. If all cloud metadata endpoints are blocked, transition to cloud domain with the confirmed negative result — do not automatically pivot to container runtime sockets (these are a different attack surface with separate authorization considerations) |
| Filter bypass succeeds but internal response not returned | Blind SSRF — the fetch succeeds but the response is not relayed to you | Use timing to infer reachability; test error messages for information leakage. If the internal service protocol is confirmed and the service is in authorized scope, crafting a blind exploit payload may be the next step — but payloads that write data (e.g., Redis SET + SAVE which modifies the RDB file) are state-modifying actions that must be evaluated against the global safety gate before execution. Not a routine failure branch |
| Bypass cycling through multiple techniques with no progress | The filter is correctly implemented at a layer you cannot control (WAF, library-level); or the function does not actually fetch URLs (false positive on the SSRF hypothesis) | Stop cycling. Classify as `precondition_failure`. Park the path and test: can another function on the same host perform outbound requests? Can you reach internal services through a different entry point (SQLi → xp_cmdshell → curl)? |

### Post-Exploitation Transitions

- **Cloud metadata credentials obtained** → Transition to [cloud domain](../cloud/router.md): validate credential, enumerate effective permissions, model IAM escalation paths. Carry the exact credential material, source endpoint, and metadata API version.
- **Internal HTTP service reachable** → Re-enter Web/API testing from the new network position. The internal service may trust requests from the exploited host without authentication — test authorization from this new identity.
- **Internal non-HTTP service reachable (Redis, SMTP, DB protocol via gopher/dict)** → Transition to [infrastructure domain](../infrastructure/router.md) with the specific service, protocol, and reachable commands.
- **File read via `file://` protocol** → Read configuration files for credentials, source code for other injection points, `/proc/self/environ` for environment variables. Transition to [internal-ad](../internal/router.md) if the host is domain-joined.

## Scene Exit

Return result classification, evidence, changed assumptions, affected paths, persistent changes, and the next parent-path decision.
