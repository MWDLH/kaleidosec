# CI/CD And Software Supply-Chain Operations: Domain Transitions

> Apply [../module-continuity.md](../module-continuity.md). Inherit the engagement, parent path, current capability, evidence, authorization profile, and module stack. Do not initialize a separate workflow. Checkpoint material results and return them to the parent path before leaving this card.

## Domain Transitions

- **→ cloud**: For federated OIDC identities, cloud-hosted CI/CD runners, deployment targets
- **→ Web/API**: For registry web UIs, Git webhooks, CI/CD dashboards
- **→ code-audit**: For build scripts, custom CI/CD logic, Infrastructure-as-Code analysis
- **→ internal/AD**: For self-hosted runners on domain-joined hosts, hybrid deployment pipelines
- **→ container**: For container image analysis, registry access, K8s deployment pipelines


## Main Attack Chain

1. **Repository identity**: What access does the current principal have? Read-only? Write? Can it modify workflow definitions? Can it create branches/PRs?
2. **Pipeline trigger and identity**: What triggers a pipeline run? What identity does the pipeline execute as? (Repository secrets, OIDC-federated cloud role, self-hosted runner context.)
3. **Secrets and runner access**: Can pipeline code access secrets? Can it reach the runner's filesystem or network? Ephemeral runner or persistent?
4. **Artifact to deployment**: Does the pipeline produce artifacts (container images, packages, binaries)? Where are they stored? Who can pull them? Are they signed?
5. **Deployment identity to target**: The deployment step uses an identity (cloud IAM role, service account, SSH key) to push to production. That identity is the final target — what does it have access to?
6. **Return to cloud or internal**: Supply-chain paths almost always end in cloud credentials or internal network access. Transition with the exact credential, trust condition, and deployment target.

## Transition Handoff

Carry the repository, project, pipeline and run, effective principal or token reference, runner context, artifact or image digest, registry and deployment target, identity trust conditions, observed capability, and the exact cloud, code, container, Web, or internal question.

## Card Exit

Classify the result, update evidence and attempted methods, record capability or risk changes, identify affected paths, and apply the return contract in [../module-continuity.md](../module-continuity.md).
