from flask import Blueprint, render_template
from flask_login import current_user, login_required

main = Blueprint("main", __name__)

@main.route('/')
def index():
    return render_template("index.html")

#current_user allows us to keep track of the current user that is logged in
@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name= current_user.name)
