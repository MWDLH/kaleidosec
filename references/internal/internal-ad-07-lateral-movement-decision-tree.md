# Internal Network, Host, And Identity Operations: Lateral Movement Decision Tree

> Apply [../module-continuity.md](../module-continuity.md). Inherit the engagement, parent path, current capability, evidence, authorization profile, and module stack. Do not initialize a separate workflow. Checkpoint material results and return them to the parent path before leaving this card.

## Lateral Movement Decision Tree

Choose technique by target OS, open ports, available credential type, required privilege, and detection profile. Do not cycle through tools without changing a meaningful variable.

```
Available credential type?
├─ Cleartext password → widest compatibility
│   ├─ Target is Windows, port 445 open, local admin?
│   │   ├─ Need interactive? → WinRM (5985/5986) if configured; else PSExec (SMB service creation)
│   │   └─ Need command output only? → WMIExec (DCOM, no service artifact) or SMBExec (service-based, leaves service artifact)
│   ├─ Target is Windows, port 5985/5986 open? → WinRM (Enter-PSSession or evil-winrm)
│   ├─ Target is Linux, port 22 open? → SSH
│   └─ Target has RDP (3389) open? → RDP (interactive GUI; assess whether source, identity, and time appear anomalous)
├─ NTLM hash only → Pass-the-Hash (NTLM auth protocols)
│   ├─ SMB (445): PSExec, SMBExec, WMIExec via Impacket with -hashes
│   ├─ WinRM: NTLM hash usable with clients that support NTLM authentication for WinRM (not Basic — Basic uses cleartext password)
│   └─ RDP: only with Restricted Admin mode (registry key on target)
├─ Kerberos ticket (TGT/TGS) → Pass-the-Ticket
│   └─ Any Kerberos-authenticated service (SMB, WinRM, HTTP, LDAP, MSSQL)
└─ No credential yet?
    ├─ SMB signing disabled on target? → NTLM relay (capture and relay NetNTLMv2)
    ├─ LLMNR/NBT-NS active on network? → name resolution poisoning → capture hash
    └─ Web app or DB on target? → application-level access first
```

## Technique Profiles — Prerequisites, Artifacts, And Noise

