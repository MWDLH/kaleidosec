# Security Policy

## Intended use

Kaleidosec is intended only for systems, applications, accounts, and environments for which the operator has explicit authorization. This repository provides decision workflows and reference material; it does not grant permission to test any target.

Do not publish through issues or pull requests:

- live credentials, tokens, private keys, cookies, or hashes;
- client names, internal hostnames, IP addresses, source code, logs, or evidence;
- private vulnerability details affecting a third party;
- weaponized material unnecessary to reproduce a project problem.

Use sanitized synthetic examples.

## Local execution surface

When installed as a Claude Code plugin, this project registers three hooks that run a local Python
script (`hooks/kaleido_gate.py`): `SessionStart`, `UserPromptSubmit`, and `PreToolUse`. The script
requires Python 3.8+ available as `python`; if that interpreter is missing the hook command fails and no
protocol is injected.

What it reads, all read-only:

- `PreToolUse`: the proposed Bash command, only to match a short list of obviously destructive patterns
  (recursive delete, persistence, credential dumping, bulk credential attempts). When one matches, it
  returns a confirmation request to the host — it never blocks silently and never executes anything.
  It is active only in a workspace that contains a sentinel and can be disabled with
  `KALEIDO_NO_GUARD=1`.

- JSON on stdin: the working directory and, for `UserPromptSubmit`, the prompt text.
- `SKILL.md` — the protocol it injects.
- `.kaleidosec` or `.pentest_session.json`, walking up to four parent directories and stopping at
  `$HOME`, to build a short state summary. These files are engagement state and may contain target
  names, scope, and findings.
- `CLAUDE.md` at the working directory, in up to four ancestor directories (stopping at `$HOME`),
  and at `~/.claude/CLAUDE.md` — only to detect an existing managed protocol block and classify it
  as current, stale, or unversioned. No other content from those files is used, and nothing from
  them is injected except a path-level notice.

What it does not do: it writes nothing to disk and makes no network requests; the exit code is
always 0.

What it prints into context:

| Situation | Output |
|---|---|
| Engagement marker present, session start | Full protocol plus a short state summary |
| Engagement marker present, later prompts | Nothing, except a one-line hint when the prompt matches pentest signals (the hook cannot see whether the protocol is still in context) |
| No marker, session start | A ~70-token entry hint, plus a notice if a managed `CLAUDE.md` block was found elsewhere |
| No marker, prompt matches pentest signals | Full protocol |
| Anything else | Nothing |

One exception to every row: a **current** managed block in `<cwd>/CLAUDE.md` already supplies the
protocol, so the gate injects no protocol text at all (only the state summary, if any). Blocks found
anywhere else do not suppress injection — a block on disk is not proof that the host loaded it — and
are reported as a notice alongside the injected text.

`KALEIDO_FORCE=1` exists only for deliberate manual injection, overriding the "a `CLAUDE.md` block
already supplies the protocol" suppression; it is never required in normal use.

Review `hooks/hooks.json` and `hooks/kaleido_gate.py` before installing. The install-time trust prompt is
the security boundary: hooks run with your user privileges.

The plugin intentionally declares no `network.hosts` allowlist. The gate itself makes no network
requests; the operator acts on whatever authorized targets the user names, so a static host list
would be misleading. Scope control lives in the authorization profile, not in a manifest allowlist.

## Reporting a project vulnerability

For vulnerabilities in the Skill, state helper, packaging, or documentation, prefer GitHub private vulnerability reporting when enabled. If unavailable, contact the repository owner privately before opening a public issue.

Include the affected file and revision, impact on activation, routing, state integrity, secret handling, or safety classification, sanitized reproduction steps, expected and actual behavior, and a proposed mitigation when available.

Do not test a suspected project issue against an external target.

## Scope

This policy covers Kaleidosec itself. Findings from an authorized engagement follow that engagement's disclosure and evidence-handling rules, not this repository's public issue process.

## Supported versions

Until tagged releases exist, only the latest revision is maintained. After releases begin, document the supported release line here.