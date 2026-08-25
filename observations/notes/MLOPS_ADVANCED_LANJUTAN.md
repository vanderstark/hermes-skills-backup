# Machine Learning Operations (Advanced) — Materi Lanjutan

> **Target Audience:** Tim AI Lab Polri (GPU Server), OSINT Lab, Akademi  
> **Level:** Intermediate → Advanced (Setelah MLOps GPU Server & vLLM dasar selesai)  
> **Estimasi Waktu:** 10–12 minggu (2 jam/hari, 5 hari/minggu)  
> **Prasyarat:** Sudah deploy vLLM serving, paham PyTorch, GPU server NVIDIA (A100/H100)

---

## 🎯 Tujuan Pembelajaran

1. **Benchmark LLM** secara ilmiah pakai **lm-evaluation-harness**
2. **Experiment tracking** profesional pakai **Weights & Biases**
3. **Hyperparameter sweep** otomatis & kolaboratif
4. **Model registry & versioning** untuk produksi
5. **CI/CD MLOps** dengan GitHub Actions + model validation
6. **Performance optimization**: PagedAttention, tensor parallelism, quantization

---

## 📚 Roadmap 12 Minggu

### Minggu 1–3: Benchmarking & Evaluation (lm-eval-harness)

| Hari | Topik | Praktik |
|------|-------|---------|
| 1–2 | **LM Eval Harness** instalasi + arsitektur | `pip install lm-eval`, verifikasi CUDA |
| 3–4 | **Core benchmarks**: MMLU, GSM8K, HellaSwag, TruthfulQA | `lm_eval --model hf --model_args pretrained=meta-llama/Llama-2-7b-hf --tasks mmlu,gsm8k` |
| 5–6 | **Custom checkpoint eval**: model hasil fine-tuning lokal | `--model_args pretrained=/path/to/my-lora-checkpoint` |
| 7–8 | **vLLM backend**: 5–10x lebih cepat daripada HF biasa | `lm_eval --model vllm --model_args pretrained=...,tensor_parallel_size=2` |
| 9–10 | **Multi-model comparison table**: Llama-2-7B vs Mistral-7B vs Phi-2 | Script `eval_all_models.sh` |
| 11–12 | **Report generation**: JSON → markdown table → PDF | `results/llama2-7b-eval.json` → `.to_markdown()` |

**Deliverable Minggu 3:** `model-benchmark-report.pdf` — perbandingan akurasi 3 model lokal Bos

---

### Minggu 4–6: Experiment Tracking (W&B)

| Hari | Topik | Praktik |
|------|-------|---------|
| 1–2 | **W&B setup**: akun gratis, API key, login | `wandb login <api_key>` |
| 3–4 | **Config tracking**: hyperparameters, dataset version | `wandb.init(project="polri-llm", config={...})` |
| 5–6 | **Real-time dashboard**: loss, accuracy, GPU util | Log `train/loss`, `val/accuracy`, `gpu/util` |
| 7–8 | **Artifacts**: model checkpoint versioning | `artifact = wandb.Artifact('model', type='model')` |
| 9–10 | **Custom visualizations**: confusion matrix, scatter plots | `wandb.plot.confusion_matrix(...)` |
| 11–12 | **Offline mode**: untuk jaringan terbatas (lab polsek) | `os.environ["WANDB_MODE"] = "offline"` |

**Deliverable Minggu 6:** Dashboard live di `wandb.ai` → `polri-llm` project

---

### Minggu 7–8: Hyperparameter Sweeps & Optimization

| Hari | Topik | Praktik |
|------|-------|---------|
| 1–2 | **Sweep configuration**: bayesian optimization | `method: 'bayes'`, metric `maximize val/accuracy` |
| 3–4 | **Parameter space**: lr, batch_size, dropout, weight_decay | Distribusi log_uniform, uniform, categorical |
| 5–6 | **Run 20 trials otomatis**: `wandb agent sweep_id` | `count=20` |
| 7–8 | **Distributed sweep**: multi-GPU coordination | `SWEEP_WORKER_ID` + `CUDA_VISIBLE_DEVICES` |
| 9–10 | **Analyze results**: best config, learning curve | Sweep report → recommendation |
| 11–12 | Lab: Fine-tuning **IndoBERT** untuk klasifikasi teks kejahatan siber | Dataset: 5000 sample teks komentar terrorisme (anonim) |

**Deliverable Minggu 8:** `sweep-report-indobert.pdf` — konfigurasi optimal untuk klasifikasi teks Polri

---

### Minggu 9–10: Model Registry & Deployment

| Hari | Topik | Praktik |
|------|-------|---------|
| 1–2 | **Model registry**: link ke W&B registry | `run.link_artifact(artifact, 'model-registry/production-models')` |
| 3–4 | **Version control**: alias `best`, `production`, `staging` | `aliases=['best', 'production']` |
| 5–6 | **A/B testing**: dua versi model di produksi | Split traffic 90:10 |
| 7–8 | **Rollback strategy**: health check + auto rollback | Monitor `vllm:num_requests_running` < threshold |
| 9–10 | Lab: Deploy **vLLM OpenAI-compatible API** di GPU server | `vllm serve <model> --tensor-parallel-size 4 --port 8000` |

