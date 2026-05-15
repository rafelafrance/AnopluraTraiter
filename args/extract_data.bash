#!/bin/bash

uv run anoplura/extract_data.py \
  --text-dir data/pdf_parsing/text \
  --lm-jsonl data/pdf_parsing/llm_data_2026-05-08.jsonl \
  --log-file data/pdf_parsing/llm_data_2026-05-08.log \
  --model-name qwen/qwen3.6-32b-a3b \
  --notes "Using the new JSONL output format"

# --model-name google/gemma-4-26b-a4b \
