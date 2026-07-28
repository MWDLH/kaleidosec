# Security Policy

## Intended use

Pentest Field Operator is intended only for systems, applications, accounts, and environments for which the operator has explicit authorization. This repository provides decision workflows and reference material; it does not grant permission to test any target.

Do not publish through issues or pull requests:

- live credentials, tokens, private keys, cookies, or hashes;
- client names, internal hostnames, IP addresses, source code, logs, or evidence;
- private vulnerability details affecting a third party;
- weaponized material unnecessary to reproduce a project problem.

Use sanitized synthetic examples.

## Reporting a project vulnerability

For vulnerabilities in the Skill, state helper, packaging, or documentation, prefer GitHub private vulnerability reporting when enabled. If unavailable, contact the repository owner privately before opening a public issue.

Include the affected file and revision, impact on activation, routing, state integrity, secret handling, or safety classification, sanitized reproduction steps, expected and actual behavior, and a proposed mitigation when available.

Do not test a suspected project issue against an external target.

## Scope

This policy covers Pentest Field Operator itself. Findings from an authorized engagement follow that engagement's disclosure and evidence-handling rules, not this repository's public issue process.

## Supported versions

Until tagged releases exist, only the latest revision is maintained. After releases begin, document the supported release line here.