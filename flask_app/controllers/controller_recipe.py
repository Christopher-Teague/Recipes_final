
##### Rename controller_"name" to be in line with project #####

from flask_app import app
from flask import render_template, request, redirect, session
from flask_app.models.model_user import Users ##### Rename to match model file #####
from flask_bcrypt import Bcrypt
from flask_app.models import model_recipe, model_user
bcrypt = Bcrypt(app)


# C **************************************************
# C **************************************************
# C **************************************************

@app.route('/recipe/new') 
def new_recipe():
    user = Users.get_one({'id': session['uuid']})
    return render_template('recipe_new.html', user = user)

@app.route('/recipe/create', methods=['POST'])
def create_recipe():
    recipe_data = {
        **request.form,
        'user_id' : session['uuid']         
    }

    is_valid = model_recipe.Recipes.validate_recipe(request.form)
    
    if not is_valid:
        return redirect('/recipe/new')

    model_recipe.Recipes.create_recipe(recipe_data)
    return redirect('/dashboard')

# R **************************************************
# R **************************************************
# R **************************************************

@app.route('/recipe/show_all')
def get_all_recipe():
    return 'get all recipe'

@app.route('/recipe/<int:id>')
def get_one_recipe(id):
    context = {
        'user' : model_user.Users.get_one({'id' : session['uuid']}),
        'recipe' : model_recipe.Recipes.get_one({'id' : id})
    }
    
    return render_template ('/recipe_show.html', **context)


# U **************************************************
# U **************************************************
# U **************************************************

@app.route('/recipe/<int:id>/edit')
def edit_recipe(id):
    context = {
        'user' : model_user.Users.get_one({'id' : session['uuid']}),
        'recipe' : model_recipe.Recipes.get_one({'id' : id})
    }
    return render_template('/recipe_edit.html', **context)

@app.route('/recipe/<int:id>/update', methods=['POST'])
def update_recipe(id):
    recipe_data = {
        **request.form,
        'user_id' : session['uuid']         
    }

    is_valid = model_recipe.Recipes.validate_recipe(request.form)

    if not is_valid:
        return redirect('/recipe/<int:id>/edit')

    model_recipe.Recipes.update_recipe(recipe_data)
    return redirect('/dashboard')

# D **************************************************
# D **************************************************
# D **************************************************

@app.route('/recipe/<int:id>/delete')
def delete_one_recipe(id):
    model_recipe.Recipes.delete_one({'id' : id})
    return redirect('/dashboard')