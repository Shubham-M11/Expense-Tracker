from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transaction_type = db.Column(db.String(20), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"<Transaction {self.id}>"


@app.route("/")
def home():

    transactions = Transaction.query.all()

    total_income = sum(
        t.amount for t in transactions
        if t.transaction_type == "Income"
    )

    total_expense = sum(
        t.amount for t in transactions
        if t.transaction_type == "Expense"
    )

    balance = total_income - total_expense

    return render_template(
        "index.html",
        total_income=total_income,
        total_expense=total_expense,
        balance=balance
    )


@app.route("/add", methods=["GET", "POST"])
def add():

    if request.method == "POST":

        transaction_type = request.form["transaction_type"]
        category = request.form["category"]
        amount = float(request.form["amount"])
        date = request.form["date"]

        if amount <= 0:
            return redirect(url_for("add"))

        transaction = Transaction(
            transaction_type=transaction_type,
            category=category,
            amount=amount,
            date=date
        )

        db.session.add(transaction)
        db.session.commit()

        return redirect(url_for("transactions"))

    return render_template("add_transaction.html")


@app.route("/transactions")
def transactions():

    transactions = Transaction.query.order_by(Transaction.id.desc()).all()

    return render_template(
        "transactions.html",
        transactions=transactions
    )


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):

    transaction = db.get_or_404(Transaction, id)

    if request.method == "POST":

        transaction.transaction_type = request.form["transaction_type"]
        transaction.category = request.form["category"]
        transaction.amount = float(request.form["amount"])
        transaction.date = request.form["date"]

        db.session.commit()

        return redirect(url_for("transactions"))

    return render_template(
        "edit_transaction.html",
        transaction=transaction
    )


@app.route("/delete/<int:id>")
def delete(id):

    transaction = db.get_or_404(Transaction, id)

    db.session.delete(transaction)

    db.session.commit()

    return redirect(url_for("transactions"))


if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(debug=True)