# Web And API Operations: Attack Primitives: Traditional Web Vulnerabilities: Cross-Site Request Forgery (CSRF)

> Apply [../module-continuity.md](../module-continuity.md). Keep the same engagement and parent path as the calling route. Load this scene only when current evidence supports its prerequisites.

### Cross-Site Request Forgery (CSRF)

#### Rapid Assessment

1. Find a state-changing request (password change, email update, fund transfer, admin action)
2. Check: does it include an anti-CSRF token? If no → potential CSRF
3. If yes: try removing the token entirely, try using an old token, try using a token from another user's session, try changing request method from POST to GET
4. Check SameSite cookie attribute: `SameSite=None` (no protection), `SameSite=Lax` (blocks on POST cross-site but not GET), `SameSite=Strict` (blocks both)
5. Check if custom headers are required (`X-Requested-With: XMLHttpRequest` — can this be bypassed with CORS misconfig?)

#### CSRF Token Bypass Techniques

| Bypass | How |
|---|---|
| Token not validated | Remove `csrf_token` parameter entirely, test if server still processes |
| Token reuse | Use same token across multiple requests (token not invalidated after use) |
| Token per-session (not per-request) | Use any valid token from any page on the same site |
| Token from another user | Request your own token, use it in an attack against another user |
| Method switch | Change POST to GET — CSRF tokens often only validated on POST |
| Token in cookie only | If CSRF token only appears in cookie (not in request body), and site has cookie-setting vulnerability, you can set your own token |
| Null/empty token | Send empty token value or omit the parameter name entirely |


## Scene Exit

Return result classification, evidence, changed assumptions, affected paths, persistent changes, and the next parent-path decision.
