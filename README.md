# Building-Retail-Data-Pipeline

DataCamp Project: Building a Retail Data Pipeline

## Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then fill in any secrets
```

## Run
```bash
python -m src.building_retail_data_pipeline.main
```

## Project layout
- `src/building_retail_data_pipeline/` — application code
- `data/raw/` — untouched source data (gitignored)
- `data/processed/` — cleaned output (gitignored)
- `tests/` — tests
