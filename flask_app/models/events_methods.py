from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user_methods import Users

db_schema = "Graduation_In_Life"

class Events: 
    def __init__(self, data) :
        self.id = data["id"]
        self.name = data["name"]
        self.date = data["date"]
        self.time = data["time"]
        self.location = data["location"]
        self.description = data["description"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.maker_id = data["maker_id"]
        self.creator = None

    @classmethod
    def validate_event(self, data):
        is_valid = True
        if len(data['name']) < 3:
            is_valid = False
            flash("Name cannot be less than 3 characters", "recipe")
        if len(data['description']) < 4:
            is_valid = False
            flash("Description must be at least 4 characters", "recipe")
        if len(data['location']) < 3: 
            is_valid = False
            flash("Location must be at least 4 characters", "recipe")
        return is_valid

    @classmethod
    def get_all_events(cls):
        query ="""
            SElECT * FROM events inner join users on events.maker_id = users.id;
        """
        result = connectToMySQL(db_schema).query_db(query)
        print("---A---")
        print(result)

        all_events = []
        for row in result: 
            one_user = Users({
                "id":row["users.id"],
                "first_name":row["first_name"],
                "last_name":row["last_name"],
                "email":row["email"],
                "password": " ",
                "created_at":row["users.created_at"],
                "updated_at":row["users.updated_at"]
            })
            one_events = Events({
                "id": row["id"],
                "name": row["name"],
                "date":row["date"],
                "time":row["time"],
                "location":row["location"],
                "description":row["description"],
                "created_at": row["created_at"],
                "updated_at":row["updated_at"],
                "maker_id":row["maker_id"]
            })
            one_events.creator = one_user
            all_events.append(one_events)
        return all_events


    @classmethod
    def get_one_event(cls, data):
        query = """
            SELECT * FROM events 
            JOIN users_has_events on users_has_events.event_id = users_has_events.user_id
            LEFT JOIN users on users.id = users_has_events.user_id where events.id =%(id)s;
        """
        result = connectToMySQL(db_schema).query_db(query, data)
        if result < 1: 
            return False
        
        result = result[0]
        one_event = Events({
            "id":result["events.id"],
            "name":result["name"],
            "date":result["date"],
            "time":result["time"],
            "location":result["location"],
            "description":result["description"],
            "created_at":result["events.created_at"],
            "updated_at":result["events.updated_at"],
        })
    
        event = Events(one_event)
        for row in result: 
            event.creator.append(cls(row))
        return event


    @classmethod 
    def destroy(cls, data):
        query = """
            DELETE FROM events where id = %(id)s;
        """
        return connectToMySQL(db_schema).query_db(query, data)

    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO events(name, date, time, location, description, created_at, maker_id) VALUES (%(name)s, %(date)s, %(time)s, %(location)s, %(description)s, now() , %(maker_id)s);
        """
        return connectToMySQL(db_schema).query_db(query, data)

    @classmethod
    def update_events(cls, data): 
        query = """
            UPDATE events SET name = %(name)s,
            date = %(date)s, time = %(time)s,
            %(location)s, updated_at = now() where events.id = %(id)s;
        """
        return connectToMySQL(db_schema).query_db(query,data)

    @classmethod 
    def destroy(cls, data):
        query = """
            DELETE FROM events where id = %(id)s;
        """

    @classmethod
    def get_one_event(cls, data):
        query = "SELECT * FROM events JOIN users ON events.user_id = users.id WHERE events.id=%(id)s;"
        results = connectToMySQL(db_schema).query_db(query, data)
        event_object = cls(results[0])
        user_dictionary = {
                    "id" : results[0]['users.id'],
                    "first_name" : results[0]['first_name'],
                    "last_name" : results[0]['last_name'],
                    "email" : results[0]['email'],
                    "password" : results[0]['password'],
                    "created_at" : results[0]['users.created_at'],
                    "updated_at" : results[0]['users.updated_at']
                }
        user_object = Users(user_dictionary)
        event_object.user = user_object
        return event_object