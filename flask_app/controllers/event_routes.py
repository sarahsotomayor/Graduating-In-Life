from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models import events_methods, user_methods

# todo add homepage template
# Homepage
@app.route("/")
def index():
    return render_template("homepage.html")

#Read
# todo add events template showing all events
# Show All Events
@app.route("/events")
def all_events():
    data = {
        "id" : session['user_id'],
    }
    return render_template("", all_events = events_methods.Events.get_all_events())

#Render Create
# todo add new event form template
# New Event Form
@app.route("/events/new")
def create_event():
    if 'user_id' not in session:
        return redirect("/")
    return render_template("create.html ")

#Create
# Process New Event Form
@app.route("/events/create", methods = ["POST"])
def create_event_process():
    if 'user_id' not in session:
        return redirect("/")
    if not events_methods.Events.validate_event(request.form):
        print("Could Not Save Event")
        return redirect("/events/new")
    data={
        "user_id" : session['user_id'],
        "name" : request.form['name'],
        "date" : request.form['date'],
        "time" : request.form['time'],
        "location" : request.form['location'],
        "description" : request.form['description'],
    }
    events_methods.Events.save(data)
    print("Event Saved", "request.form", request.form)
    return redirect("/events")

#Read
# todo need get_one_event method in events_methods.py
# todo add view event template
# View Event: user can only view event details if logged in
@app.route("/events/<int:id>")
def view_event(id):
    if 'user_id' not in session:
        return redirect("/")
    session['event_id'] = id
    data = {
        "id" : id
    }
    return render_template("vew.html", event = events_methods.Events.get_one_event(data))

#Render  Update
# todo need get_one_event method in events_methods.py
# todo add edit event template
# Edit Event: user can only edit event if logged in and user(admin) created event
@app.route("/events/edit/<int:id>")
def edit_event(id):
    if 'user_id' not in session:
        return redirect("/")
    data = {
        "id" : id
    }
    return render_template("edit.html", event = events_methods.Events.get_one_event(data))

#Update
# Process Edit Event Form
@app.route("/events/update/<int:id>", methods = ["POST"])
def edit_event_process(id):
    if 'user_id' not in session:
        return redirect("/")
    data = {
        "id" : id,
        "name" : request.form['name'],
        "date" : request.form['date'],
        "time" : request.form['time'],
        "location" : request.form['location'],
        "description" : request.form['description'],
        "user_id" : request.form['user_id']
    }
    events_methods.Events.update_events(data)
    print("request.form", request.form)
    return redirect ("/events")


# Delete Event
@app.route("/event/delete/<int:id>")
def delete_event(id):
    if 'user_id' not in session:
        return redirect("/")
    events_methods.Events.destroy({"id": id})
    print("event deleted")
    return redirect ("/events")