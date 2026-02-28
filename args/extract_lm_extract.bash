#!/bin/bash

uv run anoplura/extract_lm.py extract \
  --input-text data/pdf_parsing/text/Hoplopleura_janzeni_2001.txt \
  --output-md data/pdf_parsing/Hoplopleura_janzeni_2001_gemma3.md \
  --api-host localhost:1234 \
  --context-length 70000 \
  --model-name qwen/qwen3.5-35b-a3b
