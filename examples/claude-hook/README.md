# Optional: wire the gate with a plain settings hook

Use this only if you prefer not to install the plugin. Do **not** use both — the gate already refuses
to double-inject when it finds a managed `CLAUDE.md` block, but two hooks would still run twice.

## Steps

1. Copy `settings.json` into either:
   - `.claude/settings.json` in the engagement repository (project scope), or
   - `~/.claude/settings.json` (user scope; every session on the machine).
2. Replace `/ABSOLUTE/PATH/TO/kaleidosec` with the real path to this repository.
   - Windows: forward slashes work, e.g. `<your-path>/kaleidosec`.
3. Check the interpreter: both commands call `python`, which must be Python 3.8+.
   On macOS 12.3+ and most Linux distributions only `python3` exists — replace `python` with
   `python3` in both commands. Otherwise the hook fails with `python: command not found` and
   injects nothing.
4. Start a new session.

## Behaviour

| Situation | Result |
|---|---|
| Engagement directory contains `.kaleidosec` or `.pentest_session.json` | Protocol injected, plus a state summary |
| Prompt hits a strong keyword (渗透 / red team / nmap / 域控 …) | Protocol injected |
| Obvious destructive Bash command inside an engagement | A confirmation prompt (recursive delete, persistence, credential dumping, bulk credential attempts) |
| Anything else | Nothing injected per prompt; one entry hint at session start |

The `PreToolUse` guard is a backstop only. It matches a short list of obviously destructive commands and
asks for confirmation; it never blocks silently. Disable it with `KALEIDO_NO_GUARD=1`.

The gate reads the protocol from `SKILL.md` at the repository root, so updating the repository updates
the injected protocol. No second copy exists.

## What you will see

- **Fresh directory (no sentinel)**: one short paragraph (~70 tokens) explaining how to enter. This is
  the entry hint, not an error.
- **Engagement directory (sentinel present)**: the full protocol plus a state summary on session
  start; later prompts inject nothing, unless a pentest-shaped prompt arrives (then one hint line).
- **Unrelated work**: nothing injected.

## Verify

```bash
# no output expected
echo '{"prompt":"refactor this React component"}' | python hooks/kaleido_gate.py user-prompt

# protocol expected
echo '{"prompt":"帮我渗透一下这个站点"}' | python hooks/kaleido_gate.py user-prompt | head -3
```

Use `python3` instead of `python` wherever that is the name your system exposes.
