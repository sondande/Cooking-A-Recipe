from flask_login import UserMixin
from sqlalchemy.orm import backref
from . import db
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id=db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique= True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

    #ingredients = db.relationship("Ingredients", secondary="recipes")
    ingredients = db.relationship('Recipes', backref='user', lazy=True)
    def __repr__(self):
        return f"User('{self.username}', '{self.email})"

class Recipes( db.Model):
    __tablename__ = 'recipes'
    id = db.Column(db.Integer, primary_key=True)
    Recipe_Title = db.Column(db.String(100), nullable=False)
    Recipe_Type = db.Column(db.String(20), nullable=False)
    #Recipe_Ingredients = db.relationship('Ingredients', backref='recipe')
    Recipe_Ingredients = db.Column(db.Text, nullable=False)
    Recipe_Instructions = db.Column(db.Text, nullable=False)
    Recipe_Expected_Prep_Time = db.Column(db.String(50))
    Recipe_Expected_Cook_Time = db.Column(db.String(50))
    Recipe_Date_Posted = db.Column(db.DateTime, nullable = False, default=datetime.utcnow)

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
