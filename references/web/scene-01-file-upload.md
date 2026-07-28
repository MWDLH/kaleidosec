# Web And API Operations: Attack Primitives: Traditional Web Vulnerabilities: File Upload Attacks

> Apply [../module-continuity.md](../module-continuity.md). Keep the same engagement and parent path as the calling route. Load this scene only when current evidence supports its prerequisites.

### File Upload Attacks

**The core question is not "can I upload a file?" but "can I upload a file that the server will execute or that will cause harm?"**

#### Decision Flow

```
1. Where are uploads accepted? → avatar, document, import, attachment, media, report, profile, API file endpoints
2. What types are allowed? → test: .php, .jsp, .asp, .aspx, .war, .py, .pl, .cgi, .phtml, .php5, .shtml, .asa, .cer, .htaccess, .svg, .html, .shtml, .xml, .csv, .yml, .pdf
3. How is the type validated?
   ├─ Client-side JS only → bypass with Burp/curl
   ├─ Content-Type header → change to image/jpeg, keep malicious body
   ├─ File extension blacklist → try: .php5, .phtml, .phar, .shtml, .php., .PhP, .pHP5, .php%00.jpg, .php.jpg, .php;.jpg
   ├─ File extension whitelist → try: double extension (.php.jpg), null byte (.php%00.jpg), NTFS alternate data stream (.php::$DATA)
   ├─ Magic bytes check → add GIF89a/PNG header before PHP code, or embed code in EXIF metadata
   ├─ Content inspection → obfuscate payload, embed in polyglot, use less obvious wrappers
   └─ Server-side rendering/resizing → may strip payload → ImageMagick/Imagick exploit (ImageTragick) instead
4. Where is it stored? → within web root? accessible via direct URL? accessible via /uploads/? served with forced download header?
5. How is it served? → if Content-Type is forced to image/ but code is inside, try include via LFI
```

#### Bypass Techniques — By Validation Type

**Extension Bypass**:
```
.php → blocked? try: .php5, .php7, .php8, .phtml, .pht, .phar, .phps, .php.s, .shtml
.jsp → try: .jspx, .jspf, .jsw, .jsv
.asp → try: .aspx, .asmx, .ashx, .ascx, .asa, .cer, .cdx
```

**Content-Type Bypass**: Change `Content-Type: application/x-php` to `Content-Type: image/jpeg` or `Content-Type: image/gif`.

**Magic Bytes Bypass**:
```
GIF + PHP:  GIF89a<?php <controlled-command>; ?>  (magic bytes before code)
PNG + PHP:  \x89PNG\r\n\x1a\n... (PNG magic bytes) followed by <?php <controlled-command>; ?>
JPEG + PHP: \xff\xd8\xff\xe0... (JPEG magic bytes) with PHP code embedded in EXIF comment or metadata
SVG + XSS:  valid SVG with an event handler or script element — test whether the server serves SVG as image/svg+xml or forces a safe Content-Type
```

**Polyglot Files**: A file valid as both an image AND server-executable code. Useful against image processing that validates the image stream, not the full file content. Construction: prepend valid image magic bytes (GIF89a, PNG header, JPEG header) before the server-executable code block. Success depends on the server interpreting the file by extension rather than by magic-byte detection.

**.htaccess / web.config Upload**:
- Upload `.htaccess` with `AddType application/x-httpd-php .jpg` → all .jpg files in that directory execute as PHP
- Upload `web.config` with `<handlers><add name="php" path="*.jpg" ...>` for IIS

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


## Scene Exit

Return result classification, evidence, changed assumptions, affected paths, persistent changes, and the next parent-path decision.
