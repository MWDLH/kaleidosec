# Reverse Engineering And Protocol Capability: Workflow By Target Type

## Contents

- [Workflow By Target Type](#workflow-by-target-type)
  - [Native Binary (C/C++/Rust — .exe, .so, .dylib, ELF)](#native-binary-ccrust-exe-so-dylib-elf)
  - [Native Binary — Common Patterns to Recognize](#native-binary-common-patterns-to-recognize)
  - [Java / Kotlin Bytecode (APK)](#java-kotlin-bytecode-apk)
  - [.NET Assembly](#net-assembly)
  - [Obfuscated Code](#obfuscated-code)
  - [Protocol Reverse Engineering](#protocol-reverse-engineering)
  - [Runtime Analysis with Frida](#runtime-analysis-with-frida)


> Apply [../module-continuity.md](../module-continuity.md). Inherit the engagement, parent path, current capability, evidence, authorization profile, and module stack. Do not initialize a separate workflow. Checkpoint material results and return them to the parent path before leaving this card.

## Workflow By Target Type

### Native Binary (C/C++/Rust — .exe, .so, .dylib, ELF)

**Triage phase (5 minutes)**:
```bash
file <binary>                        # ELF 64-bit? PE32+? Mach-O?
strings <binary> | head -100         # Function names, URLs, error messages, crypto constants
strings <binary> | grep -iE "http|https|ssl|aes|rsa|sha|md5|encrypt|decrypt|key|secret|password"
readelf -h <binary> 2>/dev/null || objdump -f <binary>  # Architecture, entry point
```

**For Android native libraries**:
```bash
file lib/*.so                        # ARM32, ARM64, or x86?
strings lib/*.so | grep -iE "http|api|sign|token|key"
# Check for JNI exports (Java_<package>_<class>_<method> naming)
readelf -s lib/*.so | grep Java_
```

**Disassembly — find the function you need**:
```python
# IDA Python script: find functions referencing a specific string
import idaapi, idautils, idc

target = "X-Signature"  # or any string from strings output
for ea in idautils.Strings():
    if target in str(ea):
        print(f"String '{target}' at {hex(ea.ea)}")
        # Find cross-references to this string
        for xref in idautils.XrefsTo(ea.ea):
            func = idaapi.get_func(xref.frm)
            if func:
                print(f"  Referenced by function at {hex(func.start_ea)}")
```

**Ghidra alternative** (free, works on all platforms):
```
# Open binary in Ghidra, then:
# Window → Defined Strings → filter for your target keyword
# Right-click → References → Show References to Address
# Navigate to referencing function → decompile (Ctrl+E)
```

### Native Binary — Common Patterns to Recognize

| What You See | What It Means |
|---|---|
| `OPENSSL_init`, `EVP_EncryptInit_ex`, `AES_set_encrypt_key`, `RSA_public_encrypt` | OpenSSL crypto — look for key material passed to init functions |
| `Java_` prefix functions | JNI exports — called from Java/Kotlin code in Android |
| `ptrace`, `isDebuggerConnected`, `/proc/self/status` reads | Anti-debugging — the question path may need bypass |
| Base64 alphabet strings (`ABCDEFGH...`) | Base64 encoding — often used in request signing or token encoding |
| Hardcoded hex strings (32, 64, 128 bytes) | Possible AES keys, HMAC secrets — extract and test |
| `curl_easy_setopt`, `NSURLSession`, `HttpClient` | HTTP client setup — find where URL/headers/body are constructed |

### Java / Kotlin Bytecode (APK)

Use **jadx** (best for readability) or **Bytecode Viewer**:
```
jadx-gui app.apk
# Navigate: Source code → <package> → find the class
# Search: Ctrl+Shift+F → search for string/regex across entire decompiled codebase
# Find usage: Right-click on method/class → Find Usage
```

### .NET Assembly

Use **dnSpy** (Windows) or **ILSpy**:
```
dnSpy <app>.exe
# Search: Ctrl+Shift+K → search all loaded assemblies
# Analyze: Right-click on a method → Analyze → see call tree
# Edit: Right-click on method → Edit Method → modify and recompile in real-time
# Debug: Attach to running process → set breakpoints → step through
```

### Obfuscated Code

| Obfuscation | Tool/Approach |
|---|---|
| ProGuard / R8 (Android) | jadx usually handles this; mapping.txt may recover original names |
| .NET obfuscator (ConfuserEx, .NET Reactor) | de4dot first, then dnSpy |
| JavaScript minification | Prettier/Beautifier first, then manual rename, or use source maps (`.js.map`) if present |
| JavaScript obfuscation (JSFuck, aaencode) | Trace step by step in browser console — the final payload is what matters, not the wrapper |
| String encryption (XOR, custom) | Find decrypt function in binary → write a decoder script → decrypt all strings |
| Control flow flattening | IDA plugin (D-810), or track the state variable → build the real control flow |
| Packed binary | If `strings` shows UPX/MPRESS → try `upx -d`. If custom packer → dump from memory at runtime |

### Protocol Reverse Engineering

When you need to understand a custom protocol (binary TCP, WebSocket with custom serialization, proprietary RPC):

1. **Capture traffic**: Wireshark/tcpdump between client and server
2. **Identify patterns**: Fixed header size? Magic bytes? Length field? Type/command field? Sequence number? Checksum/CRC?
3. **Isolate fields**: Change one input → observe which bytes change in the capture
4. **Test assumptions**: Write a small script that replays/modifies captured packets. Does changing the length field break parsing? Does removing the CRC cause rejection? Does incrementing the sequence number work?
5. **For TLS-wrapped protocols**: Intercept via proxy (Burp for HTTP-based, custom MITM for binary) or hook the TLS library functions in the client (SSL_read/SSL_write via Frida)

### Runtime Analysis with Frida

When static analysis hits a wall (obfuscation, anti-analysis, runtime-decrypted code):

```javascript
// Frida: Hook a native function and inspect arguments
const targetModule = Process.getModuleByName("libsign.so");
const targetFunc = targetModule.getExportByName("generate_signature");
Interceptor.attach(targetFunc, {
    onEnter: function(args) {
        console.log("generate_signature called");
        console.log("  arg0 (data): " + Memory.readUtf8String(args[0]));
        console.log("  arg1 (key): " + hexdump(args[1], {length: 32}));
    },
    onLeave: function(retval) {
        console.log("  return: " + Memory.readUtf8String(retval));
    }
});
```

```javascript
// Frida: Hook a Java method in Android
Java.perform(function() {
    var SignUtil = Java.use("com.example.app.crypto.SignUtil");
    SignUtil.sign.implementation = function(data, secret) {
        console.log("[*] SignUtil.sign called");
        console.log("    data: " + data);
        console.log("    secret: " + secret);
        var result = SignUtil.sign.call(this, data, secret);
        console.log("    result: " + result);
        return result;
    };
});
```

---


## Card Exit

Classify the result, update evidence and attempted methods, record capability or risk changes, identify affected paths, and apply the return contract in [../module-continuity.md](../module-continuity.md).



