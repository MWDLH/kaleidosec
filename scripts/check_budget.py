#!/usr/bin/env python3
"""Fail when the always-on protocol exceeds its token budget.

The budget is what keeps the "enter in operator mode without paying a manual's worth
of tokens" promise honest. Without a check it only ever grows.

Exit code 0 = within budget (or an estimate that cannot prove otherwise),
1 = over budget.

Estimates never fail on their own: without tiktoken the count is inferred from word
count, which runs ~1% high on this corpus. A check that reports a failure it cannot
verify is worse than no check — it teaches contributors to ignore the gate. When
tiktoken is installed (as in CI) the exact count is enforced.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "SKILL.md"
BUDGET = 1500

# The word-count fallback over-reports by roughly 1% here; only a count this far past
# the budget is reliably over even after that error.
ESTIMATE_MARGIN = 1.02


def body_of(text: str) -> str:
    return re.sub(r"^---\r?\n.*?\r?\n---\r?\n", "", text, count=1, flags=re.S)


def count_tokens(text: str) -> tuple[int, str, bool]:
    """Return (tokens, method, exact)."""
    try:
        import tiktoken

        return len(tiktoken.get_encoding("cl100k_base").encode(text)), "tiktoken/cl100k", True
    except Exception:
        # Calibrated on this corpus at ~1.53 tokens/word; 1.55 keeps the estimate on the
        # high side so a real regression is never hidden.
        return int(len(text.split()) * 1.55), "estimated(words*1.55)", False


def main() -> int:
    if not SOURCE.is_file():
        print(f"ERROR: missing {SOURCE}")
        return 1
    text = SOURCE.read_text(encoding="utf-8")
    body = body_of(text)
    tokens, method, exact = count_tokens(body)

    if exact:
        status = "ok" if tokens <= BUDGET else "OVER BUDGET"
        print(f"always-on protocol: {tokens} tokens / budget {BUDGET} ({method}) - {status}")
        return 0 if tokens <= BUDGET else 1

    if tokens > BUDGET * ESTIMATE_MARGIN:
        print(
            f"always-on protocol: ~{tokens} tokens / budget {BUDGET} ({method}) - "
            "OVER BUDGET (clearly over even allowing the estimate's ~1% error)"
        )
        return 1

    note = "tiktoken would confirm it" if tokens > BUDGET else "install tiktoken for the exact count"
    print(
        f"always-on protocol: ~{tokens} tokens / budget {BUDGET} ({method}) - "
        f"not enforced without tiktoken ({note})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
