# Mini-Program Operations


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
| [Build The Surface](miniprogram-01-build-the-surface.md) | Entry: package, AppID or backend domain not yet modeled. | Which platform, backend and communication paths are in scope? |
| [Coverage Gate](miniprogram-02-coverage-gate.md) | Before the first material validation, and after any capability or position change. | Which surfaces are covered, which are not, and is the next action justified anyway? |
| [Attack Primitives: Core Vulnerability Classes](miniprogram-03-attack-primitives-core-vulnerability-classes.md) | API hosts, endpoints or signing parameters extracted from the package. | Which core class applies to this endpoint, and what proves it? |
| [Platform-Specific: WeChat Mini-Program WebView](miniprogram-04-platform-specific-wechat-mini-program-webview.md) | `web-view` component or H5 navigation present; business domain in `webviewBusinessDomain`. | Which WebView boundary can be crossed, and what is the payload context? |
| [Platform-Specific: Other Mini-Program Platforms](miniprogram-05-platform-specific-other-mini-program-platforms.md) | Non-WeChat platform identified (Alipay, Douyin, Baidu, others). | Which platform-specific boundary exists, and what differs from WeChat? |
| [Interpret Results](miniprogram-06-interpret-results.md) | After any material result, positive or negative. | What does this prove, and does it change the path ranking? |
| [Domain Transitions](miniprogram-07-domain-transitions.md) | Evidence implies a different domain, identity boundary, execution surface or network position. | Where are we now, what authority do we hold, and what is the return target? |
| [Recollect When](miniprogram-08-recollect-when.md) | New identity, privilege, asset, role, trust edge or network position. | What must be re-collected, and what evidence can be safely reused? |
