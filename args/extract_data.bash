#!/bin/bash

uv run anoplura/extract_data.py \
  --text-dir data/Durden\,\ L.A./text \
  --lm-jsonl data/Durden\,\ L.A./extract_data_260928.jsonl \
  --log-file data/Durden\,\ L.A./extract_data.log \
  --prompt prompts/anoplura.md \
  --model-name Qwen3.6-35B-A3B-MTP-GGUF:Q4_K_XL \
  --api-host http://localhost:9931/v1 \
  --timeout 900
