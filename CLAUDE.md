# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Spendly — a Flask + SQLite expense tracker built as a step-by-step tutorial project. `app.py` contains routes with `# Step N` comments marking unimplemented features (e.g. logout, profile, expense CRUD), each currently returning a placeholder string like `"Add expense — coming in Step 7"`.

**Implement only the step currently being worked on.** Do not proactively fill in other stubbed routes or jump ahead in the sequence, even if the implementation would be trivial — later steps may depend on decisions not yet made.

## Stack

- Flask 3.1 (`app.py`), stdlib `sqlite3` — no ORM, no migrations. Use `CREATE TABLE IF NOT EXISTS` for schema.
- `database/db.py` is currently a stub. It is meant to hold: `get_db()` (SQLite connection with `row_factory` and foreign keys enabled), `init_db()` (create tables), `seed_db()` (insert dev sample data).
- No package manager beyond pip; dependencies are in `requirements.txt` only (no pyproject.toml/poetry).

## Running

- `python app.py` — starts the Flask dev server on **port 5001** (not the default 5000), with `debug=True` hardcoded.
- No Makefile or npm-style scripts exist in this repo.

## Testing

`pytest` and `pytest-flask` are installed but **no test files exist yet**. Write tests alongside each step's implementation rather than assuming an existing suite to run.

## Linting

`ruff check .` (config in `ruff.toml`). Run it after editing Python files.
