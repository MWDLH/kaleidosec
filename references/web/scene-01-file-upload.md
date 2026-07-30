# Web And API Operations: Attack Primitives: Traditional Web Vulnerabilities: File Upload Attacks

> Apply [../module-continuity.md](../module-continuity.md). Keep the same engagement and parent path as the calling route. Load this scene only when current evidence supports its prerequisites.

### File Upload Attacks

**The core question is not "can I upload a file?" but "can I upload a file that the server will execute or that will cause harm?"**

#### Decision Flow

```
1. Where are uploads accepted? → avatar, document, import, attachment, media, report, profile, API file endpoints
2. What types are allowed? → test a representative executable extension for the observed server stack (.php for Apache/PHP, .jsp for Tomcat, .aspx for IIS/.NET, .war for Java app servers). Test one extension at a time — the goal is to identify which layer rejects it, not to enumerate every known executable extension
3. How is the type validated? Model the parsing chain:
   ├─ Client-side JS only → bypass with Burp/curl — this is one layer, not the whole defense
   ├─ Content-Type header → change to image/jpeg, keep code body — test whether the server inspects only MIME
   ├─ File extension check → if blocked, test a single alternative extension variant (.php5 or .phtml for PHP) to determine whether the filter is blocklist-based or allowlist-based
   ├─ Magic bytes check → prepend GIF89a before code — tests whether the server validates file content or only metadata
   ├─ Content inspection → tests whether the server parses and rewrites the file (resizing, stripping)
   └─ Server-side rendering → the server may remove embedded code during processing
   
   After each test, identify WHICH LAYER made the reject/accept decision. Do not cycle through extension variants — one representative bypass per validation layer is sufficient to model the chain.
4. Where is it stored? → within web root? accessible via direct URL? accessible via /uploads/? served with forced download header?
5. How is it served? → if Content-Type is forced to image/ but code is inside, try include via LFI
```

#### Bypass Techniques — By Validation Layer

Test one technique per validation layer. The goal is to determine which layer accepts or rejects — not to exhaust every possible extension variant.

**Extension layer**: Test a single alternative extension for the target server stack (.php5 or .phtml for Apache/PHP; .jspx or .jsw for Tomcat; .asmx or .ashx for IIS/.NET). If the less common extension succeeds where the standard one failed, the filter is blocklist-based. If both are blocked, the filter is likely allowlist-based — test a double extension or null byte.

**Content-Type layer**: Change `Content-Type` header to an allowed value while keeping the code body intact. If accepted, MIME is the only check.

**Magic bytes layer**: Prepend recognized image header bytes (GIF89a) before code. If accepted, only magic bytes are validated — the file content is not inspected.

**Server-side processing layer**: If the file is resized, re-encoded, or rendered after upload, the code payload may be stripped. Test whether code survives by uploading a known-good code file, then downloading it and checking the content.

#### Dangerous File Types Beyond Webshells

| File Type | Attack | Context |
|---|---|---|
| `.svg` | Stored XSS, SSRF via `<foreignObject>`, XML injection | Image upload accepting SVG |
| `.csv` | CSV injection: formula injection via `=` prefix, `@SUM`, or DDE — the formula executes when the CSV is opened in a spreadsheet application | Data export/import functions |
| `.xml` | XXE, billion laughs | Document import, configuration upload |
| `.yml`/`.yaml` | Deserialization via `!!python/object`, `!!javax.script.ScriptEngineManager` | Configuration import, CI/CD |
| `.pdf` | SSRF via PDF generators, JavaScript injection in PDF | Document generation |
| `.docx`/`.xlsx` | XXE in Office Open XML, macro injection | Document processing |
| `.zip`/`.tar` | Zip slip (path traversal extraction), symlink extraction | Archive upload/processing |
| `.phar` | PHP phar deserialization (class in metadata triggers `__destruct`) | PHP apps accepting any archive |

#### Common Post-Upload Attacks

1. **Uploaded file path discovery**: Check response headers (`Location`), page source for `<img>` after upload, predictable patterns (`/uploads/avatars/<userid>.jpg`), fuzz `/uploads/<year>/<month>/`
2. **LFI + File Upload combo**: If LFI exists but code execution isn't possible via LFI alone → upload PHP file → include it via LFI
3. **Zip slip**: Upload a zip containing a path-traversal entry (e.g., `<traversal-prefix>/<web-root>/<filename>.<extension>`) → extraction places the file outside the intended directory

### Failure Branches

| Failure Signal | Likely Cause | Next Variable |
|---|---|---|
| Upload succeeds (200) but file not found at predicted path | Storage path differs from prediction; file renamed server-side; file stored outside web root; uploaded to object storage (S3) not on the web server filesystem | Check response headers and body for the actual stored path or URL; test alternative path patterns; if stored in object storage, test direct bucket access and signed URL generation |
| Upload rejected — extension in blacklist but blocked | Extension blacklist is comprehensive for the tested extension | Test less common executable extensions (.php5, .phtml, .phar, .shtml, .pht); test case variations; test null-byte and double-extension bypasses |
| Upload accepted with modified extension but served as static/download (not executed) | Server configuration does not execute the file type in the upload directory; Content-Type header forces download; handler mapping missing for this extension | Test: can you include the uploaded file via a separate LFI vulnerability? If LFI exists, test whether the upload directory path is reachable through the LFI parameter. For Apache: test `.htaccess` upload with `AddType` directive. For IIS: test `web.config` upload with handler remapping. Uploading server configuration files may change processing behavior — classify by the access scope of the change |
| Polyglot file accepted but code does not execute | Image processing stripped the payload (resizing, re-encoding, metadata stripping); the server checks magic bytes AND serves as image content-type | Test: embed payload in EXIF metadata instead of raw bytes; test SVG (vector format avoids re-encoding); test a different image format the server may process differently |
| .htaccess upload rejected or ignored | Upload directory has `AllowOverride None`; the web server detects and blocks `.htaccess` uploads by filename pattern; the server is nginx/IIS (no `.htaccess` support) | For Apache: `.htaccess` filename is configurable via `AccessFileName` directive — the default is `.htaccess` but the server may use a different name. For nginx: server config is in `/etc/nginx/` and cannot be overridden per-directory via uploaded files. For IIS: test `web.config` upload with handler mapping. Uploading server configuration files may change request handling behavior — classify by the access scope and persistence of the configuration change |
| File upload endpoint requires authentication → upload succeeds but cannot trigger execution from external position | Execution requires knowledge of the file path; file is only accessible after authentication; WAF blocks requests to the upload directory | If authenticated: include the uploaded file in a same-session request; if path unknown: fuzz based on response patterns; if WAF blocks: test if file can be included via another vulnerable endpoint (LFI, SSRF) |

## Scene Exit

Return result classification, evidence, changed assumptions, affected paths, persistent changes, and the next parent-path decision.
