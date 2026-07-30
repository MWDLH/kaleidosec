# Web And API Operations: Attack Primitives: Traditional Web Vulnerabilities

> Apply [../module-continuity.md](../module-continuity.md). Inherit the engagement, parent path, current capability, evidence, authorization profile, and module stack. Do not initialize a separate workflow. Checkpoint material results and return them to the parent path before leaving this card.

## Attack Triage: Choose By Signal Combination, Not By Checklist

Do not walk the scene list in order. Combine three signal dimensions — technology stack, functional surface, and authentication context — to identify the highest-value first move.

### Signal Dimension 1: Technology Stack

Stack signals come from response headers, error messages, file extensions, JS references, and fingerprinting.

```
Observed stack → preferred first attack classes:

Java/Spring → Deserialization (Java native, Jackson, XStream), SpEL injection, JNDI injection, Actuator exposure, Struts/Spring4Shell version checks
.NET → Deserialization (BinaryFormatter, JSON.NET TypeNameHandling), ViewState analysis, path traversal (IIS short-names)
PHP → File upload → execution chain, LFI/RFI, PHP deserialization (unserialize), type-juggling auth bypass
Python → SSTI (Jinja2, Mako), pickle deserialization, debug endpoints (/console, /debugger), Flask session tampering
Node.js → SSTI (Pug, EJS, Handlebars), prototype pollution, SSRF, ReDoS, eval injection
Ruby → SSTI (ERB, Slim), YAML deserialization, mass assignment
Go → SSRF, path traversal, integer overflow, HTTP smuggling (common proxy front-end)
```

### Signal Dimension 2: Functional Surface

Functional signals come from the attack surface built in web-api-01. Prioritize the class whose prerequisites are already confirmed.

```
Observed function → matching attack class:

File upload (any kind) → File upload attacks — not just "can I upload," but the full upload→storage→execution→inclusion chain
URL fetch / import / webhook / PDF generation → SSRF (prioritize above other injection — cloud metadata, internal APIs, file:// reads)
Search / filter / report / export with DB backend → SQL injection (or NoSQL if MongoDB/Redis fingerprint confirmed)
User-content display (profile, comment, message, ticket, review) → XSS — but first confirm reflection context (HTML / attribute / JS string / JSON)
Data export to CSV/Excel/PDF → CSV injection, SSRF (if PDF generator server-side)
Payment / order / transfer / coupon / loyalty workflow → Cross-cut to business-logic capability — analyze state machine before injection
Template-editing or email-template features → SSTI
Admin file-browser / config-import → Path traversal, XXE, YAML/XML deserialization
REST resource with sequential/hashed ID pattern → IDOR / authorization bypass — test before deeper injection
Login / registration / password-reset / OAuth flow → Authentication & session attacks (JWT, OAuth, session fixation)
```

### Signal Dimension 3: Authentication Context

```
Current access → what changes the objective fastest:

Anonymous (no auth) → Authentication bypass, registration flaws, exposed admin panels, pre-auth CVEs
Low-privilege user → Authorization (IDOR, role escalation, tenant cross-access), business-logic path manipulation
Privileged user / admin → SSRF (broader network reachability), command injection, file operations, audit-log bypass
OAuth / SSO participant → Token substitution, scope upgrade, redirect_uri bypass, cross-client confusion
```

### Combining Signals — Hypothesis Generation, Not Fixed Priority

No attack class has an inherent priority. Technology stack, functional surface, and authentication context generate **candidate hypotheses**. The actual test order is determined by:

1. **Prerequisite coverage**: which attack class has the most prerequisites already confirmed by current evidence?
2. **Capability change**: which confirmation would unlock the largest movement in identity, privilege, reachability, or impact?
3. **Verification cost**: which hypothesis can be confirmed or ruled out with the fewest requests and lowest operational risk?
4. **Information gain**: which test produces evidence that advances or prunes multiple competing paths?

Example hypothesis chains (not rules):

- URL-fetch function + internal/cloud target context → SSRF is a **strong candidate** because it can produce a network-position change that no other Web vulnerability provides
- Multiple roles/tenants + sequential/hashed resource IDs → authorization flaws are a **strong candidate** because the prerequisite (multiple identity contexts) is already confirmed
- Java serialized blob observed in a cookie or parameter → deserialization is a **strong candidate** because the deserialization entry point is directly observable
- Money/inventory/identity-sensitive workflow + client-submitted price/state/quantity parameters → business-logic analysis is a **strong candidate** because the value at stake is high and injection defenses are irrelevant

When no single hypothesis has a clear advantage, select the cheapest discriminating test first — the test that narrows the hypothesis space the most per unit of cost and risk.

## Scene Router

After triage selects the leading attack class, load the matching scene card. Keep the inherited parent path. Load one scene at a time by evidence support; do not walk this table as a checklist.

| Scene | Selection rule |
|---|---|
| [File Upload Attacks](scene-01-file-upload.md) | File upload function confirmed; test the full upload→storage→execution→inclusion chain |
| [SQL Injection](scene-02-sql-injection.md) | SQL-backend signal (error, timing, parameter behavior); confirm DB type before exploiting |
| [Cross-Site Scripting (XSS)](scene-03-xss.md) | User content reflected in page; first determine reflection context (HTML/attribute/JS/JSON) |
| [Cross-Site Request Forgery (CSRF)](scene-04-csrf.md) | State-changing request without anti-CSRF token; check SameSite cookie attribute first |
| [Command Injection](scene-05-command-injection.md) | Parameter likely reaches OS command (ping, exec, nslookup, file-convert); distinguish from code injection |
| [XXE (XML External Entity)](scene-06-xxe.md) | XML accepted (SOAP, SAML, Office docs, SVG, RSS, config import); test external DTD loading first |
| [Path Traversal & File Inclusion](scene-07-file-inclusion-path-traversal.md) | File-path parameter observed; distinguish traversal (read) from inclusion (execute) |
| [Server-Side Request Forgery](scene-08-ssrf.md) | URL-fetch, webhook, PDF-generation, or import function confirmed; model the network trust chain |
| [Server-Side Template Injection](scene-09-ssti.md) | Template-editing, email-template, or expression-evaluation feature; fingerprint engine before exploiting |
| [Deserialization Attacks](scene-10-deserialization.md) | Serialized object in request (base64 blob, `rO0` prefix, PHP serialized format, YAML input); identify language before payload selection |

## Card Exit

Classify the result, update evidence and attempted methods, record capability or risk changes, identify affected paths, and apply the return contract in [../module-continuity.md](../module-continuity.md).
