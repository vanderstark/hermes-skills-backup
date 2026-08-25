# Advanced Kubernetes Security & Zero Trust — Materi Lanjutan

> **Target Audience:** Tim DevOps Datacenter 170-Server, AI Lab (GPU Server)  
> **Level:** Intermediate → Advanced (Setelah Kubernetes Container Orchestration dasar selesai)  
> **Estimasi Waktu:** 10–12 minggu (2 jam/hari, 5 hari/minggu)  
> **Prasyarat:** Sudah paham K8s dasar (pods, deployments, services, namespaces), kubectl, Linux security

---

## 🎯 Tujuan Pembelajaran

1. **CIS Kubernetes Benchmark** — audit & hardening
2. **Admission Control**: OPA Gatekeeper / Kyverno policies
3. **Service Mesh**: Istio mTLS, traffic encryption
4. **Zero Trust Network**: default-deny network policies
5. **Workload Identity**: SPIFFE/SPIRE, no static secrets
6. **RBAC hardening**: least-privilege, audit ClusterRoleBindings

---

## 📚 Roadmap 12 Minggu

### Minggu 1–3: Cluster Hardening & CIS Benchmark

| Hari | Topik | Praktik |
|------|-------|---------|
| 1–2 | **kube-bench**: CIS Benchmark automated audit | `kube-bench run --targets master,node` |
| 3–4 | **Control plane**: API server flags, etcd encryption | `--encryption-provider-config` |
| 5–6 | **kubelet**: anonymous auth disabled, read-only port closed | `/var/lib/kubelet/config.yaml` |
| 7–8 | **RBAC**: list all ClusterRoleBindings, find `cluster-admin` | `kubectl get clusterrolebindings -o json` |
| 9–10 | **Pod Security**: PSA (Pod Security Admission) enforce | `kubectl label ns --enforce=restricted` |
| 11–12 | Lab: **Harden 1-node K8s** (k3s/kind) ke CIS level 1 | Document semua perubahan |

**Deliverable Minggu 3:** `cis-hardening-report.pdf` — before/after score + remediations

---

### Minggu 4–6: Admission Control & Policy Engine

| Hari | Topik | Praktik |
|------|-------|---------|
| 1–2 | **Kyverno basics**: policy types (validate, mutate, generate) | `kubectl apply -f policy.yaml` |
| 3–4 | **OPA Gatekeeper**: Rego policy language | ConstraintTemplate + Constraint |
| 5–6 | **Image policies**: no `latest`, must from trusted registry | Kyverno `image` rule |
| 7–8 | **Privilege policies**: no `privileged`, no `hostPath` | Block `securityContext.privileged=true` |
| 9–10 | Lab: **10 policies** untuk namespace Polri | Enforce restricted + custom rules |
| 11–12 | **Policy testing**: `kyverno test` + CI integration | Block non-compliant deploys |

**Deliverable Minggu 6:** `kyverno-policies-pack.yaml` — 10 production-ready policies

---

### Minggu 7–8: Service Mesh & mTLS

| Hari | Topik | Praktik |
|------|-------|---------|
| 1–2 | **Istio install**: sidecar injection | `istioctl install --set profile=demo` |
| 3–4 | **mTLS strict mode**: encrypt all east-west traffic | `PeerAuthentication mtls: STRICT` |
| 5–6 | **AuthorizationPolicy**: service-to-service allowlist | Deny by default, allow explicit |
| 7–8 | **Traffic management**: canary, circuit breaker | VirtualService + DestinationRule |
| 9–10 | Lab: **Zero Trust mesh** untuk 3 microservice Polri | API → DB → Cache all mTLS |
| 11–12 | **Observability**: Kiali + Jaeger tracing | Visualize mTLS coverage |

**Deliverable Minggu 8:** `zero-trust-mesh.pdf` — architecture + mTLS coverage report

---

### Minggu 9–10: Network Policies & Micro-Segmentation

| Hari | Topik | Praktik |
|------|-------|---------|
| 1–2 | **Default-deny**: namespace isolation | `deny-all` NetworkPolicy |
| 3–4 | **Calico/Cilium**: CNI with policy engine | CiliumNetworkPolicy (L3-L7) |
| 5–6 | **Egress control**: limit outbound to known endpoints | Allow only `github.com`, `docker.io` |
| 7–8 | **DNS policies**: restrict DNS queries | Cilium `L7 DNS` policy |
| 9–10 | Lab: **Micro-segmentation** per unit (intelkam/reskrim/binmas) | Separate namespaces + policies |
| 11–12 | **Zero Trust Network Access (ZTNA)**: Cloudflare/Azure/BeyondCorp | External access via identity |

**Deliverable Minggu 10:** `network-segmentation.pdf` — namespace map + policy matrix

---

### Minggu 11–12: Workload Identity & Final Audit

