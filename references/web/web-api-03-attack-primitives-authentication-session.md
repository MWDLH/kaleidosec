# Web And API Operations: Attack Primitives: Authentication & Session

> Apply [../module-continuity.md](../module-continuity.md). Inherit the engagement, parent path, current capability, evidence, authorization profile, and module stack. Do not initialize a separate workflow. Checkpoint material results and return them to the parent path before leaving this card.

## Attack Primitives: Authentication & Session

### JWT Attack Matrix

Before any JWT attack, determine: library, algorithm, key source, claim validation, and consumer.

| Attack Vector | Prerequisites | Test Method | Success Signal | False Positive Risk |
|---|---|---|---|---|
| **alg:none** | Library accepts `none` algorithm; processing chain does not independently validate signature | Set `alg: none` in header, remove signature, keep payload — use only as a low-cost discriminator when processing-chain evidence supports the test | Backend accepts unsigned token through the full serving path | Gateways or middleware may add independent validation; a backend acceptance requires confirming which layer made the decision |
| **HMAC key confusion** | Asymmetric algorithm (RS256/ES256) used; public key obtainable; implementation does not bind algorithm to key type; allowed algorithm set includes HMAC | Convert `alg` to `HS256`, sign payload with the recovered public key as HMAC secret | Token accepted by the consuming service | Library correctly enforces algorithm-per-key binding even when the algorithm set appears broad |
| **JWK/JKU injection** | Consumer supports embedded JWK (`jwk` header) or fetches keys from a URL (`jku` header); the processing chain after any gateway also respects these headers | Confirm header support first; then embed attacker-controlled JWK or host a JWKS at the JKU URL — distinguish gateway acceptance from backend reliance | Backend verifies signature using attacker-provided key material | Gateway strips or overrides these headers before the backend processes them; JKU URL checked against a trusted allowlist |
| **kid injection** | `kid` value enters a file path, database query, or dynamic key-resolution path that the attacker can influence | First confirm whether kid reaches a resolving path beyond a static key-map lookup; then test traversal, injection, or resource confusion only against the identified resolution mechanism | Key resolution returns attacker-chosen material or an unintended key | kid used only as an in-memory map key with no interpreter; attacker-visible kid value is unrelated to internal resolution |
| **Algorithm downgrade** | Library supports multiple algorithms; the weaker algorithm is accepted for this token type; key material usable under the weaker algorithm | Change algorithm to a weaker variant within the supported set; verify the resulting token is still accepted | Token verified with downgraded algorithm strength | Library enforces minimum algorithm per key or per token class |
| **Substitution (cross-service)** | Multiple services consume the same JWT issuer; validation differs across consumers; audience claim not enforced | Use a token issued by service A against service B; test both same-audience and missing-audience scenarios | Token accepted across a trust boundary that should be separate | Audience claim properly validated; service B requires additional claims or scopes not present |
| **Expiration bypass** | `exp`/`nbf` validation logic has gaps: missing claims accepted, clock skew too wide, or validation occurs only in some layers | Test: remove `exp`, set far-future value, set `exp` within server clock-skew margin, or use negative `nbf` | Expired or not-yet-valid token still accepted through the full serving path | Clock skew legitimately accepted within configured bounds; multiple validation layers catch the gap |
| **Resource consumption via key material** | Server parses attacker-supplied key-set material (JWK set size, key count, or key parameter depth) before completing verification | Send a token with controlled-size JWK, large key count, or deeply nested key parameters — stay within authorized scale limits | Processing time or memory diverges measurably from baseline | This is an availability and scale-sensitive test: use small samples, incremental increases, and explicit stop conditions. Escalate to L3 when exceeding pre-authorized scale. Latency fluctuation alone is not a DoS finding. |

**Decision flow for JWT**:
1. Is the token a JWT? (three base64url segments separated by dots)
2. Decode the header: what `alg`? Any `jwk`/`jku`/`kid`? Any `typ` or `cty`?
3. Determine the processing chain: which components see the token before the backend? (CDN, API gateway, WAF, sidecar proxy, backend framework)
4. Is a public key obtainable? (well-known endpoint, client code, error messages, other tokens)
5. Map which services consume this token — microservice sprawl increases substitution risk.
6. Select the lowest-cost discriminating test for the leading hypothesis rather than following a fixed sequence.

### JWT Result Interpretation

| Result | Signal | Next Action |
|---|---|---|
| **Success** | Token with modified algorithm/header/key accepted, backend returns protected resource | Confirm it is the backend accepting, not just the gateway; record the exact modification, algorithm, and key source; classify the finding under authorization impact |
| **Partial** | Token accepted by one layer but rejected by another (e.g., gateway passes, backend rejects) | Identify which layer validated what; check whether the gateway alone is sufficient for any useful access; test direct backend connection if reachable |
| **Ambiguous** | Server returns 200 but response body is a generic error or empty; or behavior varies across repeated attempts | Compare response length, headers, and timing with a known-valid token; test with a guaranteed-invalid token to establish error baseline; rule out caching or load-balancer inconsistency |
| **Failure** | Token rejected consistently; no evidence of processing-chain difference | Does NOT prove the algorithm or key binding is secure — it proves the current parameters were rejected. Check: is the algorithm in the accepted set? Is the key format correct? Is another validation layer catching it first? |

