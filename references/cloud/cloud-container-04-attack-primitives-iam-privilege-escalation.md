# Cloud, Container, Kubernetes, And SaaS Operations: Attack Primitives: IAM Privilege Escalation

> Apply [../module-continuity.md](../module-continuity.md). Inherit the engagement, parent path, current capability, evidence, authorization profile, and module stack. Do not initialize a separate workflow. Checkpoint material results and return them to the parent path before leaving this card.

## Attack Primitives: IAM Privilege Escalation

The core question: **"With the permissions I have right now, can I grant myself more permissions?"**

### Authorization And Action Levels

| Level | Scope | Examples |
|---|---|---|
| **L0/L1 — Read-only enumeration and path modeling** | Enumerate policies, roles, trust relationships, and effective permissions; model escalation paths | `iam:ListAttachedUserPolicies`, `iam:GetPolicyVersion`, `iam:ListRoles`, `iam:SimulatePrincipalPolicy`; Azure role assignment listing; GCP `projects.getIamPolicy` |
| **L2 — Controlled proof without persistent control** | Assume a role if the trust policy allows; generate a temporary credential via an approved pathway; validate that a modeled path reaches an expected identity | `sts:AssumeRole` into an allowed role; use a short-lived token to confirm its effective permissions — do not create durable keys, modify trust, or change resource policies |
| **L3 — Permission, trust policy, role binding, key, workload, or control-plane changes** | Any action that creates, modifies, or deletes IAM entities, trust relationships, role definitions, resource policies, or durable credentials | All `Create*`, `Update*`, `Put*`, `Attach*`, `Detach*`, `Delete*` on IAM resources; key creation; trust policy modification; role definition writes |

Default behavior: first output reachable escalation paths and their missing prerequisites. Do not execute IAM changes unless the authorization profile explicitly approves L3 actions for the current target.

---

### AWS IAM Escalation Paths

Each path answers: "I can do action X, and that lets me do action Y, which eventually gives me AdministratorAccess." The path is only valid when the target resource, companion action, permission boundary, explicit deny, SCP, and execution identity all align.

| I Have Permission To... | Escalation Path | Prerequisites And Constraints |
|---|---|---|
| `iam:CreatePolicyVersion` (which can set the new version as default via `--set-as-default`) OR `iam:SetDefaultPolicyVersion` (which switches to an existing version) | `CreatePolicyVersion` can create a new version and set it as the default in one call; `SetDefaultPolicyVersion` switches the default to an already-existing version. Both can escalate if they change the effective policy on the calling principal. | The policy must be attached to the calling principal. A permissions boundary on the principal may limit the effective scope. SCPs at the organization level may also deny the expanded actions. The two permissions are distinct paths — having only one is sufficient for that path. |
| `iam:AttachUserPolicy` / `iam:AttachRolePolicy` | Attach `AdministratorAccess` or another privileged managed policy to the calling principal | The calling principal must have `iam:AttachUserPolicy` or `iam:AttachRolePolicy` scoped to itself. Permissions boundary, SCP, and explicit denies in the target policy still apply. |
| `iam:AddUserToGroup` | Add the calling user to an existing privileged group | Requires that the target group actually has privileged policies attached. Group membership changes are logged and visible. |
| `iam:CreateAccessKey` | Create an access key for another IAM user with higher privileges | The target user must exist and must not already have the maximum access keys (default 2). Permissions boundary and SCP on the target user still apply to the stolen key. |
| `iam:CreateLoginProfile` | Create a console password for an IAM user that currently has no console access | The target user must exist and must not already have a login profile. Console access may be further restricted by IP-based IAM policy conditions. |
| `iam:UpdateAssumeRolePolicy` | Modify a role's trust policy to allow the calling principal (or a controlled principal) to assume it | The role must have privileged permissions beyond what the caller already has. After trust modification, `sts:AssumeRole` must succeed — the caller needs both actions. The target role's permissions boundary, SCP, and session policy on assume still constrain the result. |
| `iam:PassRole` + `ec2:RunInstances` | Pass a privileged role to a new EC2 instance; access the instance and retrieve its credentials from IMDS | Requires: ability to launch EC2 (including AMI, subnet, security group selection), ability to reach the instance afterward (SSH or SSM), and the instance profile role having higher privileges. The passed role must be in the same account. IMDS version (v1 vs v2) affects credential retrieval. |
| `iam:PassRole` + `lambda:CreateFunction` or `lambda:UpdateFunctionCode` | Pass a privileged execution role to a Lambda function; trigger the function with attacker code | Requires: ability to create or update a Lambda, the passed role must be a Lambda execution role, the function must be invocable afterward, and CloudWatch Logs or direct output must be reachable to read results. |
| `sts:AssumeRole` | Assume an existing privileged role if the trust policy already allows it | The trust policy must include the calling principal (or a broad enough condition). Assumed-role sessions are temporary (15min–12h). A session policy passed during assume can further restrict permissions. |
| `cloudformation:CreateStack` / `cloudformation:UpdateStack` | Deploy or update a stack that creates, modifies, or assumes a privileged IAM role | When a service role is specified, `iam:PassRole` is required and permissions are constrained by that role. When no service role is specified, CloudFormation may use the caller's temporary credentials. Verify which identity the stack actually executes under before assuming the modeled permissions are available. |
| `ssm:SendCommand` + target discovery | Execute commands on an SSM-managed EC2 instance; from that execution context, test whether IMDS exposes a higher-privilege instance role | The caller needs `ssm:SendCommand` on the target and access to the document used. The instance must be managed by SSM. Instance-role capability is not inherited automatically: an instance profile must exist, IMDS must be reachable from the process context, and the returned credentials must have useful permissions. |

