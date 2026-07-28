# Mobile Operations: Coverage Gate

> Apply [../module-continuity.md](../module-continuity.md). Inherit the engagement, parent path, current capability, evidence, authorization profile, and module stack. Do not initialize a separate workflow. Checkpoint material results and return them to the parent path before leaving this card.

## Coverage Gate

Before exploit-oriented testing, understand:
- Launch and authentication flows (how does the app establish identity?)
- Principal roles (anonymous, user, premium, admin?)
- Backend calls (REST? GraphQL? gRPC? custom protocol? WebSocket?)
- Local data stores (SharedPreferences, SQLite, Realm, CoreData, UserDefaults, Keychain/Keystore)
- Inter-process/inter-app entry points (exported Activities, BroadcastReceivers, ContentProviders, Services, URL schemes, universal links)
- WebView usage (JavascriptInterface in Android, WKScriptMessageHandler in iOS)
- Cryptographic boundaries (where are keys stored? what is encrypted? key derivation?)
- Native code areas (JNI in Android, C/C++/Swift interop in iOS)

---


## Card Exit

Classify the result, update evidence and attempted methods, record capability or risk changes, identify affected paths, and apply the return contract in [../module-continuity.md](../module-continuity.md).
