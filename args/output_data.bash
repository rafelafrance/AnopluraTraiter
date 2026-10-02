#!/bin/bash

uv run anoplura/output_data.py \
  --lm-jsonl data/Durden\,\ L.A./extract_data_260928.jsonl \
  --csv-out data/Durden\,\ L.A./output_data_261002.csv \
  --log-file data/Durden\,\ L.A./output_data.log
