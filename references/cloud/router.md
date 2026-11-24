# Cloud, Container, Kubernetes, And SaaS Operations


## Continuity And Loading Rules

Read [../module-continuity.md](../module-continuity.md) before invoking a card. Keep one engagement state and one attack-path graph across all cards and domains.

1. Load entry and coverage cards first when they exist.
2. Load only the technical card supported by current evidence; do not enumerate cards as a checklist.
3. Keep the current parent path unless evidence creates a genuinely independent path.
4. Checkpoint before a domain transition and after a card returns material evidence.
5. When multiple domains cooperate, keep one primary domain and record supporting domains in state.

## Card Router

| Card | Load when evidence shows (field / response signature) | Must answer after loading |
|---|---|---|
| [Establish Context](cloud-container-01-establish-context.md) | Entry: no cloud provider, account, identity or control-plane model yet. | Which provider, account and identity are in scope, and what authority does it carry? |
| [Build The Surface — Practical First Steps](cloud-container-02-build-the-surface-practical-first-steps.md) | Cloud credential, role ARN, metadata reachability or console access obtained. | Which control-plane surfaces are reachable, and what is the cheapest first probe? |
| [Attack Primitives: Metadata Service](cloud-container-03-attack-primitives-metadata-service.md) | SSRF, container or workload that may reach link-local metadata (169.254.169.254 / fd00:ec2::254). | Is metadata reachable and does it yield credentials or identity? |
| [Attack Primitives: IAM Privilege Escalation](cloud-container-04-attack-primitives-iam-privilege-escalation.md) | Low-privilege cloud identity held; policies, roles or trust relationships readable. | Which IAM path escalates, and what is the minimum proof with rollback? |
| [Attack Primitives: Storage & Data Exposure](cloud-container-05-attack-primitives-storage-data-exposure.md) | Bucket, blob, object store or public URL discovered. | Is the object publicly or cross-tenant readable, and what sample proves it? |
| [Attack Primitives: Container Security](cloud-container-06-attack-primitives-container-security.md) | Inside a container, or evidence of `docker.sock`, privileged mode, hostPath mounts or weak isolation. | Which escape primitive is actually available, and what is its blast radius? |
| [Attack Primitives: Serverless](cloud-container-07-attack-primitives-serverless.md) | Function URL, event source, environment variables or execution role exposed. | Which function weakness yields data or execution, and what bounds it? |
| [Interpret Results](cloud-container-08-interpret-results.md) | After any material result, positive or negative. | What does this prove, and does it change the path ranking? |
| [Domain Transitions](cloud-container-09-domain-transitions.md) | Evidence implies a different domain, identity boundary, execution surface or network position. | Where are we now, what authority do we hold, and what is the return target? |
| [Recollect When](cloud-container-10-recollect-when.md) | New identity, privilege, asset, role, trust edge or network position. | What must be re-collected, and what evidence can be safely reused? |
