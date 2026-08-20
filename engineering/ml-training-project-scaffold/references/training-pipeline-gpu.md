# GPU Training Pipeline (Unsloth QLoRA)

## Install
```bash
pip install unsloth trl transformers datasets accelerate
```

## Optimized Script
```python
import os
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:128"

from datasets import load_dataset
from transformers import TrainingArguments
from trl import SFTTrainer
from unsloth import FastLanguageModel, is_bfloat16_supported

# Load dataset
ds = load_dataset("json", data_files="training/dataset/full_training_data.jsonl", split="train")
ds = ds.map(lambda x: {"text": f"### INSTRUCTION:\n{x['instruction']}\n\n### INPUT:\n{x['input']}\n\n### OUTPUT:\n{x['output']}"}, num_proc=4)

# Load model QLoRA
model, tok = FastLanguageModel.from_pretrained(
    model_name="unsloth/mistral-7b-v0.3",
    max_seq_length=1024,
    load_in_4bit=True,
    dtype="auto",
    device_map="auto",
)

model = FastLanguageModel.get_peft_model(
    model, r=64, lora_alpha=128, lora_dropout=0,
    target_modules=["q_proj","k_proj","v_proj","o_proj"],
    bias="none", use_gradient_checkpointing=True
)

# Trainer
trainer = SFTTrainer(
    model=model, tokenizer=tok, train_dataset=ds,
    dataset_text_field="text", max_seq_length=1024,
    args=TrainingArguments(
        per_device_train_batch_size=1, gradient_accumulation_steps=8,
        warmup_steps=10, num_train_epochs=2,
        learning_rate=2e-4, fp16=True, bf16=is_bfloat16_supported(),
        logging_steps=5, output_dir="models/finetuned",
        report_to="none", save_strategy="epoch"
    )
)

trainer.train()
model.save_pretrained("models/finetuned")
tok.save_pretrained("models/finetuned")
```

## Key Optimizations
- QLoRA 4-bit: 75% VRAM reduction
- Gradient checkpointing: larger effective batch
- r=64, alpha=128: good balance for 7B models
- 2 epochs: sufficient for SFT on 800 samples
