#!/usr/bin/env python3
"""Kaleidosec gate — deterministic context injector for hook-based agents.

Design rule: decide by *environment marker*, never by asking the model.
A marker file (.pentest_session.json / .kaleidosec / legacy .pfo_active) or an
explicit env var is a boolean fact. Keyword matching is only a fallback for cold
starts.

The injected text is the single source of truth: the body of SKILL.md with its
YAML front matter stripped. No second copy is kept, so the kernel cannot drift.

Usage (called by an agent hook, JSON on stdin):
    python kaleido_gate.py session-start
    python kaleido_gate.py user-prompt

Exit code is always 0. Anything printed to stdout is injected into the
agent context. Printing nothing is the normal, cheap path.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from pathlib import Path

MARKER_NAMES = (".pentest_session.json", ".kaleidosec", ".pfo_active")
MAX_PARENT_WALK = 4
MAX_SOURCE_WALK = 6

# SessionStart has no prompt; these signals let an engagement-looking workspace enter
# the mode without the user creating any file.
ENGAGEMENT_DIR_HINTS = (
    "pentest", "engagement", "redteam", "red-team", "adversary", "渗透", "红队", "攻防",
)
ENGAGEMENT_FILE_HINTS = (".kaleidosec", ".pentest_session.json", ".pfo_active")
ENGAGEMENT_FILE_PATTERNS = ("*.har", "*.burp", "*.nmap", "nuclei*.txt", "httpx*.txt", "subdomains*.txt")


def looks_like_engagement(cwd: Path | None) -> bool:
    if cwd is None:
        return False
    path = cwd.resolve()
    lowered = str(path).lower()
    if any(hint in lowered for hint in ENGAGEMENT_DIR_HINTS):
        return True
    if any((path / name).exists() for name in ENGAGEMENT_FILE_HINTS):
        return True
    for pattern in ENGAGEMENT_FILE_PATTERNS:
        if next(path.glob(pattern), None) is not None:
            return True
    return False

# Strong: domain-exclusive, low false-positive. A hit alone is enough to inject.
STRONG_KEYWORDS = (
    "pentest", "penetration test", "red team", "redteam", "offensive security",
    "kerberoast", "lateral movement", "privilege escalation", "privesc",
    "webshell", "reverse shell", "burp", "nmap", "bloodhound", "hashcat",
    "渗透", "渗透测试", "打点", "提权", "横向", "内网", "域控", "授权测试", "红队",
    "红蓝对抗", "攻防", "攻防演练", "挖洞", "漏洞挖掘", "反弹",
)

# Weak: frequent in coding/repair/writing tasks. Only counts next to an object word.
WEAK_KEYWORDS = (
    "sql injection", "sqli", "xss", "ssrf", "rce", "idor", "cve-",
    "payload", "bypass", "exploit", "免杀", "漏洞", "利用", "提审",
)

# Object words that turn a weak signal into a real target-scoped request.
# Deliberately excludes broad terms (系统 / 服务 / 环境 / 地址 / server / api): they
# appear in ordinary development talk and do not identify a concrete target.
OBJECT_WORDS = (
    "目标", "主机", "站点", "网站", "接口", "域名",
    "target", "host", "site", "endpoint", "domain", "url", "ip",
)

# SessionStart in a workspace without a marker: a short, ignorable invitation.
# Without it a new engagement never learns that the mode exists (no marker -> no
# protocol -> nobody writes the marker).
INVITE = (
    "<!-- Kaleidosec: no engagement marker here; operator mode is off. -->\n"
    "Say what you are doing (e.g. 渗透 / red team / 攻防 / 挖洞) and the mode enters "
    "automatically. Optionally add `.kaleidosec` to keep this workspace in operator mode "
    "across sessions and resume. Ignore if unrelated, or if ~/.claude/CLAUDE.md has a Kaleidosec block."
)

# Emitted only when a sentinel exists but a pentest-shaped prompt arrives; the hook has
# no session memory, so it cannot know whether SessionStart already injected.
HINT_SENTINEL = (
    "<!-- Kaleidosec: sentinel present; if the protocol is not in context, restart or /clear "
    "(ignore if it is above). -->"
)

PFO_BLOCK = re.compile(r"<!--\s*(?:KALEIDO|PFO)-BEGIN(?:\s+source=([0-9a-f]{8}))?\s*-->")


# Explicit writing requests are not engagements, unless a real target is named.
WRITING_WORDS = ("写一篇", "写个文档", "写一份", "教程", "科普", "介绍文章")


def prompt_hits(prompt: str) -> bool:
    text = prompt.lower()
    if any(w in text for w in WRITING_WORDS) and not any(o in text for o in OBJECT_WORDS):
        return False
    if any(k in text for k in STRONG_KEYWORDS):
        return True
    return any(k in text for k in WEAK_KEYWORDS) and any(o in text for o in OBJECT_WORDS)


def body_fingerprint(body: str) -> str:
    return hashlib.sha256(body.encode("utf-8")).hexdigest()[:8]


def block_state(candidate: Path, fingerprint: str) -> tuple[str, str] | None:
    """Classify a PFO block in one CLAUDE.md.

    Returns None when the file has no block, else (kind, message) with kind in
    {"fresh", "stale", "unversioned"}.
    """
    try:
        text = candidate.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    match = PFO_BLOCK.search(text)
    if not match:
        return None
    recorded = match.group(1)
    if not recorded:
        return "unversioned", (
            f"<!-- Kaleidosec: unversioned PFO block in {candidate}; freshness cannot be verified. "
            "Remove it or re-add it with source=<hash>. -->"
        )
    if recorded != fingerprint:
        return "stale", (
            f"<!-- Kaleidosec: stale PFO block in {candidate} "
            f"(source={recorded}, current={fingerprint}); re-sync or remove it. -->"
        )
    return "fresh", (
        f"<!-- Kaleidosec: {candidate} already carries the current protocol; "
        "duplicate injection is wasteful. Remove that block to avoid it. -->"
    )


def claude_md_state(cwd: Path | None, fingerprint: str) -> tuple[str, str]:
    """Decide whether an existing PFO block already supplies the protocol.

    Only <cwd>/CLAUDE.md may suppress injection: it is the one location the host is
    guaranteed to load. A block anywhere else (ancestors, $HOME/CLAUDE.md,
    ~/.claude/CLAUDE.md) yields a notice and the gate still injects — "a block was
    found" is not "the block is in context".
    """
    if cwd is None:
        return "absent", ""
    cwd = cwd.resolve()
    notices: list[str] = []

    local = cwd / "CLAUDE.md"
    if local.is_file():
        state = block_state(local, fingerprint)
        if state is not None and state[0] == "fresh":
            return "block", ""
        if state is not None:
            notices.append(state[1])

    user = Path.home() / ".claude" / "CLAUDE.md"
    if user.is_file() and user.resolve() != local.resolve():
        state = block_state(user, fingerprint)
        if state is not None:
            notices.append(state[1])

    home = Path.home().resolve()
    current = cwd.parent
    for _ in range(MAX_PARENT_WALK):
        candidate = current / "CLAUDE.md"
        if candidate.is_file() and candidate.resolve() != local.resolve():
            state = block_state(candidate, fingerprint)
            if state is not None:
                notices.append(state[1])
        if current == home or current.parent == current:
            break
        current = current.parent

    if notices:
        return "notice", "\n".join(notices)
    return "absent", ""

FRONT_MATTER = re.compile(r"^﻿?---\r?\n.*?\r?\n---\r?\n", re.S)


def strip_front_matter(text: str) -> str:
    match = FRONT_MATTER.match(text)
    return text[match.end():] if match else text


def find_source() -> Path | None:
    """Locate the single source of truth for injected text.

    Search order, upward from this file:
      1. SKILL.md with a sibling references/ directory
      2. skills/kaleidosec/SKILL.md (installed-plugin layout)

    The thin plugin entry has no references/ and is therefore never selected; the
    specific skill name keeps a sibling skill in the same host from being injected.
    """
    here = Path(__file__).resolve()
    for depth, parent in enumerate(here.parents):
        if depth > MAX_SOURCE_WALK:
            break
        candidate = parent / "SKILL.md"
        if candidate.is_file() and (parent / "references").is_dir():
            return candidate
        candidate = parent / "skills" / "kaleidosec" / "SKILL.md"
        if candidate.is_file() and (candidate.parent / "references").is_dir():
            return candidate
    return None


def marker_scope_ok(marker: Path, start: Path) -> bool:
    """A marker may declare scope_root; when present, the working directory must be inside it."""
    try:
        data = json.loads(marker.read_text(encoding="utf-8"))
    except Exception:
        return True
    if not isinstance(data, dict):
        return True
    root = data.get("scope_root")
    if not root:
        return True
    root_path = Path(str(root))
    if not root_path.is_absolute():
        root_path = marker.parent / root_path
    try:
        start.resolve().relative_to(root_path.resolve())
        return True
    except ValueError:
        return False


def find_marker(start: Path | None) -> Path | None:
    if start is None:
        return None
    current = start.resolve()
    home = Path.home().resolve()
    for _ in range(MAX_PARENT_WALK + 1):
        # Never inherit a marker from $HOME or above. On shallow home layouts that would
        # inject every unrelated project and leak engagement details into it.
        if current == home:
            break
        for name in MARKER_NAMES:
            candidate = current / name
            if candidate.exists() and marker_scope_ok(candidate, start):
                return candidate
        if current.parent == current:
            break
        current = current.parent
    return None


def read_stdin_json() -> dict:
    try:
        raw = sys.stdin.buffer.read().decode("utf-8", "replace")
        if not raw.strip():
            return {}
        data = json.loads(raw)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def force_utf8_stdio() -> None:
    """Hooks exchange UTF-8 JSON regardless of the OS locale (notably Windows/cp936)."""
    for stream, kwargs in (
        (sys.stdin, {"encoding": "utf-8", "errors": "replace"}),
        (sys.stdout, {"encoding": "utf-8"}),
        (sys.stderr, {"encoding": "utf-8", "errors": "replace"}),
    ):
        try:
            stream.reconfigure(**kwargs)
        except Exception:
            pass


def state_summary(marker: Path) -> tuple[str, bool]:
    """Return (summary, readable). Resume guidance only when there is something to resume."""
    try:
        data = json.loads(marker.read_text(encoding="utf-8"))
    except Exception:
        return "", False
    if not isinstance(data, dict):
        return "", False

    lines = ["## Kaleidosec session state (injected from marker)"]
    objective = data.get("objective")
    if objective:
        lines.append(f"- objective: {objective}")
    scope = data.get("scope") or {}
    if isinstance(scope, dict):
        status = scope.get("status")
        if status:
            if status == "confirmed":
                ref = scope.get("authorization_ref")
                status = (
                    f"confirmed (self-declared, ref: {ref})" if ref
                    else "confirmed (self-declared, no credential)"
                )
            lines.append(f"- scope status: {status}")
        assets = scope.get("assets") or []
        if assets:
            shown = ", ".join(str(a) for a in assets[:8])
            lines.append(f"- assets: {shown}{' ...' if len(assets) > 8 else ''}")
    ctx = data.get("domain_context") or {}
    # "unclassified" is the init default; reporting it adds tokens without information.
    if isinstance(ctx, dict) and ctx.get("primary_domain") not in (None, "", "unclassified"):
        lines.append(f"- primary domain: {ctx['primary_domain']}")

    paths = data.get("attack_paths") or []
    active = [p for p in paths if isinstance(p, dict) and p.get("status") in {"active", "deep_dive"}]
    if active:
        lines.append(f"- active paths: {len(active)}")
        for item in active[:5]:
            title = item.get("title") or item.get("id") or "unnamed"
            nxt = item.get("next_action") or ""
            lines.append(f"  - {title}{(' → ' + str(nxt)) if nxt else ''}")

    nxt = data.get("next_decision") or {}
    has_next = False
    if isinstance(nxt, dict):
        action = nxt.get("recommended_action") or nxt.get("action")
        if action:
            lines.append(f"- next decision: {action}")
            has_next = True

    if len(lines) == 1:
        return "", True
    if active or has_next:
        lines.append("- Resume from the recorded path; do not restart collection from zero.")
    return "\n".join(lines), True


# Minimal, high-confidence guard for the highest-impact actions. This is a last-resort
# net, not a sandbox: it only recognizes obvious destructive commands and asks the human
# to confirm. Anything else relies on the protocol in SKILL.md.
GUARD_PATTERNS = (
    (re.compile(r"\brm\s+-[A-Za-z]*r[A-Za-z]*f|\brm\s+-[A-Za-z]*f[A-Za-z]*r", re.I), "recursive force delete"),
    (re.compile(r"\bdel\s+/[sf]|\brd\s+/s|\brmdir\s+/s", re.I), "recursive delete"),
    (re.compile(r"\b(format\s+[a-z]:|\bmkfs\b|\bshred\b|dd\s+if=.*of=/dev/)", re.I), "destructive disk operation"),
    (re.compile(r"\bschtasks\s+/create\b|\bsc(\.exe)?\s+create\b|\breg(\.exe)?\s+add\b[^\n]*\\Run\b|"
                r"\bsystemctl\s+enable\b|\bcrontab\s+-e\b|\blaunchctl\s+load\b", re.I), "persistence"),
    (re.compile(r"\bmimikatz\b|\bsecretsdump\b|procdump[^\n]*lsass|comsvcs\.dll[^\n]*MiniDump|"
                r"\breg(\.exe)?\s+save\b[^\n]*\bSAM\b", re.I), "credential dumping"),
    (re.compile(r"\bhydra\b|\bmedusa\b|\bpatator\b", re.I), "bulk credential attempts"),
)

GUARD_BYPASS_ENV = "KALEIDO_NO_GUARD"


def handle_pre_tool(payload: dict, cwd: Path | None) -> int:
    """Ask for human confirmation on obvious high-impact shell commands inside an engagement."""
    if os.environ.get(GUARD_BYPASS_ENV, "").strip() in {"1", "true", "yes"}:
        return 0
    if cwd is None or find_marker(cwd) is None:
        return 0  # not an engagement workspace; stay out of the way
    if payload.get("tool_name") != "Bash":
        return 0
    tool_input = payload.get("tool_input") or {}
    command = str(tool_input.get("command") or "")
    if not command:
        return 0
    for pattern, label in GUARD_PATTERNS:
        if pattern.search(command):
            result = {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "ask",
                    "permissionDecisionReason": (
                        f"Kaleidosec guard: recognized {label}. Confirm this action is "
                        "authorized and intended before it runs."
                    ),
                }
            }
            sys.stdout.write(json.dumps(result) + "\n")
            return 0
    return 0


def main() -> int:
    force_utf8_stdio()
    event = sys.argv[1] if len(sys.argv) > 1 else "user-prompt"
    payload = read_stdin_json()

    cwd_raw = payload.get("cwd") or os.environ.get("PFO_CWD") or os.getcwd()
    cwd = Path(cwd_raw) if cwd_raw else None

    if event == "pre-tool":
        return handle_pre_tool(payload, cwd)

    source = find_source()
    if source is None:
        print(
            f"Kaleidosec: protocol source not found near {Path(__file__).resolve().parent}; "
            "injection disabled (expected SKILL.md + references/)",
            file=sys.stderr,
        )
        return 0
    try:
        body = strip_front_matter(source.read_text(encoding="utf-8"))
    except Exception:
        return 0

    md_state, md_notice = claude_md_state(cwd, body_fingerprint(body))
    marker = find_marker(cwd)
    forced = os.environ.get(
        "KALEIDO_FORCE", os.environ.get("PFO_FORCE", "")
    ).strip() in {"1", "true", "yes"}
    prompt = str(payload.get("prompt") or "")

    # SessionStart already injected the protocol (or a cwd CLAUDE.md supplies it); do not
    # re-send it on every message. If the sentinel was created mid-session the protocol may
    # be missing from context, so a pentest-shaped prompt gets one short hint.
    if event == "user-prompt" and not forced:
        if marker is not None or md_state == "block":
            if md_state != "block" and prompt_hits(prompt):
                sys.stdout.write(HINT_SENTINEL + "\n")
            return 0

    if md_state == "block" and not forced:
        # The cwd CLAUDE.md carries the current protocol; deliver only the state summary.
        # KALEIDO_FORCE is the manual escape hatch: it must be able to inject even here.
        if event == "session-start" and marker is not None:
            summary, _ = state_summary(marker)
            if summary:
                sys.stdout.write(summary + "\n")
        return 0

    auto_entered = False
    if not marker and not forced:
        if event == "session-start":
            if looks_like_engagement(cwd):
                # The workspace looks like an engagement; enter without asking for a file.
                auto_entered = True
            else:
                # No marker yet: give a short, ignorable entry hint so a new engagement is
                # not a silent dead end. A notice about an existing block travels with it.
                text = INVITE if not md_notice else INVITE + "\n" + md_notice
                sys.stdout.write(text + "\n")
                return 0
        elif not prompt_hits(prompt):
            return 0  # cheap path: inject nothing

    out = [
        "<!-- Kaleidosec: injected by gate -->",
        f"Resource root: {source.parent.resolve()}",
        "All references/ and modes/ paths in this protocol are relative to that directory.",
    ]
    if md_notice:
        out.append(md_notice)
    if auto_entered:
        out.append(
            "<!-- Kaleidosec: engagement-like workspace detected; operator mode entered. "
            "Add `.kaleidosec` to make this stable across sessions. -->"
        )
    out.append(body)

    if marker is not None:
        summary, readable = state_summary(marker)
        if summary:
            out.append("")
            out.append(summary)
        if event == "session-start":
            out.append("")
            if readable:
                out.append(
                    "A marker file is present: this workspace is already in operator mode. "
                    "Resume the engagement."
                )
            else:
                out.append(f"<!-- Kaleidosec: marker {marker} is unreadable; fix or recreate it. -->")

    sys.stdout.write("\n".join(out))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except SystemExit:
        raise
    except Exception:
        raise SystemExit(0)
