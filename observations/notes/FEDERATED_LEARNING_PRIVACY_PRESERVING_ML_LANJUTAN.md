# Federated Learning & Privacy-Preserving ML — Materi Lanjutan

> **Target Audience:** Tim AI Lab Polri (GPU Server), 5 Unit (Intelkam, Reskrim, Binmas, Sabhara, Lantas)  
> **Level:** Intermediate → Advanced (Setelah MLOps Advanced selesai)  
> **Estimasi Waktu:** 10–12 minggu (2 jam/hari, 5 hari/minggu)  
> **Prasyarat:** Sudah paham PyTorch, vLLM serving, distributed training, W&B tracking

---

## 🎯 Tujuan Pembelajaran

1. **Federated Learning** architecture (centralized, decentralized, hierarchical)
2. **Flower/PySyft** framework untuk multi-node training
3. **Secure Aggregation** — hanya weights yang dikirim, data tetap lokal
4. **Differential Privacy** — noise injection untuk privacy guarantee
5. **Split Learning** — model terpisah antar party (no raw data exchange)
6. **Privacy attack defense**: gradient inversion, membership inference

---

## 📚 Roadmap 12 Minggu

### Minggu 1–3: Federated Learning Fundamentals

| Hari | Topik | Praktik |
|------|-------|---------|
| 1–2 | **FL architecture**: FedAvg, FedProx, FedOpt | Diagram client-server topology |
| 3–4 | **Flower setup**: server + 3 client simulasi | `pip install flwr`, `flwr example` |
| 5–6 | **Local training**: client train on local data | PyTorch `train()` loop per client |
| 7–8 | **Aggregation**: weighted average of weights | Server `aggregate_fit()` |
| 9–10 | **Communication**: gRPC / WebSocket between nodes | `flwr.client` + `flwr.server` |
| 11–12 | Lab: **3 polsek simulasi** FL untuk klasifikasi teks kejahatan | Dataset lokal per polsek (no centralization) |

**Deliverable Minggu 3:** `fl-sim-3node.pdf` — arsitektur + hasil akurasi terdistribusi

---

### Minggu 4–6: Privacy-Preserving Techniques

| Hari | Topik | Praktik |
|------|-------|---------|
| 1–2 | **Differential Privacy**: ε, δ, Gaussian noise | `opacus` library |
| 3–4 | **DP-SGD**: clip gradient + noise | `dp_model = PrivacyEngine()` |
| 5–6 | **Secure Aggregation**: masked client updates | Crypto primitive (SecAgg) |
| 7–8 | **Split Learning**: cut layer = no raw exchange | Client A (bottom) → Server (top) |
| 9–10 | **Homomorphic Encryption** (intro): compute on ciphertext | `tenseal` Pyfhel |
| 11–12 | Lab: **DP-FedAvg** dengan ε=1.0, δ=1e-5 | Banding akurasi vs privacy cost |

**Deliverable Minggu 6:** `privacy-tradeoff.pdf` — ε vs accuracy curve + recommendation

---

### Minggu 7–8: Advanced FL & Attack Defense

| Hari | Topik | Praktik |
|------|-------|---------|
| 1–2 | **Gradient Inversion Attack**: reconstruct input dari gradien | `DLG` / `iDLG` attack demo |
| 3–4 | **Membership Inference**: deteksi apakah data di training set | Shadow model attack |
| 5–6 | **Model Poisoning**: malicious client update | Byzantine-robust aggregation (Krum, TrimmedMean) |
| 7–8 | **Backdoor Attack**: trigger pattern di FL | Defend: anomaly detection on updates |
| 9–10 | Lab: **Robust aggregation** dengan Krum vs FedAvg | Compare under 20% malicious clients |
| 11–12 | **Federated Evaluation**: lm-eval-harness di FL context | Benchmark global model |

**Deliverable Minggu 8:** `fl-security-report.pdf` — 4 attack PoC + defense effectiveness

---

### Minggu 9–10: Production FL Infrastructure

| Hari | Topik | Praktik |
|------|-------|---------|
| 1–2 | **Kubernetes FL**: Flower on K8s with 170-server DC | `flwr/k8s` Helm chart |
| 3–4 | **GPU server integration**: H100 as aggregator | `flwr.server` on `192.168.147.179` |
| 5–6 | **TLS/mTLS**: secure communication antar node | Certificates via SPIFFE |
| 7–8 | **Monitoring**: W&B for FL rounds | Log per-client metrics |
| 9–10 | Lab: **Cross-polsek FL** dengan 5 unit sebagai client | Intelkam+Reskrim+Binmas+Sabhara+Lantas |

