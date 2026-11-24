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

## Why it exists

AI agents do not lack vulnerability knowledge. They can explain SQL injection classes, Kerberos
authentication, and IAM escalation paths better than most people. What they lack is the ability to keep
making sound trade-offs in a real, dynamic, incomplete environment:

- Which path does the evidence actually support?
- Which one has the best value-to-cost ratio?
- On failure, which variable should change — not which tool?
- After gaining a new privilege, how does the original chain continue?

These judgments are hard to encode as a fixed workflow, because they depend on the shape of the target,
the evidence already collected, and the remaining budget. Kaleidosec turns them into an operating
protocol an agent can carry.

## Field problems and mechanisms

| Common problem | Kaleidosec mechanism |
|---|---|
| Swapping tools on failure without diagnosing | 8-way failure classification (execution / environment / access / reachability / method / prerequisite / hypothesis / route value); change one variable per attempt |
| Treating scanner output as a finding | Evidence classes (fact / inference / hypothesis / unknown / rejected); a fingerprint or CVE match is not a vulnerability |
| Restarting reconnaissance after a domain change | Module call stack + parent-path return contract; identity, network position, evidence and objective travel with the agent |
| Drilling one path forever | Four path states (active / deep-dive / parked / closed); parking requires a reactivation condition |
| Unexplainable decisions | Each step states: current judgment / key evidence / unknowns / why now / what to change on failure |

## Relationship to automated pentest tooling

Automated tools excel at **coverage**: sweeping known surfaces quickly and offloading repetitive work.
What actually consumes time in the field is **trade-off**: where to start, how deep to go, when to stop.

Kaleidosec works on the latter. It is designed to run alongside existing scanners, exploitation
frameworks and proxies: the tools execute, while Kaleidosec decides what to execute, in what order, and
when to stop.

## How it works

Kaleidosec models an authorized engagement as a continuously updated decision loop:

```text
locate current position → consolidate evidence → rank candidate paths
→ run one bounded action → interpret the result → update state → re-rank
```

Three properties of the loop:

**Depth is judged, not classified.** Instead of mapping a target onto fixed categories, it weighs five
dimensions: exposed surface, identity and privilege boundaries, decision-changing unknowns, objective
value, and available budget. It starts at the lightest depth, escalates when evidence moves, and closes
when gains stop.

**Evidence discipline.** Fact, inference, hypothesis, unknown and rejected are recorded separately. Every
action is bound to confirmed facts; nothing is done merely because a tool is available.

**Active stopping.** Every path carries a cost/benefit trade-off. When gain no longer justifies cost, the
path is parked with an explicit reactivation condition instead of mechanically completing a tool list.

## Design principles

Decision-making is split into three layers:

| Layer | Content | Decided by |
|---|---|---|
| **L0 hard boundaries** | Human approval for high-impact actions, whether to inject, mandatory baseline, add-locks-only | Rules, non-negotiable |
| **L1 judgment** | Target complexity, route selection, depth escalation, stopping, how deep to go | Model, dynamic |
| **L2 traceability** | Per-step judgment, next action, what to change on failure; depth recorded in state | Mandatory record |

In one line: rules decide "may we, do we enter, must we do it"; the model decides "where, how deep, when to stop".

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

### Prerequisite (hook mode only)

The plugin calls a local Python script from two hooks. It needs **Python 3.8+** available as `python`
(on Windows, tick "Add python.exe to PATH" during installation).

macOS 12.3+ and most Linux distributions ship only `python3`; the hook then fails with
`python: command not found`. Three options: create a shim
`sudo ln -sf "$(command -v python3)" /usr/local/bin/python`; use the manual hook and replace `python`
with `python3`; or use it as a plain skill (no Python required).

### Claude Code (recommended: plugin, enters the mode automatically)

```
/plugin marketplace add MWDLH/kaleidosec
/plugin install kaleidosec --marketplace MWDLH/kaleidosec
```

On Claude Code older than 2.1.275, use two steps:

```
/plugin marketplace add MWDLH/kaleidosec
/plugin install kaleidosec@kaleidosec
```

Takes effect in a **new session**. In a directory with a sentinel, or when a prompt hits a strong signal,
the mode is entered; unrelated work injects nothing and only sees one short entry hint at session start.

