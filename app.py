from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

expenses = []


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
    app.run(debug=True)