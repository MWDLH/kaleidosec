# Web And API Operations: Attack Primitives: Traditional Web Vulnerabilities: Deserialization Attacks

> Apply [../module-continuity.md](../module-continuity.md). Keep the same engagement and parent path as the calling route. Load this scene only when current evidence supports its prerequisites.

### Deserialization Attacks — Language-Aware Decision

Deserialization is language-specific, framework-specific, and version-specific. A gadget chain for Jackson won't work on XStream. A PHP chain for Laravel won't work on Symfony. **Identify the exact deserialization entry point before selecting payloads.**

### Decision Entry

Load this scene when:
- [FACT] A serialized object appears in a request, response, cookie, or hidden form field
- [FACT] Base64-encoded blob with language-specific prefixes: `rO0` (Java), `Tzo`/`Tzoy`/`Tzoz` (PHP serialized), `gASV` (Python pickle), `AAEAAAD/////` (.NET BinaryFormatter)
- [FACT] YAML input accepted where `!!java`/`!!python` tags may be processed
- [FACT] A `Content-Type: application/x-java-serialized-object` or similar header is observed
- [INFERENCE] The application accepts user-supplied data that is deserialized (job parameters, session data, cached objects, RPC arguments)

Do not load solely on: CVE scanner alert without confirmed deserialization entry point; generic `readObject` grep match without data-flow confirmation from user input.

### Attack Progression Decision Tree

```
0. CONFIRM THE DESERIALIZATION ENTRY POINT (before any payload)
   ├─ Trace the user-controlled data to a deserialization call — a serialized blob in a request
   │   does not prove it reaches a deserializer. Verify: is the blob actually deserialized,
   │   or is it stored/compared as an opaque string?
   ├─ Modify one byte of the serialized data → does the application behavior change?
   │   A different error, stack trace, or response strongly suggests deserialization.
   └─ A base64 blob alone is not a finding. Do not proceed to gadget selection without
       confirming the data reaches a deserialization function.

1. Identify the language and serialization format
   ├─ Java serialized: starts with 0xAC 0xED, base64 often begins with "rO0"
   ├─ PHP serialized: pattern like a:N;{s:N:"...";...} or base64 starting with "Tzo"
   ├─ Python pickle: starts with 0x80 (protocol 2+) or base64 "gASV"
   ├─ .NET BinaryFormatter: base64 starts with "AAEAAAD/////"
   ├─ JSON with type metadata: contains "$type", "__type", "@class", "javaType"
   └─ YAML: contains "!!" type tags like "!!javax.script.ScriptEngineManager"

2. Identify the exact framework — gadget chains are framework-specific AND version-specific
   │
   ├─ Java deserialization:
   │   ├─ CommonsCollections (CC1-CC7) → many legacy apps, WebLogic, JBoss
   │   ├─ Spring + Jackson → @JsonTypeInfo, enableDefaultTyping, or JsonTypeInfo.Id.CLASS
   │   ├─ XStream → <dynamic-proxy>, <sorted-set>, processAnnotations
   │   ├─ SnakeYAML → !!javax.script.ScriptEngineManager, CVE-2022-1471
   │   ├─ Hessian/Burlap → HessianInput.readObject(), usually no type check
   │   └─ Kryo → RegistrationRequired=false (known classes bypass)
   │
   ├─ PHP deserialization:
   │   ├─ Native unserialize() → phpggc chains: Laravel, Symfony, Drupal, WordPress, CodeIgniter
   │   ├─ PHAR deserialization → phar:// stream triggers unserialize on metadata
   │   └─ Signed/encrypted serialized cookies → if key leaked, forge arbitrary objects
   │
   ├─ Python deserialization:
   │   ├─ pickle.loads() → __reduce__ gadget, built-in RCE
   │   ├─ yaml.load() (not safe_load) → !!python/object/apply:... → RCE
   │   ├─ PyTorch torch.load() → pickle-based, model files can contain code
   │   └─ joblib.load() → also pickle-based
   │
   ├─ .NET deserialization:
   │   ├─ BinaryFormatter → ysoserial.net: TypeConfuseDelegate, TextFormattingRunProperties
   │   ├─ JSON.NET TypeNameHandling → $type with known gadget, requires TypeNameHandling.All or Objects
   │   ├─ DataContractSerializer → known types in configuration
   │   └─ LosFormatter / ObjectStateFormatter → ViewState deserialization, MAC validation state
   │
   └─ Node.js deserialization:
       ├─ node-serialize / serialize-to-js → eval-based, immediately dangerous
       └─ js-yaml with !!js/function → schema: DEFAULT_FULL_SCHEMA or unsafe load

3. Select gadget chain by framework AND version — there is no "universal" first-test chain
   ├─ Determine the framework version before selecting a chain. A chain that works on
   │   CommonsCollections4 will not work on CommonsCollections3. The "first try" depends
   │   on the version, not on a fixed priority list.
   ├─ When version is unknown → first prove the deserialization call executes (modify harmless
   │   data in the serialized object and observe the application response). Then narrow the
   │   version by testing framework-specific features before attempting RCE chains.
   └─ Do not cycle through tool output chains. If the first version-matched chain fails,
       diagnose which prerequisite is missing before trying another.

4. Deliver the payload
   ├─ Is the payload base64-encoded? → yes for most HTTP-delivered Java/.NET chains
   ├─ Is the payload in a cookie/header/body/upload? → adapt encoding and transport
   └─ Does the response confirm deserialization? → error, timeout, or RCE signal
```

