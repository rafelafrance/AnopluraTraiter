#!/bin/bash

uv run anoplura/output_data.py \
  --llm-data-dir data/pdf_parsing/llm_data_2026-05-02 \
  --csv-out data/pdf_parsing/llm_data_2026-05-02.csv \
  --log-file data/pdf_parsing/llm_data_2026-05-02.log \
  --notes "Trying new prompts on live data"
