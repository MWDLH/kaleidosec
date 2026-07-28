# Cloud, Container, Kubernetes, And SaaS Operations: Attack Primitives: Storage & Data Exposure

> Apply [../module-continuity.md](../module-continuity.md). Inherit the engagement, parent path, current capability, evidence, authorization profile, and module stack. Do not initialize a separate workflow. Checkpoint material results and return them to the parent path before leaving this card.

## Attack Primitives: Storage & Data Exposure

### S3 Bucket / Azure Blob / GCS Bucket Discovery

The most common cloud finding. A misconfigured bucket with public read or write access.

```bash
# S3 — manual check
aws s3 ls s3://<bucket-name> --no-sign-request
curl http://<bucket-name>.s3.amazonaws.com/                     # public read check
curl http://<bucket-name>.s3.amazonaws.com/ --upload-file x.txt # public write check

# S3 — predictable names
# <company>-backup, <company>-data, <company>-logs, <company>-static, <company>-dev, <company>-terraform, <company>-cloudformation
# <product>-media, <product>-uploads, <product>-export, <product>-cdn
# Test these against discovered company/product names.

# Azure Blob — manual check
curl "https://<storageaccount>.blob.core.windows.net/<container>?restype=container&comp=list"

# GCP — manual check
curl "https://storage.googleapis.com/<bucket-name>"
gsutil ls gs://<bucket-name>

# Common file types to look for in exposed buckets:
# *.tfstate (Terraform state — full infrastructure config + secrets)
# *.pem, *.ppk (private keys)
# *.sql, *.dump, *.bak, *.mdb (database backups)
# .env, .env.* (environment files with credentials)
# *.log (application logs — may contain tokens, credentials in query strings)
# cloudformation/*, cfn/* (CloudFormation templates with parameters)
# kubeconfig, .kube/config (Kubernetes credentials)
# id_rsa, authorized_keys (SSH keys inadvertently backed up)
# credentials, credentials.csv (AWS credential exports)
```

---


## Card Exit

Classify the result, update evidence and attempted methods, record capability or risk changes, identify affected paths, and apply the return contract in [../module-continuity.md](../module-continuity.md).
