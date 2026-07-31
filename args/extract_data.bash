#!/bin/bash

uv run anoplura/extract_data.py \
  --text-dir data/pdf_parsing/text \
  --lm-jsonl data/pdf_parsing/extract_data_260731.jsonl \
  --log-file data/pdf_parsing/extract_data.log \
  --prompt prompts/anoplura.md \
  --model-name qwen3.6-27b-ud \
  --temperature 0.1 \
  --notes "Try using a stronger model for extractions"
