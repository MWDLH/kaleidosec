# Web And API Operations


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
| [Build The Surface](web-api-01-build-the-surface.md) | Entry: endpoints or tech stack not yet modeled; no bounded question recorded. | What is the position, the bounded question, and the next discriminating action? |
| [Attack Primitives: Traditional Web Vulnerabilities](web-api-02-attack-primitives-traditional-web-vulnerabilities.md) | Reflected parameters, HTML/template concatenation, upload or parser entry points, framework version in errors. | Are these classes reachable here, and what one request confirms or kills each? |
| [Attack Primitives: Authentication & Session](web-api-03-attack-primitives-authentication-session.md) | Login, token, cookie or session handling visible; `Set-Cookie` anomalies; JWT claims; session fixation points. | Which auth/session assumption is client-controlled, and what proves it? |
| [Attack Primitives: Authorization](web-api-04-attack-primitives-authorization.md) | Object, tenant, role or account IDs in requests; same resource returning different results per identity; 200/403 boundaries. | Where is the ownership check missing, and what second identity proves it? |
| [Attack Primitives: Injection & Input Processing](web-api-05-attack-primitives-injection-input-processing.md) | Parameter reaches a SQL/OS/LDAP/template/deserialization sink; SQL errors, command echo, template evaluation in responses. | Which sink is actually reachable and controllable, and what is the minimum proof? |
| [Attack Primitives: Business Logic & Race Conditions](web-api-06-attack-primitives-business-logic-race-conditions.md) | Price, amount, quantity or state supplied by the client; multi-step flow allowing skip, replay or concurrency. | Which invariant is enforced only on the client, and what sequence violates it? |
| [Interpret Results](web-api-07-interpret-results.md) | After any material result, positive or negative. | What does this prove, and does it change the path ranking? |
| [Domain Transitions](web-api-08-domain-transitions.md) | Evidence implies a different domain, identity boundary, execution surface or network position. | Where are we now, what authority do we hold, and what is the return target? |
| [Recollect When](web-api-09-recollect-when.md) | New identity, privilege, asset, role, trust edge or network position. | What must be re-collected, and what evidence can be safely reused? |
