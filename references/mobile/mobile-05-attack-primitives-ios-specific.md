# Mobile Operations: Attack Primitives: iOS-Specific

> Apply [../module-continuity.md](../module-continuity.md). Inherit the engagement, parent path, current capability, evidence, authorization profile, and module stack. Do not initialize a separate workflow. Checkpoint material results and return them to the parent path before leaving this card.

## Attack Primitives: iOS-Specific

### URL Scheme Hijacking

iOS apps register custom URL schemes (`myapp://`, `fb123://`). Custom URL schemes have no reliable domain-ownership binding — multiple apps can register the same scheme, and the OS routing behavior should not be treated as a stable security guarantee.

```bash
# List registered URL schemes (in Info.plist)
plutil -p <app>.app/Info.plist | grep CFBundleURLSchemes

# Test: from Safari or another app, open the scheme with controlled parameters
```

**What to test**:
- If the URL carries a session token, auth code, or password reset token → demonstrate that a controlled receiving app can obtain these parameters through scheme registration
- If the URL triggers a sensitive action (password change, payment, account linking) without user confirmation → parameter injection
- If the app does not validate the source application → any app can invoke the scheme

**Minimum success signal**: A controlled receiving app demonstrably obtains sensitive parameters from a URL scheme invocation. The existence of a custom URL scheme in the Info.plist is not a finding by itself.

### Universal Links

Universal Links (`https://example.com/path`) are Apple's verified deep-link mechanism. The association is established through: the server hosting `/.well-known/apple-app-site-association` (AASA) over HTTPS; the AASA `appID`/`appIDs` entries (typically `TeamID.BundleID` format); and the app's Associated Domains entitlement declaring the same domain.

**Security boundaries**:
- The AASA is a JSON file served over HTTPS — it is not itself signed with the app's Team ID
- The `appID` combines the Team ID and Bundle ID
- The Associated Domains entitlement must match the domain in the AASA
- All three (server domain, AASA content, app entitlement) must align for the association to be established
- If the AASA is missing or misconfigured, the link typically falls back to opening in the browser — this is a degraded user experience, not automatically a security finding

**Test**: Check `https://<domain>/.well-known/apple-app-site-association`. Verify the path patterns and whether overly broad patterns could capture authentication callbacks or sensitive URLs. A misconfigured or absent AASA alone does not create a hijack path — additional conditions (open redirect on the domain, Web content control, custom scheme fallback) are needed for a complete security chain.

### URL Scheme vs Universal Link Conflict

If both a custom scheme and a Universal Link are registered, iOS prefers Universal Links for `https://` taps. Custom schemes are invoked only when the scheme is explicitly opened (`myapp://`). An app using a custom scheme for `https://` callbacks (OAuth redirect_uri) should also implement Universal Links — the custom scheme alone provides no origin verification.

### Keychain Accessibility

```bash
# Dump keychain items (jailbreak required for unrestricted cross-app access)
./keychain_dumper -a

# Check accessibility flags for each item:
# kSecAttrAccessibleAlways — accessible anytime, even when device is locked (deprecated since iOS 10)
# kSecAttrAccessibleAlwaysThisDeviceOnly — same, but not included in backups (deprecated since iOS 10)
# kSecAttrAccessibleAfterFirstUnlock — accessible after first unlock after reboot (default)
# kSecAttrAccessibleWhenUnlocked — only when device is unlocked (most secure for sensitive items)
# kSecAttrAccessibleWhenPasscodeSetThisDeviceOnly — requires passcode, not in backups (iOS 8+)
```

**How accessibility, access groups, and entitlements interact**:
- **Accessibility** determines under what device state (locked/unlocked/after first unlock) the item is accessible.
- **Access Group** (keychain-access-groups entitlement) and **code signing** determine which application can read the item. A wide accessibility flag does not automatically break cross-app Keychain isolation — the access group and entitlement still gate which app can access the item.
- **Risk scenarios**: longer exposure windows when the device is unlocked; backup migration when the item is included in backups (depends on accessibility category, sync attributes, backup method, and platform behavior — not solely on the absence of `ThisDeviceOnly`); shared access groups when multiple apps share a keychain group; or a compromised device context.

