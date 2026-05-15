#!/bin/bash

uv run anoplura/output_data.py \
  --lm-jsonl data/pdf_parsing/llm_data_2026-05-08.jsonl \
  --csv-out data/pdf_parsing/llm_data_2026-05-08.csv \
  --log-file data/pdf_parsing/llm_data_2026-05-08.log \
  --notes "Trying new prompts on live data"
