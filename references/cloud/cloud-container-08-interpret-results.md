# Cloud, Container, Kubernetes, And SaaS Operations: Interpret Results

> Apply [../module-continuity.md](../module-continuity.md). Inherit the engagement, parent path, current capability, evidence, authorization profile, and module stack. Do not initialize a separate workflow. Checkpoint material results and return them to the parent path before leaving this card.

## Interpret Results

Cloud testing requires careful interpretation:

- **AccessDenied vs NotFound**: AWS returns AccessDenied for both actual denial AND for resources that don't exist (to prevent enumeration). You need to distinguish: if you know a bucket name is valid and get AccessDenied → you know it exists.
- **Service Control Policy (SCP)**: Even an AdministratorAccess role may be restricted by an SCP at the AWS Organization level. When something should work but doesn't, check for SCPs.
- **Session policies**: `AssumeRole` can pass a session policy that restricts permissions below what the role grants.
- **Resource-based vs identity-based policy**: S3 bucket policies, KMS key policies, Lambda resource policies override/supplement IAM policies. Always check both.

---


## Card Exit

Classify the result, update evidence and attempted methods, record capability or risk changes, identify affected paths, and apply the return contract in [../module-continuity.md](../module-continuity.md).
