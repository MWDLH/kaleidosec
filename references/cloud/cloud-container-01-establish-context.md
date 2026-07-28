# Cloud, Container, Kubernetes, And SaaS Operations: Establish Context

> Apply [../module-continuity.md](../module-continuity.md). Inherit the engagement, parent path, current capability, evidence, authorization profile, and module stack. Do not initialize a separate workflow. Checkpoint material results and return them to the parent path before leaving this card.

## Establish Context

Record provider, tenant/account, subscription/project, region, current principal, authentication source (IAM user, role, service account, federated identity), active roles, resource inventory, network boundaries, logging configuration, and credential lifetime. For containers, record image, runtime, namespace, pod/task identity, mounts, capabilities, service account, metadata access, and control-plane reachability.

A cloud engagement has fundamentally different trust boundaries than an internal network. The attack surface is **API-driven**, **identity-centric**, and **automation-heavy**. Everything is software-defined — which means misconfiguration is the primary vulnerability class, not buffer overflows.

---


## Card Exit

Classify the result, update evidence and attempted methods, record capability or risk changes, identify affected paths, and apply the return contract in [../module-continuity.md](../module-continuity.md).
