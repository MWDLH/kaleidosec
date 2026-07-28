# Cloud, Container, Kubernetes, And SaaS Operations: Build The Surface — Practical First Steps

> Apply [../module-continuity.md](../module-continuity.md). Inherit the engagement, parent path, current capability, evidence, authorization profile, and module stack. Do not initialize a separate workflow. Checkpoint material results and return them to the parent path before leaving this card.

## Build The Surface — Practical First Steps

### Step 1: Who Am I?

```bash
# AWS
aws sts get-caller-identity
aws iam list-account-aliases
aws configure list

# Azure
az account show
az ad signed-in-user show
az account list --query "[].{Name:name, ID:id, Default:isDefault}"

# GCP
gcloud auth list
gcloud config list project
gcloud auth print-identity-token 2>/dev/null
```

### Step 2: What Can I See?

```bash
# AWS — core inventory
aws ec2 describe-instances --query 'Reservations[*].Instances[*].[InstanceId,State.Name,PrivateIpAddress,PublicIpAddress,IamInstanceProfile,Tags]'
aws iam list-users --query 'Users[*].[UserName,UserId,CreateDate,PasswordLastUsed]'
aws iam list-roles --query 'Roles[*].[RoleName,Arn]'
aws s3 ls
aws rds describe-db-instances
aws lambda list-functions

# Azure
az vm list --query "[].{Name:name, RG:resourceGroup, Location:location}"
az storage account list --query "[].{Name:name, RG:resourceGroup, TLS:enableHttpsTrafficOnly}"
az keyvault list --query "[].{Name:name, RG:resourceGroup}"

# GCP
gcloud compute instances list
gcloud storage buckets list
gcloud sql instances list
gcloud functions list
```

### Step 3: What Trusts What?

Cloud privilege escalation is rarely about binary exploitation. It's about **finding a path from your current identity to a higher-privileged identity through IAM policy chains**.

---


## Card Exit

Classify the result, update evidence and attempted methods, record capability or risk changes, identify affected paths, and apply the return contract in [../module-continuity.md](../module-continuity.md).
