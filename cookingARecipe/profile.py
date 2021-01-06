from flask import Blueprint, render_template, redirect, request
from flask.helpers import url_for
from flask_login import login_required, current_user
from . import db
from .models import Recipes

profile = Blueprint('profile', __name__, url_prefix='/loggedin')

@profile.route('/profile')
@login_required
def profilePage():
    return render_template('profile.html', name= current_user.name)

@profile.route('/viewrecipes', methods=['GET'])
@login_required
def viewRecipes():
    all_recipes = Recipes.query.order_by(Recipes.Recipe_Date_Posted).all()
    return render_template('viewrecipes.html', recipes= all_recipes)

@profile.route('/viewrecipes/<int:id>')
@login_required
def viewRecipeDetails(id):
    recipe_id= Recipes.query.get_or_404(id)
    return render_template('viewR.html', recipe=recipe_id)

@profile.route('/addrecipe', methods=['POST', 'GET'])
@login_required
def addRecipe():
    if request.method == 'POST':
        recipe_title = request.form['Recipe_Title']
        recipe_type= request.form['type-of-meal']
        recipe_ingredients= request.form['ingredients']
        recipe_instructions=request.form['instructions']
        recipe_expected_prep_time=request.form['prep']
        recipe_expected_cook_time = request.form['cook']
        new_recipe= Recipes(Recipe_Title=recipe_title, Recipe_Type=recipe_type, Recipe_Ingredients=recipe_ingredients, Recipe_Instructions=recipe_instructions, Recipe_Expected_Prep_Time = recipe_expected_prep_time, Recipe_Expected_Cook_Time= recipe_expected_cook_time)
        db.session.add(new_recipe)
        db.session.commit()
        return redirect(url_for('profile.viewRecipes'))
    else:
        return render_template('addrecipe.html')

#@profile.route("/addrecipes-ingredients", methods=['POST'])
#@login_required
#def addrecipesIngredients():
#    if request.method == 'POST':
#        ingredientInput = request.form['ingredientsInput']

#        return redirect(url_for("profile.addRecipe"))