### Deserialization Entry Points By Framework

| Language | Signal | Framework | First Test — Prove Deserialization Exists |
|---|---|---|---|
| Java | base64 blob starting `rO0` | Native ObjectInputStream | Modify one byte of the blob → does application behavior change? (error difference, timeout, stack trace) |
| Java | JSON with `@class` or `@type` | Jackson | Send valid JSON without type metadata → accepted? Then add a non-existent `@class` → different error? |
| Java | XML with `<dynamic-proxy>` | XStream | Send valid XML without proxy → accepted? Add a malformed proxy → error reveals XStream? |
| Java | YAML config input | SnakeYAML | Send scalar YAML only → accepted? Add `!!` tag → does parser reject or process? |
| PHP | `O:N:"ClassName":M:{...}` | Native unserialize | Modify one byte of serialized data → does application behavior change? |
| PHP | `phar://` stream wrapper reachable | PHAR | Verify phar:// is accepted as a stream path before constructing polyglot |
| Python | `\x80\x04\x95...` (pickle v4) | pickle.loads | Modify pickle bytes → does application error change? |
| Python | `!!python/object/apply:subprocess.Popen` | PyYAML | Test `yaml.load` vs `yaml.safe_load` → does unsafe load actually happen? |
| .NET | base64 `AAEAAAD/////` | BinaryFormatter | Modify one byte → error reveals BinaryFormatter? |
| .NET | JSON `"$type":"..."` | JSON.NET | Test TypeNameHandling setting by sending JSON with and without $type → is type resolution active? |
| Node.js | `{"key":"_$$ND_FUNC$$_function(){...}"}` | node-serialize | Confirm the serialization format is node-serialize (not JSON, not msgpack) before testing eval |

### Failure Branches

| Failure Signal | Likely Cause | Next Variable |
|---|---|---|
| Payload sent, application returns generic error or empty response | The gadget chain does not match the framework version; or the deserialization fails silently (class not found on classpath) | Verify the framework version first. Test a non-RCE deserialization behavior change (e.g., modify non-code object data in the serialized blob) to confirm deserialization executes at all. If deserialization executes but RCE chain fails, the chain is wrong for this version — not the deserialization |
| Tool-generated chain fails across multiple versions | The tool's chain targets a class or library not present in this application; or the application uses a custom ClassLoader or resolveClass override that filters gadget classes | Enumerate what IS on the classpath (error messages, debug output, dependency files). A chain that relies on CommonsCollections won't work if the app doesn't include CommonsCollections. Check actual dependencies before cycling through chains |
| RCE payload returns connection error (LDAP/RMI/JNDI callback not received) | The callback absence could mean: gadget mismatch (chain didn't execute), deserialization didn't occur, DNS resolution failed, protocol blocked, callback service unreachable, execution chain error, OR egress filtering. Only one of several possibilities | Do NOT conclude "egress filtering" from callback absence alone. Test each hypothesis independently: confirm deserialization executes with a behavior-change test first; verify callback service is reachable from a known-good source; test a different protocol or callback destination. Only attribute the failure to egress filtering when independent outbound tests confirm the target cannot reach you while deserialization execution is separately confirmed |
| Deserialization confirmed (non-RCE behavior change observed) but all RCE chains fail | The runtime environment restricts execution (SecurityManager, container sandbox, seccomp, AppLocker) | Record the deserialization primitive as confirmed. Park the RCE path with a concrete reactivation condition. Test deserialization for lower-impact outcomes: file read via gadget, SSRF via URL class, information leak via exception handling. A deserialization primitive without RCE is still a finding — it means the application deserializes untrusted data |
| Base64 blob present but not deserialized — it's an opaque session token or cache key | The blob is never actually deserialized; it's stored and compared as a raw string | This is NOT a deserialization vulnerability. Do not spend time on it. Record the observation and move to the next attack class |

## Scene Exit

Return result classification, evidence, changed assumptions, affected paths, persistent changes, and the next parent-path decision.
