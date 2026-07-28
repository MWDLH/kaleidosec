# Web And API Operations: Build The Surface

> Apply [../module-continuity.md](../module-continuity.md). Inherit the engagement, parent path, current capability, evidence, authorization profile, and module stack. Do not initialize a separate workflow. Checkpoint material results and return them to the parent path before leaving this card.

## Build The Surface

### Asset Discovery

Map hosts, virtual hosts, exposed services, routes, parameters, HTTP methods, content types, CORS configuration, authentication flows, session management, roles, APIs, WebSocket channels, file uploads, third-party integrations, administrative functions, error behavior, and backend dependencies.

The minimum discoverable surface includes:

- **Hosts and vhosts**: IP ranges, DNS zone transfer attempts, certificate transparency logs (crt.sh), reverse DNS, virtual host brute force with Host header variations. Distinguish CDN/WAF front-ends from origin servers.
- **Endpoints and parameters**: spidering, sitemaps, robots.txt, JS source maps, API schemas (OpenAPI/Swagger, GraphQL introspection), mobile client endpoints, old documentation. Prefer passive discovery (archive.org, public search, exposed `.git`, exposed config files) before active fuzzing.
- **Technology fingerprint**: HTTP response headers (Server, X-Powered-By, Set-Cookie session names), favicon hashes, error page defaults, JS framework signatures, Wappalyzer patterns, specific endpoint behavior (e.g., `/actuator`, `/wp-admin`, `/api/docs`).

Capture representative requests for anonymous access and each available role. Build a **role-operation-resource matrix** before broad authorization testing: for each role, record which endpoints are reachable and with what methods. Record client-side routes and referenced APIs, but verify server enforcement independently — client code is a map, not a security guarantee.

### Tool Selection by Capability Class

Choose tools by capability needed, not by name or habit:

| Capability | Example Tools | When to Use | Avoid When |
|---|---|---|---|
| HTTP interception & replay | Burp Suite, mitmproxy, Caido | Authenticated session testing, custom header/encoding manipulation | Target uses non-HTTP protocols |
| Endpoint discovery | ffuf, dirsearch, feroxbuster | Scope confirmed, rate limits understood, wordlist matched to tech stack | No rate-limiting awareness, production with strict SLA |
| Technology fingerprinting | WhatWeb, Wappalyzer, builtwith API | Initial surface mapping | Already have tech stack from docs/source |
| DNS & service enumeration | dig, host, Nmap service scan | Scope includes infrastructure | Pure web-app scope, cloud API-only target |
| Schema extraction | GraphQL Voyager, OpenAPI parsers | API-first applications | REST without documentation |
| Content discovery | katana, gospider, hakrawler | JS-heavy SPAs, API-driven apps | Pure server-rendered without JS |
| Bounded template scanning | nuclei with curated templates | Matched technology, verified scope, known rate tolerance | Broad untargeted scan, unverified template quality |

**Tool availability check**: Before building a workflow around a tool, verify it exists in the current environment. Prefer native commands or small single-purpose binaries over large frameworks when both can answer the question.

### Coverage Gate

Before exploit-oriented testing, confirm representation of:

| Surface | Minimum Understanding | Critical Unknowns |
|---|---|---|
| Authentication flows | Login, registration, password reset, MFA enrollment/verification, session issuance | OAuth/OIDC provider and flow type, token format, session storage (cookie vs JWT vs opaque) |
| Application roles | Each role's accessible operations, tenant scope, privilege model | Hidden/admin role existence, role assignment logic |
| High-value operations | Fund transfer, data export, user management, configuration change, API key generation | Business-logic validation sequence |
| Major APIs | REST endpoints per role, GraphQL schema, WebSocket events, async job submission | Internal/admin-only API versions |
| Data identifiers | Object IDs, user IDs, tenant IDs, resource IDs — format, predictability, enumeration surface | IDOR-able parameters not visible in client code |
| Upload/import functions | Allowed types, size limits, processing pipeline, storage location, retrieval method | Server-side processing (ImageMagick, LibreOffice, FFmpeg) |
| Trust boundaries | Internal services, third-party APIs, cloud metadata, webhooks, outgoing requests | SSRF-able parameters and their network reachability |
| Error & debug surfaces | Verbose errors, stack traces, debug endpoints, health checks, actuator-like surfaces | Information leakage in different response states |

Coverage is sufficient when the next action is evidence-supported and missing information is unlikely to make it random or misdirected. Do not confuse completeness with exhaustive enumeration.

---


## Card Exit

Classify the result, update evidence and attempted methods, record capability or risk changes, identify affected paths, and apply the return contract in [../module-continuity.md](../module-continuity.md).
