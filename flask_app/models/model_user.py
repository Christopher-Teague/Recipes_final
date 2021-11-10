
##### Rename model_"name" to reflect project #####

# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_bcrypt import Bcrypt
from flask_app import app
from flask_app.models.model_recipe import Recipes

import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

bcrypt = Bcrypt(app)

##### rename 'schema_name' #####
DATABASE_SCHEMA = 'recipes_db'
##### RENAME: class_name(cap first letter), DATABASE_SCHEMA ##### 
##### users, column_name, all_users, new_users_id #####

class Users:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email= data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.recipes = []

# C **************************************************
# C **************************************************
# C **************************************************

    @classmethod
    def create_user(cls, data):
        query = 'INSERT INTO users (first_name, last_name, email, password ) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s)'
        new_users_id = connectToMySQL(DATABASE_SCHEMA).query_db(query,data)

        return new_users_id

# R **************************************************
# R **************************************************
# R **************************************************

    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM users;'
        results = connectToMySQL(DATABASE_SCHEMA).query_db(query)
        all_users = []
        for users in results:
            all_users.append(cls(users))  ### remane cls to CLASS assigned
        return all_users

    @classmethod
    def get_one(cls, data):
        query = 'SELECT * FROM users WHERE id = %(id)s;'
        results = connectToMySQL(DATABASE_SCHEMA).query_db(query, data)
        if not results:
            return results
        return cls(results[0])

    @classmethod
    def get_by_email(cls, data):
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        results = connectToMySQL(DATABASE_SCHEMA).query_db(query, data)
        if len(results) < 1:
            return False

        return Users(results[0])

# U **************************************************
# U **************************************************
# U **************************************************

    @classmethod
    def update_one(cls, **data):
        query = 'UPDATE users SET column_name = %(column_name)s WHERE id = %(id)s'
        return connectToMySQL(DATABASE_SCHEMA).query_db(query, data)

# D **************************************************
# D **************************************************
# D **************************************************

    # @classmethod
    # def delete_one(cls, **data):
    #     query = 'DELETE FROM users WHERE id = %(id)s'
    #     connectToMySQL(DATABASE_SCHEMA).query_db(query, data)
    #     return id

############# one_table, many_table, single_left, single_right, class_right #############

    @classmethod
    def one_with_many(cls, data):
        query = "SELECT * FROM users LEFT JOIN recipes ON recipes.user_id = users.id WHERE users.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        
        user = cls(results[0])
        
        for row_from_db in results:
            recipe_data = {
                'id' : row_from_db['recipes.id'],
                'name' : row_from_db['name'],
                'description' : row_from_db['description'],
                'instructions' : row_from_db['instructions'],
                'under_30' : row_from_db['under_30'],
                'date_made' : row_from_db['date_made'],
                'created_at' : row_from_db['recipes.created_at'],
                'updated_at' : row_from_db['recipes.updated_at'],
                'user_id' : row_from_db['user_id']
            }
            one_recipe = Recipes(recipe_data)
            user.recipes.append(one_recipe)
            print(recipe_data)
        return user


# **************** VALIDATIONS GO HERE****************

    @staticmethod
    def validate_registration(post_data):
        is_valid = True

        if len(post_data['first_name']) < 2:
            flash ("First name must be at least 2 characters!")
            is_valid = False

        if len(post_data['last_name']) < 2:
            flash ("Last name must be at least 2 characters!")
            is_valid = False
        
        # if len(post_data['email']) < 3:
        #     flash ("Email must be at least 2 characters!")
        #     is_valid = False

        if not EMAIL_REGEX.match(post_data['email']):
            flash("invalid email address!")
            is_valid = False
        else:
            user = Users.get_by_email({'email': post_data['email']})
            if user:
                flash("Email is already in use!")
                is_valid = False
        
        if len(post_data['password']) < 2:
            flash ("Password must be at least 2 characters!")
            is_valid = False

        if post_data['password'] != post_data['confirm_password']:
            flash("Passwords do not match!")
            is_valid = False

        return is_valid

    @staticmethod
    def validate_login(post_data):
        
        user = Users.get_by_email({'email': post_data['email']})

        if not user:    
            flash ('User credentials are not valid!')
            return False 
        print(user)
        print(post_data['password'])
        if not bcrypt.check_password_hash(user.password, post_data['password']):
            flash ('User credentials are not valid!')
            return False

        return True