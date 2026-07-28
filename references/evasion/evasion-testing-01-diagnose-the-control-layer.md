# Authorized Control-Evasion And Environment Adaptation: Diagnose The Control Layer

> Apply [../module-continuity.md](../module-continuity.md). Inherit the engagement, parent path, current capability, evidence, authorization profile, and module stack. Do not initialize a separate workflow. Checkpoint material results and return them to the parent path before leaving this card.

## Diagnose The Control Layer

Which layer is actually blocking you?

| Layer | Symptom | Diagnostic Test |
|---|---|---|
| **Anti-malware (AV)** | File deleted or quarantined on write, process killed immediately on launch | Write a simple text file with EICAR test string. If deleted → signature-based AV |
| **EDR (CrowdStrike, Defender ATP, Carbon Black, SentinelOne)** | Process runs briefly then terminates, no file deletion but process disappears; or tool runs but network connections from it are blocked | Run `whoami`, `hostname`, `dir` first — simple commands that work. Then try `netstat -ano` — if process gets killed at this point → behavioral EDR |
| **AMSI (Anti-Malware Scan Interface)** | PowerShell/.NET scripts blocked with "This script contains malicious content", specific cmdlets blocked | `[Ref].Assembly.GetType('System.Management.Automation.AmsiUtils').GetField('amsiInitFailed','NonPublic,Static').SetValue($null,$true)` — if scripts work after this → AMSI |
| **PowerShell Constrained Language Mode** | "Cannot invoke method. Method invocation is supported only on core types" or restricted cmdlets | `$ExecutionContext.SessionState.LanguageMode` → if "ConstrainedLanguage" → CLM enabled |
| **AppLocker / WDAC** | "This program is blocked by group policy" when executing .exe/.dll/.ps1 | Try running from `C:\Windows\Temp\` vs `C:\Users\Public\Documents\` — if different results → path-based AppLocker rules |
| **Windows Defender Application Control** | Similar to AppLocker but at kernel level; even signed binaries may be blocked unless explicitly allowed | Check `Get-CimInstance -ClassName Win32_DeviceGuard -Namespace root\Microsoft\Windows\DeviceGuard` |
| **Credential Guard** | Mimikatz `sekurlsa::logonpasswords` returns empty or partial results; LSA protection blocks read | `reg query HKLM\SYSTEM\CurrentControlSet\Control\Lsa /v RunAsPPL` → 1 = LSA Protection on |
| **Network segmentation** | Can reach some hosts but not others; specific ports blocked | `Test-NetConnection <host> -Port <port>` from multiple source hosts to map segmentation rules |
| **Network IDS/IPS** | Specific exploit payload blocked (connection reset, no response) while normal traffic flows | Test benign version of the same protocol first. Then add one suspicious element at a time — identify which element triggers blocking |
| **Rate limiting / WAF** | 403 after N requests, CAPTCHA, or connection throttling | Slow down, rotate user-agents and IPs if authorized, use different endpoints |
| **Honeypot / Canary** | Anomalous service on expected port, decoy credentials, or decoy files | Test carefully: is this a real production service or a trap? Abort if unsure |

---


## Card Exit

Classify the result, update evidence and attempted methods, record capability or risk changes, identify affected paths, and apply the return contract in [../module-continuity.md](../module-continuity.md).
