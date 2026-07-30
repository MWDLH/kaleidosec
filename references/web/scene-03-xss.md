# Web And API Operations: Attack Primitives: Traditional Web Vulnerabilities: Cross-Site Scripting (XSS) — Practical Operator View

> Apply [../module-continuity.md](../module-continuity.md). Keep the same engagement and parent path as the calling route. Load this scene only when current evidence supports its prerequisites.

### Cross-Site Scripting (XSS) — Practical Operator View

**The only XSS that matters is the one with security impact.** Don't report `alert(1)` unless it proves a real attack chain.

### Decision Entry

Before investing time in XSS, answer: what is the victim role? What data or actions does that role have access to? Does the target have CSP, HttpOnly cookies, or SameSite that limits the payload's practical impact?

### Attack Progression Decision Tree

```
1. Determine the reflection context (this determines everything)
   ├─ HTML body context → widest exploit surface, standard payloads work
   ├─ HTML attribute context → need attribute-break + event handler
   │   └─ onmouseover, onfocus, onerror, ontoggle, onanimationend
   ├─ JavaScript string context → break out of string + inject code
   │   └─ '</script><img src=x onerror=alert(1)> or \'-alert(1)-//
   ├─ JavaScript context without quotes → no string break needed, inject expression
   ├─ URL/href context → javascript: protocol or data: URL
   └─ CSS context → expression(), -moz-binding, @import (IE/old Firefox only, rarely exploitable)

2. Check what defenses are active BEFORE crafting payloads
   ├─ CSP header present? → check script-src (unsafe-inline? nonce? allowlisted domains?) and connect-src (where can exfiltrated data go?)
   ├─ HttpOnly on session cookie? → document.cookie unavailable, but same-origin fetch() with credentials still sends cookies automatically
   ├─ SameSite cookie? → irrelevant for same-origin XSS — the payload executes on the target origin, requests are same-site by default
   ├─ Trusted Types? → DOM sink enforcement, eval blocked — may prevent DOM-based XSS sinks
   └─ WAF? → test with benign reflection first, then escalate

3. Select payload complexity based on defense level
   ├─ No CSP, no HttpOnly → simplest payload, maximum impact — both cookie theft and same-origin CSRF possible
   ├─ CSP without unsafe-inline → both inline scripts and event handlers blocked → need nonce/hash reuse, CSP bypass via allowlisted CDN/JSONP endpoint, or DOM clobbering
   ├─ CSP with unsafe-inline → inline scripts and event handlers both allowed — standard payloads work, but verify connect-src allows exfiltration to attacker-controlled host
   ├─ HttpOnly set → cookie theft blocked, but XSS still makes same-origin authenticated requests — pivot to in-app actions, credential phishing overlay, or data exfiltration via application features
   └─ Strict CSP + Trusted Types → execution surface is minimal — verify whether any bypass exists before assuming impact; if no bypass, record the XSS context and park

4. Distinguish XSS types — different investment profiles
   ├─ Reflected → requires victim interaction (click link), limited value unless victim is high-privilege
   ├─ Stored → payload executes for every viewer, high value — prioritize identifying stored XSS
   ├─ DOM-based → payload in URL fragment or client-side data, server never sees it
   └─ Blind XSS → submit payloads in fields likely viewed by staff (support ticket, user registration, order comment, profile fields, file names on upload). Use a callback endpoint you control (XSS Hunter/bXSS/custom) to confirm execution and capture the viewer's origin, User-Agent, and cookie scope. Bound submissions to a single test account's data within authorized scope — do not spray payloads across production user content. Blind XSS that fires in admin/staff context is typically the most valuable XSS finding.
```

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
| **Stored XSS** | Steal admin session → CSRF-protected admin actions, deface, credential harvesting via fake login form, keylogging on target page |
| **Reflected XSS** | Phishing chain: send link → session theft → account takeover, or: chain with CSRF for one-click attack |
| **DOM XSS** | Often missed by scanners; grep JS source for `innerHTML`, `document.write()`, `eval()`, `location.href` patterns |
| **Blind XSS** | Use XSS Hunter / bXSS / custom callback — fires in admin/staff context, most valuable XSS findings |
| **Self-XSS** | Report only if chainable: self-XSS + CSRF = one-click compromise of other users |

### Failure Branches

| Failure Signal | Likely Cause | Next Variable |
|---|---|---|
| Reflection confirmed but all script/event payloads stripped | Server-side filter removes HTML tags or attributes; WAF blocks requests containing HTML; output encoding is applied correctly | Test whether encoding is context-dependent — a parameter reflected in an HTML attribute may be encoded differently than the same value in JSON. Test non-script HTML injection (img, iframe, style, link) — may enable phishing or content injection without script execution |
| Payload survives in response but doesn't execute in browser | CSP blocks the execution vector; browser XSS auditor (legacy); the surrounding HTML structure prevents valid DOM parsing of the injection; payload lands after a DOM element that stops parsing | Inspect the exact DOM position. Test: break out of the enclosing element first, then inject payload. For CSP: check if any allowed script-src domain hosts JSONP or user-content that can be abused |
| Stored XSS payload appears in own session but not for other users | Per-user isolation (stored content only served to the author); admin review queue separates content from viewer-facing pages; different rendering path per role | Test the content in other role contexts (admin review view, customer-facing view, public profile). If truly per-user isolated, stored XSS impact is limited to self-XSS |
| DOM-based XSS identified in client code but not triggerable via URL/input | The vulnerable code path is dead code; the source (location.hash, postMessage, WebSocket) is not attacker-controllable; CSP rule prevents the sink | Verify the source is truly unreachable: check if postMessage origin is validated; check if WebSocket endpoint is authenticated. If confirmed unreachable, park with reactivation condition tied to code changes |
| XSS confirmed but HttpOnly + CSP restrict exfiltration — what's the actual impact? | HttpOnly blocks cookie theft; CSP connect-src may block exfiltration to external hosts. But same-origin XSS still makes authenticated requests to the application's own API, can modify page content for phishing, exfiltrate data via application features (export, messaging, profile update), or keylog on the vulnerable origin | Assess impact honestly: if the application handles sensitive data or actions, same-origin request forgery and content manipulation are often sufficient for a material finding. If the application is purely informational (no accounts, no sensitive actions), the finding may be low severity — record and move on. Do not claim the combination of these defenses makes exploitation impossible |

## Scene Exit

Return result classification, evidence, changed assumptions, affected paths, persistent changes, and the next parent-path decision.