| Technique | Prerequisites Beyond Credential | Observable Artifacts | Noise Level And Why |
|---|---|---|---|
| **PSExec** | Local admin on target, SMB 445, ADMIN$ share accessible | Windows service created (random name by default), service binary written to disk or ADMIN$, Event ID 7045 | **Very high** — service creation + binary write is a strong EDR signature; choose based on reliability, artifacts, detection risk, and task value, not a fixed rank |
| **SMBExec** | Local admin on target, SMB 445, ADMIN$ share accessible | Service created for each command, output file written to `%SYSTEMROOT%\Temp\` or similar and read back via share, service control manager events, patch file cleanup may leave remnants | **High** — service creation events and share-based output retrieval are distinct from normal admin activity; output files may persist if cleanup fails |
| **WMIExec** | Local admin on target, DCOM ports (135 + ephemeral high ports), WMI service running | WMI process creation (`Win32_Process.Create`), remote temporary output files may be written and read back, WMI activity logged | **Moderate** — process-based execution without service creation is less anomalous than PSExec/SMBExec; output retrieval writes temporary files on the target |
| **AtExec** | Local admin on target, SMB 445, Task Scheduler service | Scheduled task artifact (Event ID 4698), task XML registered at `\Windows\System32\Tasks\`, command output written to temp file and read via ADMIN$ | **High** — scheduled task creation is monitored; task may persist if cleanup fails |
| **WinRM / PSRemoting** | Target configured for WinRM (5985/5986), principal authorized for remote management via endpoint ACL, policy, group membership, and token evaluation | PowerShell event log (4104 script block logging if enabled), WinRM operational log, no service or disk artifact on target | **Moderate** — native admin tool but PowerShell logging captures commands; not "Remote Management Users or Administrators" alone determines access — endpoint ACL, GPO, and token claims also apply |
| **DCOM (MMC20.Application, ShellWindows, etc.)** | Local admin on target, DCOM ports, DCOM object registration | DCOM object activation event, process creation under dllhost.exe or svchost.exe, child process of DCOM launcher | **Moderate** — DCOM object choice affects detection profile; ShellBrowserWindow/ShellWindows are more common in normal activity than MMC20.Application |
| **RDP** | RDP access granted (port 3389), principal in Remote Desktop Users or equivalent | RDP event log (Event ID 4624 type 10), GUI session artifacts | **Variable** — whether this appears anomalous depends on source IP, identity, time of day, and whether the account normally uses RDP; not inherently "low noise" |
| **SSH** | SSH server enabled, principal authorized (password or key) | SSH auth log, shell history | **Variable** — anomalous if the target is a Windows host where SSH is rarely used, or if source identity/time are unusual |
| **Schtasks** | Local admin, SMB 445 or direct RPC to Task Scheduler | Scheduled task creation (Event ID 4698), task and output files on disk | **High** — task creation events + disk artifacts |
| **Service (SC)** | Local admin, SMB 445 or direct RPC to Service Control Manager | Service creation (Event ID 7045), binary on disk (unless using service DLL), registry key under `HKLM\SYSTEM\CurrentControlSet\Services` | **Very high** — service creation is among the most monitored events |
| **WMI Event Subscription** | Local admin, DCOM ports | `__EventFilter`, `__EventConsumer`, `__FilterToConsumerBinding` instances in WMI repository — **persistent across reboots** | **L3 — persistence** — this is a durable control mechanism, not a routine lateral movement technique; requires explicit approval under the authorization profile |

**Rule of thumb**: Choose the technique whose reliability, artifacts, detection risk, and task value best fit the current position and objective. WMI permanent event subscriptions are persistence, classified as L3, and must not be offered as routine lateral movement without explicit approval. Enabling WinRM or modifying its configuration via GPO is a configuration change and falls under L3.

## Failure Classification

After a failed lateral movement attempt, classify the failure before choosing the next action:

| Failure Class | Observable Signal | Next Variable To Change |
|---|---|---|
| **Authentication failure** | `STATUS_LOGON_FAILURE`, `STATUS_ACCESS_DENIED`, `STATUS_ACCOUNT_RESTRICTION` | Credential quality, account restrictions (logon hours, workstation restriction, smart card), target local-vs-domain account context |
| **Network logon granted but no remote execution privilege** | SMB share listing works, but service/WMI/WinRM access denied | Execution method (try WMI if SCM denied, try WinRM if DCOM blocked), check local group membership and privilege token |
| **Port reachable but management endpoint not configured** | TCP connect succeeds to 445/5985 but no SMB negotiate or WinRM WS-Management response | Use an alternate protocol on open ports, or check if a web management interface exists on another port. Enabling WinRM or modifying GPO to configure it is an L3 configuration change — do not offer this as a routine fallback without explicit approval |
| **Remote execution succeeded but command output retrieval failed** | Command ran (process visible, side effect observed) but no stdout returned | Output redirection method, check firewall blocking ephemeral ports for DCOM callback, check WinRM message size limits |
| **EDR or application-control policy blocked the attempt** | Service/task created then immediately deleted, process spawned then killed, `STATUS_ACCESS_DENIED` on admin-privileged action despite valid credential | Alternate execution method with different process ancestry, LOLBin instead of external tool, signed binary, or process injection; check which specific behavior triggered the block before changing tools |

Do not respond to a failure solely by switching to another tool of the same class. Identify which layer failed, change the relevant variable, and retry only when the new attempt tests a distinct hypothesis.


## Card Exit

Classify the result, update evidence and attempted methods, record capability or risk changes, identify affected paths, and apply the return contract in [../module-continuity.md](../module-continuity.md).
