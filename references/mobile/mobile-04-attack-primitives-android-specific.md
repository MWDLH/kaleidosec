# Mobile Operations: Attack Primitives: Android-Specific

> Apply [../module-continuity.md](../module-continuity.md). Inherit the engagement, parent path, current capability, evidence, authorization profile, and module stack. Do not initialize a separate workflow. Checkpoint material results and return them to the parent path before leaving this card.

## Attack Primitives: Android-Specific

### Exported Components

An exported component is reachable from outside the application. Whether it is exploitable depends on five factors — `android:exported` is only one of them.

**Judgment factors (evaluate ALL, not just `android:exported`)**:

1. **Explicit `android:exported`** — `true` means exported; `false` means not exported. An explicit `android:exported="false"` takes precedence and is not overridden by Intent Filters.
2. **Intent Filter** — any component with at least one `<intent-filter>` is exported by default on API < 31 unless `android:exported="false"` is explicitly set. On Android 12+ (API 31+), the `android:exported` attribute must be explicit for components with Intent Filters; the platform refuses to install if it is missing.
3. **API-level default behavior** — a ContentProvider without `android:exported` is exported by default on API < 17, not exported on API ≥ 17.
4. **Manifest merger result** — library manifests, build variants, and Gradle overrides can change the final exported state; inspect the merged manifest (`app/build/intermediates/merged_manifests/`), not just the source manifest.
5. **Component-level permission** — an exported component protected by `android:permission` requires the caller to hold that permission. Signature-level permissions (`signature`) restrict callers to apps signed with the same certificate. Additionally, the caller's UID, calling package, and any runtime checks in `onCreate`/`onReceive`/`onStartCommand` form another authorization layer.

**What to test**:

```bash
# List components from the merged manifest — not just the source
aapt dump xmltree <app>.apk AndroidManifest.xml | grep -E "activity|service|receiver|provider" -A5

# Attempt to interact and observe which layer blocks
# Activity
adb shell am start -n <package>/<activity> --es <key> "<value>"
# BroadcastReceiver
adb shell am broadcast -n <package>/<receiver> --es <key> "<value>"
# ContentProvider
adb shell content query --uri content://<authority>/<path>
# Service
adb shell am startservice -n <package>/<service>
```

**Attack surface checklist per component type**:

- **ContentProvider**: Can unauthorized callers read or write data? SQL injection in query parameters? Path traversal in `_file` providers (`openFile`)? `call()` method exposed with dangerous functionality?
- **BroadcastReceiver**: Does the receiver trigger a sensitive action on receiving an Intent? Does it validate the sender's identity (UID, package, signature, permission)? Can an unordered broadcast be intercepted?
- **Activity**: Does launching the Activity bypass an authentication screen? Does it accept Intent extras that control navigation or data display without validation? Are debug/hidden Activities reachable?
- **Service**: Does `onStartCommand` or `onBind` perform privileged operations? Does it check the caller? Can binding to the Service expose a Binder interface with dangerous methods?

### Exported Component Failure Branches

| Symptom | Likely Cause | Next Action |
|---|---|---|
| `am start` returns "Permission Denial" | Component-level `android:permission` blocks; caller lacks the required permission | Check the required permission string; evaluate whether a different calling package or a platform-signed caller could hold it; if signature-level, test only if you control the signing key |
| `am start` succeeds (Activity opens) but the sensitive action does not occur | Runtime check in `onCreate`/`onResume` rejects the caller based on UID, package name, or Intent validation | Trace the runtime checks in the decompiled code; identify the exact validation condition to bypass or satisfy |
| Component not found or not exported | Manifest merger overrode the source `exported`; API-level default changed the effective value; component name differs from the source class name | Inspect the merged manifest; use `aapt` on the final APK; check ProGuard/R8 mapping if class names are obfuscated |
| ContentProvider query returns no rows or error | Provider enforces row-level filtering based on calling identity; SQL-level constraint rejects the query | Inspect the provider implementation for `query()` logic; check whether a different URI path bypasses the filter |
| Activity launched but API call from the opened screen is rejected by the backend | Client-side navigation succeeded but server-side authorization enforced | This is NOT a client vulnerability — the backend correctly enforced auth. Record that the client exposes the endpoint but the backend blocked it; this is a defense-in-depth finding, not a bypass |

---

### WebView Attacks

WebView risks require a chain of conditions. Do not report a single configuration flag as a vulnerability.

**Risk evaluation requires ALL of these to be true for a material finding**:

