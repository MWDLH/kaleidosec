# CI/CD And Software Supply-Chain Operations: Interpret Results

> Apply [../module-continuity.md](../module-continuity.md). Inherit the engagement, parent path, current capability, evidence, authorization profile, and module stack. Do not initialize a separate workflow. Checkpoint material results and return them to the parent path before leaving this card.

## Interpret Results

- **Repository permission vs workflow permission**: A user with write access to a repo can potentially trigger workflows that use repo secrets. Assess actual vs expected privilege.
- **Secret detection finding**: A regex-detected "secret" (e.g., `ghp_...` pattern) may be a placeholder, example, or expired token. Always validate before reporting.
- **Build log exposure**: CI/CD logs may contain secrets printed by misconfigured scripts. Check old build logs, not just current ones.
- **Fork PR vs branch PR**: Know the distinction. Fork PRs run in the fork's context by default (no secrets). `pull_request_target` and `workflow_run` change this.

---


## Card Exit

Classify the result, update evidence and attempted methods, record capability or risk changes, identify affected paths, and apply the return contract in [../module-continuity.md](../module-continuity.md).
