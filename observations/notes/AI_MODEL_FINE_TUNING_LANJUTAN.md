# 🧠 AI Model Fine-Tuning (LoRA/QLoRA): Buat "Otak" AI Khusus Polri

**Skill dasar:** `mlops/llm-training`  
**Kategori:** MLOps / AI  
**Target:** GPU server Bos  
**Bahasa:** Indonesian

---

## 🎯 Ringkasan Skill

Fine-tuning model besar (seperti Llama-3.1 8B atau 70B) membutuhkan memori besar-besar (80GB+VRAM). Namun, **LoRA** dan **QLoRA** memungkinkan kita:

- ✅ Fine-tune model dengan hanya **1-2 GPU** (misal: 2x RTX 4090 24GB)
- ✅ Hasil akurasi hampir sama dengan fine-tuning penuh
- ✅ Waktu training lebih cepat (karena belajar "adapasi" bukan refaktur seluruh bobot)

---

## 🔧 Alur Kerja (GPU Server → Model Khusus)

### Tahap 1: Pemahaman LoRA vs QLoRA

| Feature | LoRA | QLoRA |
|---|---|---|
| Precision | FP16/FP32 | 4-bit |
| Memory Usage | Tinggi | Sangat Rendah |
| Training Speed | Sedang | Cepat |
| Accuracy | Baik | Sangat Baik |

**Kapan pakai QLoRA?**  
Kalau GPU-nya < 24GB VRAM (misal: 1x A6000 48GB atau 2x RTX 4090 24GB).

---

### Tahap 2: Setup Lingkungan

```bash
# 1. Install Python & PyTorch dengan CUDA
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# 2. Install peft & bitsandbytes (untuk LoRA)
pip install peft bitsandbytes transformers accelerate

# 3. Install Unsloth (lebih cepat & hemat memori)
pip install unsloth
```

---

### Tahap 3: Contoh Fine-Tuning untuk Tugas Intelkam

```python
# 1. Load model dengan QLoRA
from unsloth import FastLanguageModel

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "meta-llama/Llama-3.1-8B",
    max_seq_length = 2048,
    dtype = "float16",
    load_in_4bit = True,
)

# 2. Tambah LoRA adapter
model = FastLanguageModel.get_peft_model(
    model,
    r = 16,  # rank LoRA
    target_modules = ["q_proj", "k_proj", "v_proj", "o_proj"],
    lora_alpha = 16,
    lora_dropout = 0.1,
)

# 3. Train dengan data kejahatan siber Polri
training_args = TrainingArguments(
    per_device_train_batch_size = 2,
    gradient_accumulation_steps = 4,
    warmup_steps = 100,
    max_steps = 500,
    learning_rate = 2e-5,
    fp16 = True,
    logging_steps = 10,
    output_dir = "output/polri-intelkam-model",
)

trainer = TrlTrainer(
    model = model,
    args = training_args,
    train_dataset = dataset,
    data_collator = DataCollatorForLanguageModeling(tokenizer, mlm = False),
)
trainer.train()
```

---

## 📋 Use Case untuk Lab Polri

| Use Case | Hasil Model | Nilai |
|---|---|---|
| Analisis laporan kejahatan siber | Model bisa ringkas laporan PDF jadi 5 poin utama |
| Pengolahan percakapan telegram | Ekstrak info penting dari chat teks |
| Analisis dokumen hukum | Jawab pertanyaan berdasarkan isi dokumen (Q&A) |

---

## ⚠️ Pitfalls

- Jangan langsung pakai dataset publik — modelnya nggak *understood* jargon Polri
- Verifikasi hasil training dulu di *offline evaluation*
- Simpan file model di storage terpusat (NFS/ CephFS)

---

**Status:** Siap kerja  
**Next Step:** Grab dataset latihan dari portal publik Polri + scraping berita kejahatan siber
