# Dataset Templates (Alpaca-style JSONL)

## Format
```json
{"instruction": "Teks instruksi", "input": "Konteks opsional", "output": "Jawaban"}
```

## Domain-Specific Generators (Python)
```python
import json, random

templates = [
    "Jelaskan langkah-langkah awal penyelidikan kejahatan siber",
    "Apa itu chain of custody dalam penanganan bukti digital?",
    "Cara mendeteksi aktivitas mencurigakan di jaringan",
]

dataset = []
for i in range(800):
    tmpl = random.choice(templates)
    dataset.append(json.dumps({
        "instruction": f"{tmpl} (Kasus #{i+1})",
        "input": "",
        "output": f"Jawaban kasus #{i+1}: Analisis teknis mengenai {tmpl.lower()}."
    }, ensure_ascii=False))

with open("training_data.jsonl", "w") as f:
    f.write("\n".join(dataset))
```

## Best Practices
- 500-1000 entries minimum for meaningful fine-tuning
- Use `ensure_ascii=False` for Indonesian/Unicode
- No PII in training data
- Diverse instructions to avoid overfitting
