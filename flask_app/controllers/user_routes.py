from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models import user_methods
from flask import flash, session, render_template, redirect, request

# todo need to return a template and redirected in register route
@app.route("/register")
def register_user():
    return render_template("registration.html ")

@app.route("/register", methods=["POST"])
def register():

    create_acc = { 
        "first_name":request.form["first_name"],
        "last_name":request.form["last_name"],
        "email":request.form["email"],
        "password":bcrypt.generate_password_hash(request.form["password"]),
        "created_at":request.form["created_at"]
    }
    users_id = user_methods.Users.save(create_acc)
    session["user_id"] = users_id
    return redirect("/events ")

@app.route("/login")
def logIn_user():
    return render_template("login.html")

#todo redirect to the 
@app.route("/login", methods=["POST"])
def logIn():

    logIn_acc = { 
        "email":request.form["email"],
        "password":request.form["password"]
    }
    user_inf = user_methods.Users.get_email(logIn_acc)
    if not user_inf:
        flash("Invalid Email / Password" , 'log')
        return redirect(" /login")

    if not bcrypt.check_password_hash(logIn_acc.password, request.form["password"]):
        flash("Invalid Email / Password" , 'log')
        return redirect("/login")   
    session["users_id"] = logIn_acc.id
    return redirect ("/events")

@app.route("/logout")
def logout_user():
    if 'user_id' not in session:
        return redirect("/")
    session.clear()
    print("User logged out")
    return redirect("/")