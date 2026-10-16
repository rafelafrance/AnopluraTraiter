#!/bin/bash

image_dirs=data/Durden_LA/images
new_dir=data/Durden_LA/stitches

for images in "$image_dirs"/*; do
    base_name=$(basename $images)
    echo "$base_name"
    uv run anoplura/pdf_parsers/stitch.py \
        --slices-json "$images"/"$base_name".json \
        --image-dir "$new_dir"/"$base_name" \
        --description-pattern "$base_name"
done
