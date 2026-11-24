# Kaleidosec

[简体中文](README.md) | English

> **Every angle, a different path.**
> *As the view shifts, the security landscape unfolds.*

Kaleidosec is a **penetration-testing decision mode** for AI agents. It ships no scanner, orchestrates no
tools, and generates no payloads. What it injects is a decision protocol: how to assess a target, how to
rank paths, how to ground each step in evidence, and when to stop.

The name comes from the kaleidoscope: change the identity, the entry point, or the angle, and the same
target shows a different attack surface. A seasoned tester does not stare at one angle; they rotate
between views and pick the path worth taking.

Kaleidosec ships as a Claude Code plugin: one always-on decision protocol plus two lifecycle hooks.
Once installed, it enters the mode in an engagement directory or on a clear signal, and stays out of the
way otherwise. It can also be used as a plain skill.

---

## What it solves

AI agents do not lack vulnerability knowledge. They can explain SQL injection classes, Kerberos
authentication, and IAM escalation paths better than most people. What they lack is the ability to keep
making sound trade-offs in a real, dynamic, incomplete environment: where to start, how deep to go, when
to stop.

Automated tools excel at **coverage**, sweeping known surfaces quickly. What actually consumes time in the
field is **trade-off**. Kaleidosec works on the latter — it runs alongside existing scanners, exploitation
frameworks and proxies: the tools execute, while Kaleidosec decides what to execute, in what order, and
when to stop.

| Common problem | Kaleidosec mechanism |
|---|---|
| Swapping tools on failure without diagnosing | 8-way failure classification; change one variable per attempt |
| Treating scanner output as a finding | Evidence classes: fact / inference / hypothesis / unknown / rejected |
| Restarting reconnaissance after a domain change | Module call stack + parent-path return; identity and evidence travel along |
| Drilling one path forever | Four path states (active / deep-dive / parked / closed); parking requires a reactivation condition |
| Unexplainable decisions | Each step states judgment / evidence / unknowns / why now / what to change on failure |

## How it works

An authorized engagement is modeled as a continuously updated decision loop:

```text
locate position → consolidate evidence → rank candidate paths
→ run one bounded action → interpret the result → update state → re-rank
```

Three principles drive the loop:

- **Depth is judged**: weigh exposed surface, identity and privilege boundaries, decision-changing
  unknowns, objective value, and budget. Start at the lightest depth, escalate when evidence moves, close
  when gains stop.
- **Evidence discipline**: keep fact, inference, hypothesis, unknown and rejected separate. Every action is
  bound to confirmed facts; nothing is done merely because a tool is available.
- **Active stopping**: when gain no longer justifies cost, park the path with an explicit reactivation
  condition instead of mechanically completing a tool list.

Decision-making is layered: hard boundaries are fixed by rules (human approval for high-impact actions,
whether to inject, mandatory baseline), judgment is left to the model (route, depth, stopping), and every
step is recorded.

### Highest safety red line

High-impact actions require human confirmation. This layer outranks every workflow and depth decision —
pre-authorization cannot override it, and "approved earlier" is not approval now:

- **Persistence**: scheduled tasks, services, startup items, backdoors, account creation
- **Trust or privilege change**: domain admin, ACLs, certificate templates, IAM, token issuance
- **Production or control-plane mutation**: business config, WAF/EDR, security groups, routes, DNS
- **Irreversible or business-interrupting**: data deletion, bulk exfiltration, DoS validation, production DB writes
- **State-changing active attack**: data writes, dropping files, self-propagation, bulk credential guessing

When no human is available, the branch is parked as "pending confirmation" — never silently downgraded or
self-approved.

The plugin also asks for confirmation on a small set of obviously high-impact shell commands (recursive
delete, persistence, credential dumping, bulk credential attempts) as a backstop. It covers only the most
obvious forms and does not replace human judgment.

## Coverage

**8 attack surfaces, 6 cross-cutting capabilities.** Cards load on evidence, never as a checklist.