---

### OAuth 2.0 / OIDC Misconfiguration Patterns

| Pattern | How It Works | Key Signal | Verification |
|---|---|---|---|
| **redirect_uri bypass** | Authorization code delivered to attacker-controlled URI | `redirect_uri` validation accepts substring match, open redirect on allowed domain, or `localhost` with mixed port | Register `https://victim.com.attacker.com`, `https://victim.com/redirect?url=@attacker.com`, or `http://localhost:9999` |
| **state parameter missing** | CSRF on authorization request → victim's account linked to attacker's identity | No `state` parameter in `/authorize` request | Complete OAuth login with attacker account, observe if victim's resources appear |
| **PKCE absent + auth code interception** | Authorization code intercepted via redirect_uri manipulation or mobile app intent hijack | `code_challenge` and `code_challenge_method` missing from authorization request | Attempt code replay without PKCE verifier |
| **scope upgrade** | Add privileged scopes to authorization request; server may approve without user re-consent | Server does not re-confirm scope changes | Add `admin`/`offline_access`/internal scopes to request |
| **Client secret in client-side code** | SPA, mobile app, or public client embeds `client_secret` | `client_secret` in JS bundle, APK strings, or binary | The secret cannot be treated as confidential — test whether the server incorrectly relies on it to establish client identity (e.g., accepting it as the sole client authentication at the token endpoint) |
| **Mixing response types** | Authorization endpoint accepts a `response_type` not registered for this client, or the token endpoint accepts a `grant_type` not registered | Authorization endpoint returns a response mode inconsistent with client registration; the authorization code is not bound to client, redirect URI, and PKCE verifier; the token endpoint accepts a mismatched code/client/redirect_uri/verifier combination | Test each `response_type` the authorization server supports against the client's registered grant types; verify the token endpoint does not accept code exchanges from mismatched client or redirect_uri |

**Decision flow for OAuth**: First, identify the grant type (authorization_code, implicit, client_credentials, password, device_code, refresh_token). Then determine whether the client is confidential or public. A `client_secret` in a public client is a deployment mistake; whether it creates a security vulnerability depends on whether the authorization server relies on that secret to authenticate the client.

### OAuth Result Interpretation

| Result | Signal | Next Action |
|---|---|---|
| **Success** | Authorization code or token obtained under attacker-controlled conditions; attacker gains access to victim resources or elevated scope | Confirm the scope and resource access are real; bound the impact to specific users, tenants, or privileges |
| **Partial** | redirect_uri bypass works but the code cannot be exchanged (PKCE or client authentication blocks it); or the code is issued but no useful scope granted | Record which link held and which broke; this partial result may chain with another weakness (e.g., client secret exposure) |
| **Ambiguous** | Authorization server returns success but the token is opaque; or redirect happens but no code visible (fragment mode) | Confirm the authorization server metadata (discovery document); determine the actual grant type and response mode; evaluate the token's effective permissions by calling the resource server with it; use token introspection only when the client is authorized and the endpoint is available. An opaque token does not determine the protocol flow — do not switch to a different grant type based on token format alone |
| **Failure** | Server rejects the modified redirect_uri, enforces PKCE, or refuses scope escalation | This proves the server enforced the specific check — not that the entire OAuth implementation is secure. Remaining unknowns: token replay, refresh token rotation, client authentication at token endpoint, session binding |

---

### Session Management Attacks

Beyond JWT and OAuth — classic session attacks remain relevant:

- **Session fixation**: Does the application reuse session IDs before and after authentication? Test: note session cookie before login, check if same after login.
- **Session pattern screening**: Collect a sample of session IDs and examine structure — sequential, time-based, or structured patterns indicate a predictable generation scheme. This is preliminary pattern screening and does not prove cryptographic unpredictability.
- **Concurrent session policy**: Can one account have multiple concurrent sessions? Is there a logout-all mechanism that works?
- **Session timeout**: Test both absolute timeout and idle timeout. Does "Remember Me" extend it unreasonably?
- **Logout completeness**: Is the session invalidated server-side, or only the cookie cleared client-side? Replay old session cookie after logout.
- **Password change session preservation**: Does changing password invalidate all existing sessions?

### Session Result Interpretation

| Result | Signal | Next Action |
|---|---|---|
| **Success** | Session ID unchanged after login (fixation), pattern predicts another session ID (predictable), or old cookie still valid after logout/password change | Confirm the affected session's privilege scope; test whether the finding enables account takeover or session hijacking |
| **Partial** | Session ID structure suggests a pattern but prediction fails (entropy higher than estimated, or server-side binding catches the guess) | Record the observed structure; park unless a stronger signal (leaked source, timing side-channel) emerges |
| **Ambiguous** | Session appears reused but server behavior differs (different user data, partial logout) | Compare across multiple accounts and endpoints; check for session merging, caching, or CDN interference |
| **Failure** | Session IDs appear cryptographically random; logout and password change invalidate them server-side; no fixation observed | A negative result on session testing does not mean authentication is secure — it only means session management passed these specific checks |


## Card Exit

Classify the result, update evidence and attempted methods, record capability or risk changes, identify affected paths, and apply the return contract in [../module-continuity.md](../module-continuity.md).
