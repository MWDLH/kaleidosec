# CI/CD And Software Supply-Chain Operations: Build The Surface — Practical Enumeration

> Apply [../module-continuity.md](../module-continuity.md). Inherit the engagement, parent path, current capability, evidence, authorization profile, and module stack. Do not initialize a separate workflow. Checkpoint material results and return them to the parent path before leaving this card.

## Build The Surface — Practical Enumeration

### Source Repository Reconnaissance

```bash
# GitHub organization/discovery
gh org list                                          # orgs linked to your token
gh repo list <org> --limit 200 --json name,visibility,isFork,defaultBranch
gh api /orgs/<org>/repos --paginate -q '.[].full_name'

# Find sensitive files in repos (if you have access or repo is public)
# Search for:
# - .pem, .key, .pfx, .p12 (private keys)
# - .env, .env.*, appsettings.*.json, secrets.* (config with credentials)
# - terraform.tfstate, .tfstate (Terraform state)
# - .npmrc, .pypirc, .docker/config.json (package registry credentials)
# - id_rsa, id_ed25519 (SSH keys)
# - Jenkinsfile, .github/workflows/*.yml, .gitlab-ci.yml (CI/CD definitions)
# - .git-credentials, .netrc (stored git credentials)
# - connectionStrings, DB_PASSWORD, API_KEY (secrets in code)

# GitHub dorking examples (even for repos you don't have access to):
# org:<target> filename:.env
# org:<target> filename:.npmrc
# org:<target> "password" language:yaml
# org:<target> "BEGIN RSA PRIVATE KEY"
# org:<target> path:.github/workflows/
```

### CI/CD Pipeline Discovery

```bash
# GitHub Actions
ls -la .github/workflows/
cat .github/workflows/*.yml

# What to look for in workflow YAML:
# 1. Trigger: pull_request_target? (dangerous — runs in context of BASE repo)
# 2. Secrets referenced: ${{ secrets.DEPLOY_KEY }}, ${{ secrets.AWS_ACCESS_KEY_ID }}
# 3. Checkout: actions/checkout with ref: ${{ github.event.pull_request.head.ref }} (untrusted input)
# 4. Script injection: run: echo "${{ github.event.issue.title }}" (untrusted input in shell)
# 5. Workflow_run: triggered by another workflow — what identity does it run as?
# 6. Environment: environment: production — which protection rules apply?
# 7. OIDC: uses: aws-actions/configure-aws-credentials with role-to-assume → can you assume that role?

# GitLab CI
cat .gitlab-ci.yml
# Check: include: directives (remote files?), variables:, before_script:, services:

# Jenkins (if you have access to Jenkins instance)
# /script (Groovy script console — if accessible, full RCE on Jenkins master)
# /job/<name>/config.xml (job configuration, may contain credentials)
# /credentials/store/system/domain/_/ (credential store)
```

---


## Card Exit

Classify the result, update evidence and attempted methods, record capability or risk changes, identify affected paths, and apply the return contract in [../module-continuity.md](../module-continuity.md).