| Surface | Coverage |
|---|---|
| **Web/API** | SQLi, XSS, CSRF, SSRF, SSTI, deserialization, JWT, OAuth, GraphQL, race conditions, file upload, command injection |
| **Mobile** | Android components, iOS Keychain/ATS, WebView, deep links, certificate pinning bypass, backend APIs |
| **Internal/AD** | Kerberos attacks, ACL abuse, AD CS, lateral movement, credential extraction, LOLBins, domain trust hopping |
| **Cloud/Containers** | AWS/Azure/GCP IAM escalation, metadata service, K8s RBAC, container escape, serverless, storage exposure |
| **AI security** | Prompt injection, tool-calling abuse, RAG poisoning, file/URL handling, model supply chain |
| **Supply chain** | CI/CD pipeline attacks, OIDC abuse, dependency confusion, runner hijacking, IaC analysis, artifact registries |
| **Mini-programs** | wx.login trust chain, cloud-function authorization, WebView, payment logic, platform identity |
| **Infrastructure** | Redis/MongoDB/ES exposure, VPN, default credentials, thick clients, network appliances |

| Capability | Coverage |
|---|---|
| **Code audit** | Sink catalogs for Java/PHP/Python/JS/Go/C#, source-to-sink tracing, codebase audit workflow |
| **Reverse engineering** | Native binaries, Java/.NET decompilation, Frida hooks, custom protocols and state machines |
| **PoC development** | Bounded validation scripts, failure diagnosis, per-class templates and tool selection |
| **Identity & network** | Credential types, tunneling and pivoting patterns, network-position modeling, credential prioritization |
| **Defense evasion** | AMSI/AppLocker/LSA Protection diagnosis, EDR behavior understanding, controlled adaptation |
| **Business logic** | State-machine abuse, workflow bypass, semantic violations, incentive abuse, cross-platform analysis |

## Installation

Requires Python 3.8+ available as `python` (on macOS/Linux with only `python3`, see
[`examples/claude-hook/`](examples/claude-hook/)).

```
/plugin marketplace add MWDLH/kaleidosec
/plugin install kaleidosec --marketplace MWDLH/kaleidosec
```

Takes effect in a **new session**. Just say what you are doing (e.g. "pentest this site",
"check the domain controller", "run nmap") and the mode enters automatically; opening a
workspace that looks like an engagement (name containing pentest / engagement / red-team, or
containing `.har` / `.burp` / nmap output) also enters it. Add `.kaleidosec` only if you want a
fixed workspace and cross-session resume.

To skip the plugin, wire the hooks manually via
[`examples/claude-hook/`](examples/claude-hook/), or use it as a plain skill:

```bash
git clone https://github.com/MWDLH/kaleidosec.git ~/.claude/skills/kaleidosec
```

## Host support

Claude Code supports both plugin and manual-hook auto-entry. As a plain skill it works in Claude Code and
Codex, invoked by description. dsh adaptation is planned for a later release.

## Repository

```text
kaleidosec/
|-- SKILL.md                    ← single always-on protocol (injection source)
|-- .claude-plugin/             ← plugin manifest + marketplace
|-- hooks/                      ← hooks.json + kaleido_gate.py (deterministic injection)
|-- skills/kaleidosec/          ← thin plugin skill entry
|-- modes/                      ← STANDARD / DEEP on-demand cards
|-- references/                 ← 14 domain & capability directories, each with a router
|-- scripts/                    ← state helper + budget/sync checks
|-- examples/claude-hook/       ← manual hook fallback
|-- CHANGELOG.md / CONTRIBUTING.md / SECURITY.md / LICENSE
```

## Authorization and disclaimer

Intended only for security testing, red-team exercises and attack-defense assessments for which you hold
explicit authorization. You must ensure lawful authorization for every target and accept full
responsibility for your actions. Do not retain unredacted client data, credentials, evidence or target
information in reports or commits.

Output and constraints are not guaranteed to be reliable. The model can misjudge or misoperate; any
high-impact or sensitive action should be reviewed by a human, who bears the risk. The guard only reduces
the chance of obvious mistakes and is not a security guarantee.

## License

[MIT](LICENSE)