| Hari | Topik | Praktik |
|------|-------|---------|
| 1–2 | **SPIFFE/SPIRE**: workload identity federation | `spire-server` + `spire-agent` |
| 3–4 | **No static secrets**: Vault CSI driver | Pod mounts secret via Vault |
| 5–6 | **External Secrets Operator**: sync from Vault/AWS | `ExternalSecret` resource |
| 7–8 | **Final CIS re-audit**: verify all fixes persist | `kube-bench` again |
| 9–10 | **Penetration test**: `cloud-k8s` skill authorized test | Verify no escape path |
| 11–12 | Report + presentasi ke tim DevOps & direktur | `docs-generator` |

**Deliverable Minggu 12:**  
- `K8S_ZERO_TRUST_REPORT.pdf`  
- `spire-deployment.yaml` + `vault-csi-config`  
- Live demo: pod-to-pod mTLS + denied egress

---

## 🛠️ Toolchain Wajib Diinstall

```bash
# CIS Benchmark
curl -L https://github.com/aquasecurity/kube-bench/releases/latest/download/kube-bench_*.deb -o kube-bench.deb
dpkg -i kube-bench.deb

# Policy Engine
kubectl apply -f https://github.com/kyverno/kyverno/releases/latest/download/install.yaml
kubectl apply -f https://raw.githubusercontent.com/open-policy-agent/gatekeeper/master/deploy/gatekeeper.yaml

# Service Mesh
curl -L https://istio.io/downloadIstio | sh
istioctl install --set profile=demo

# CNI with policy
kubectl apply -f https://raw.githubusercontent.com/cilium/cilium-cli/main/install.yaml
cilium install

# Secrets
helm repo add hashicorp https://helm.releases.hashicorp.com
helm install vault hashicorp/vault

# Workload Identity
helm install spire-crds spire/spire-crds
helm install spire spire/spire

# Local cluster for lab
curl -sfL https://get.k3s.io | sh -  # or: kind create cluster
```

---

## 📂 File Referensi Penting (dari Skill Asli)

| File | Path | Kegunaan |
|------|------|----------|
| K8s Cloud Checklist | `security/reverse-skill/cloud-k8s/references/k8s-cloud-checklist.md` | Full audit list |
| Cloud K8s Workflow | `security/reverse-skill/cloud-k8s/SKILL.md` | RBAC, secrets, admission |
| Supply Chain Security | `security/supply-chain-security/SKILL.md` | Image/SBOM/CI |
| MLOps Serving | `mlops/inference/serving-llms-vllm/references/server-deployment.md` | vLLM on K8s |

---

## 🎯 Use Case Polri (Khusus)

| Unit | Namespace | Isolation Requirement |
|------|-----------|----------------------|
| **Intelkam** | `intelkam` | No egress to public, only internal SIEM |
| **Reskrim** | `reskrim` | Restricted PV, encrypted etcd |
| **Binmas** | `binmas` | Public ingress via ZTNA only |
| **Sabhara** | `sabhara` | High-availability, no downtime |
| **Lantas** | `lantas` | ANPR workload, GPU node affinity |

**Key Principle:** Default-deny everything. Explicit allow per service. Workload identity (SPIFFE) bukan IP/secret.

---

## ✅ Checklist Kelulusan (Harus Semua ✅)

- [ ] **kube-bench** CIS score ≥ 90% (remediate all critical/high)
- [ ] Deploy **Kyverno** dengan 10 production policies (enforced)
- [ ] Deploy **Istio mTLS STRICT** untuk 3 microservice
- [ ] Implement **default-deny NetworkPolicy** + per-namespace allowlist
- [ ] Setup **SPIRE** workload identity (no static K8s secrets)
- [ ] Integrate **Vault CSI** untuk secret mounting
- [ ] **Micro-segmentation** 5 unit namespaces
- [ ] Authorized **penetration test** via `cloud-k8s` → no escape path
- [ ] Presentasi live demo (mTLS + denied egress)

---

## 🚀 Next Steps Setelah Selesai

1. **Confidential Computing**: TEE (Intel SGX) untuk sensitive workload
2. **eBPF Security**: Cilium Tetragon runtime detection
3. **GitOps Security**: ArgoCD with signed commits
4. **Multi-Cluster Zero Trust**: federation antar DC (170-server)
5. **LLM Serving Security**: vLLM pod hardening (koneksi LLM Security)

---

## 📎 Referensi Eksternal

- CIS Kubernetes Benchmark: https://www.cisecurity.org/benchmark/kubernetes
- Kyverno: https://kyverno.io/
- OPA Gatekeeper: https://open-policy-agent.github.io/gatekeeper/
- Istio: https://istio.io/
- Cilium: https://cilium.io/
- SPIFFE/SPIRE: https://spiffe.io/
- Vault: https://www.vaultproject.io/
- Kube-bench: https://github.com/aquasecurity/kube-bench
- BeyondCorp (Google): https://cloud.google.com/beyondcorp
