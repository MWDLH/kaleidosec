# Internal Network, Host, And Identity Operations: Basic Internal Network Attacks: LLMNR/NBT-NS/mDNS Name Resolution Poisoning

> Apply [../module-continuity.md](../module-continuity.md). Keep the same engagement and parent path as the calling route. Load this scene only when current evidence supports its prerequisites.

### LLMNR/NBT-NS/mDNS Name Resolution Poisoning

**The easiest initial foothold in many internal networks.** When Windows cannot resolve a name via DNS, it falls back to LLMNR (Link-Local Multicast Name Resolution), then NBT-NS (NetBIOS Name Service). Both are multicast/broadcast and unauthenticated. Linux/macOS use mDNS similarly.

**Attack**: Listen for name resolution failures on the network. When you see a request for a name that doesn't exist in DNS, respond claiming to be that name. The victim sends their NetNTLMv2 hash to authenticate to your fake service.

```bash
# Responder (Linux) — the standard tool
sudo responder -I <interface> -wdPv
# Output: NetNTLMv2 hashes captured to /usr/share/responder/logs/

# Crack captured hashes
hashcat -m 5600 responder_hashes.txt /path/to/wordlist --force
```

**What you typically get**:
- User NetNTLMv2 hashes (crackable offline)
- Occasional machine account hashes (harder to crack)
- Clear-text credentials from misconfigured services/applications using basic auth

**Defensive context**: LLMNR/NBT-NS should be disabled in secure environments (GPO: `Network Security: Restrict NTLM`). If Responder gets nothing, the network may already be hardened — that's useful intelligence.

**Detection**: Responder is noisy. Most EDR/NDR solutions detect it immediately. Know your engagement rules.


## Scene Exit

Return result classification, evidence, changed assumptions, affected paths, persistent changes, and the next parent-path decision.
