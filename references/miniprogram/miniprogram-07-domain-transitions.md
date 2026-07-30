# Mini-Program Operations: Domain Transitions

> Apply [../module-continuity.md](../module-continuity.md). Inherit the engagement, parent path, current capability, evidence, authorization profile, and module stack. Do not initialize a separate workflow. Checkpoint material results and return them to the parent path before leaving this card.

## Domain Transitions

- **→ Web/API**: Backend testing is the primary objective. Most mini-program vulnerabilities are actually backend authorization flaws exposed through the mini-program interface.
- **→ code-audit**: For recovered JS bundles that contain business logic or cryptographic operations.
- **→ reverse-protocol**: For native mini-program runtimes or custom encryption in communications.
- **→ cloud**: For cloud functions (WeChat Cloud Base, Alipay Cloud Function) that may have broader cloud access.
- **→ business-logic**: For payment logic, coupon/incentive abuse, workflow bypass, and state-machine attacks — these are common in mini-program commerce flows and follow the same decision framework regardless of platform


## Main Attack Chain

1. **Extract package and routes**: Unpack the mini-program, extract the app config, JS bundles, and backend endpoint list. Identify the authentication flow (wx.login → code → backend → custom session, or alternative).
2. **Test platform identity trust**: Verify that the backend validates the platform-asserted identity (OpenID/UnionID) rather than trusting client-provided user identifiers. Test code reuse, AppID binding, and session_key handling.
3. **Test backend authorization from outside the mini-program**: Replay API calls captured from the mini-program using a standard HTTP client. The mini-program runtime is just a specialized HTTP client — all authorization tests from Web/API apply.
4. **Prove backend impact**: The finding is never "mini-program client code has a flaw" unless that flaw changes a server-side outcome. A client-side restriction bypass only matters if the backend accepts the bypassed request.
5. **Return to Web/API**: Every mini-program backend finding is actually a Web/API finding. Transition with the exact endpoint, auth token, session context, and the authorization gap demonstrated.

## Transition Handoff

Carry the platform, app identifier, package version, routes, endpoints, account and session context, platform identity fields, signing or cryptographic logic, cloud-function references, and the exact server-side or runtime question.

## Card Exit

Classify the result, update evidence and attempted methods, record capability or risk changes, identify affected paths, and apply the return contract in [../module-continuity.md](../module-continuity.md).
