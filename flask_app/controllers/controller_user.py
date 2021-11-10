
##### Rename controller_"name" to be in line with project #####

from flask.typing import AfterRequestCallable
from flask_app import app
from flask import render_template, request, redirect, session
from flask_app.models.model_user import Users
from flask_app.models.model_recipe import Recipes

 ### Rename to match model file #####
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    user = Users.get_one({'id': session['uuid']})
    all_recipes = Recipes.get_all()
    return render_template('dashboard.html', user = user, all_recipes = all_recipes)

@app.route('/logout')
def logout():
    del session['uuid'] 
    
    return redirect('/')

# C **************************************************
# C **************************************************
# C **************************************************

@app.route('/register', methods = ['POST'])
def register_user():
    if not Users.validate_registration(request.form):    
    
        return redirect('/')

    hashword = bcrypt.generate_password_hash(request.form['password'])
    data = {
        **request.form,
        'password' : hashword
    }
    
    user_id = Users.create_user(data)
    session['uuid'] = user_id

    return redirect("/dashboard")


@app.route('/login', methods=['POST'])
def login():
    if not Users.validate_login(request.form):
        return redirect('/')

    user = Users.get_by_email({'email' : request.form['email']})

    session['uuid'] = user.id

    return redirect ('/dashboard')


# @app.route('/user/create', methods=['POST'])
# def create_user():
#     return redirect('/')

# R **************************************************
# R **************************************************
# R **************************************************

@app.route('/user/show_all')
def get_all_user():
    return 'get all user'

@app.route('/user/<int:id>')
def get_one_user():
    return 'get one user'


# U **************************************************
# U **************************************************
# U **************************************************

@app.route('/user/<int:id>/edit')
def edit_user():
    return render_template('/')

@app.route('/user/<int:id>/update', methods=['POST'])
def update_one_user():
    return redirect('/')

# D **************************************************
# D **************************************************
# D **************************************************

@app.route('/user/<int:id>/delete')
def delete_one_user():
    return 'delete one user'