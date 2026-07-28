# Mini-Program Operations: Interpret Results

> Apply [../module-continuity.md](../module-continuity.md). Inherit the engagement, parent path, current capability, evidence, authorization profile, and module stack. Do not initialize a separate workflow. Checkpoint material results and return them to the parent path before leaving this card.

## Interpret Results

- **Client-side restriction vs backend enforcement**: Mini-programs extensively use `wx.if` / `wx:if` for conditional rendering. Removing UI restrictions in the unpacked JS does not prove a vulnerability — verify the backend also skips the check.
- **Dev vs release mode**: Some mini-programs leave debug mode on (`wx.setEnableDebug`). Dev mode grants access to vConsole and real-time performance panels — may leak API responses and internal state.
- **Old package version**: If you obtained an old version of the package, note it. The current production version may have different code. Test backend endpoints (which are server-side) rather than relying on client code alone.

---


## Card Exit

Classify the result, update evidence and attempted methods, record capability or risk changes, identify affected paths, and apply the return contract in [../module-continuity.md](../module-continuity.md).
