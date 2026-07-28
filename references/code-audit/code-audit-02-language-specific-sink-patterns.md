# Code Audit Capability: Language-Specific Sink Patterns

## Contents

- [Language-Specific Sink Patterns](#language-specific-sink-patterns)
  - [Java](#java)
  - [PHP](#php)
  - [Python](#python)
  - [JavaScript/Node.js](#javascriptnodejs)
  - [Go](#go)
  - [C# / .NET](#c-net)


> Apply [../module-continuity.md](../module-continuity.md). Inherit the engagement, parent path, current capability, evidence, authorization profile, and module stack. Do not initialize a separate workflow. Checkpoint material results and return them to the parent path before leaving this card.

## Language-Specific Sink Patterns

Do not search for "vulnerable" or "dangerous" as keywords. Search for the actual function calls that indicate dangerous operations.

### Java

| Category | Sink Functions |
|---|---|
| SQL | `Statement.executeQuery()`, `PreparedStatement` with concatenation (not parameterized), `jdbcTemplate.query()` with `+` concatenation, JPA native query with string concat, MyBatis `${}` (not `#{}`) |
| Command exec | `Runtime.getRuntime().exec()`, `ProcessBuilder` with user input, `Runtime.exec()` |
| Deserialization | `ObjectInputStream.readObject()`, `ObjectMapper.readValue()` with default typing, `XStream.fromXML()`, `Yaml.load()` (not `Yaml.safeLoad()`), `HessianInput.readObject()` |
| File path traversal | `File()` with unvalidated user input, `Paths.get()`, `FileInputStream()`, `ServletFileUpload` + no path sanitization |
| XXE | `DocumentBuilderFactory` (XXE enabled by default in Java 7), `SAXParserFactory`, `XMLInputFactory` without `XMLInputFactory.IS_SUPPORTING_EXTERNAL_ENTITIES=false`, `TransformerFactory` without `FEATURE_SECURE_PROCESSING` |
| SSRF | `URL.openConnection()`, `HttpURLConnection`, `RestTemplate`, `HttpClient`, `okhttp3` — any HTTP client with user-controlled host/URL |
| Template injection | `Velocity.evaluate()`, `FreeMarker Template.process()` |
| JNDI injection | `InitialContext.lookup(user_input)`, `Context.lookup()` (Log4Shell = `InitialContext.lookup()` with JNDI string) |
| SpEL injection | `ExpressionParser.parseExpression(user_input)`, `SpelExpressionParser`, `@Value()` in Spring with user-controlled expression |

**Quick audit script**:
```bash
grep -rn "readObject\|ObjectInputStream" --include="*.java"
grep -rn "Runtime.getRuntime()\|ProcessBuilder" --include="*.java"
grep -rn "\.exec(\|\.lookup(" --include="*.java"
grep -rn "DocumentBuilderFactory\|SAXParserFactory\|XMLInputFactory" --include="*.java"
grep -rn "\.load(" --include="*.java" | grep -v "safeLoad\|\.class"
```

### PHP

| Category | Sink Functions |
|---|---|
| Command injection | `system()`, `exec()`, `shell_exec()`, `passthru()`, `popen()`, `proc_open()`, `` `backtick` `` |
| Code injection | `eval()`, `assert()` (in PHP < 8), `preg_replace()` with `/e` (PHP < 7), `create_function()`, `include()`/`require()` with user input (LFI → RCE) |
| SQL injection | `mysql_query()`, `mysqli_query()`, `pg_query()`, PDO with emulated prepares, Laravel `DB::raw()` with concatenation, `$wpdb->query()` with unsanitized input |
| File inclusion | `include`, `require`, `include_once`, `require_once` with variable path, `file_get_contents()` with `php://input` or remote URL |
| Deserialization | `unserialize()` — any occurrence is worth examining |
| File upload | `move_uploaded_file()`, `copy()` with `$_FILES[...]['tmp_name']`, no `is_uploaded_file()` check, no extension validation |
| SSRF/XSPA | `file_get_contents(url)`, `curl_exec()`, `fopen(url)`, `fsockopen()` |
| XXE | `simplexml_load_string()`, `DOMDocument::loadXML()` with `LIBXML_NOENT` (entity loading enabled by default) |

**Quick audit script**:
```bash
grep -rn "unserialize\|eval\|exec(\|shell_exec\|system(" --include="*.php"
grep -rn "\$_GET\[\|\$_POST\[\|\$_REQUEST\[\|\$_COOKIE\[" --include="*.php" | head -50
grep -rn "include\|require" --include="*.php" | grep '\$'
grep -rn "mysql_query\|mysqli_query\|->query(" --include="*.php"
```

### Python

| Category | Sink Functions |
|---|---|
| Command injection | `os.system()`, `os.popen()`, `subprocess.call(shell=True)`, `subprocess.Popen(shell=True)`, `eval()`, `exec()`, `compile()` |
| Deserialization | `pickle.load()`, `pickle.loads()`, `yaml.load()` (not `yaml.safe_load()`), `dill.load()`, `torch.load()` (pickle-based), `joblib.load()`, `marshal.loads()` |
| SSTI | `render_template_string(user_input)`, `jinja2.Template(user_input).render()`, `mako.template.Template(user_input)` |
| SQL injection | Raw SQL with `%` formatting, `.format()`, f-strings, Django `raw()`, SQLAlchemy `text()` with concatenation |
| SSRF | `requests.get(user_url)`, `urllib.request.urlopen(user_url)`, `httpx.get(user_url)`, `aiohttp.ClientSession().get(user_url)` |
| File path | `open(user_path)`, `Path.read_text()`, `shutil.copy()` |

**Quick audit script**:
```bash
grep -rn "pickle.loads\|pickle.load\|yaml.load(" --include="*.py" | grep -v "safe_load"
grep -rn "subprocess.*shell=True\|os\.system\|os\.popen\|exec(\|eval(" --include="*.py"
grep -rn "requests\.\(get\|post\|put\|delete\)(" --include="*.py" | grep -v "http://localhost"
grep -rn "render_template_string\|\.from_string(" --include="*.py"
```

### JavaScript/Node.js

| Category | Sink Functions |
|---|---|
| Command injection | `child_process.exec()`, `child_process.spawn()` with shell:true, `child_process.execSync()`, `eval()`, `Function()` |
| Code injection | `eval()`, `new Function()`, `vm.runInNewContext()` (sandbox escape), `setTimeout(string)`, `setInterval(string)` |
| Prototype pollution | `obj[key][key2] = value` (recursive merge), `lodash.merge()`, `Object.assign()` with user-controlled keys, `__proto__` not filtered |
| SSTI | `pug.render(user_input)`, `handlebars.compile(user_input)`, `ejs.render(user_input)`, `_.template(user_input)` (lodash) |
| NoSQL injection | `mongodb.collection.find({username: {$ne: ''}})` — user input used directly as query object |
| Path traversal | `fs.readFile(user_path)`, `path.join()` without normalize, `express.static()` |
| SSRF | `axios.get(user_url)`, `http.get(user_url)`, `fetch(user_url)`, `request(user_url)` |

**Quick audit script**:
```bash
grep -rn "child_process\.exec\|\.execSync\|eval(" --include="*.js"
grep -rn "\.merge\|\.extend\|Object\.assign" --include="*.js"
grep -rn "\.render(" --include="*.js" | grep -v "res\.render"
```

### Go

| Category | Sink Functions |
|---|---|
| Command injection | `os/exec.Command(user_input)`, `exec.CommandContext()` with unsanitized args |
| SQL injection | `db.Query(fmt.Sprintf(...))`, `db.Exec(fmt.Sprintf(...))` — any string formatting into SQL |
| SSRF | Any `http.Get()`, `http.Post()`, `http.NewRequest()` with user-controlled URL |
| Template injection | `html/template` → auto-escapes (safe), but `text/template` → raw output (SSTI if user controls template content) |
| Path traversal | `ioutil.ReadFile(user_path)`, `os.Open(user_path)` without Clean/Abs |

### C# / .NET

| Category | Sink Functions |
|---|---|
| Command injection | `Process.Start(user_input)`, `Process.StartInfo.Arguments` from user input |
| SQL injection | `SqlCommand.CommandText = user_string`, string concatenation in SQL, Entity Framework raw SQL |
| Deserialization | `BinaryFormatter.Deserialize()`, `DataContractSerializer` with unknown types, `Json.NET` with `TypeNameHandling.All` or `TypeNameHandling.Objects`, `LosFormatter.Deserialize()`, `ObjectStateFormatter.Deserialize()` |
| XXE | `XmlDocument.Load()` without `XmlResolver = null`, `XmlReader` without `DtdProcessing = DtdProcessing.Prohibit` |
| Path traversal | `File.ReadAllText(user_path)`, `Path.Combine()` without validation |

---


## Card Exit

Classify the result, update evidence and attempted methods, record capability or risk changes, identify affected paths, and apply the return contract in [../module-continuity.md](../module-continuity.md).
