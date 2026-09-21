# Spendly

A simple expense tracker built with Flask and SQLite. Register, log in, and
track your expenses by category.

## Features

- Email/password registration and login (passwords hashed with Werkzeug)
- Add, edit, and delete expenses, scoped to the logged-in user
- Expense categories: Food, Transport, Bills, Health, Entertainment,
  Shopping, Other
- Dashboard with total spend and a per-expense breakdown

## Tech stack

- [Flask](https://flask.palletsprojects.com/) 3.1
- SQLite (via the standard library `sqlite3` module, no ORM)
- Server-rendered Jinja templates, no frontend framework

## Setup

Requires Python 3.11+.

```bash
git clone https://github.com/tusharsriMNNIT/spendly.git
cd spendly
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Running locally

```bash
python app.py
```

The app starts on **http://localhost:5001** (debug mode is on). The SQLite
database (`expense_tracker.db`) and its tables are created automatically on
first run, along with a seeded demo account:

- Email: `demo@spendly.com`
- Password: `demo123`

## Linting

```bash
ruff check .
```