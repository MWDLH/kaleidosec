# Web And API Operations: Attack Primitives: Authorization

> Apply [../module-continuity.md](../module-continuity.md). Inherit the engagement, parent path, current capability, evidence, authorization profile, and module stack. Do not initialize a separate workflow. Checkpoint material results and return them to the parent path before leaving this card.

## Attack Primitives: Authorization

Authorization testing is verifying that the server enforces the same access model across every endpoint, method, role, and data field. Three dimensions must be tested independently.

### Authorization Dimensions

| Dimension | Question | Example |
|---|---|---|
| **Object-level (IDOR)** | Can user A access object owned by user B? | `GET /api/orders/12345` with User B's session returns User A's order |
| **Function-level** | Can a low-privilege user call an admin function? | `POST /api/admin/users` with a regular user session creates a new user |
| **Field-level** | Can a user read or write a field they shouldn't? | `PATCH /api/users/me` with `{"role":"admin"}` in the body — the role field should not be client-writable |
| **Tenant-level (cross-tenant)** | Can Tenant A access Tenant B's data? | Same role in different tenant — authorization must be scoped per tenant |
| **Contextual** | Can a user perform an action that should be restricted by business context? | Transferring money from a closed account, accessing orders outside their region |

### IDOR/Authorization Bypass Decision Tree

```
Can object ID be found in client code/response?
├─ Yes → Is ID predictable (sequential, timestamp, hash of known value)?
│   ├─ Sequential → Enumerate adjacent IDs with other user's session
│   │   └─ Success? → IDOR confirmed. Test cross-tenant.
│   ├─ Hash → Can we find the hashing function in client code or guess pattern?
│   │   └─ Yes → Generate IDs for other objects, test.
│   └─ UUID/random → Check: are IDs leaked elsewhere? (public pages, shared objects, email notifications, webhook calls, export functions)
│       └─ Leaked elsewhere → Test those IDs.
└─ No (POST/GraphQL without IDs) → Check role and field manipulation:
    ├─ role=admin, role_id=1, group_id, tenant_id, is_admin=true in request body?
    ├─ GraphQL: can query/mutation expose other users' data via filter arguments?
    └─ Mass assignment: add &is_admin=true or &role=admin to POST/PATCH body.
```

### Authorization Model Testing Matrix

Create a matrix of [role × endpoint × method] and test systematically:

| Endpoint | Method | Anonymous | User A | User B (same tenant) | User C (other tenant) | Admin |
|---|---|---|---|---|---|---|
| /api/users | GET | Expected 401 | Expected: own only | Should NOT see A's data | Should NOT see A's data | Expected: all |
| /api/users/123 | GET | 401 | If 123=A: 200; else 403 | Should be 403 | Should be 403 | 200 |
| /api/users/123 | PUT | 401 | If 123=A: 200; else 403 | Should be 403 | Should be 403 | 200 |
| /api/admin/config | GET | 401 | 403 | 403 | 403 | 200 |
| /api/admin/users | POST | 401 | 403 (function-level) | 403 | 403 | 200 |

### Function-Level Authorization

Admin functions (user management, system config, data export, billing operations) must verify the caller's role at the server. Test: identify all admin endpoints from JS source, API docs, or common paths. Call each with a low-privilege session. A 403/404 may mean enforcement or may mean the endpoint name differs from the admin UI — distinguish by testing with the admin session first, then with a regular session.

### Field-Level Authorization

A `PATCH /api/users/me` or `PUT /api/profiles/123` may accept fields the client should not control. Test: add `"role":"admin"`, `"isVerified":true`, `"balance":999999`, `"tenant_id":"<other_tenant>"`, or `"internal_notes":"..."` to the request body. The server should either ignore (strip silently) or reject (400/422) unauthorized fields. Acceptance (200 + field value reflected) is a field-level authorization finding.

### Result Interpretation

| Result | Signal | Next Action |
|---|---|---|
| **Success (bypass confirmed)** | Different-role or different-user session receives protected data or performs protected action | Record the exact endpoint, method, role gap, and affected object/function/field; scope the impact to specific users, tenants, or operations |
| **Partial** | Response differs between roles but not consistently — works on some endpoints but not others, or works with one method but not another | The authorization model is inconsistently enforced. Record the pattern; each inconsistent endpoint is a separate finding |
| **Ambiguous** | Server returns 200 but response body differs between sessions in an unexpected way (empty vs partial vs cached) | Compare response length, headers, and content across sessions; rule out caching, CDN, and load-balancer variance; use a fresh resource created by each session independently |
| **Failure** | All cross-role and cross-user requests return 401/403/404 | Authorization is consistently enforced for the tested endpoints. This does not prove all endpoints are secure — only the tested ones |


## Card Exit

Classify the result, update evidence and attempted methods, record capability or risk changes, identify affected paths, and apply the return contract in [../module-continuity.md](../module-continuity.md).
