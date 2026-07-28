# Web And API Operations: Attack Primitives: Business Logic & Race Conditions

> Apply [../module-continuity.md](../module-continuity.md). Inherit the engagement, parent path, current capability, evidence, authorization profile, and module stack. Do not initialize a separate workflow. Checkpoint material results and return them to the parent path before leaving this card.

## Attack Primitives: Business Logic & Race Conditions

### Race Condition Patterns

Modern applications have more race condition surfaces than traditional ones:

- **Limit-overrun races**: Redeem a coupon code twice, withdraw more than balance, apply discount after checkout
- **Multi-endpoint races**: Confirm email change + password reset in parallel (race between confirmation and token issuance)
- **HTTP/2 single-packet attack**: Send multiple concurrent requests in a single TCP packet (Burp Suite's turbo intruder or custom scripts) — defeats per-request rate limiting
- **Database transaction races**: SELECT → check condition → UPDATE pattern without proper locking (TOCTOU)
- **File system races**: Temp file creation + symlink + use (TOCTOU on file operations)

**Test method**: Send identical requests simultaneously (within 1-5ms). HTTP/2 or HTTP/1.1 with last-byte sync technique. Look for: duplicate operations, negative balances, inconsistent state.

### GraphQL Attack Surface

| Attack Class | Test | Tool |
|---|---|---|
| **Introspection leak** | `{__schema{types{name,fields{name,args{name,type{name}}}}}}` | GraphQL Voyager, inql |
| **Field suggestion leak** | Send invalid field name, observe suggestion response | Manual |
| **Batching attack** | Send same mutation 100× in single request array | Altair, Postman |
| **Alias-based rate bypass** | `{a:login(password:"a") b:login(password:"b") ... z:login(password:"z")}` | Manual script |
| **Depth/recursion DoS** | `{a{b{c{d{e{f{g{h{i{j{k{l{m{n{o{p{q{r{s{t{u{v{w{x{y{z{...}}}}}}}}}}}}}}}}}}}}}}}}}}` | graphql-cop |
| **Directive overloading** | `@skip`, `@include` manipulation, custom directives with side effects | Manual |
| **Subscription hijack** | Subscribe to private events/mutations of other users | Manual with WebSocket client |

---


## Card Exit

Classify the result, update evidence and attempted methods, record capability or risk changes, identify affected paths, and apply the return contract in [../module-continuity.md](../module-continuity.md).
