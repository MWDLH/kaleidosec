# Changelog

All notable changes to Kaleidosec are documented here.

## 2.0.1 — 2026-11-24

### Added

- **PreToolUse guard**: inside an engagement workspace, a short list of obviously destructive Bash
  commands (recursive delete, persistence, credential dumping, bulk credential attempts) now triggers a
  human confirmation prompt. It is a backstop, not a sandbox; disable with `KALEIDO_NO_GUARD=1`.
- README: dedicated "highest safety red line" section emphasizing human confirmation for high-impact
  actions, plus an honest note that model output and constraints are not guaranteed reliable.

## 2.0.0 — 2026-11-23

First release under the Kaleidosec name. This is a structural upgrade from the 1.1
`pentest-field-operator` skill.

### Changed

- **Renamed** to Kaleidosec; repository, plugin, and skill are all `kaleidosec`.
- **Distribution**: from a single skill to a Claude Code plugin (skill + hooks), installed with two
  commands; a plain-skill installation path remains available.
- **Always-on protocol** reduced from roughly 3,500 to about 1,400 tokens.
- **Depth selection** replaced the static QUICK/STANDARD/DEEP classification with a judgment framework
  (five dimensions, escalation signals, self-correction).
- **State verbs** expanded to eight (`init`, `position`, `check`, `fact`, `path`, `park`, `promote`, `report`).
- **Routing indexes** for all 14 domains rewritten from generic conditions to evidence triggers plus the
  question each card must answer.
- **Safety model** reworded to decide by impact, with an explicit "only add locks, never relax" rule and a
  no-human-available branch.

### Added

- **Deterministic mode injection**: a sentinel file or a strong keyword enters the mode; unrelated work
  injects nothing (one short entry hint at session start only).
- **Plugin packaging**: `.claude-plugin/` manifests, `hooks/`, thin skill entry, manual-hook example.
- **Budget and sync checks** (`scripts/check_budget.py`, `scripts/check_sync.py`) with a CI workflow.
- **Scope control**: optional `scope_root` on a sentinel limits inheritance.
- **Authorization reference**: `init --scope-status confirmed` requires `--authorization-ref`.

### Fixed

- Sentinel lookup no longer walks past `$HOME`; a stray home sentinel cannot leak engagement data into
  unrelated projects.
- Only a current managed block in `<cwd>/CLAUDE.md` suppresses injection; blocks elsewhere produce a
  notice and the protocol is still injected.
- No repeated full-protocol injection on every prompt.
- Stale or unversioned `CLAUDE.md` blocks are reported instead of silently ignored.
- `PFO_FORCE` (now `KALEIDO_FORCE`) can override block suppression.
- Various documentation and packaging issues found during review.

### Compatibility

- Legacy sentinel `.pfo_active` is still recognized.
- Legacy environment variable `PFO_FORCE` is still honored.
- Legacy `CLAUDE.md` blocks using `PFO-BEGIN` are still detected.
- The plain-skill installation method is unchanged (copy the repository into a skills directory).

### Known limitations

- Codex and dsh adapters are not included in this release.
- A plugin icon is not bundled yet.

## 1.1.0 — 2026-07-30

- Web attack triage, business-logic capability, and technical accuracy overhaul.