**Jailbreak context**: `keychain_dumper` on a jailbroken device uses entitlement injection to read all keychain items regardless of access group. This does not represent a vulnerability in the target app.

**Minimum success signal**: A Keychain finding must include the specific data exposed, its sensitivity, the accessibility flag, access group constraints, device state prerequisites, and the extraction method. An accessibility flag alone is not a finding.

### ATS (App Transport Security) Settings

ATS enforces HTTPS and minimum TLS versions for `NSURLSession` connections.

```bash
plutil -p <app>.app/Info.plist | grep -A20 NSAppTransportSecurity
```

| ATS Key | Effect |
|---|---|
| `NSAllowsArbitraryLoads` = true | Platform transport restrictions are relaxed for all domains — the app may connect over HTTP or weak TLS |
| `NSAllowsArbitraryLoadsInWebContent` = true | Relaxation applies only to WebView content |
| `NSExceptionDomains` | Per-domain overrides — `NSTemporaryExceptionAllowsInsecureHTTPLoads` allows HTTP to a specific domain |
| `NSExceptionMinimumTLSVersion` | Lowers minimum TLS version for a domain |

**What matters**: `NSAllowsArbitraryLoads=true` confirms that platform-enforced transport restrictions are lifted. This becomes a finding when sensitive traffic is actually observed over insecure transport. A per-domain exception requires observing the actual traffic to that domain. The configuration entry in Info.plist is evidence of relaxed restrictions, not proof of exploitability — the finding is the observed insecure transmission of sensitive data.

### Certificate Pinning Bypass

| Method | Requirements | Reliability | Notes |
|---|---|---|---|
| **Frida script** (universal unpin) | Frida + jailbreak | High | Hooks `SecTrustEvaluateWithError` and related functions |
| **Objection** (`ios sslpinning disable`) | objection (built on Frida) + jailbreak | High | Automated Frida-based unpinning |
| **Modify IPA** (remove pinning logic + resign) | Decrypted IPA, signing certificate, device or simulator | High but needs re-signing | Remove pinning from binary or patch Info.plist |
| **Disable ATS** | Modify Info.plist `NSAppTransportSecurity` | Low | Only works if pinning is implemented via ATS exceptions, not custom `URLSessionDelegate` |
| **Proxy via iptables + self-signed cert** | Root + transparent proxy | Medium | Network-level — bypasses pinning only if pinning implementation is weak |

**Key judgment**: Certificate pinning bypass is a testing capability that enables traffic inspection, not a finding by itself. Report what the decrypted traffic revealed, not the bypass. The bypass remains a testing step regardless of method.

### iOS Result Interpretation

| Finding | Minimum Evidence | Transition |
|---|---|---|
| URL scheme carries sensitive parameters | Demonstrated parameter capture by a controlled receiving app | Token or data usable outside the app → test against backend API (Web/API domain) |
| Keychain item with weak accessibility + sensitive data | Specific data content, accessibility flag, access group, device state prerequisites, and extraction method | Sensitive data exposed under the identified conditions → test whether it grants backend access or contains user secrets |
| ATS disabled with observed insecure transmission | Info.plist configuration PLUS captured traffic showing sensitive data over HTTP or weak TLS | Transport degradation confirmed → test what data the backend sends in cleartext (Web/API domain) |
| ATS per-domain exception without observed insecure traffic | Info.plist configuration only | Configuration finding only — do not report as exploitable without observed traffic |
| Universal Link association missing or misconfigured | Absent or malformed AASA, or entitlement mismatch | Falls back to browser — not automatically a security finding. Test whether additional conditions (open redirect, domain control, custom scheme fallback) create a chain |


## Card Exit

Classify the result, update evidence and attempted methods, record capability or risk changes, identify affected paths, and apply the return contract in [../module-continuity.md](../module-continuity.md).