To skip the plugin, wire the hooks manually via [`examples/claude-hook/`](examples/claude-hook/).

### Plain skill (no automatic injection)

```bash
git clone https://github.com/MWDLH/kaleidosec.git \
  ~/.claude/skills/kaleidosec
```

**Codex** — copy or clone into the Codex skills directory (project `.agents/skills/`, user `~/.agents/skills/`):

```bash
git clone https://github.com/MWDLH/kaleidosec.git \
  .agents/skills/kaleidosec
```

Restart the client after installation. Keep the directory intact; internal routing depends on relative paths.

## Entering the mode

Place the sentinel `.kaleidosec` in the engagement directory (the legacy `.pfo_active` is still recognized):

```json
{"engagement_id":"acme-01","objective":"decide whether the low-privilege account reaches the DC","tier":"quick"}
```

An optional fourth field `scope_root` limits inheritance to that subtree:

```json
{"engagement_id":"acme-01","objective":"…","tier":"standard","scope_root":"."}
```

## Usage

```
Use $kaleidosec.

Objective: decide whether this low-privilege domain account can reach a materially harmful outcome.
Scope: lab.example.internal and 12 hosts below it.
Authorization: L0-L2 pre-approved; persistence prohibited.
Current access: VPN, one standard domain user.
Evidence: [host details, service scan, identity enumeration]

Continue on the path with the strongest evidence and the highest value.
```

Resume: supply the matching `.pentest_session.json` and the agent resumes from the parent path instead of
starting over.

## Host support

| Host | Loading | Determinism |
|---|---|---|
| Claude Code (plugin) | `hooks/` auto-injection + skill | **High**: sentinel or strong keyword enters the mode |
| Claude Code (manual hook) | `examples/claude-hook/settings.json` | **High**: same as above |
| Claude Code (plain skill) | copy into `~/.claude/skills/` | Low: description-driven invocation |
| Codex | `.agents/skills/` | Low: description-driven invocation |
| dsh | not yet adapted | — |

"Determinism" means the mode does not depend on the model remembering to use it; low-determinism hosts
still need an explicit call.

## Repository

```text
kaleidosec/
|-- SKILL.md                    ← single always-on protocol (the injection source)
|-- .claude-plugin/             ← plugin manifest + marketplace
|-- hooks/                      ← hooks.json + kaleido_gate.py (deterministic injection)
|-- skills/kaleidosec/          ← thin plugin skill entry (points to root protocol)
|-- modes/                      ← STANDARD / DEEP on-demand cards
|-- references/                 ← 14 domain & capability directories, each with a router
|-- scripts/                    ← state helper + budget/sync checks
|-- examples/claude-hook/       ← manual hook fallback when not using the plugin
|-- agents/openai.yaml          ← Codex interface definition
|-- README.md / README.en.md
|-- CHANGELOG.md / CONTRIBUTING.md / SECURITY.md / LICENSE
```

## Upgrading from v1

Kaleidosec 2.0 is a structural upgrade from the 1.1 `pentest-field-operator` skill:

- Name unified as `kaleidosec`; installation is now a plugin (two commands)
- Always-on protocol reduced from ~3.5k tokens to ~1.4k
- Static tiering replaced by a judgment framework; deterministic injection and state verbs added
- Legacy `.pfo_active`, `PFO_FORCE`, and `CLAUDE.md` blocks are still recognized

See [CHANGELOG.md](CHANGELOG.md).

## Authorization and disclaimer

Kaleidosec is intended **only** for security testing, red-team exercises and attack-defense assessments
for which you hold explicit authorization.

- You must ensure you have lawful authorization for every target and stay within its scope.
- This project grants no testing permission and accepts no responsibility for your actions or their consequences.
- Do not use it against systems, networks, accounts or data you are not authorized to test.
- The tool itself performs no attacks; execution is carried out by the agent and external tools you choose, at your own responsibility.
- Do not retain unredacted client data, credentials, evidence or target information in reports or commits.
- Untested surfaces must not be reported as complete; output does not replace professional judgment or legal authorization.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Never commit real target data, credentials or client evidence.

## License

[MIT](LICENSE)
