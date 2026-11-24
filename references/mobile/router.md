# Mobile Operations


## Continuity And Loading Rules

Read [../module-continuity.md](../module-continuity.md) before invoking a card. Keep one engagement state and one attack-path graph across all cards and domains.

1. Load entry and coverage cards first when they exist.
2. Load only the technical card supported by current evidence; do not enumerate cards as a checklist.
3. Keep the current parent path unless evidence creates a genuinely independent path.
4. Checkpoint before a domain transition and after a card returns material evidence.
5. When multiple domains cooperate, keep one primary domain and record supporting domains in state.

## Card Router

| Card | Load when evidence shows (field / response signature) | Must answer after loading |
|---|---|---|
| [Build The Surface](mobile-01-build-the-surface.md) | Entry: APK/IPA obtained; platform, signing and backend not yet modeled. | Which platform, protections and backend surfaces are in scope? |
| [Coverage Gate](mobile-02-coverage-gate.md) | Before the first material validation, and after any capability or position change. | Which surfaces are covered, which are not, and is the next action justified anyway? |
| [Attack Primitives: Traditional Mobile Vulnerabilities](mobile-03-attack-primitives-traditional-mobile-vulnerabilities.md) | Static analysis shows exported components, plaintext storage, weak crypto or missing certificate validation. | Which traditional class is real on-device, and what observation proves it? |
| [Attack Primitives: Android-Specific](mobile-04-attack-primitives-android-specific.md) | Android package with `ContentProvider`, intents, WebView, JNI or debuggable flags. | Which Android-specific boundary is exploitable, and what is the precondition? |
| [Attack Primitives: iOS-Specific](mobile-05-attack-primitives-ios-specific.md) | iOS package with URL schemes, Keychain usage, ATS exceptions or jailbreak checks. | Which iOS-specific boundary is exploitable, and what is the precondition? |
| [Interpret Results](mobile-06-interpret-results.md) | After any material result, positive or negative. | What does this prove, and does it change the path ranking? |
| [Domain Transitions](mobile-07-domain-transitions.md) | Evidence implies a different domain, identity boundary, execution surface or network position. | Where are we now, what authority do we hold, and what is the return target? |
| [Recollect When](mobile-08-recollect-when.md) | New identity, privilege, asset, role, trust edge or network position. | What must be re-collected, and what evidence can be safely reused? |
