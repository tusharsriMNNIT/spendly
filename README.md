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

## Deployment

**GitHub alone cannot serve this site.** GitHub Pages only hosts static
files (HTML/CSS/JS) — it has no way to run a Python process, handle form
submissions, or persist a SQLite database. GitHub can host the *source
code* (which this repository already does), but running the app requires
an actual host that executes Python, such as:

- [Render](https://render.com/)
- [Railway](https://railway.app/)
- [Fly.io](https://fly.io/)
- [PythonAnywhere](https://www.pythonanywhere.com/)

Note also that `app.run(debug=True)` in `app.py` is for local development
only — a production deployment should run behind a real WSGI server (e.g.
gunicorn) with debug mode off, and SQLite's single-file database should be
placed on persistent storage the hosting platform doesn't wipe on redeploy.
