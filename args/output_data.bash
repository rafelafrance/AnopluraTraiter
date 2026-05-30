#!/bin/bash

uv run anoplura/output_data.py \
  --lm-jsonl data/pdf_parsing/llm_data_2026-05-29.jsonl \
  --csv-out data/pdf_parsing/llm_data_2026-05-29.csv \
  --log-file data/pdf_parsing/llm_data_2026-05-29.log \
  --notes "Adding new terms to extract"
