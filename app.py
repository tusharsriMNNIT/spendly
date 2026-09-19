from datetime import date, datetime
from functools import wraps

from flask import Flask, abort, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from database.db import get_db, init_db, seed_db

app = Flask(__name__)
app.secret_key = "dev-secret-key"  # fine for local dev; use a real secret in production

with app.app_context():
    init_db()
    seed_db()

CATEGORIES = ["Food", "Transport", "Bills", "Health", "Entertainment", "Shopping", "Other"]


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return wrapped


def validate_expense_form(amount, category, date_value):
    if not amount or not category or not date_value:
        return "Amount, category, and date are required."
    try:
        amount_value = float(amount)
    except ValueError:
        return "Amount must be a number."
    if amount_value <= 0:
        return "Amount must be greater than zero."
    if category not in CATEGORIES:
        return "Please choose a valid category."
    try:
        datetime.strptime(date_value, "%Y-%m-%d")
    except ValueError:
        return "Date must be in YYYY-MM-DD format."
    return None


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not name or not email or not password:
            return render_template("register.html", error="All fields are required.")

        conn = get_db()
        existing = conn.execute(
            "SELECT id FROM users WHERE email = ?", (email,)
        ).fetchone()
        if existing:
            conn.close()
            return render_template(
                "register.html", error="An account with that email already exists."
            )

        password_hash = generate_password_hash(password)
        cursor = conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            (name, email, password_hash),
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()

        session["user_id"] = user_id
        session["user_name"] = name
        return redirect(url_for("profile"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        conn = get_db()
        user = conn.execute(
            "SELECT id, name, password_hash FROM users WHERE email = ?", (email,)
        ).fetchone()
        conn.close()

        if user is None or not check_password_hash(user["password_hash"], password):
            return render_template("login.html", error="Invalid email or password.")

        session["user_id"] = user["id"]
        session["user_name"] = user["name"]
        return redirect(url_for("profile"))

    return render_template("login.html")


# ------------------------------------------------------------------ #
# Authenticated routes                                                #
# ------------------------------------------------------------------ #

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("landing"))


@app.route("/profile")
@login_required
def profile():
    conn = get_db()
    expenses = conn.execute(
        "SELECT id, amount, category, date, description FROM expenses "
        "WHERE user_id = ? ORDER BY date DESC, id DESC",
        (session["user_id"],),
    ).fetchall()
    conn.close()

    total = sum(expense["amount"] for expense in expenses)

    return render_template(
        "profile.html",
        user_name=session.get("user_name"),
        expenses=expenses,
        total=total,
    )


@app.route("/expenses/add", methods=["GET", "POST"])
@login_required
def add_expense():
    if request.method == "POST":
        amount = request.form.get("amount", "").strip()
        category = request.form.get("category", "").strip()
        date_value = request.form.get("date", "").strip()
        description = request.form.get("description", "").strip() or None

        error = validate_expense_form(amount, category, date_value)
        if error:
            return render_template(
                "expense_form.html",
                categories=CATEGORIES,
                error=error,
                form_action=url_for("add_expense"),
                heading="Add expense",
                submit_label="Add expense",
                amount=amount,
                category=category,
                date=date_value,
                description=description or "",
            )

        conn = get_db()
        conn.execute(
            "INSERT INTO expenses (user_id, amount, category, date, description) "
            "VALUES (?, ?, ?, ?, ?)",
            (session["user_id"], float(amount), category, date_value, description),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("profile"))

    return render_template(
        "expense_form.html",
        categories=CATEGORIES,
        error=None,
        form_action=url_for("add_expense"),
        heading="Add expense",
        submit_label="Add expense",
        amount="",
        category="",
        date=date.today().isoformat(),
        description="",
    )


@app.route("/expenses/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit_expense(id):
    conn = get_db()
    expense = conn.execute(
        "SELECT id, amount, category, date, description FROM expenses "
        "WHERE id = ? AND user_id = ?",
        (id, session["user_id"]),
    ).fetchone()

    if expense is None:
        conn.close()
        abort(404)

    if request.method == "POST":
        amount = request.form.get("amount", "").strip()
        category = request.form.get("category", "").strip()
        date_value = request.form.get("date", "").strip()
        description = request.form.get("description", "").strip() or None

        error = validate_expense_form(amount, category, date_value)
        if error:
            conn.close()
            return render_template(
                "expense_form.html",
                categories=CATEGORIES,
                error=error,
                form_action=url_for("edit_expense", id=id),
                heading="Edit expense",
                submit_label="Save changes",
                amount=amount,
                category=category,
                date=date_value,
                description=description or "",
            )

        conn.execute(
            "UPDATE expenses SET amount = ?, category = ?, date = ?, description = ? "
            "WHERE id = ? AND user_id = ?",
            (float(amount), category, date_value, description, id, session["user_id"]),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("profile"))

    conn.close()
    return render_template(
        "expense_form.html",
        categories=CATEGORIES,
        error=None,
        form_action=url_for("edit_expense", id=id),
        heading="Edit expense",
        submit_label="Save changes",
        amount=expense["amount"],
        category=expense["category"],
        date=expense["date"],
        description=expense["description"] or "",
    )


@app.route("/expenses/<int:id>/delete", methods=["POST"])
@login_required
def delete_expense(id):
    conn = get_db()
    conn.execute(
        "DELETE FROM expenses WHERE id = ? AND user_id = ?",
        (id, session["user_id"]),
    )
    conn.commit()
    conn.close()
    return redirect(url_for("profile"))


if __name__ == "__main__":
    app.run(debug=True, port=5001)
