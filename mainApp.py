import re
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLAlCHEMY_DATABASE_URI']= 'sqlite:///cooking.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return 'User: ' + str(self.userName)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        return redirect('Dashboard.html')
    return render_template('login.html')

@app.route('/<string:user>/<int:id>/dashboard', methods=['POST', 'GET'])
def dashboard(user, id):
    if request.method == 'POST':
        return redirect('Dashboard.html')
    return render_template('login.html')

@app.route('/<string:user>/<int:id>/viewRecipes')
def viewRecipes(user, id):
    return render_template('viewRecipes')

@app.route('/<string:user>/<int:id>/editRecipes')
def editRecipes(user, id):
    return render_template('editRecipes')

@app.route('/<string:user>/<int:id>/editRecipes')
def deleteRecipes(user, id):
    return redirect('/<string:user>/<int:id>/viewRecipes)')

@app.route('/login')
def profile():
    return render_template('profile.html')

if __name__ == '__main__':
    app.run(debug=True)
