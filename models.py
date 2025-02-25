from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow)
    category = db.Column(db.String(50), nullable=False)  # Expense category

    def __repr__(self):
        return f"<Transaction {self.id} - {self.description}: {self.amount}>"
