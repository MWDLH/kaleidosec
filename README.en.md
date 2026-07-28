# Pentest Field Operator

[简体中文](README.md) | English

**An evidence-driven penetration testing Skill for AI agents — think like a senior operator, not a script kiddie.**

<br>

AI agents don't lack vulnerability knowledge. Ask one about SQL injection types, Kerberos authentication flows, or AWS privilege escalation paths — it'll answer better than most engineers.

What they lack is the ability to make the right call, repeatedly, in a real, dynamic, information-incomplete engagement.

Pentest Field Operator exists to close that gap. It doesn't teach an agent how to use sqlmap — it teaches it how to *think*:

- What evidence do I have? What critical information is still missing?
- Which path has the highest value right now?
- When something fails, which variable do I change — instead of which tool I switch to?
- After gaining new access, how do I continue the original attack chain?

In short: it gives an AI agent an operating system for real penetration testing.

---

## What it solves

| Common Agent Failure | How Pentest Field Operator Fixes It |
|---|---|
| :repeat: **Tool cycling** — swaps tools on failure without diagnosing the cause | 8-layer failure classification (execution / environment / access / reachability / method / prerequisite / hypothesis / route value) — changes one variable at a time |
| :newspaper: **Alert = finding** — reports every scanner output as confirmed | Evidence grading (fact / inference / hypothesis / unknown / rejected) — a fingerprint or CVE match is not a confirmed vulnerability |
| :dizzy_face: **Cross-domain amnesia** — restarts discovery after every pivot | Module stack + parent-path return protocol — carries identity, network position, evidence, and objective across domains |
| :tunnel: **Tunnel vision** — drills one path indefinitely | Four-state path management (active / deep_dive / parked / closed) — parks low-value paths with a reactivation condition |
| :shrug: **Decision black box** — can't explain why this step was chosen | Every action outputs: current judgment, key evidence, critical unknowns, why this step ranks first, and what to change on failure |

---

## How it works — in 30 seconds

The Skill turns penetration testing into a **decision loop** that never loses state:

```
Where am I? → What do I know? → What's the best path?
→ Execute one bounded action → What happened?
→ What changed? → Back to step one
```

It does this through four mechanisms that no other pentest Skill provides:

:compass: **Evidence-driven decisions** — Every action is justified by confirmed facts, not tool availability. `"I'm doing X because we observed Y, and the unknown Z could change the route."`

:fork_and_knife: **Attack path management** — Paths are tracked, ranked, deepened, parked, or closed. No tunnel vision. No checklist-driven shallowness.

:link: **Cross-domain continuity** — When you pivot from a web app to internal AD to cloud IAM, the agent carries identity, network position, evidence, and the parent objective. It doesn't start over.

:shield: **Practical safety model** — Actions are classified by actual impact (L0–L3), not tool names. Routine work flows without interruption; persistence, trust changes, and control-plane mutation require explicit approval.

---

## A real example

```
Operator: "I have a low-privilege domain user. Can we reach DA?"

Agent [Skill loaded]:
  1. Establish position: whoami, groups, network interfaces, domain controller
  2. Collect: enumerate SPNs → find a service account with MSSQLSvc SPN
  3. Decision: Kerberoast the service account (low noise, high info gain)
  4. Execute: GetUserSPNs → crack offline → cleartext password
  5. Validate: crackmapexec → local admin on SQL-01
  6. Pivot: WMIExec to SQL-01 → discover linked server to DC
  7. Impact: xp_cmdshell on DC via linked server → Domain Admin confirmed
  8. Cleanup: remove test account, document chain, save session state
```

Each step was chosen because evidence supported it, not because a checklist said so. Each failure would have been diagnosed at the correct layer — credential quality, network reachability, EDR interference — rather than cycling tools.

---

## Coverage

**8 attack surfaces. 5 cross-cutting capabilities.** Cards load only when evidence supports them — the agent never traverses directories as a checklist.

