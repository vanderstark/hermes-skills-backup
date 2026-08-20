# CPU Training Pipeline (llama.cpp)

## Build llama.cpp
```bash
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp && make
```

## Fine-tuning Script (train_cpu.sh)
```bash
#!/bin/bash
./llama.cpp/llama-finetune \
  --model-base ./models/base-model \
  --train-data ./training/dataset/training_data.jsonl \
  --threads $(nproc) \
  --ctx 512 \
  --epochs 1
```

## Notes
- CPU training is 10-50x slower than GPU
- Use small models (3-7B GGUF)
- Reduce context to 512 for memory
- Suitable for testing, not production training

## Alternative: CPU Inference Only
If full training too slow, use pre-trained GGUF:
```bash
./llama.cpp/llama-cli -m ./models/model.gguf -p "Your prompt"
```
