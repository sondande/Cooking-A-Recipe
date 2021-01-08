from flask_login import UserMixin
from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique= True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

    #ingredients = db.relationship("Ingredients", secondary="recipes")
    ingredients = db.relationship('Recipes', backref='user', lazy=True)

    def set_name(self, name):
        self.name = name

    def set_email(self, email):
        self.email = email

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_password(self):
        return self.password

class Recipes(db.Model):
    __tablename__ = 'recipes'
    id = db.Column(db.Integer, primary_key=True)
    Recipe_Title = db.Column(db.String(100), nullable=False)
    Recipe_Author = db.Column(db.String(1000))
    Recipe_Type = db.Column(db.String(20), nullable=False)
    Recipe_Img= db.Column(db.String(500), nullable =False)
    Recipe_Ingredients = db.Column(db.Text, nullable=False)
    Recipe_Instructions = db.Column(db.Text, nullable=False)
    Recipe_Expected_Prep_Time = db.Column(db.String(50), nullable=False)
    Recipe_Time_Prep = db.Column(db.String(20), nullable=False)
    Recipe_Expected_Cook_Time = db.Column(db.String(50), nullable=False)
    Recipe_Time_Cook = db.Column(db.String(20), nullable=False)
    Recipe_Date_Posted = db.Column(db.DateTime, nullable = False, default=datetime.today)
    Recipe_Public_Status = db.Column(db.String(20), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"{self.Recipe_Title}"
    #user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    #product_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'))

    #user = db.relationship('User', backref=backref("recipes", cascade="all, delete-orphan"))
    #ingredient = db.relationship('Ingredients', backref=backref("recipes", cascade="all, delete-orphan"))

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ingredient_name = db.Column(db.String(40), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Recipe('{self.ingredient_name}')"
#class Ingredients(UserMixin, db.Model):
    #__tablename__ = 'ingredients'
    #id = db.Column(db.Integer, primary_key=True)
    #ingredient = db.Column(db.String(100), nullable=False)

    #users = db.relationship("User", secondary="recipes")
