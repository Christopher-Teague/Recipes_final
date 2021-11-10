
##### Rename model_"name" to reflect project #####

# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_bcrypt import Bcrypt
from flask_app import app

import re	# the regex module
# create a regular expression object that we'll use later   
# EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

# bcrypt = Bcrypt(app)

##### rename 'schema_name' #####
DATABASE_SCHEMA = 'recipes_db'
##### RENAME: class_name(cap first letter), DATABASE_SCHEMA ##### 
##### recipes, column_name, all_recipes, new_recipes_id #####

class Recipes:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.under_30 = data['under_30']
        self.date_made = data['date_made']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        

# C **************************************************
# C **************************************************
# C **************************************************

    @classmethod
    def create_recipe(cls, data):
        query = 'INSERT INTO recipes (name, description, instructions, under_30, date_made, user_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(under_30)s, %(date_made)s, %(user_id)s)'
        print(data)
        new_recipes_id = connectToMySQL(DATABASE_SCHEMA).query_db(query,data)

        return new_recipes_id

# R **************************************************
# R **************************************************
# R **************************************************

    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM recipes;'
        results = connectToMySQL(DATABASE_SCHEMA).query_db(query)
        all_recipes = []
        for recipes in results:
            all_recipes.append(cls(recipes))  ### remane cls to CLASS assigned
        return all_recipes

    @classmethod
    def get_one(cls, data):
        query = 'SELECT * FROM recipes WHERE id = %(id)s;'
        results = connectToMySQL(DATABASE_SCHEMA).query_db(query, data)
        if not results:
            return results
        return cls(results[0])

# U **************************************************
# U **************************************************
# U **************************************************

    @classmethod
    def update_recipe(cls, data):
        query = 'UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, date_made = %(date_made)s WHERE id = %(id)s'
        return connectToMySQL(DATABASE_SCHEMA).query_db(query, data)

# D **************************************************
# D **************************************************
# D **************************************************

    @classmethod
    def delete_one(cls, data):
        query = 'DELETE FROM recipes WHERE id = %(id)s'
        connectToMySQL(DATABASE_SCHEMA).query_db(query, data)
        return id


# **************** VALIDATIONS GO HERE****************

    @staticmethod
    def validate_recipe(post_data):
        is_valid = True

        if len(post_data['name']) < 3:
            flash ("Name must be at least 3 characters!")
            is_valid = False

        if len(post_data['description']) < 3:
            flash ("Description must be at least 3 characters!")
            is_valid = False
        
        if len(post_data['instructions']) < 3:
            flash ("Instructions must be at least 3 characters!")
            is_valid = False
        
        if  len(post_data['date_made']) < 3:
            flash ("Must input a date!")
            is_valid = False
        
        return is_valid