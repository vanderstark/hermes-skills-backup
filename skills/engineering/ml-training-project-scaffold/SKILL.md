---
name: ml-training-project-scaffold
description: Scaffold ML training projects with auto GitHub deploy.
---

# ML Training Project Scaffold

**Trigger:** User wants to create an AI/ML training project with datasets, fine-tuning pipelines, and automated GitHub deployment.

## Core Workflow

### 1. Project Structure
```
/project-root/
├── training/
│   ├── dataset/          # JSONL training data (Alpaca format)
│   └── scripts/          # Training pipelines (GPU + CPU)
├── inference/
├── models/
├── docker/
└── docs/
```

### 2. Dataset Generation (Alpaca Format)
```json
{"instruction": "Task description", "input": "Context", "output": "Expected response"}
```
- Generate 500-1000 entries for meaningful fine-tuning
- Domain-specific templates
- Use `ensure_ascii=False` for Indonesian/multilingual

### 3. Training Pipeline Scripts

**GPU (Unsloth/QLoRA):**
```python
# FastLanguageModel.from_pretrained(load_in_4bit=True)
# get_peft_model(r=64, lora_alpha=128, gradient_checkpointing=True)
# SFTTrainer with fp16/bf16, 2 epochs
```

**CPU (llama.cpp):**
```bash
# ./llama-finetune --model-base ./models/base --train-data ./data.jsonl --threads $(nproc)
```

### 4. Automated GitHub Deployment

**Repo Creation:**
```bash
curl -X POST -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/user/repos \
  -d '{"name":"repo-name","private":false,"auto_init":false}'
```

**Push with Token:**
```bash
git remote set-url origin https://$TOKEN@github.com/user/repo.git
git push -u origin main --force
rm -f /tmp/gh_token_file
```

**Execute via Python when terminal/shell fails:**
```python
import subprocess
subprocess.run(['git', '-C', repo_path, 'push', 'origin', 'main', '--force'])
```

## Pitfalls & Solutions

| Issue | Solution |
|-------|----------|
| Terminal/shell tools fail | Use `execute_code` with `subprocess.run()` |
| Repo doesn't exist | Create via GitHub API first |
| Token exposure | Store in `/tmp/gh_token_file` chmod 600, delete after push |
| Large dataset memory | Use `datasets.load_dataset` with streaming |
| OOM on GPU | QLoRA 4-bit + gradient checkpointing + smaller batch |

## References
- `references/github-api-repo-create.md` — GitHub API patterns
- `references/dataset-templates.md` — Domain-specific templates
- `references/training-pipeline-gpu.md` — Unsloth QLoRA config
- `references/training-pipeline-cpu.md` — llama.cpp CPU fine-tuning