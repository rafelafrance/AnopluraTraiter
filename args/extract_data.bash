#!/bin/bash

uv run anoplura/extract_data.py \
  --text-dir data/pdf_parsing/text \
  --raw-lm-dir data/pdf_parsing/raw_data \
  --model-name qwen/qwen3.6-35b-a3b

# --model-name google/gemma-4-26b-a4b \