**Deliverable Minggu 10:** Pipeline deploy model: `git push → train → test → register → deploy`

---

### Minggu 11–12: CI/CD MLOps & Final Project

| Hari | Topik | Praktik |
|------|-------|---------|
| 1–2 | **GitHub Actions MLOps**: trigger training on new data | `.github/workflows/train.yml` |
| 3–4 | **Validation gate**: block deploy if accuracy < threshold | `acc_drop_gates` |
| 5–6 | **Data drift detection**: monitoring input distribution | `wandb.Table` + statistical test |
| 7–8 | **Speculative decoding**: gunakan LeDir/LlamaDraft untuk LLM besar | 2–3x throughput gain |
| 9–10 | **Final Project**: Fine-tune **Indo-LLaMA-7B** untuk QA sistem peraturan Polri | Dataset 10K QA pairs dari Peraturan Kapolri |
| 11–12 | Presentasi hasil ke tim laboratorium | Demo API QA + W&B dashboard |

**Deliverable Minggu 12:**  
- `mlops-ci-cd-polri.yaml` (GitHub Actions)  
- `indo-llama-qaperrpol.h5` (model fine-tuned)  
- Demo API: `http://192.168.147.179:8000/v1/chat/completions`  
- Dashboard live: `wandb.ai/polri-labs/indo-llama-qaperrpol`

---

## 🛠️ Toolchain Wajib Diinstall

```bash
# lm-eval-harness
pip install lm-eval[eval]

# Weights & Biases
pip install wandb

# vLLM
pip install vllm

# HuggingFace Hub
pip install huggingface_hub

# Locust (load test untuk API)
pip install locust

# Prometheus client (monitoring vLLM)
pip install prometheus-client

# Docker (serving)
docker pull vllm/vllm-openai:latest
```

---

## 📂 File Referensi Penting (dari Skill Asli)

| File | Path | Kegunaan |
|------|------|----------|
| Benchmark Guide | `mlops/evaluation/evaluating-llms-harness/references/benchmark-guide.md` | 60+ task deskripsi |
| API Evaluation | `mlops/evaluation/evaluating-llms-harness/references/api-evaluation.md` | vLLM + OpenAI API |
| Distributed Eval | `mlops/evaluation/evaluating-llms-harness/references/distributed-eval.md` | Multi-GPU eval |
| Server Deployment | `mlops/inference/serving-llms-vllm/references/server-deployment.md` | Docker + K8s config |
| Quantization | `mlops/inference/serving-llms-vllm/references/quantization.md` | AWQ/GPTQ/FP8 |
| Sweeps | `mlops/evaluation/weights-and-biases/references/sweeps.md` | Hyperparameter tuning |
| Integrations | `mlops/evaluation/weights-and-biases/references/integrations.md` | PyTorch, TF, Transformers |

---

## 🎯 Use Case Polri (Khusus)

| Unit | Skenario MLOps | Prioritas |
|------|----------------|-----------|
| **Intelkam** | Threat intel classification, OSINT entity extraction | 🔴 Critical |
| **Reskrim** | Evidence tagging, document summarization | 🔴 Critical |
| **Binmas** | Community sentiment analysis, report auto-categorization | 🟠 High |
| **Sabhara** | Dispatch routing optimization, incident prediction | 🟠 High |
| **Lantas** | ANPR plate recognition, violation detection | 🟠 High |
| **Akademi** | AI curriculum lab, student model fine-tuning experiments | 🟡 Medium |

**Hardware Target:** GPU server Bos (`192.168.147.179`, H100 ×4)
- vLLM tensor parallelism: `--tensor-parallel-size 4`
- Quantization: `--quantization awq` untuk 70B models

---

## ✅ Checklist Kelulusan (Harus Semua ✅)

- [ ] Benchmark **3 model lokal** (Llama-2, Mistral, Phi-2) pakai lm-eval-harness
- [ ] Deploy **vLLM OpenAI-compatible API** di GPU server
- [ ] Setup **W&B experiment tracking** + real-time dashboard
- [ ] Jalankan **20-trial sweep** untuk fine-tuning IndoBERT
- [ ] Registrasikan model ke **W&B Model Registry**
- [ ] Deploy **CI/CD pipeline** (GitHub Actions → W&B → vLLM)
- [ ] Implement **speculative decoding** untuk 2x+ throughput
- [ ] Fine-tune **Indo-LLaMA-7B** untuk QA Peraturan Polri
- [ ] Presentasi demo ke tim laboratorium

---

## 🚀 Next Steps Setelah Selesai

1. **Federated Learning** untuk kolaborasi model antar polsek
2. **Prompt Engineering** terstandarisasi (prompt-governance)
3. **LLM Application Security** (LLM security skill — prompt injection, tool abuse)
4. **MLflow integration** sebagai alternatif W&B (self-hosted)
5. **Model serving dengan Ray Serve** untuk scaling multi-model

---

## 📎 Referensi Eksternal

- lm-evaluation-harness: https://github.com/EleutherAI/lm-evaluation-harness
- Weights & Biases: https://docs.wandb.ai/
- vLLM: https://docs.vllm.ai/
- Leaderboard (model comparison): https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard