from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

expenses = []

class Expense(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    expense = db.Column(db.String(100), nullable=False)

    amount = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"{self.expense}"

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/add-expense", methods=["GET", "POST"])
def add_expense():

    if request.method == "POST":

        expense = request.form["expense_name"]
        amount = request.form["amount"]

        expenses.append(
            {
                "expense": expense,
                "amount": amount
            }
        )

        return redirect(url_for("view_expenses"))

    return render_template("add_expense.html")


@app.route("/expenses")
def view_expenses():
    return render_template(
        "expenses.html",
        expenses=expenses
    )


if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(debug=True)