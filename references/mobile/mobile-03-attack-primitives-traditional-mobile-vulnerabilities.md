# Mobile Operations: Attack Primitives: Traditional Mobile Vulnerabilities

> Apply [../module-continuity.md](../module-continuity.md). Inherit the engagement, parent path, current capability, evidence, authorization profile, and module stack. Do not initialize a separate workflow. Checkpoint material results and return them to the parent path before leaving this card.

## Attack Primitives: Traditional Mobile Vulnerabilities

### Insecure Local Storage

**Android**:
```bash
# SharedPreferences (often world-readable)
adb shell run-as <package> cat /data/data/<package>/shared_prefs/*.xml
# Check file permissions (MODE_WORLD_READABLE? MODE_WORLD_WRITEABLE?)

# SQLite databases
adb shell run-as <package> ls /data/data/<package>/databases/
adb pull /data/data/<package>/databases/<db>.db
sqlite3 <db>.db .dump

# Internal storage files
adb shell run-as <package> ls -la /data/data/<package>/files/
adb shell run-as <package> cat /data/data/<package>/files/*

# External storage (SD card — always world-readable on older Android)
adb shell ls -la /sdcard/Android/data/<package>/
adb shell ls -la /storage/emulated/0/Android/data/<package>/

# Check Android backup (android:allowBackup=true → can extract data via adb backup)
adb backup -apk <package> -f backup.ab
# Convert and extract: dd if=backup.ab bs=1 skip=24 | openssl zlib -d > backup.tar
```

**iOS**:
```bash
# NSUserDefaults (plist storage)
# /var/mobile/Containers/Data/Application/<UUID>/Library/Preferences/<bundle>.plist

# SQLite/CoreData
# /var/mobile/Containers/Data/Application/<UUID>/Documents/
# /var/mobile/Containers/Data/Application/<UUID>/Library/

# Keychain (requires jailbreak or tool like keychain_dumper)
./keychain_dumper -a  # dump all accessible keychain items
# Even without jailbreak: if app stores sensitive data in Keychain with kSecAttrAccessibleAlways,
# it may be accessible from any app (pre-iOS 10 default)

# Plist files in app bundle (may contain API keys, initial config)
plutil -p <app>.app/Info.plist
plutil -p <app>.app/Settings.bundle/Root.plist 2>/dev/null
```

### Hardcoded Secrets

Search for:
```
# API keys, tokens, secrets
grep -rnE "([a-zA-Z0-9_-]{20,64})" --include="*.java" --include="*.kt" --include="*.swift" --include="*.m"
grep -rnE "secret|api[_-]?key|token|password|private|client[_-]?secret" apk_source/

# Firebase URLs
grep -rnE "firebaseio\.com|firebase\.google\.com" apk_source/

# AWS/Azure/GCP credentials
grep -rnE "AKIA|ASIA" apk_source/                  # AWS access keys
grep -rnE "DefaultEndpointsProtocol" apk_source/    # Azure connection strings
grep -rnE "ya29\.[0-9a-zA-Z_-]+" apk_source/        # GCP OAuth tokens
```

**Key judgment**: A hardcoded API key in a mobile app is NOT automatically a finding. Determine:
1. Is this key meant to be public? (e.g., Firebase web API key, Google Maps key with referer restriction)
2. What can this key access? (test in isolation — does it grant data access? admin operations?)
3. Is the key shared across multiple apps? (revoke impact)
4. Can the key be used from outside the app? (key restrictions, referer, bundle ID binding)

### Weak Authentication/Authorization in Mobile Backend

The mobile app is just another HTTP client. Test the backend independently:

1. **Replay API calls** from mobile app via Burp Suite. Test:
   - Remove/change the Authorization header → still works?
   - Access another user's data by changing user ID parameter
   - Use old token/session after logout
   - Bypass 2FA endpoints by calling protected API directly
   
2. **Client-side authorization checks**: The app shows/hides UI elements based on role. Test if the API enforces the same — send admin-level API calls from a regular user session.

3. **Token generation logic in client**: If the app constructs authentication tokens in client code (signing logic, custom HMAC creation), the secret is in the binary. Extract the secret, generate valid tokens for any user.

4. **Biometric bypass**: Apps often use biometrics (Face ID, fingerprint) as a UI convenience, caching the actual credential. Check if bypassing the biometric prompt gives access to the underlying session token without re-authentication.

---


## Card Exit

Classify the result, update evidence and attempted methods, record capability or risk changes, identify affected paths, and apply the return contract in [../module-continuity.md](../module-continuity.md).
