# Infrastructure, VPN, Middleware, And Desktop Operations: Attack Primitives: VPN & Network Appliances

> Apply [../module-continuity.md](../module-continuity.md). Inherit the engagement, parent path, current capability, evidence, authorization profile, and module stack. Do not initialize a separate workflow. Checkpoint material results and return them to the parent path before leaving this card.

## Attack Primitives: VPN & Network Appliances

### VPN Testing Priorities

1. **Default credentials**: Every VPN appliance has them. Test: admin/admin, admin/<blank>, root/<vendor_name>, <vendor>/<vendor>
2. **Pre-authentication vulnerabilities**: Check CVE for the specific version. CVE-2021-22893 (Pulse Secure), CVE-2022-30525 (Zyxel), CVE-2023-46805 (Ivanti) — these are RCE BEFORE authentication.
3. **SSL VPN web interfaces**: Tested as web apps ([../web/router.md](../web/router.md)) plus: path traversal in resource fetching, XSS in error messages, SQLi in auth forms
4. **IPSec/IKE**: `ike-scan <host>` — identify vendor and version. Aggressive mode → crack PSK: `ike-scan -A -id=peer <host> --pskcrack=hash.txt`
5. **Post-auth privilege escalation**: Usually tested after credential discovery. Check: multi-tenancy bypass, read-only admin can become full admin, user portal can access admin portal

### Network Device Checklist

For each device (router, switch, firewall, load balancer):

```
- SNMP community string "public" or "private"? (read config, read ACLs)
- Telnet enabled? (cleartext credentials in transit)
- HTTP (not HTTPS) management interface? (cleartext credentials)
- Default credentials still active?
- Firmware version → CVE search (many appliances have known RCE)
- SSH: check supported ciphers/KEX (ssh-audit.py)
- Management accessible from untrusted networks?
- IPv6 management accessible while IPv4 is restricted?
```

---


## Card Exit

Classify the result, update evidence and attempted methods, record capability or risk changes, identify affected paths, and apply the return contract in [../module-continuity.md](../module-continuity.md).
