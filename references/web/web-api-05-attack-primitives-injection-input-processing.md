# Web And API Operations: Attack Primitives: Injection & Input Processing

> Apply [../module-continuity.md](../module-continuity.md). Inherit the engagement, parent path, current capability, evidence, authorization profile, and module stack. Do not initialize a separate workflow. Checkpoint material results and return them to the parent path before leaving this card.

## Attack Primitives: Injection & Input Processing

This card covers injection classes that cross-cut specific attack types, and provides the shared failure classification used by all injection scenes.

### SQL Injection — Triage Before Exploitation

For structured SQL injection testing, load [scene-02-sql-injection](scene-02-sql-injection.md) from web-api-02. This section covers the pre-exploitation triage:

1. **Observe error behavior**: Does `'` produce an error? What error? (ODBC, JDBC, PDO, native driver — each has distinct error patterns)
2. **Observe blind behavior**: Does `' AND '1'='1` differ from `' AND '1'='2`? (Boolean-based blind)
3. **Observe timing**: `' AND SLEEP(5)--` (MySQL), `' WAITFOR DELAY '0:0:5'--` (MSSQL), `' AND pg_sleep(5)--` (PostgreSQL), `' AND DBMS_LOCK.SLEEP(5)--` (Oracle)
4. **Observe out-of-band**: confirm network reachability from the database server — use a controlled callback target authorized in the engagement scope
5. **Only after confirming injection** → load scene-02 for database-type determination and exploitation path selection.

### Server-Side Request Forgery, SSTI, and Deserialization

These attack classes have dedicated scene cards with full decision trees, failure branches, and post-exploitation transitions. Load from web-api-02's scene router when evidence supports the prerequisites:

- **SSRF** → [scene-08-ssrf](scene-08-ssrf.md): trust chain modeling, protocol escalation, cloud metadata, URL bypass matrix
- **SSTI** → [scene-09-ssti](scene-09-ssti.md): engine fingerprinting, language-specific RCE chains, sandbox escape
- **Deserialization** → [scene-10-deserialization](scene-10-deserialization.md): language/framework identification, gadget chain selection, version-specific payloads

### HTTP Request Smuggling Decision Tree

1. **Identify front-end/back-end architecture**: Different servers for routing vs application? CDN? Load balancer? HTTP/2 downgrade to HTTP/1.1 at any hop?
2. **Determine which variant applies** — connection reuse must be confirmed; a single timeout is not sufficient to establish smuggling:
   - **CL.TE**: Front-end uses Content-Length, back-end uses Transfer-Encoding → Send `Transfer-Encoding: chunked` with conflicting small CL → back-end reads more than front-end intended
   - **TE.CL**: Front-end uses Transfer-Encoding, back-end uses Content-Length → Send chunked body with trailing content beyond CL → back-end processes trailing as next request
   - **TE.TE**: Both use Transfer-Encoding, but interpret header obfuscation differently → Send `Transfer-Encoding: chunked\r\nTransfer-Encoding: x` — one engine treats as chunked, other treats as identity
3. **Test signal**: Confirm connection reuse across multiple requests. Does a request time out (waiting for bytes from a poisoned socket)? Does a subsequent innocent request receive a 400 or unexpected response? Is the behavior reproducible?
4. **Exploit path**: Request queue poisoning (steal other users' requests), response queue poisoning (control responses to other users), cache poisoning via smuggled content. Establish safe stop conditions before testing on production connections.

### Injection Failure Classification (Shared Across All Injection Cards)

Use this table whenever an injection attempt fails, regardless of attack class.

| Failure | Likely Cause | Next Variable |
|---|---|---|
| No error or behavioral difference from any payload | Input is not interpreted by the suspected sink; or the injection point is wrong; or output encoding hides the difference | Change the injection point (different parameter, header, or body field); test with a guaranteed-safe value first to confirm the parameter is reflected or processed |
| Error but no data extraction (WAF block, generic error page, or connection reset) | WAF or input filter detected the payload pattern; or the sink error is caught and replaced with a generic message | Change encoding or structure of the payload; use blind/time-based methods instead of error-based. Rotating source IP is not a routine failure branch — only consider it when the authorization profile explicitly allows source restriction circumvention. |
| Timing-based test shows delay but cannot confirm injection | Network latency, server load, or caching causes false-positive timing | Establish a statistical baseline appropriate to the target's response-time distribution and the authorized test scale; choose a delay that exceeds normal variance by a clear margin. Verify with a second independent timing test or an alternative blind technique before concluding. |
| OOB callback not received | Egress filtering blocks outbound connections from the target server; DNS, HTTP, proxy, or resolver configuration prevents the callback | Diagnose which layer failed: test DNS resolution independently, test HTTP egress independently, verify the callback destination is reachable from the operator side. Do not default to switching protocols — use the protocol that matches the diagnosed egress path. |

## Card Exit

Classify the result, update evidence and attempted methods, record capability or risk changes, identify affected paths, and apply the return contract in [../module-continuity.md](../module-continuity.md).
