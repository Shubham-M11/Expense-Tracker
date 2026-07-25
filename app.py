from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    expense = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Expense {self.expense}>"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/add-expense", methods=["GET", "POST"])
def add_expense():

    if request.method == "POST":

        expense_name = request.form["expense_name"]
        amount = request.form["amount"]

        new_expense = Expense(
            expense=expense_name,
            amount=float(amount)
        )

        db.session.add(new_expense)
        db.session.commit()

        return redirect(url_for("view_expenses"))

    return render_template("add_expense.html")


@app.route("/expenses")
def view_expenses():

    expenses = Expense.query.all()

    total_amount = sum(expense.amount for expense in expenses)
    return render_template(
    "expenses.html",
    expenses=expenses,
    total_amount=total_amount
)



@app.route("/delete/<int:id>")
def delete(id):

    expense = db.get_or_404(Expense, id)

    db.session.delete(expense)

    db.session.commit()

    return redirect(url_for("view_expenses"))


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):

    expense = db.get_or_404(Expense, id)

    if request.method == "POST":

        expense.expense = request.form["expense_name"]
        expense.amount = float(request.form["amount"])

        db.session.commit()

        return redirect(url_for("view_expenses"))

    return render_template(
        "edit_expense.html",
        expense=expense
    )

if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(debug=True)