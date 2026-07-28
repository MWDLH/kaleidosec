# Mini-Program Operations: Coverage Gate

> Apply [../module-continuity.md](../module-continuity.md). Inherit the engagement, parent path, current capability, evidence, authorization profile, and module stack. Do not initialize a separate workflow. Checkpoint material results and return them to the parent path before leaving this card.

## Coverage Gate

Before exploitation, map:

| Area | Key Questions |
|---|---|
| **Backend APIs** | All HTTP endpoints, cloud function names, WebSocket connections, upload URLs |
| **Platform identity** | How does the app authenticate? (wx.login → code → server → OpenID? Or custom token?) |
| **Session lifecycle** | How are sessions stored? (wx.setStorageSync?) When do they expire? |
| **Cloud functions** | Which cloud functions are exposed? Are they callable from outside the mini-program? |
| **Payment/High-value operations** | wx.requestPayment flow, balance checking, coupon redemption, order manipulation |
| **Deep links / Navigation** | wx.navigateToMiniProgram, app scheme links, QR code parameters |
| **Local sensitive data** | What's in wx.getStorageSync? Tokens? User profiles? Payment info? |
| **Subpackages / plugins** | Separate subpackages, third-party plugins — each has its own attack surface |
| **Update mechanism** | Does the app check for updates? Is there a forced update path? Can it be bypassed? |

---


## Card Exit

Classify the result, update evidence and attempted methods, record capability or risk changes, identify affected paths, and apply the return contract in [../module-continuity.md](../module-continuity.md).