**Enumeration before escalation**:
```bash
aws iam list-attached-user-policies --user-name <user>
aws iam list-attached-role-policies --role-name <role>
aws iam get-policy-version --policy-arn <arn> --version-id <v1>
aws iam list-roles --query "Roles[?AssumeRolePolicyDocument.Statement[?Principal.AWS && contains(Principal.AWS, '<your_arn>')]].RoleName"
aws iam get-user-policy --user-name <user> --policy-name <policy>
aws iam simulate-principal-policy --policy-source-arn <arn> --action-names <actions>
```

**Output paths before executing**: For each modeled escalation, record the action chain, the missing prerequisites, the permissions boundary and SCP applicable at the target, and whether the final effective identity exceeds the current. Do not execute IAM write actions without L3 authorization.

---

### Azure IAM Escalation Patterns

Azure role assignments combine an RBAC role definition (Owner, Contributor, Reader, or custom) with a scope (Management Group → Subscription → Resource Group → Resource). Role-assignment permission at a scope normally applies to that scope and descendants, not to a parent scope. Separate Azure RBAC roles from Entra ID directory roles — they control different planes.

| I Have... | Escalation | Prerequisites And Constraints |
|---|---|---|
| `Microsoft.Authorization/roleAssignments/write` | Assign an available role to a principal at the authorized scope or a descendant | Verify the permission at the exact assignment scope; permission on a resource group does not permit assignment at the parent subscription. PIM may require activation, deny assignments may block the result, and the caller also needs access to the selected role definition. |
| `Microsoft.Authorization/roleDefinitions/write` | Create or modify a custom role definition with expanded actions | Custom role creation scope matters — a role created at subscription scope can be assigned across that subscription. Built-in roles cannot be modified. |
| `Microsoft.Web/sites/.../publishxml` or `Microsoft.Web/sites/.../listPublishingCredentials` | Download publishing profile for a Function App or Web App | The publishing credentials grant deployment access; whether they also grant access to the app's managed identity depends on whether the identity is system-assigned and the credential type. Test the managed identity endpoint from the app context, not just from the credential alone. |
| Runbook with `Contributor` on automation account + runbook edit permission | Modify runbook code; execution runs as the automation account's managed identity or Run As account | Runbook execution identity may differ from the editor's identity. Check whether the runbook's Run As account or managed identity has broader permissions. |
| `Microsoft.KeyVault/vaults/accessPolicies/write` | Add a principal to a Key Vault access policy | This applies only to the legacy access-policy model. RBAC-based vaults use `Microsoft.Authorization/roleAssignments/write` at the vault or descendant scope; verify that the chosen role actually grants the required data-plane action. |
| VM `runCommand` or `Microsoft.Compute/virtualMachines/runCommand/action` | Execute a script on the VM as SYSTEM (Windows) or root (Linux) | If the VM has a managed identity, the script can request an IMDS token for that identity. Access the token and test its effective permissions against Azure Resource Manager or other services. |

**Key distinction**: Azure RBAC roles control Azure Resource Manager. Entra ID directory roles control the identity platform (user/group/application management). A principal with Entra ID `Global Administrator` can escalate to Azure RBAC `User Access Administrator` by elevating access in Entra ID → Azure resource management.

---

### GCP IAM Escalation

