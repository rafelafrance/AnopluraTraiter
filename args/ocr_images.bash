#!/bin/bash

image_dirs=data/Durden_LA/stitches
ocr_dir=data/Durden_LA/ocr_text

for image_dir in "$image_dirs"/*/*; do
    base_name=$(basename $image_dir)
    echo "$base_name"
    uv run anoplura/pdf_parsers/ocr_images.py \
        --image-dir "$image_dir" \
        --ocr-file "$ocr_dir"/"$base_name".txt \
        --timeout 240
done
