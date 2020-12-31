from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User

auth = Blueprint("auth", __name__, static_folder="static", template_folder="templates")

@auth.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email=request.form.get('email')
        username=request.form.get('username')
        password=request.form.get('password')
        if request.form.get('remember'):
            rememberResult=True
        else:
            rememberResult=False

        user = User.query.filter_by(email=email).first()

        if not username or not check_password_hash(user.password, password):
            flash('Account already exists with that email')
            return redirect(url_for('auth.register'))

        login_user(user, remember=rememberResult)
        return redirect(url_for('main.profile'))
    else:
        return render_template("login.html")

@auth.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        email=request.form.get('email')
        username=request.form.get('username')
        password=request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Account already exists with that email')
            return redirect(url_for('auth.register'))

        #sha256 is a hash encryption method to hide the user's password through making the code encrypted
        new_user = User(email=email, username=username, password=generate_password_hash(password), method='sha256')
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    else:
        return render_template("register.html")

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
