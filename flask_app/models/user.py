from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    DB = "provimi"
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.confirmpassword = data['confirmpassword']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def add(cls,data):
        query = "insert into users (first_name,last_name,email,password,confirmpassword) values(%(first_name)s, %(last_name)s, %(email)s, %(password)s, %(confirmpassword)s);"
        result = connectToMySQL(cls.DB).query_db(query,data)
        return result
    
    @classmethod
    def get_all_users(cls):
        query = "select * from users left join books;"
        result = connectToMySQL(cls.DB).query_db(query)
        users = []
        if result:
            for user in users:
                users.append(user)
            return users
        return users

    @classmethod
    def get_user_by_email(cls,data):
        query = "select * from users where email = %(email)s;"
        result = connectToMySQL(cls.DB).query_db(query,data)
        if result:
            return result[0]
        return False
    
    @classmethod
    def get_user_by_id(cls,data):
        query = "select * from users where id = %(id)s;"
        result = connectToMySQL(cls.DB).query_db(query,data)
        if result:
            return result[0]
        return False
    
    @classmethod
    def get_user_by_user_id(cls, data):
        query = 'SELECT * FROM users where id = %(user_id)s;'
        result = connectToMySQL(cls.DB).query_db(query, data)
        if result:
            return result[0]
        return False
    
    @classmethod
    def update(cls, data):
        query ="UPDATE users set first_name = %(first_name)s, last_name = %(last_name)s WHERE id = %(id)s;"
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM users where id = %(id)s;"
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @staticmethod
    def validate_userRegister(user):
        is_valid = True
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", 'emailRegister')
            is_valid = False

        if len(user['password']) <= 1:
            flash("Password is required!", 'passwordRegister')
            is_valid = False
        elif len(user['password']) < 8:
            flash("Password must be at least 8 characters!", 'passwordRegister')
            is_valid = False
        elif not any(char.isdigit() for char in user['password']):
            flash("Password must contain at least 1 number!", 'passwordRegister')
            is_valid = False
        elif not any(char.isupper() for char in user['password']):
            flash("Password must contain at least 1 uppercase letter!", 'passwordRegister')
            is_valid = False
            
        if len(user['confirmpassword'])<=1 or user['confirmpassword'] != user['password']:
            flash("Confirm password is incorrect!", 'passwordConfirm')
            is_valid = False
        if len(user['first_name'])<2:
            flash("First name is required!", 'nameRegister')
            is_valid = False
        if len(user['last_name'])<2:
            flash("Last name is required!", 'lastNameRegister')
            is_valid = False
        return is_valid


    @staticmethod
    def validate_user(user):
        is_valid= True
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", 'emailLogin')
            is_valid = False
        if len(user['password'])<1:
            flash("Password is required!", 'passwordLogin')
            is_valid = False
        return is_valid

    
    @staticmethod
    def validate_userUpdate(user):
        is_valid = True
        if len(user['first_name'])<1:
            flash("First name is required!", 'first_nameUpdate')
            is_valid = False
        if len(user['last_name'])<1:
            flash("Last name is required!", 'last_nameUpdate')
            is_valid = False
        if len(user['email'])<1:
            flash("Email is required!", 'emailUpdate')
            is_valid = False
        return is_valid