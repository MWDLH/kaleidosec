# Code Audit Capability: Audit Workflow By Codebase Type

> Apply [../module-continuity.md](../module-continuity.md). Inherit the engagement, parent path, current capability, evidence, authorization profile, and module stack. Do not initialize a separate workflow. Checkpoint material results and return them to the parent path before leaving this card.

## Audit Workflow By Codebase Type

### Web Application (MVC / API)

1. **Start at the router/controller layer**: Map every HTTP endpoint → handler function
2. **Trace authentication/authorization**: Is auth middleware applied? Per-endpoint or per-route? Are there unauthenticated API endpoints near authenticated ones?
3. **For each handler**: Identify ALL user-controlled input sources (route params, query string, body, headers, cookies, uploaded files)
4. **Trace each input to its sinks**: Use IDE "Find Usages" / grep to follow the data flow. Does it go to a dangerous sink without validation?
5. **Prioritize**: Auth bypass > SQLi > Command Injection > SSRF > Deserialization > File operations > XSS

### Mobile Backend API (Same as Web but Check:)

- Token validation logic: is it JWT validation? (see JWT attack matrix in web-api)
- Mobile-specific endpoints: /api/v1 vs /api/v2 — version skew between mobile client and backend
- Hardcoded credentials in API client code (from mobile decompilation)

### Infrastructure-as-Code (Terraform / CloudFormation / Pulumi)

- **Hardcoded secrets**: `password = "..."`, `secret = "..."`, `access_key = "..."`, `private_key = "..."` in `.tf` files
- **Overly permissive IAM**: `actions = ["*"]`, `resources = ["*"]`, `effect = "Allow"` — combine all three → AdministratorAccess
- **Public resources**: `aws_s3_bucket_public_access_block`, `acl = "public-read"`, `"0.0.0.0/0"` in security groups
- **Missing encryption**: `encrypted = false`, `ssl_enforcement_enabled = false`
- **State file exposure**: `.tfstate` in S3 without encryption/versioning

---


## Card Exit

Classify the result, update evidence and attempted methods, record capability or risk changes, identify affected paths, and apply the return contract in [../module-continuity.md](../module-continuity.md).
