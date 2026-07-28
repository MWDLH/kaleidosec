# Mini-Program Operations: Build The Surface

> Apply [../module-continuity.md](../module-continuity.md). Inherit the engagement, parent path, current capability, evidence, authorization profile, and module stack. Do not initialize a separate workflow. Checkpoint material results and return them to the parent path before leaving this card.

## Build The Surface

Acquire the authorized package (`.wxapkg` for WeChat, `.alipay` for Alipay, `.baidu` for Baidu, etc.) or development artifact. Record platform, app identifier (AppID), version, build mode (dev/trial/release), subpackages, framework, permissions declared, routes/pages, cloud functions, storage usage, update behavior, and backend domains.

Mini-programs are **not web apps running in a browser**. They run inside the platform's native runtime (WeChat, Alipay, Douyin, Baidu) with platform-provided APIs, cloud functions, and identity layers. The trust boundary is different — the platform asserts identity (OpenID/UnionID), and the mini-program's backend must validate that assertion.

### Package Acquisition and Extraction

```bash
# WeChat mini-program (.wxapkg)
# Option 1: From rooted Android device
adb shell ls /data/data/com.tencent.mm/MicroMsg/<user_hash>/appbrand/pkg/
adb pull /data/data/com.tencent.mm/MicroMsg/<user_hash>/appbrand/pkg/<AppID>.wxapkg

# Option 2: From WeChat PC client
# Located in: C:\Users\<user>\Documents\WeChat Files\<wxid>\Applet\<appid>\
# Or: ~/Library/Containers/com.tencent.xinWeChat/Data/Library/Application Support/com.tencent.xinWeChat/...

# Unpack wxapkg
# Use: https://github.com/superggn/unwxapkg or wxappUnpacker
node wuWxapkg.js <file>.wxapkg

# Unpack subpackages (separate .wxapkg files with _sub suffix)
# These contain additional pages and logic — often the most interesting parts

# Alipay mini-program (.alipay → .apk renamed)
# Similar extraction from Alipay app data directory
# Use Alipay-specific unpacker (e.g., alipay-mini-unpacker)
```

### What to Extract First

```bash
# After unpacking, examine these first:
app-config.json          # App metadata, permissions, plugins, network timeout, worker config
app-service.js           # Main logic bundle (often minified/obfuscated)
app.json                 # Pages, window config, tabBar, networkTimeout, requiredBackgroundModes
project.config.json      # Dev settings (debug mode, cloud function root, miniprogramRoot)

# Search for backend endpoints
grep -rnE "https?://[a-zA-Z0-9._-]+" unpacked/ | sort -u
grep -rnE "wx\.request|wx\.uploadFile|wx\.downloadFile" unpacked/
grep -rnE "apiUrl|baseUrl|serverUrl|host_url|domain" unpacked/
grep -rnE "AppId|appid|APPID|app_key|appSecret|secretKey" unpacked/

# Search for cloud functions
grep -rnE "wx\.cloud\.callFunction|cloud\.init" unpacked/
grep -rnE "\"function\":" unpacked/  # cloud function names

# Search for platform identity usage
grep -rnE "wx\.login|code2Session|getOpenId|getUnionId" unpacked/
grep -rnE "wx\.getUserInfo|wx\.getPhoneNumber|wx\.getLocation" unpacked/
```

---


## Card Exit

Classify the result, update evidence and attempted methods, record capability or risk changes, identify affected paths, and apply the return contract in [../module-continuity.md](../module-continuity.md).
