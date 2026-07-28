# CI/CD And Software Supply-Chain Operations: Attack Primitives: Registry & Deployment Attacks

> Apply [../module-continuity.md](../module-continuity.md). Inherit the engagement, parent path, current capability, evidence, authorization profile, and module stack. Do not initialize a separate workflow. Checkpoint material results and return them to the parent path before leaving this card.

## Attack Primitives: Registry & Deployment Attacks

### Container Registry

```bash
# Public Docker Hub
docker pull <org>/<image>:<tag>
docker history <org>/<image>:<tag> --no-trunc  # shows all layers and their build commands
# Check for: COPY of .env, hardcoded credentials in ENV, ADD of private keys

# AWS ECR
aws ecr describe-repositories
aws ecr list-images --repository-name <repo>
aws ecr get-login-password | docker login --username AWS --password-stdin <account>.dkr.ecr.<region>.amazonaws.com

# Azure ACR
az acr repository list --name <registry>
az acr repository show-tags --name <registry> --repository <repo>

# GCP GCR
gcloud container images list --repository=gcr.io/<project>
# Check for public access
```

### Deployment Access

If you compromise a CI/CD pipeline or registry, the deployment target is the next hop:

- **K8s deployment**: Can you push a modified image to the registry the cluster pulls from? Can you modify the deployment manifest (kubectl from pipeline)?
- **Serverless deployment**: Can you update Lambda/Cloud Function code? Your code runs as its IAM role.
- **VM/SSH deployment**: Does the pipeline use SSH keys or passwords to deploy? Extract from pipeline secrets/variables.
- **Configuration management**: Ansible/Chef/Puppet/Salt — pipeline has SSH keys to every managed host. One pipeline compromise = every managed host.

---


## Card Exit

Classify the result, update evidence and attempted methods, record capability or risk changes, identify affected paths, and apply the return contract in [../module-continuity.md](../module-continuity.md).
