from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models import user_methods
from flask import flash, session, render_template, redirect, request

@app.route("/register")
def register_user():
    return render_template("registration.html")

@app.route("/register", methods=["POST"])
def register():

    if user_methods.Users.users_validation(request.form):
        create_acc = { 
            "first_name":request.form["first_name"],
            "last_name":request.form["last_name"],
            "email":request.form["email"],
            "password":bcrypt.generate_password_hash(request.form["password"])
        }
        users_id = user_methods.Users.save(create_acc)
        session["user_id"] = users_id
        return redirect("/events ")
    else:
        return redirect("/register")

@app.route("/login")
def logIn_user():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def logIn():
    print("\n___Check Login__")
    print("\n___Request.form__", request.form)
    logIn_acc = { 
        "email":request.form["email"],
        "password":request.form["password"]
    }
    user_in_db = user_methods.Users.get_email(logIn_acc)
    print("\n___ User_in_db __",user_in_db)
    if not user_in_db:
        flash("Invalid Email / Password" , 'log')
        return redirect("/login")

    if not bcrypt.check_password_hash(user_in_db.password, request.form["password"]):
        print("\n___Password Invalid__")
        flash("Invalid Email / Password" , 'log')
        return redirect("/login")   
    print("\n___Login and Password valid???__")
    session["user_id"] = user_in_db.id
    return redirect ("/events")

@app.route("/logout")
def logout_user():
    if 'user_id' not in session:
        return redirect("/")
    session.clear()
    print("User logged out")
    return redirect("/")
