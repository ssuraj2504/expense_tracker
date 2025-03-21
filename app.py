from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user
from models import db, User, bcrypt, login_manager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key_here'

# Initialize Extensions
db.init_app(app)  # Correctly register the database with the app
bcrypt.init_app(app)
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Account created! Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))

        flash('Invalid credentials. Please try again.', 'danger')

    return render_template('login.html')

# Logout Route
@app.route('/logout')
def logout():
    logout_user()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('home'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Now correctly placed inside app context
    app.run(debug=True)
