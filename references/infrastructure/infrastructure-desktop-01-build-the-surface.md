# Infrastructure, VPN, Middleware, And Desktop Operations: Build The Surface

> Apply [../module-continuity.md](../module-continuity.md). Inherit the engagement, parent path, current capability, evidence, authorization profile, and module stack. Do not initialize a separate workflow. Checkpoint material results and return them to the parent path before leaving this card.

## Build The Surface

Inventory addresses, services, protocols, versions, management planes, authentication sources, certificates, routing/segmentation role, exposed configuration, update mechanisms, client binaries, local storage, IPC, privileged services, and backend dependencies.

This domain covers everything that isn't a web app, mobile app, cloud service, or AD domain controller — but makes up a large portion of real penetration test targets. Think: VPN concentrators, network appliances, middleware (Redis, RabbitMQ, Elasticsearch), industrial control systems, desktop applications, and thick clients.

### Service Discovery — Concrete Methods

```bash
# Phase 1: Broad but quiet — TCP SYN scan, common ports only
nmap -sS -p 21,22,23,25,53,80,443,445,1433,1521,3306,3389,5432,5900,6379,8080,8443,9000,9090,9200,11211,27017 --open -oA nmap_quick <target_range>

# Phase 2: Full port scan on identified hosts (only if scope/time allow)
nmap -sS -p- --open -oA nmap_full <specific_host> --max-retries 1 --min-rate 1000

# Phase 3: Service version detection on open ports (noisy — use selectively)
nmap -sV -sC -p <open_ports> -oA nmap_detail <specific_host>

# Phase 4: UDP scan on critical services (SNMP, DNS, NTP, TFTP, SIP, IKE)
nmap -sU -p 53,161,162,500,623,1900 --open -oA nmap_udp <target_range>
```

### Technology Fingerprint per Port

| Port | Service | Quick Fingerprint |
|---|---|---|
| 21 | FTP | `ftp <host>` — banner, anonymous login allowed? `ftp> quote USER anonymous; quote PASS anonymous` |
| 22 | SSH | `ssh -v <host>` — server version, supported auth methods. Try common creds: root:root, admin:admin, ubuntu:ubuntu |
| 23 | Telnet | `telnet <host>` — banner, no auth required? |
| 25/465/587 | SMTP | `smtp-user-enum -M VRFY -U users.txt -t <host>` — user enumeration via VRFY/EXPN/RCPT TO |
| 161/162 | SNMP | `snmpwalk -v1 -c public <host>` and `snmpwalk -v2c -c public <host>` — default community strings |
| 623 | IPMI | `ipmitool -I lanplus -H <host> -U admin -P admin user list` — BMC access, default creds |
| 1433 | MSSQL | `impacket-mssqlclient <domain>/<user>:<pass>@<host>` — try sa: with empty password |
| 1521 | Oracle | `tnscmd10g version -h <host>` or `odat tnscmd -s <host> --ping` — Oracle TNS listener |
| 3306 | MySQL | `mysql -h <host> -u root` — root with no password? |
| 3389 | RDP | `xfreerdp /v:<host> /u:Administrator /p:""` — NLA level, if disabled: guest/empty password access |
| 5432 | PostgreSQL | `psql -h <host> -U postgres` — default superuser with no password? |
| 5900 | VNC | `vncviewer <host>` — no authentication required? |
| 5985/5986 | WinRM | `evil-winrm -i <host> -u <user> -p <pass>` — admin access via WinRM |
| 6379 | Redis | `redis-cli -h <host> INFO` — unauthenticated? `CONFIG SET dir /var/www/html` → webshell |
| 9200 | Elasticsearch | `curl http://<host>:9200/_cat/indices` — unauthenticated? All data readable? |
| 11211 | Memcached | `echo "stats items" \| nc <host> 11211` — unauthenticated? Sensitive data in cache? |
| 27017 | MongoDB | `mongo <host>:27017` — unauthenticated? `show dbs;` |

---


## Card Exit

Classify the result, update evidence and attempted methods, record capability or risk changes, identify affected paths, and apply the return contract in [../module-continuity.md](../module-continuity.md).
