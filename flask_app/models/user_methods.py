from flask_app.config.mysqlconnection import connectToMySQL 
from flask_app import app
from flask import flash
import re
from flask_bcrypt import Bcrypt

regex_email = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

bcrypt = Bcrypt(app)

db_schema = "graduation_in_life"
class Users: 
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.event = []


    @classmethod
    def get_all_users(cls, data):
        query = """
            select * from users;
        """
        return connectToMySQL(db_schema).query_db(query, data)
    
    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) values (%(first_name)s, %(last_name)s, %(email)s, %(password)s, now(),now());
        """
        return connectToMySQL(db_schema).query_db(query, data)

    @staticmethod 
    def users_validation(validation):
        check_user = {"email": validation['email']}
        query = """
            SELECT * FROM users where email = %(email)s;
        """
        result =  connectToMySQL(db_schema).query_db(query, validation)

        isValid = True 
        if result: 
            flash("Email Already Exist", "reg")
            return False
        # if len(validation["email"]) < 1: 
        #     flash("Email must not be blank", "reg")
        #     isValid = False
        # if not regex_email.match(validation["email"], "reg"):
        #     flash("Email does not match", "reg")
        #     isValid = False
        if len(validation["first_name"]) < 3 and len(validation["last_name"]) < 3: 
            flash("First and Last name must be at least 3 characters", "reg")
        if len(validation["password"]) < 8:
            flash("Password at least 8 characters", "reg")
            isValid= False 
        if len(validation["password"]) != validation["confirmPassword"]:
            flash("Password Doesn't match", "reg")
            isValid = False
    
    @classmethod
    def get_email(cls, data):
        query = """
            SELECT * FROM users WHERE email = %(email)s;
        """
        result = connectToMySQL(db_schema).query_db(query, data)
        # checking email if it's  already existed
        if not result:
            return None
        return cls(result[0])
    
    @classmethod
    def get_user(cls, id):
        data = {"id" : id}
        query = """
            SELECT * FROM users WHERE id = %(id)s;
        """
        result = connectToMySQL(db_schema).query_db(query, data)
        # checking email if it's  already existed
        if not result:
            return None
        return cls(result[0])
        

