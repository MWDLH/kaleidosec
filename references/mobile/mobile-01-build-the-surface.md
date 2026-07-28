# Mobile Operations: Build The Surface

> Apply [../module-continuity.md](../module-continuity.md). Inherit the engagement, parent path, current capability, evidence, authorization profile, and module stack. Do not initialize a separate workflow. Checkpoint material results and return them to the parent path before leaving this card.

## Build The Surface

Record package/bundle identifier, version, platform and OS range, architecture (ARM32/ARM64/x86), signing identity, entitlements/manifest permissions, exported components, deep links/URI schemes, native libraries (.so/.dylib), frameworks, SDKs, update channels, backend endpoints, local storage, cryptographic usage, and runtime protections (certificate pinning, root/jailbreak detection, obfuscation, anti-debugging, anti-tampering).

### Static Analysis — What to Extract First

**Android (APK/AAB)**:
```bash
# Decompile
apktool d app.apk -o apk_extracted               # smali + resources
jadx -d apk_source app.apk                        # Java source (preferred for readability)
unzip app.apk -d apk_unzipped                     # raw contents

# Key files to examine immediately
AndroidManifest.xml                                # permissions, exported components, deep links, backup flag
res/xml/network_security_config.xml                # certificate pinning, cleartext traffic policy
classes.dex (multiple for multidex)                # compiled app code — use jadx
lib/<arch>/*.so                                    # native libraries
assets/*                                           # bundled files, JS bundles, local HTML
res/values/strings.xml                             # hardcoded strings, API keys, endpoints
META-INF/*                                         # signing certificates

# Check if debuggable (AndroidManifest.xml)
grep -i "debuggable" AndroidManifest.xml
# android:debuggable="true" → can attach debugger, run arbitrary code
```

**iOS (IPA)**:
```bash
unzip app.ipa -d ipa_extracted
# Payload/<app>.app/ contains the bundle

# Key files
Info.plist                                          # permissions, URL schemes, ATS settings
embedded.mobileprovision                            # provisioning profile (team ID, devices, entitlements)
<app> (Mach-O binary)                               # main executable
Frameworks/*.framework/*                            # bundled frameworks
PlugIns/*.appex/                                    # extensions
```

**Backend endpoint discovery (both platforms)**:
```bash
# Search for URLs, API paths, internal hosts
grep -rnE "https?://[a-zA-Z0-9._-]+" apk_source/ | sort -u
grep -rnE "/api/v[0-9]+|/graphql|/rest|/oauth|/auth" apk_source/
grep -rnE "AWS|azure|cloud|firebase|s3|storage\.googleapis" apk_source/

# Extract strings from native libraries
strings lib/<arch>/*.so | grep -E "https?://|/api/|secret|key|token"
```

---


## Card Exit

Classify the result, update evidence and attempted methods, record capability or risk changes, identify affected paths, and apply the return contract in [../module-continuity.md](../module-continuity.md).
