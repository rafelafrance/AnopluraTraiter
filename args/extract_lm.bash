#!/bin/bash

uv run anoplura/extract_lm.py \
  --text-dir data/pdf_parsing/text_test \
  --raw-lm-dir data/pdf_parsing/raw_lm_test \
  --model-name qwen/qwen3.6-35b-a3b

# --model-name google/gemma-4-26b-a4b \
