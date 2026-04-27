#!/bin/bash

uv run anoplura/extract_data.py \
  --text-dir data/pdf_parsing/text \
  --raw-data-dir data/pdf_parsing/raw_data_2026-04-27 \
  --model-name qwen/qwen3.6-35b-a3b \
  --log-file data/pdf_parsing/raw_data_2026-04-27.log \
  --notes "Trying new prompts on live data"

# --model-name google/gemma-4-26b-a4b \
