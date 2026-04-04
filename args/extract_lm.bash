#!/bin/bash

uv run anoplura/extract_lm.py \
  --text-dir data/pdf_parsing/text \
  --json-dir data/pdf_parsing/json \
  --api-host localhost:1234 \
  --model google/gemma-4-26b-a4b \
  --temperature 0.01
