# 🤖 Machine Learning Ops (MLOps): GPU Server & Local LLM Mastery

**Ditulis:** 24 Agustus 2026  
**Kategori:** Machine Learning Ops (MLOps)  
**Target User:** Bos (GPU Server User, 170-server DC)  
**Bahasa:** Indonesian (Bahasa Indonesia)

---

## 🎯 Ringkasan

Skill **MLOps** fokus pada pengelolaan siklus hidup model AI di infrastruktur mandiri Bos (khususnya GPU Server). Mencakup:
- Manajemen model & dataset dari Hugging Face
- Deployment local LLM (Inference) di hardware Bos (CPU/GPU)
- Pelacakan eksperimen training/fine-tuning (Weights & Biases)
- Evaluasi performa model secara objektif

**Hasil Akhir:** Bos memiliki kendali penuh atas model AI yang berjalan di server internal tanpa bergantung pada API eksternal yang mahal.

---

## 📚 Skill Roadmap: 3 Lapis Pembelajaran

### Tier 1: Dasar (Focus Sesi Ini)
- ✅ `mlops/huggingface-hub` — Search, download, and upload models/datasets via `hf` CLI
- ✅ `mlops/llama-cpp` — Local GGUF inference (CPU/GPU/Apple Silicon)
- ✅ `mlops/weights-and-biases` — Log ML experiments, sweeps, and model registry

### Tier 2: Intermediate (Lanjutan)
- 🔷 `mlops/serving-llms-vllm` — High-throughput LLM serving (untuk traffic tinggi)
- 🔷 `mlops/evaluating-llms-harness` — Benchmark LLMs (MMLU, GSM8K, dll)
- 🔷 `mlops/fine-tuning-pipelines` — Unsloth/QLoRA automation for GPU server

### Tier 3: Advanced (Production Mastery)
- 🟦 `mlops/kubernetes-gpu-orchestration` — Managing GPU workloads in K8s
- 🟦 `mlops/model-quantization` — Creating custom GGUF/EXL2/AWQ quants
- 🟦 `mlops/vector-db-ops` — Scaling Milvus/Qdrant/Pinecone for RAG

---

## 🔧 Core Workflow: Local AI Deployment

### Fase 1: Discovery & Acquisition (Hugging Face)
```bash
# 1. Login ke HF (gunakan token Bos)
export HF_TOKEN=your_token
hf auth login

# 2. Cari model yang sedang trending (misal: Llama 3.2 GGUF)
hf models list --sort trending --search "Llama-3.2 GGUF"

# 3. Download model spesifik
hf download bartowski/Llama-3.2-3B-Instruct-GGUF --include "*Q4_K_M.gguf" --local-dir ./models
```
**Tools:** `huggingface-hub`

### Fase 2: Local Inference (llama.cpp)
```bash
# Jalankan server lokal yang kompatibel dengan OpenAI API
llama-server -m ./models/Llama-3.2-3B-Instruct-Q4_K_M.gguf -c 4096 --n-gpu-layers 35

# Test koneksi via curl
curl http://localhost:8080/v1/chat/completions -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "Halo Jarvis!"}]}'
```
**Tools:** `llama-cpp`

### Fase 3: Experiment Tracking (W&B)
```python
import wandb

# Inisialisasi eksperimen fine-tuning
wandb.init(project="drone-nav-ai", config={"learning_rate": 0.0001, "epochs": 10})

# Log metrics selama training
wandb.log({"loss": 0.5, "accuracy": 0.85})
```
**Tools:** `weights-and-biases`

---

## 🎬 Use Cases (Real-World GPU Server Context)

### Skenario 1: Fine-Tuning Model untuk Intelkam
Bos ingin model AI yang paham istilah intelijen dan bahasa hukum Indonesia:
1. Siapkan dataset di lab 170-server.
2. Lakukan fine-tuning menggunakan GPU Server (via Python/Unsloth).
3. Track progress training (loss/accuracy) via `weights-and-biases`.
4. Upload model hasil training ke private repo di Hugging Face via `hf upload`.

### Skenario 2: Private Assistant "Jarvis" Offline
Membangun asisten AI yang berjalan 100% di server lokal Polri:
1. Download model GGUF (Llama/Qwen) menggunakan `huggingface-hub`.
2. Deploy asisten via `llama-cpp` server.
3. Integrasikan dengan Telegram Bot Bos (via local API endpoint).

### Skenario 3: Evaluasi Vendor AI
Memastikan model AI dari pihak ketiga benar-benar akurat:
1. Gunakan `evaluating-llms-harness` untuk run benchmark standard (MMLU).
2. Bandingkan hasil model vendor vs open-source model (Llama/Mistral).
3. Buat laporan perbandingan performa teknis.

---

## 💡 Key Insights & Pitfalls

### ✅ Best Practices
- **Quantization:** Gunakan `Q4_K_M` untuk keseimbangan terbaik antara kecepatan dan kualitas. Gunakan `Q6_K` jika Bos butuh akurasi coding/logika tinggi.
- **GPU Layers:** Selalu maksimalkan `--n-gpu-layers` jika Bos menggunakan GPU NVIDIA untuk mempercepat response time (inference).
- **Security:** Gunakan `HF_TOKEN` sebagai environment variable, jangan hardcode di script.

### ⚠️ Pitfalls (Hindari!)
- **OOM (Out Of Memory):** Jangan paksa load model 70B di GPU 24GB tanpa kuantisasi (GGUF/AWQ). Server akan crash atau sangat lambat.
- **Token Leak:** Hati-hati saat `hf upload`, pastikan tidak ada file `.env` atau data sensitif yang ikut terunggah ke Hugging Face public repo.
- **Ignoring Evaluations:** Jangan hanya percaya "vibe" model; selalu jalankan benchmark formal untuk memastikan model tidak mengalami "regression" setelah fine-tuning.

---

**Status:** Ready to Learn (Tier 1 - Dasar)  
**Estimated Time to Mastery:** 4 minggu @ 8 jam/minggu  
**Next Milestone:** Tier 2 (LLM Serving with vLLM & Automated Evaluation)
