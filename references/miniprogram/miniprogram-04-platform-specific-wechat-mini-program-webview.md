# Mini-Program Operations: Platform-Specific: WeChat Mini-Program WebView

> Apply [../module-continuity.md](../module-continuity.md). Inherit the engagement, parent path, current capability, evidence, authorization profile, and module stack. Do not initialize a separate workflow. Checkpoint material results and return them to the parent path before leaving this card.

## Platform-Specific: WeChat Mini-Program WebView

The `<web-view>` component loads web pages within the mini-program. This is a critical trust boundary.

**Test**:
1. Can the WebView load arbitrary URLs? (Check `src` attribute — is it hardcoded or user-controlled?)
2. Can the web page call `wx.miniProgram.postMessage` to exfiltrate data from the mini-program?
3. Can the web page call `wx.miniProgram.navigateBack` to manipulate navigation?
4. Does the WebView pass authentication to the loaded page? (URL parameters with tokens?)
5. If the WebView loads HTTP (not HTTPS) pages — MITM within the mini-program context
6. If the WebView loads `https://open.weixin.qq.com/connect/oauth2/authorize` with a different `appid` — potential OAuth token theft

---


## Card Exit

Classify the result, update evidence and attempted methods, record capability or risk changes, identify affected paths, and apply the return contract in [../module-continuity.md](../module-continuity.md).
