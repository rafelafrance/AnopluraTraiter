#!/bin/bash

uv run anoplura/output_data.py \
  --lm-jsonl data/pdf_parsing/extract_data_260731.jsonl \
  --csv-out data/pdf_parsing/output_data_260801.csv \
  --log-file data/pdf_parsing/output_data.log \
  --notes "Fixing setae count output"
