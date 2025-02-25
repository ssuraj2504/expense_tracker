from flask import Flask, render_template, request, redirect, url_for
from models import db, Transaction

app = Flask(__name__)

# Configure the database (using SQLite for simplicity)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)

# Ensure tables are created before running the app
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        amount = request.form['amount']
        description = request.form['description']
        category = request.form['category']

        if amount and description:
            new_transaction = Transaction(amount=float(amount), description=description, category=category)
            db.session.add(new_transaction)
            db.session.commit()

    transactions = Transaction.query.all()
    total_income = sum(t.amount for t in transactions if t.category == 'Income')
    total_expense = sum(t.amount for t in transactions if t.category != 'Income')
    balance = total_income - total_expense

    return render_template("home.html", transactions=transactions, total_income=total_income, total_expense=total_expense, balance=balance)

@app.route('/delete/<int:id>')
def delete_transaction(id):
    transaction = Transaction.query.get(id)
    if transaction:
        db.session.delete(transaction)
        db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