| Domain | Coverage |
|---|---|
| :globe_with_meridians: **Web/API** | SQLi, XSS, CSRF, SSRF, SSTI, Deserialization, JWT, OAuth, GraphQL, Race Conditions, File Upload, Command Injection |
| :iphone: **Mobile** | Android Components, iOS Keychain & ATS, WebView, Deep Links, Certificate Pinning, Backend API |
| :busts_in_silhouette: **Internal/AD** | Kerberos, ACL Abuse, AD CS, Lateral Movement, Credential Dumping, LOLBin, Trust Hopping |
| :cloud: **Cloud/Container** | AWS/Azure/GCP IAM, IMDS, K8s RBAC, Container Escape, Serverless, Storage Exposure |
| :robot: **AI Security** | Prompt Injection, Tool Calling, RAG Poisoning, File & URL Processing, Model Supply Chain |
| :package: **Supply Chain** | CI/CD Pipelines, OIDC, Dependency Confusion, Runner Takeover, IaC, Registries |
| :satellite: **Mini-Program** | wx.login Trust Chain, Cloud Functions, WebView, Payment Logic, Platform Identity |
| :desktop_computer: **Infrastructure** | Redis/MongoDB/ES, VPN, Default Credentials, Thick Clients, Network Appliances |

| Capability | Coverage |
|---|---|
| :microscope: **Code Audit** | Java/PHP/Python/JS/Go/C# Sink Patterns, Source-to-Sink Data-Flow Analysis |
| :wrench: **Reverse & Protocol** | Native Binary, Java/.NET Decompilation, Frida Runtime Hooking, Custom Protocol Analysis |
| :test_tube: **PoC Development** | Bounded Exploit Validation, Failure Debugging, Tool Engineering, PoC Templates |
| :bust_in_silhouette: **Identity & Network** | Credential Type Reference, Tunneling & Pivoting, Network Position Modeling |
| :shield: **Evasion** | AMSI/AppLocker/LSA Protection Diagnosis, EDR Behavioral Detection Awareness |

---

## Installation

**Claude Code** — copy or clone to the user skills directory:

```bash
git clone https://github.com/MWDLH/pentest-field-operator.git \
  ~/.claude/skills/pentest-field-operator
```

**Codex** — copy or clone to the Codex skills directory:

```bash
git clone https://github.com/MWDLH/pentest-field-operator.git \
  $CODEX_HOME/skills/pentest-field-operator
```

Or copy manually to `~/.codex/skills/pentest-field-operator`.

Restart your client after installation. Keep the directory intact — internal routing depends on relative paths.

## Usage

```
Use $pentest-field-operator.

Objective: determine whether this low-privilege domain account can
reach a material security outcome.
Scope: lab.example.internal and the 12 hosts listed below.
Authorization: L0-L2 are pre-authorized; no persistence.
Current access: VPN, one domain user account.
Evidence: [attach host info, service scan, identity enumeration]

Continue from the strongest evidence-supported path.
```

To resume an interrupted engagement, provide the matching `.pentest_session.json`.

---

## Repository

```text
pentest-field-operator/
|-- SKILL.md              ← Core operator rules, safety gates, decision contracts
|-- agents/openai.yaml    ← Codex interface definition
|-- scripts/              ← State management helper (Python 3.9+)
|-- references/           ← 13 domain & capability directories, each with a router
|-- README.md / README.en.md
|-- CONTRIBUTING.md / SECURITY.md / LICENSE
```

---

## Design boundaries

- :white_check_mark: Authorized security testing only
- :white_check_mark: Does not assume tools are installed — checks availability first
- :white_check_mark: Does not store live passwords, tokens, or private keys
- :white_check_mark: Does not claim untested surfaces were tested
- :white_check_mark: Does not replace professional judgment or legal authorization

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Never submit real target data, credentials, or client evidence.

## License

[MIT](LICENSE)
