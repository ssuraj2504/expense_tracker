from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import UserMixin, LoginManager
from datetime import datetime
import app



db = SQLAlchemy()
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow)
    category = db.Column(db.String(50), nullable=False)  # Expense category

    def __repr__(self):
        return f"<Transaction {self.id} - {self.description}: {self.amount}>"
    
with app.app_context():
    db.create_all() # Create tables based on the models
