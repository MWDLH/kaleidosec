# Mobile Operations: Interpret Results

> Apply [../module-continuity.md](../module-continuity.md). Inherit the engagement, parent path, current capability, evidence, authorization profile, and module stack. Do not initialize a separate workflow. Checkpoint material results and return them to the parent path before leaving this card.

## Interpret Results

- **Emulator artifacts**: Some anti-tampering checks trigger on emulators. Distinguish a real vulnerability from an emulator-detection false positive.
- **Instrumentation side effects**: Frida hooks can crash the app or change timing behavior. If something fails only with Frida attached, it may not be a real finding.
- **TLS interception failure**: Is the app protecting against MITM (pinning)? Good security measure, not a vulnerability.
- **Backend denial**: The app can't reach the backend → check network setup, not the app. But also check: does the app have a local fallback mode that exposes data when offline?

---


## Card Exit

Classify the result, update evidence and attempted methods, record capability or risk changes, identify affected paths, and apply the return contract in [../module-continuity.md](../module-continuity.md).
