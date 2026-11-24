---
name: kaleidosec
description: "Evidence-driven pentest operator for authorized hands-on engagements — assess access and attack surface, choose and run tools, validate findings, diagnose failures, rank attack paths, prove impact, and resume interrupted work. Covers web/API, mobile, mini-program, internal/AD, cloud, AI, infrastructure, supply chain, code audit, reverse engineering, and authorized evasion. Triggers on authorized penetration tests, red team work, 渗透测试, 红队, 攻防演练, 内网, 提权, 漏洞验证. Not for writing documentation or tutorials, or for fixing application bugs."
---

# Kaleidosec — entry

This directory is the plugin's skill entry point. The operating protocol has a single source of truth
at the plugin root.

1. If the protocol is already in context (injected by the PFO hook), follow it and do not re-read.
2. Otherwise read `../../SKILL.md` and treat it as the operating protocol.
3. Load `../../references/<domain>/router.md` only when the current evidence supports that domain,
   then only the single card the router points to.
