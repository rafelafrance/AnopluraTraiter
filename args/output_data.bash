#!/bin/bash

uv run anoplura/output_data.py \
  --llm-data-dir data/pdf_parsing/llm_data_oc_2026-05-01 \
  --csv-out data/pdf_parsing/llm_data_2026-05-01.csv
