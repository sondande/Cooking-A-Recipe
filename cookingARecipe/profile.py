from flask import Blueprint, render_template, redirect, request, session, flash, url_for
from flask.globals import current_app
from flask_login import login_required, current_user
from . import db
from .models import User, Recipes
import os
from werkzeug.utils import secure_filename

profile = Blueprint('profile', __name__, url_prefix='/loggedin')

@profile.route('/profile', methods=['POST', 'GET'])
@login_required
def profilePage():
    user = User.query.get(session['uid'])
    if request.method == 'POST':
        user_email = request.form['User-Email']
        old_password = request.form['User-Old-Password']
        new_password = request.form['User-New-Password']
        user_name = request.form['User-Name']

        if user.check_password(old_password):
            user.set_name(user_name)
            user.set_email(user_email)
            user.set_password(new_password)
            flash("New Password: " + user.get_password())
        else:
            flash("Old password entered is invalid. Try again")
            return render_template('profile.html', user=user)

        db.session.commit()

        #return render_template('profile.html', user=user)
        return redirect(url_for('profile.profilePage'))
    else:
        return render_template('profile.html', user=user)

@profile.route('/viewmyrecipes', methods=['GET'])
@login_required
#View current user's recipes
def viewMyRecipes():
    user = User.query.get(session['uid'])
    all_recipes = Recipes.query.filter(Recipes.Recipe_Author == user.name ).all()
    return render_template('viewMyrecipes.html', recipes=all_recipes)

@profile.route('/viewrecipes', methods=['GET'])
@login_required
#View all recipes that are labeled as public
def viewRecipes():
    all_recipes = Recipes.query.filter(Recipes.Recipe_Public_Status == "Public").all()
    return render_template('viewrecipes.html', recipes= all_recipes)

@profile.route('/viewrecipes/<int:id>')
@login_required
#view recipes current user created
def viewRecipeDetails(id):
    user= User.query.get(current_user.id)
    recipe= Recipes.query.get_or_404(id)
    filename=recipe.Recipe_Img
    return render_template('viewR.html', filename=filename,recipe=recipe, user=user)

@profile.route('/addrecipe', methods=['POST', 'GET'])
@login_required
def addRecipe():
    user = User.query.get(current_user.id)
    if request.method == 'POST':
        recipe_title = request.form['Recipe_Title']
        recipe_author = user.name
        recipe_type= request.form['type-of-meal']
        recipe_ingredients= request.form['ingredients']
        recipe_instructions=request.form['instructions']
        recipe_expected_prep_time = request.form['prep']
        recipe_time_prep= request.form['time_prep']
        recipe_expected_cook_time = request.form['cook']
        recipe_time_cook= request.form['time_cook']
        recipe_status= request.form['status']

        if request.files:
            image = request.files["file"]
            filename = secure_filename(image.filename)
            image.save(os.path.join(current_app.config["IMAGE_UPLOADS"], filename))
        else:
            flash("That file extension is not allowed")
            return redirect(request.url)

        new_recipe= Recipes(Recipe_Title=recipe_title, Recipe_Author=recipe_author , Recipe_Img=filename ,Recipe_Type=recipe_type, Recipe_Ingredients=recipe_ingredients, Recipe_Instructions=recipe_instructions, Recipe_Expected_Prep_Time = recipe_expected_prep_time, Recipe_Time_Prep=recipe_time_prep, Recipe_Time_Cook=recipe_time_cook, Recipe_Expected_Cook_Time= recipe_expected_cook_time, Recipe_Public_Status=recipe_status)
        db.session.add(new_recipe)
        db.session.commit()
        return redirect(url_for('profile.viewMyRecipes'))
    else:
        return render_template('addrecipe.html')

@profile.route('/viewrecipes/edit/<int:id>', methods=['POST', 'GET'])
@login_required
def editRecipe(id):
    recipe= Recipes.query.get_or_404(id)
    if request.method == 'POST':
        recipe.Recipe_Title = request.form['Recipe_Title']
        recipe.Recipe_Type = request.form['type-of-meal']
        recipe.Recipe_Ingredients = request.form['ingredients']
        recipe.Recipe_Instructions =request.form['instructions']
        recipe.Recipe_Expected_Prep_Time = request.form['prep']
        recipe.Recipe_Time_Prep = request.form['time_prep']
        recipe.Recipe_Expected_Cook_Time = request.form['cook']
        recipe.Recipe_Time_Cook = request.form['time_cook']
        recipe.Recipe_Public_Status = request.form['status']
        db.session.commit()
        return redirect(url_for('profile.viewMyRecipes'))
    else:
        return render_template('editRecipe.html', recipe=recipe)

@profile.route('/viewrecipes/<int:id>/delete')
@login_required
def deleteRecipe(id):
    recipe= Recipes.query.get_or_404(id)
    db.session.delete(recipe)
    db.session.commit()
    return redirect(url_for('profile.viewMyRecipes'))

def allowed_image(filename):

    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in current_app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


def allowed_image_filesize(filesize):

    if int(filesize) <= current_app.config["MAX_IMAGE_FILESIZE"]:
        return True
    else:
        return False

@profile.route('/display/<filename>')
def display_image(filename):
	#print('display_image filename: ' + filename)
	return redirect(url_for('static', filename=filename), code=301)

#@profile.route("/addrecipes-ingredients", methods=['POST'])
#@login_required
#def addrecipesIngredients():
#    if request.method == 'POST':
#        ingredientInput = request.form['ingredientsInput']

#        return redirect(url_for("profile.addRecipe"))
