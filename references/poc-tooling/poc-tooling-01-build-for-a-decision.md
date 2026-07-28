# PoC, Debugging, And Tool Engineering Capability: Build For A Decision

> Apply [../module-continuity.md](../module-continuity.md). Inherit the engagement, parent path, current capability, evidence, authorization profile, and module stack. Do not initialize a separate workflow. Checkpoint material results and return them to the parent path before leaving this card.

## Build For A Decision

A PoC must answer a security question, not maximize capability. The best PoC is the simplest one that proves the finding.

Define expected observations before writing code:

| Observation | Meaning |
|---|---|
| **Positive** | Vulnerability confirmed — PoC demonstrates the expected security impact |
| **Negative** | Vulnerability NOT confirmed — condition absent, control present, or hypothesis wrong |
| **Partial** | Some precondition met, but exploitation incomplete — need more data or different approach |
| **Ambiguous** | Result could mean multiple things — PoC design flaw or insufficient observability |

### PoC Header Template

Every generated PoC script must start with this comment block:

```text
Purpose: <what security question this answers, in one sentence>
Environment: <OS, language version, required tools>
Dependencies: <pip packages, system libs, network access needed>
Risk: <what this script does to the target — read-only? creates data? changes state?>
Target assumptions: <what we assume is true about the target — mark UNVERIFIED for untested assumptions>
Evidence output: <what to capture as proof — file path, screenshot, log excerpt>
Cleanup: <how to undo changes, if any>
Self-check status: <PASSED/FAILED/NOT TESTED — does the script syntax-check and run locally in dry-run mode?>
```

### Example

```python
"""
Purpose: Verify if /api/users/{id} is vulnerable to IDOR between Tenant A and Tenant B
Environment: Python 3.8+, no special libraries required (stdlib only)
Dependencies: None (uses urllib from stdlib)
Risk: Read-only — makes GET requests with test accounts; does not modify data
Target assumptions:
  - UNVERIFIED: user IDs are sequential integers
  - UNVERIFIED: API token format is Bearer <jwt> (from client code analysis)
  - CONFIRMED: API base URL is https://api.target.com/v2 (from traffic capture)
Evidence output: HTTP response differences printed to stdout; full responses saved to ./evidence/
Cleanup: None — read-only, no target state change
Self-check status: PASSED — syntax ok, dry-run mode verified with local mock server
"""
```

---


## Card Exit

Classify the result, update evidence and attempted methods, record capability or risk changes, identify affected paths, and apply the return contract in [../module-continuity.md](../module-continuity.md).
