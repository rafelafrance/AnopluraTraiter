#!/bin/bash

uv run anoplura/output_data.py \
  --lm-jsonl data/Durden_LA/extract_data_261019.jsonl \
  --csv-out data/Durden_LA/output_data_261019.csv \
  --log-file data/Durden_LA/output_data.log
