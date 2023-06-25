from flask_app import app 
# todo importing the controllers file at server.py
from flask_app.controllers import event_routes, user_routes




if __name__ == "__main__":
    app.run(debug=True)