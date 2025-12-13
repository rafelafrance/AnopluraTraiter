#!/bin/bash

today=$(date +"%Y-%m-%d")
text_dir=data/pdf_parsing/text
output_dir=data/pdf_parsing/output_"$today"

mkdir -p "$output_dir"

for path in $text_dir/*.txt; do
  stem=$(basename "$path" .txt)

  echo "$stem"

  uv run anoplura/extract_rules.py \
    --text-input "$path" \
    --html-output "$output_dir"/"$stem"_"$today".html \
    --markdown-output "$output_dir"/"$stem"_"$today".md

done
