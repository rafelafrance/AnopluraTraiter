#!/bin/bash

uv run anoplura/output_data.py \
  --lm-jsonl data/pdf_parsing/llm_data_2026-06-01.jsonl \
  --csv-out data/pdf_parsing/llm_data_2026-06-01.csv \
  --log-file data/pdf_parsing/llm_data_2026-06-01.log \
  --notes "Adding new terms to extract"
