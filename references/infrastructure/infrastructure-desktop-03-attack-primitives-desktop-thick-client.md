# Infrastructure, VPN, Middleware, And Desktop Operations: Attack Primitives: Desktop & Thick Client

> Apply [../module-continuity.md](../module-continuity.md). Inherit the engagement, parent path, current capability, evidence, authorization profile, and module stack. Do not initialize a separate workflow. Checkpoint material results and return them to the parent path before leaving this card.

## Attack Primitives: Desktop & Thick Client

### Application Analysis

```bash
# Windows: Identify technologies
# Use Sysinternals: ProcMon (file/reg access), ProcExp (loaded DLLs), TCPView (network connections)
# Use API Monitor for Win32 API tracing

# .NET: easy to decompile
dnSpy <app>.exe  # view and debug .NET apps — can modify code in real-time

# Java: easy to decompile
jd-gui <app>.jar
# Check: hardcoded credentials, embedded config, obfuscation

# Native (C/C++): harder, but strings often reveal everything
strings <app>.exe | grep -iE "password|secret|connection|server|http"
# Check for: DLL hijacking candidates, weak named pipe ACLs, writable service binaries
```

### Common Desktop App Vulnerabilities

1. **DLL Hijacking**: App loads DLLs from current directory or PATH without full path. Place malicious DLL with same name → code execution in app's privilege context.
   ```powershell
   # Use ProcMon to find DLLs loaded with NAME NOT FOUND in unprotected directories
   # Check if any are in C:\Users\<user>\Downloads\ (user-writable, often in PATH)
   ```

2. **Named Pipe Impersonation**: App creates a named pipe with weak ACL. Connect as lower-privileged user, impersonate the app's higher-privileged client.
   ```powershell
   # List named pipes
   Get-ChildItem \\.\pipe\
   # Check permissions
   accesschk \\.\pipe\<pipename>
   # If Authenticated Users or Everyone has write access — potential impersonation target
   ```

3. **COM Object Hijacking**: App instantiates COM objects by CLSID. If the registered DLL is missing or in a writable path → replace with malicious DLL.
   ```powershell
   # Find missing COM registrations via ProcMon (NAME NOT FOUND for InprocServer32)
   # If the path is writable by current user → create malicious DLL → COM activation runs it
   ```

4. **Writable Service Binaries / Unquoted Service Paths**: 
   ```powershell
   # Find services with writable binary paths
   Get-WmiObject win32_service | Where-Object {$_.PathName} | ForEach-Object {
     $path = $_.PathName.Trim('"').Split(' ')[0]
     if (Test-Path $path) {
       $acl = Get-Acl $path
       if ($acl.Access.IdentityReference -match 'BUILTIN\\Users|Everyone|Authenticated Users') {
         Write-Host "WRITABLE: $($_.Name) -> $path"
       }
     }
   }
   ```

5. **Auto-elevation / BypassUAC**: Applications with `autoElevate=true` in manifest run elevated without UAC prompt if trusted. Combine with DLL hijacking in a trusted directory for UAC bypass.

---


## Card Exit

Classify the result, update evidence and attempted methods, record capability or risk changes, identify affected paths, and apply the return contract in [../module-continuity.md](../module-continuity.md).
