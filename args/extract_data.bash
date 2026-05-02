#!/bin/bash

uv run anoplura/extract_data.py \
  --text-dir data/pdf_parsing/text \
  --llm-data-dir data/pdf_parsing/llm_data_2026-05-02 \
  --log-file data/pdf_parsing/llm_data_2026-05-02.log \
  --model-name qwen/qwen3.6-32b-a3b \
  --notes "Trying OpenCode's prompts on live data"

# --model-name google/gemma-4-26b-a4b \
