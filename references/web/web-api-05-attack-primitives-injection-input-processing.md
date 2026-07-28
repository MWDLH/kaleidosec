# Web And API Operations: Attack Primitives: Injection & Input Processing

> Apply [../module-continuity.md](../module-continuity.md). Inherit the engagement, parent path, current capability, evidence, authorization profile, and module stack. Do not initialize a separate workflow. Checkpoint material results and return them to the parent path before leaving this card.

## Attack Primitives: Injection & Input Processing

### SQL Injection — Beyond the Basic Payload

Don't start with `' OR 1=1--`. Start with **database fingerprinting**:

1. **Observe error behavior**: Does `'` produce an error? What error? (ODBC, JDBC, PDO, native driver — each has distinct error patterns)
2. **Observe blind behavior**: Does `' AND '1'='1` differ from `' AND '1'='2`? (Boolean-based blind)
3. **Observe timing**: `' AND SLEEP(5)--` (MySQL), `' WAITFOR DELAY '0:0:5'--` (MSSQL), `' AND pg_sleep(5)--` (PostgreSQL), `' AND DBMS_LOCK.SLEEP(5)--` (Oracle)
4. **Observe out-of-band**: confirm network reachability from the database server — use a controlled callback target authorized in the engagement scope
5. **Only after confirming injection** → determine: database type, version, current user, privileges, file read/write capabilities, command execution pathways.

**Database-specific exploitation paths**:

| DBMS | File Read | File Write | Command Execution | Key Config to Check |
|---|---|---|---|---|
| MySQL/MariaDB | LOAD_FILE() | SELECT ... INTO OUTFILE | UDF library (plugin_dir writable) | secure_file_priv, plugin_dir |
| PostgreSQL | pg_read_file() | COPY ... TO/FROM | CREATE EXTENSION, COPY FROM PROGRAM | pg_execute_server_program role |
| MSSQL | OPENROWSET BULK | xp_cmdshell disabled? Try sp_OACreate | xp_cmdshell, sp_OACreate, xp_regread/write | xp_cmdshell enabled? sp_configure |
| Oracle | UTL_FILE | UTL_FILE | DBMS_SCHEDULER, Java stored procedures | UTL_FILE_DIR, Java permissions |
| SQLite | readfile() | writefile() | load_extension() | Extension loading enabled? |

**Post-exploitation transitions from SQLi**:
- **Command execution obtained** → you are now at the OS level on the database host. Transition to [internal-ad domain](../internal/router.md): establish current position (whoami, ip, network reachability), then enumerate domain membership and lateral paths.
- **File read/write only, no command execution** → read web application source to find other injection points or hardcoded credentials; write a webshell to the web root if the web and DB share a filesystem.
- **Database contains linked servers (MSSQL)** → `EXEC sp_linkedservers` → `EXEC ('...') AT [linked_server]` — lateral movement through the database tier. Transition to internal-ad.
- **Database credentials differ from OS credentials** → the DB may run under a domain service account with broader privileges than the web server. Test the extracted credential against SMB/WinRM.

### Server-Side Request Forgery (SSRF) — Trust Chain Analysis

SSRF is not one vulnerability. It's a **trust chain exploration**. Model the target's network map:

```
Internet → [WAF/CDN] → [Load Balancer] → [Web App] → [Internal API: 10.x]
                                                    → [Metadata: 169.254.169.254]
                                                    → [Cache/Queue: Redis, RabbitMQ]
                                                    → [Database: 10.x]
                                                    → [Management: Jenkins, K8s API]
                                                    → [Cloud metadata IMDSv1/v2]
```

**SSRF protocol/encoding bypass matrix**:

