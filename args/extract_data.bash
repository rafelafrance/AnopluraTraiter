#!/bin/bash

uv run anoplura/extract_data.py \
  --text-dir data/Durden_LA/ocr_text \
  --lm-jsonl data/Durden_LA/extract_data_261019.jsonl \
  --log-file data/Durden_LA/extract_data.log \
  --prompt prompts/anoplura.md \
  --model-name unsloth/Qwen3.8-27B-UD-Q8_K_XL \
  --api-host http://localhost:9931/v1 \
  --timeout 900
