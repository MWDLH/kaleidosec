# Web And API Operations: Interpret Results

> Apply [../module-continuity.md](../module-continuity.md). Inherit the engagement, parent path, current capability, evidence, authorization profile, and module stack. Do not initialize a separate workflow. Checkpoint material results and return them to the parent path before leaving this card.

## Interpret Results

Compare behavior across roles, resources, methods, encodings, and equivalent endpoints. Distinguish:

- **Application rejection** (intended 4xx, business logic denial) from **intermediary blocking** (WAF 403/406 with distinct signature) from **client-side enforcement** (JS validation that doesn't reach the server)
- **Cached behavior** (stale response, CDN cache hit headers) from **real backend response** (`Cache-Control: no-cache` header or cache-busting parameter)
- **Backend failure** (5xx, timeout) from **backend behavior** — a 500 on `'` is an information leak, not SQL injection proof

**Every automated scanner finding requires manual verification**:
- Version string match ≠ vulnerable (backport patching, build configuration, mitigating controls)
- Payload reflection ≠ XSS (check Content-Type, CSP, X-Frame-Options, SameSite cookies, sandboxed iframe, sanitization context)
- Error message containing SQL ≠ exploitable SQL injection (check if parameter actually reaches database query)
- 200 OK on unauthorized request ≠ authorization bypass (verify response body contains actual sensitive data, not just empty 200)

---


## Card Exit

Classify the result, update evidence and attempted methods, record capability or risk changes, identify affected paths, and apply the return contract in [../module-continuity.md](../module-continuity.md).