| Technique | Example | When It Works |
|---|---|---|
| Alternative representation | `http://2130706433/` (decimal), `http://0x7F000001/` (hex), `http://017700000001/` (octal) | IPv4 parsing differences |
| DNS rebinding | Domain resolves to allowed IP first, then to internal IP | Long-lived SSRF with DNS TTL tricks |
| URL scheme switching | `file:///etc/passwd`, `gopher://`, `dict://`, `ftp://` | Library uses generic URL parser |
| Redirect following | External server responds 302 → `http://169.254.169.254/` | HTTP client follows redirects |
| IPv6 bypass | `http://[::ffff:169.254.169.254]/` | IPv6 support, IPv4-only filter |
| Host header vs URL divergence | Request to `http://safe.com/` with `Host: 169.254.169.254` | Front-end and back-end parse URL differently |
| URL encoding | Double-encoding, Unicode normalization, backslash as separator | URL parser inconsistency between filter and fetcher |
| CRLF injection | `http://safe.com/%0d%0aHost:%20169.254.169.254` | HTTP library with CRLF in URL |

**Cloud metadata service differences**:

| Cloud | Metadata Endpoint | IMDSv1 | IMDSv2 | Key Header/Token |
|---|---|---|---|---|
| AWS | 169.254.169.254 | Yes (GET) | Yes (PUT for token) | `X-aws-ec2-metadata-token` (v2) |
| Azure | 169.254.169.254 | No | Only (with `Metadata: true` header) | `Metadata: true` |
| GCP | 169.254.169.254, metadata.google.internal | Yes (with `Metadata-Flavor: Google` header or without) | Required header | `Metadata-Flavor: Google` |
| DigitalOcean | 169.254.169.254 | Yes | No | None |
| Alibaba Cloud | 100.100.100.200 | Yes | No | None |
| OpenStack | 169.254.169.254 | Yes | No | None |

**Post-exploitation transitions from SSRF**:
- **Metadata credentials obtained** → you have cloud IAM credentials. Transition to [cloud domain](../cloud/router.md): validate the credential (`get-caller-identity`), enumerate effective permissions, model IAM escalation paths.
- **Internal service reachable (HTTP)** → you reached a web application, API, or management panel on an internal host. Re-enter Web/API testing from the internal network position. The internal service may trust requests from the exploited host without authentication.
- **Internal service reachable (non-HTTP: Redis, SMTP, database protocol via gopher/dict)** → transition to [infrastructure domain](../infrastructure/router.md): test the specific service for unauthorized access, default credentials, or data exposure.
- **File read via `file://` or `gopher://`** → you have local file read on the web server. Read configuration files for credentials, source code for other injection points, or `/proc/self/environ` for environment variables. Transition to internal-ad if the host is domain-joined.

### Deserialization Attack Decision Framework

Don't blindly throw ysoserial payloads. First answer: **what language/framework? Where does untrusted input enter the deserialization call?**

| Language | Common Frameworks | Danger Signs | Test Approach |
|---|---|---|---|
| Java | ObjectInputStream, Jackson, XStream, SnakeYAML, Hessian, Kryo | `readObject()`, `@JsonProperty`, `<java>`, base64+`rO0` prefix | ysoserial gadget chains, marshalsec, JNDI injection via LDAP/RMI |
| PHP | `unserialize()`, Laravel, Symfony, Drupal | User input reaching `unserialize()`, serialized session handlers, serialized cookies | phpggc gadget chains, `__wakeup`/`__destruct`/`__toString` magic methods |
| Python | pickle, PyYAML `yaml.load()`, jsonpickle | `pickle.loads(user_input)`, `yaml.load(user_input)` (not `safe_load`) | `__reduce__` gadget, `yaml.load` with `!!python/object` |
| .NET | BinaryFormatter, DataContractSerializer, JSON.NET TypeNameHandling | `$type` in JSON, `TypeNameHandling.All` or `Objects` | ysoserial.net, TypeConfuseDelegate |
| Ruby | Marshal.load, YAML.load | `Marshal.load(params[:data])`, `YAML.load` (not `safe_load`) | Universal RCE deserialization gadget (pre-2.7 Ruby Marshal) |
| Node.js | node-serialize, serialize-to-js, `eval()` on JSON | `unserialize()` from npm packages, `child_process` in templates | `require('child_process').exec()` in IIFE |

**Critical PHP deserialization pattern**: Even if you can't find a gadget chain in the application's own classes, the application likely includes Composer dependencies. `phpggc -l` lists all available gadget chains by framework.

