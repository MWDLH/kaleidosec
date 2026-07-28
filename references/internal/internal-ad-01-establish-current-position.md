# Internal Network, Host, And Identity Operations: Establish Current Position

> Apply [../module-continuity.md](../module-continuity.md). Inherit the engagement, parent path, current capability, evidence, authorization profile, and module stack. Do not initialize a separate workflow. Checkpoint material results and return them to the parent path before leaving this card.

## Establish Current Position

Before any action, capture the current operating state. Record **who you are**, **where you are**, **what you can see**, and **what controls exist**.

### Position Assessment Commands (Windows)

Run these in order — each output informs the next:

```
# --- Identity ---
whoami /all                    # user, groups, privileges (SeImpersonate, SeDebug, SeBackup?)
echo %USERDOMAIN%              # domain or workgroup
echo %LOGONSERVER%             # which DC authenticated this session
klist                          # current Kerberos tickets (any TGT? service tickets?)
net user %USERNAME% /domain    # domain account details, group membership
net localgroup administrators  # who has local admin
gpresult /r                    # applied GPOs (find restricted groups, scripts, software installs)

# --- Network Position ---
ipconfig /all                  # interfaces, DNS servers, DHCP, domain suffix
route print                    # routing table — find other network segments
netstat -ano                   # active connections, listening services, process IDs
arp -a                         # ARP cache — directly reachable hosts
nslookup <domain>              # DNS resolution and DC discovery
nltest /dclist:<domain>        # enumerate domain controllers
nltest /domain_trusts          # trust relationships
nltest /dsgetdc:<domain>       # which DC is current, which site

# --- Host Context ---
systeminfo                     # OS version, build, hotfixes (patch level)
tasklist /v                    # running processes — is AV/EDR present?
wmic qfe list brief            # installed patches (find missing ones)
driverquery /v                 # kernel drivers — EDR filter drivers
sc query type=driver           # more driver details
net share                      # shared folders (password in SYSVOL/scripts?)
icacls C:\*                    # some writable paths for DLL hijacking?

# --- Defensive Controls ---
# Check for: Windows Defender (MsMpEng.exe), CrowdStrike (CSFalconService), 
# Carbon Black (CbDefense), SentinelOne (SentinelAgent), McAfee, Symantec, Trend Micro
# Check PowerShell execution policy, AppLocker/WDAC, Credential Guard, LSA Protection
reg query "HKLM\SYSTEM\CurrentControlSet\Control\Lsa" /v "RunAsPPL"         # LSA Protection
reg query "HKLM\SYSTEM\CurrentControlSet\Control\DeviceGuard" /v "EnableVirtualizationBasedSecurity"  # VBS/Credential Guard
reg query "HKLM\SOFTWARE\Policies\Microsoft\Windows\SRPV2"                   # AppLocker
```

**Linux/non-Windows on internal network**: Capture `id`, `sudo -l`, `ip addr`, `ip route`, `ss -tlnp`, `ps aux`, `cat /etc/resolv.conf`, `env`, mounted filesystems, cron jobs, SSH keys, and known_hosts. Check if the host is joined to AD via SSSD, Winbind, or PBIS.

### Position Assessment — Linux

```
id; sudo -l; uname -a; cat /etc/os-release
ip addr show; ip route show; ss -tlnp
ps auxf; systemctl list-units --state=running
env | sort; cat /etc/resolv.conf
find /home -name "id_rsa" -o -name "*.pem" -o -name "authorized_keys" 2>/dev/null
cat /etc/krb5.conf 2>/dev/null; klist 2>/dev/null
# Check SSSD/Winbind AD integration
cat /etc/sssd/sssd.conf 2>/dev/null; net ads info 2>/dev/null
# Mounted shares — potential data access
mount | grep cifs; df -h
```

Do not begin with broad lateral activity. First determine what the current position can see, what identities and trust relationships exist, and which assets contribute to the objective.

---


## Card Exit

Classify the result, update evidence and attempted methods, record capability or risk changes, identify affected paths, and apply the return contract in [../module-continuity.md](../module-continuity.md).