GCP IAM grants permissions through Allow policies. IAM Deny policies, Principal Access Boundaries, organization policy constraints, and service-specific controls can all restrict what a principal can actually do. Service accounts are both principals and resources — the key vectors are impersonation and key material access. Organization Policy is not equivalent to IAM Deny — each has distinct constraints and evaluation semantics.

| I Have... | Escalation | Prerequisites And Constraints |
|---|---|---|
| `iam.serviceAccounts.getAccessToken` | Generate a short-lived OAuth 2.0 access token for a target service account — effectively impersonate that account | The token is scoped to the permissions of that service account. Check: which roles are granted to the service account? Does the service account have organization-level policy constraints? Token lifetime is typically 1 hour. |
| `iam.serviceAccountKeys.create` | Create a long-lived JSON key for a service account — persistent access outside the current session | Key creation is audited (audit log: `google.iam.admin.v1.CreateServiceAccountKey`). The key is a durable credential that survives the current engagement context. Classify as L3. |
| `iam.roles.update` | Modify an existing custom role to add permissions | Only custom roles can be modified; predefined roles are immutable. The role must be at a scope where you have this permission. Changes take effect for all principals bound to that role. Classify as L3. |
| `iam.serviceAccounts.setIamPolicy` | Modify the IAM policy on a service account — grant yourself or a controlled principal the ability to impersonate it or create keys | This is a control-plane change equivalent to rewriting trust. Classify as L3. |
| `cloudbuild.builds.create` + ability to specify a service account | Trigger a Cloud Build that runs as a higher-privilege service account | The build runs with the permissions of the specified service account. Check whether the build output, logs, or resulting artifacts are reachable to exfiltrate results. |
| `cloudfunctions.functions.update` or `cloudfunctions.functions.create` | Modify a Cloud Function's code; it executes as its runtime service account | The runtime service account may have permissions beyond those of the caller. Test the function's effective permissions after update. |

**Resource-level IAM and policy constraints**: GCP allows IAM policies at the organization, folder, project, and resource level. Effective access is the intersection of Allow policies, IAM Deny policies, Principal Access Boundaries, organization policy constraints, and resource-level controls. Check each layer: IAM Deny policies can explicitly block permissions; organization policies enforce specific constraints (not all organization policies function as denies); service account OAuth scopes limit token capability regardless of IAM roles. Verify actual API call results rather than relying on policy simulation alone.

---

### Failure Interpretation

| Failure Signal | Possible Cause | Next Action |
|---|---|---|
| API returns `AccessDenied` / `403` | Permission not granted, SCP/org policy denies, resource-level policy blocks, or the resource does not exist (AWS AccessDenied can mean either) | Test the same action on a resource known to exist; test with a different action to distinguish permission denial from resource existence |
| `iam:SimulatePrincipalPolicy` returned `allowed` but the actual call was denied | Permissions boundary, SCP, session policy, or resource-level policy not modeled by the simulator | Re-evaluate permissions boundary and explicit denies; check the full policy evaluation chain |
| Trust policy modified but `AssumeRole` still fails | Trust policy propagation delay (typically seconds but can be longer with eventual consistency); external ID or condition mismatch; session policy restriction | Wait and retry with exponential backoff (5s, 15s, 30s); verify every condition key (sts:ExternalId, SourceIdentity, etc.) matches |
| Action succeeded (role created, policy attached, key generated) but the resulting identity does not have the expected permissions | Permissions boundary on the principal; SCP at the organization/account level; inline policy not merged as expected; resource-level policy on the target resource | AWS: cross-check identity policies, resource policies, permissions boundary, session policies, and SCP — simulation results are one input, not conclusive. Azure: check effective role assignments at the current scope, deny assignments, PIM activation state, and data-plane permissions. GCP: check resource IAM policies, Deny policies, organization constraints, and verify with actual API calls. |
| Resource not found during escalation attempt | Resource ARN/name incorrect, resource in different account/region/subscription/project, or resource was deleted | Verify the resource path against the current provider context before escalating |
| Higher-level restriction blocks the action | AWS SCP or resource deny, Azure deny assignment/policy effect, or GCP IAM Deny/PAB/service-specific organization constraint applies | Identify the provider-specific control and its scope. Treat it as a hard stop only for actions actually covered by that control; do not generalize one denied action to the entire account, subscription, or project. |


## Card Exit

Classify the result, update evidence and attempted methods, record capability or risk changes, identify affected paths, and apply the return contract in [../module-continuity.md](../module-continuity.md).