**Post-exploitation transition from deserialization RCE**: Same OS-level transition as SQLi → command execution. Establish position, enumerate network, transition to internal-ad or cloud.

### HTTP Request Smuggling Decision Tree

1. **Identify front-end/back-end architecture**: Different servers for routing vs application? CDN? Load balancer? HTTP/2 downgrade to HTTP/1.1 at any hop?
2. **Determine which variant applies** — connection reuse must be confirmed; a single timeout is not sufficient to establish smuggling:
   - **CL.TE**: Front-end uses Content-Length, back-end uses Transfer-Encoding → Send `Transfer-Encoding: chunked` with conflicting small CL → back-end reads more than front-end intended
   - **TE.CL**: Front-end uses Transfer-Encoding, back-end uses Content-Length → Send chunked body with trailing content beyond CL → back-end processes trailing as next request
   - **TE.TE**: Both use Transfer-Encoding, but interpret header obfuscation differently → Send `Transfer-Encoding: chunked\r\nTransfer-Encoding: x` — one engine treats as chunked, other treats as identity
3. **Test signal**: Confirm connection reuse across multiple requests. Does a request time out (waiting for bytes from a poisoned socket)? Does a subsequent innocent request receive a 400 or unexpected response? Is the behavior reproducible?
4. **Exploit path**: Request queue poisoning (steal other users' requests), response queue poisoning (control responses to other users), cache poisoning via smuggled content. Establish safe stop conditions before testing on production connections.

### Server-Side Template Injection (SSTI) Quick Reference

| Engine | Detection Payload | Key Classes/Functions |
|---|---|---|
| Jinja2 (Python) | `{{7*7}}` → 49 | `{{''.__class__.__mro__[2].__subclasses__()}}` → find Popen |
| Twig (PHP) | `{{7*7}}` → 49 | `{{_self.env.registerUndefinedFilterCallback('exec')}}{{_self.env.getFilter('id')}}` |
| Freemarker (Java) | `${7*7}` → 49 | `<#assign ex="freemarker.template.utility.Execute"?new()>${ex("id")}` |
| Velocity (Java) | `#set($x=7*7)$x` → 49 | `#set($s="")$s.getClass().forName("java.lang.Runtime").getMethod(...)` |
| Smarty (PHP) | `{7*7}` → 49 | `{system('id')}` if enabled, `{Smarty_Internal_Write_File}` |
| ERB (Ruby) | `<%= 7*7 %>` → 49 | `<%= system('id') %>` |
| Handlebars (JS) | `{{constructor.constructor('return this.process')().mainModule.require('child_process').execSync('id')}}` | Depends on sandbox escape |

### Injection Failure Classification

| Failure | Likely Cause | Next Variable |
|---|---|---|
| No error or behavioral difference from any payload | Input is not interpreted by the suspected sink; or the injection point is wrong; or output encoding hides the difference | Change the injection point (different parameter, header, or body field); test with a guaranteed-safe value first to confirm the parameter is reflected or processed |
| Error but no data extraction (WAF block, generic error page, or connection reset) | WAF or input filter detected the payload pattern; or the database error is caught and replaced with a generic message | Change encoding or structure of the payload; use blind/time-based methods instead of error-based. Rotating source IP is not a routine failure branch — only consider it when the authorization profile explicitly allows source restriction circumvention. |
| Timing-based test shows delay but cannot confirm database/command | Network latency, server load, or caching causes false-positive timing | Establish a statistical baseline appropriate to the target's response-time distribution and the authorized test scale; choose a delay that exceeds normal variance by a clear margin. Verify with a second independent timing test or an alternative blind technique before concluding. |
| OOB callback not received | Egress filtering blocks outbound connections from the database/web server; DNS, HTTP, proxy, or resolver configuration prevents the callback | Diagnose which layer failed: test DNS resolution independently, test HTTP egress independently, verify the callback destination is reachable from the operator side. Do not default to switching protocols — use the protocol that matches the diagnosed egress path. |


## Card Exit

Classify the result, update evidence and attempted methods, record capability or risk changes, identify affected paths, and apply the return contract in [../module-continuity.md](../module-continuity.md).
