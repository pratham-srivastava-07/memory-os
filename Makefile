docker compose up -d
python -m pytest
ruff check .
ruff format .
python scripts/ingest.py