| Condition | What To Verify |
|---|---|
| **Attacker-controllable content** | Does the WebView load a URL or HTML that an attacker can influence? Direct URL from Intent extra? Insecure deeplink parameter? Content from an untrusted source? Response from an HTTP (not HTTPS) connection? |
| **JavaScript enabled** | `setJavaScriptEnabled(true)` alone does not create a vulnerability — it is a prerequisite. Combined with attacker-controllable content and an exposed interface, it becomes dangerous. |
| **JavaScript Interface exposed** | `addJavascriptInterface(obj, name)` exposes annotated methods of `obj` to JavaScript running in the WebView. On API < 17 (Android 4.2), ALL public methods (including `getClass()`) are accessible via reflection — this enables RCE. On API ≥ 17, only `@JavascriptInterface`-annotated methods are callable. Verify: which methods are actually annotated and reachable? Does the interface method perform a sensitive operation? |
| **File access from file URLs** | `setAllowUniversalAccessFromFileURLs(true)` allows `file://` URLs to read any file via XHR and send it to any origin. `setAllowFileAccessFromFileURLs(true)` is similar but restricted to other `file://` URLs. Both are rarely needed. |
| **SSL error bypass** | `onReceivedSslError(handler.proceed())` without validating the certificate chain — makes MITM trivial. Check if this is a blanket bypass or conditional on a specific certificate check. |
| **Navigation and origin restrictions** | `setAllowUniversalAccessFromFileURLs` and `shouldOverrideUrlLoading` may allow or block navigation. Check whether the WebView allows navigation to arbitrary URLs or restricts to a known set. |

**Test method**: Identify whether the WebView loads attacker-controllable content. If yes, enumerate the JavaScript Interface methods. If the WebView loads file:// URLs from Intent parameters, test path traversal to sensitive files. If SSL errors are bypassed, test MITM and observe what client data is exposed.

### WebView Failure Branches

| Symptom | Likely Cause | Next Action |
|---|---|---|
| WebView present but content not controllable | URL is hardcoded with no external parameter; no deeplink or Intent path reaches it | Park this surface — record the WebView exists, note the lack of controllable input; this is not a finding |
| `addJavascriptInterface` present but targetSdkVersion ≥ 17 and no `@JavascriptInterface` methods are dangerous | Only annotated methods are callable; inspected annotations reveal no sensitive operations | Document the interface methods for context; if none perform privileged actions, no finding |
| WebView loads attacker URL but JavaScript Interface methods throw or return empty | Method checks the calling origin or requires authentication state not present in the WebView context | Inspect the method implementation for origin checks, session requirements, or parameter validation |
| SSL error bypass present but content loaded is only static/non-sensitive | Impact limited — the bypass still degrades transport security | Report as a transport security degradation; severity depends on what data could be exposed in a MITM scenario |

---

### Deep Link / Intent Hijacking

Deep links are URI schemes that open specific screens. Exploitation requires distinguishing three layers.

**Three layers — test each independently**:

1. **Client navigation**: Did the deep link open a protected screen? This alone is insufficient — the backend may still enforce authorization.
2. **Parameter processing**: Does the deep link parameter reach a dangerous operation (WebView URL, SQL query, file path, JavaScript execution)? Test each parameter for injection relevant to its sink.
3. **Backend authorization**: After the screen opens, does the API call return protected data or perform a privileged action? If the backend rejects the request (401/403), the deep link opened the screen but did not bypass security.

**App Link / Universal Link verification**: On Android 6+, App Links (`autoVerify="true"`) require the server to host `/.well-known/assetlinks.json` to verify domain ownership. Without this, the system shows a disambiguation dialog (if multiple apps handle the scheme) or the deep link may not open at all. Test whether the app relies on App Link verification for security — a missing or misconfigured `assetlinks.json` may allow another app to intercept the link.

**Intent hijacking**: An implicit Intent (no target component specified) can be intercepted by any app that declares a matching Intent Filter. The receiving app can read the Intent extras. Check: does the app send sensitive data (tokens, session IDs, user info) in implicit Intent extras?

```bash
adb shell am start -W -a android.intent.action.VIEW -d "scheme://host/path?param=<value>"
```

### Deep Link Failure Branches

| Symptom | Likely Cause | Next Action |
|---|---|---|
| Deep link opens correct screen but API returns 401/403 | Backend authorization enforced — client navigation bypass insufficient | No authorization bypass. Record that client navigation is possible; check if the screen leaks any UI or metadata even before the API call completes |
| Deep link accepted but parameter not reflected or processed | Parameter filtered, sanitized, or not consumed by the target screen | Trace the parameter through the decompiled code to its actual sink; test alternative parameter names or encoding |
| Deep link rejected or App Link verification fails | assetlinks.json missing, incorrect package fingerprint, or system-level Link Handling policy | Verify the hosted assetlinks.json; check whether the deep link works with `autoVerify="false"` or as a custom scheme fallback |
| Implicit Intent intercepted by another app | Intent Filter conflict; the receiving app is not the intended target | Intent hijacking confirmed if the intercepted data includes sensitive extras. Test: register the same Intent Filter in a test app and observe what data arrives |


## Card Exit

Classify the result, update evidence and attempted methods, record capability or risk changes, identify affected paths, and apply the return contract in [../module-continuity.md](../module-continuity.md).
