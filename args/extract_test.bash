#!/bin/bash

uv run anoplura/extract_data.py \
  --text-dir data/pdf_parsing/junk \
  --lm-jsonl data/pdf_parsing/llm_data_2026-06-01.jsonl \
  --log-file data/pdf_parsing/llm_data_2026-06-01.log \
  --prompt prompts/test.md \
  --model-name qwen/qwen3.6-32b-a3b \
  --temperature 0.1 \
  --notes "Test new extract prompts and code"

# --model-name google/gemma-4-26b-a4b \
