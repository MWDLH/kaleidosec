# Mini-Program Operations: Platform-Specific: Other Mini-Program Platforms

> Apply [../module-continuity.md](../module-continuity.md). Inherit the engagement, parent path, current capability, evidence, authorization profile, and module stack. Do not initialize a separate workflow. Checkpoint material results and return them to the parent path before leaving this card.

## Platform-Specific: Other Mini-Program Platforms

### Alipay Mini-Program
- Authentication: `my.getAuthCode()` → code → backend → Alipay API → user_id
- Similar trust chain issues as WeChat — test `auth_code` reuse and cross-app code usage
- `my.getOpenUserInfo()` may have different privacy scopes — check if backend validates scope

### Baidu Smart Mini-Program
- Uses `swan.login()` / `swan.getUserInfo()`
- Similar patterns — different API names, same security principles

### Douyin/ByteDance Mini-Program
- `tt.login()` / `tt.getUserInfo()`
- Note: Douyin mini-programs have stricter review — many vulnerabilities come from incorrect use of platform APIs rather than platform API flaws

---


## Card Exit

Classify the result, update evidence and attempted methods, record capability or risk changes, identify affected paths, and apply the return contract in [../module-continuity.md](../module-continuity.md).