**Deliverable Minggu 10:** `fl-prod-architecture.pdf` — K8s topology + mTLS + monitoring

---

### Minggu 11–12: Final Project & Compliance

| Hari | Topik | Praktik |
|------|-------|---------|
| 1–2 | **Regulation mapping**: UU PDP, GDPR-style constraints | Privacy law untuk data Polri |
| 3–4 | **Audit trail**: who trained what, when | Blockchain/append-only log |
| 5–6 | **Final project**: FL untuk **deteksi modus kejahatan** lintas unit | 5 clients, DP-enabled, robust agg |
| 7–8 | **Presentation**: demo distributed training | Live: 5 nodes → global model |
| 9–10 | Report + handover ke tim keamanan | `docs-generator` |
| 11–12 | Retrospective & next step (Federated LLM?) | Roadmap 6 bulan |

**Deliverable Minggu 12:**  
- `fl-final-model.bin` (global model)  
- `FL_COMPLETION_REPORT.pdf`  
- Live demo: 5-polsek training

---

## 🛠️ Toolchain Wajib Diinstall

```bash
# Federated Learning
pip install flwr flwr-datasets
pip install pysyft  # alternative framework

# Differential Privacy
pip install opacus
pip install tensorflow-privacy

# Secure Computation
pip install tenseal  # HE
pip install Pyfhel

# FL on K8s
helm repo add flwr https://flwr.ai/helm
helm install flwr flwr/flwr

# Monitoring (dari MLOps skill)
pip install wandb

# Attack simulation
pip install membership-inference  # research
```

---

## 📂 File Referensi Penting (dari Skill Asli)

| File | Path | Kegunaan |
|------|------|----------|
| Benchmark Guide | `mlops/evaluation/evaluating-llms-harness/references/benchmark-guide.md` | Eval methodology |
| HF Hub | `mlops/huggingface-hub/SKILL.md` | Model distribution |
| W&B Sweeps | `mlops/evaluation/weights-and-biases/references/sweeps.md` | Hyperparam tuning |
| vLLM Deploy | `mlops/inference/serving-llms-vllm/references/server-deployment.md` | Serving global model |

---

## 🎯 Use Case Polri (Khusus)

| Unit | Data Lokal | FL Contribution |
|------|------------|----------------|
| **Intelkam** | OSINT reports, threat actor profiles | Global threat model |
| **Reskrim** | Case files, modus operandi | Crime pattern detector |
| **Binmas** | Community reports, sentiment | Social stability predictor |
| **Sabhara** | Patrol logs, incident reports | Resource allocation optimizer |
| **Lantas** | Violation records, ANPR data | Traffic violation predictor |

**Key Benefit:** Data tidak pernah keluar polsek → **UU PDP compliant**. Hanya *model weights* (encrypted) yang dikirim ke server pusat (GPU H100).

---

## ✅ Checklist Kelulusan (Harus Semua ✅)

- [ ] Deploy **Flower FL** dengan 3-node simulation (local)
- [ ] Implement **DP-SGD** dengan ε ≤ 1.0, δ ≤ 1e-5
- [ ] Demonstrasikan **gradient inversion attack** + defense
- [ ] Implement **robust aggregation** (Krum) under 20% malicious
- [ ] Deploy **FL on K8s** dengan mTLS
- [ ] Train **cross-polsek model** (5 units) dengan DP
- [ ] Map ke **UU PDP** compliance checklist
- [ ] Presentasi live demo 5-node training

---

## 🚀 Next Steps Setelah Selesai

1. **Federated LLM**: fine-tune Indo-LLaMA secara terdistribusi (FL + LoRA)
2. **Secure Multi-Party Computation**: beyond DP, cryptographic guarantee
3. **Confidential Computing**: TEE (Intel SGX, AMD SEV) untuk FL node
4. **MLOps Security**: model signing untuk FL updates (koneksi LLM Security)
5. **Cross-Agency FL**: Polri + pemda (with consent) untuk smart city

---

## 📎 Referensi Eksternal

- Flower: https://flower.ai/docs/
- PySyft: https://github.com/OpenMined/PySyft
- Opacus (DP): https://opensource.facebook.com/projects/opacus/
- Google DP: https://github.com/google/differential-privacy
- SecAgg: https://arxiv.org/abs/1706.04138
- FedML: https://github.com/FedML-AI/FedML
- UU PDP Indonesia: https://www.dpr.go.id/dokjdih/document/uu/UU_2022_27.pdf
