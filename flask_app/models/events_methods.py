from flask_app.config.mysqlconnection import connectToMySQL

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
def get_all_events(cls):
    query ="""
        SElECT * FROM users JOIN events on users.id = events.maker_id
    """
    result = connectToMySQL(db_schema).query_db(query)

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
            "id": row["events.id"],
            "name": row["name"],
            "date":row["date"],
            "time":row["time"],
            "location":row["location"],
            "description":row["description"],
            "created_at": row["events.created_at"],
            "updated_at":row["events.updated_at"]
        })
    one_events.creator = one_user
    all_events.append(one_events)
    return all_events

@classmethod
def save(cls, data):
    query = """
        INSERT INTO events(name, date, time, location, description, created_at) VALUES (%(name)s, %(date)s, %(time)s, %(location)s, now());
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

    