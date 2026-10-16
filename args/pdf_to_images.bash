#!/bin/bash

pdf_dir=data/Durden_LA/pdf

for pdf in "$pdf_dir"/*; do
    echo "$pdf"
    uv run anoplura/pdf_parsers/pdf_to_images.py \
        --in-pdf "$pdf" \
        --image-dir data/Durden_LA/images
done
