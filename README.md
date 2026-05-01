# AnopluraTraiter

The Anoplura Traits Database Project

## What we're doing

Extract traits and locations from scientific literature about lice (Anoplura). That is, if I'm given text like

```
Maximum head width, 0.150–0.163 mm (mean, 0.17 mm, n = 4).
One long Dorsal Principal Head Seta (DPHS), one small Dorsal
Accessory Head Seta (DAcHS) anteromedial to DPHS, one
Dorsal Posterior Central Head Seta (DPoCHS), two to three Dorsal
Preantennal Head Setae (DPaHS), two Sutural Head Setae (SHS),
three Dorsal Marginal Head Setae (DMHS), three to four Apical
Head Setae (ApHS). Head, thorax, and abdomen lightly sclerotized.
```

I will extract:

- max width: part = head, n = 4, mean = 0.17, mean_units = mm, low = 0.15, high = 0.163, length_units = mm,
- dorsal principal head setae: count = 1
- dorsal accessory head setae: count = 1
- dorsal posterior central head setae: count = 1
- dorsal preantennal head setae: low = 2, high = 3
- sutural head setae: count = 2
- dorsal marginal head setae: count = 3
- apical head setae: low = 3, high = 4
- etc.

## Information extraction strategy

There are 3 general steps for the process:

1. OCR the PDFs to get text with small language models specifically designed for OCR, like Chandra-OCR.

2. Extract information as raw text.
I use medium sized models for this step like gemma4 or qwen3.6.
The data is in raw form with numeric ranges get lumped into a single field and IDs as a single string.
I only parse one set of traits at a time, so a single text file will get parsed for seta counts,
and then body size in separate passes.
I do this so that I don't overwhelm the models with long and complicated prompts.
The output is in JSON format.

3. Finally, I put the data from step 2 into a format that researchers want.
I tend to not use models for this step and just code simple parsers; it's just easier.

## Install

You will need to have Python 3.14 (or later) installed. You can install the requirements into your python environment like so:

```
make install
```

## Run

### OCR PDFs

TODO

### Extract data from text

```bash
uv run anoplura/extract_data.py \
  --text-dir data/text \
  --raw-data-dir data/raw_data \
  --model-name qwen/qwen3.6-35b-a3b \
  --log-file data/raw_data.log \
  --notes "A note to put into the log file"
```

### Clean extracted data

TODO
