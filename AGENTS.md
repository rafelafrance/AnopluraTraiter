# AGENTS.md

## Setup
- **Python >= 3.14** required (pyproject.toml `requires-python`). README still says 3.13 — trust pyproject.toml.
- Install deps: `make install` (runs `uv sync`). No `pip` — this project uses `uv` exclusively.

## Run
- **Extract (LLM):** `uv run anoplura/extract_data.py --text-dir data/pdf_parsing/text --raw-data-dir data/pdf_parsing/raw_data_<date> --model-name <model> --log-file <path>.log --notes "<note>"`
- **Clean (rule-based):** `uv run anoplura/clean_data.py --raw-data-dir <raw_dir> --cleaned-data-dir <cleaned_dir> --log-file <path>.log --notes "<note>"`
- Example commands are in `args/*.bash`.
- **Lint:** `ruff check .` (pre-commit runs `ruff --fix` + `ruff-format`).
- **Pre-commit:** `pre-commit run --all-files`.
- **Test:** `make test` (`uv run -m unittest discover`).

## Architecture
- **Data flow:** `data/pdf_parsing/text/*.txt` → `extract_data.py` (LLM) → `data/pdf_parsing/raw_data_*/` → `clean_data.py` (parsers) → `data/pdf_parsing/cleaned_data_*/`.
- `anoplura/extract_data.py` — iterates `PROMPTS` dict (12 keys: seta_counts, antennae_segments, body_length, head_width, thorax_width, sternite_counts, tergite_counts, plate_counts, dpts_length, mesothracic_spiracle, denticle_counts). Makes one API call per prompt per text file, sequentially.
- `anoplura/clean_data.py` — dispatches `CLEANERS` dict by key. **CLEANERS is all commented-out stubs** — the cleaning step is not yet functional. Also, the `--raw-data-dir` and `--cleaned-data-dir` help strings are swapped; the flags themselves work correctly.
- `anoplura/pylib/` — shared utils: `log.py` (logging setup), `str_util.py` (string/number parsing, JSON fence stripping), `roman.py` (roman numeral conversion).
- Default API host: `http://localhost:1234/v1` (override with `--api-host`).

## Gotchas
- LLM output is stripped of ````json` fences before `json.loads()` via `strip_json_fences()`.
- Ruff selects `ALL` rules minus a long ignore list. All D1xx (docstring) rules are ignored — no docstrings required. `notebooks/` is excluded entirely.
- Testing uses `unittest`, not `pytest`.
- `data/`, `output/`, `old/`, `notebooks/` are gitignored.
