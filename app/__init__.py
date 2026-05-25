#===========================================================
# APP NAME HERE
# By YOUR NAME HERE
#===========================================================

from flask import Flask, request, session, render_template, flash, redirect, send_file, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from os import getenv
from io import BytesIO
import html
from app.helpers import *


# Create the app
app = Flask(__name__)


#===========================================================
# App Routes Handlers
#===========================================================
@app.get("/")
def show_welcome():
    return render_template("pages/welcome.jinja")
#-----------------------------------------------------------
# Signup Page
#-----------------------------------------------------------
@app.get("/user/new")
def show_signup_form():
    return render_template("pages/user_form.jinja")

#-----------------------------------------------------------
# Login Page
#-----------------------------------------------------------
@app.get("/user/login")
def show_login_form():
    return render_template("pages/login_page.jinja")

#-----------------------------------------------------------
# New Message Page
#-----------------------------------------------------------
@app.get("/message/new")
def show_message_form():
    return render_template("pages/message_form.jinja")

#-----------------------------------------------------------
# Handle user signup
#-----------------------------------------------------------
@app.post("/user")
def add_user():
    forename = request.form.get('forename', '').strip()
    surname  = request.form.get('surname',  '').strip()
    username = request.form.get('username', '').strip().lower()
    password = request.form.get('password', '').strip()

    with connect_db() as db:
        sql = "SELECT id FROM users WHERE username=?"
        params = (username,)
        user = db.execute(sql, params).fetchone()

        if user:
            flash(f"Username '{username}' already exists", "error")
            return redirect("/user/new")

        password_hash = generate_password_hash(password)

        sql = """
            INSERT INTO users (forename, surname, username, password_hash)
            VALUES (?, ?, ?, ?)
        """
        params = (forename, surname, username, password_hash)
        db.execute(sql, params)

        flash("Account created. Please login", "success")
        return redirect("/user/login")

#-----------------------------------------------------------
# Handle user login
#-----------------------------------------------------------
    
@app.post("/login")
def login_user():
    username = request.form.get('username', '').strip().lower()
    password = request.form.get('password', '').strip()

    with connect_db() as db:
        sql = """
            SELECT id, forename, surname, password_hash
            FROM users
            WHERE username=?
        """
        params = (username,)
        user = db.execute(sql, params).fetchone()

        if not user:
            flash(f"Unknown user", "error")
            return redirect("/user/login")

        if not check_password_hash(user["password_hash"], password):
            flash(f"Incorrect password", "error")
            return redirect("/user/login")

        session["logged_in"] = True
        session["user"] = {
            "id":       user["id"],
            "username": username,
            "forename": user["forename"],
            "surname":  user["surname"],
        }

        flash("Login successful", "success")
        return redirect("/")
    
#-----------------------------------------------------------
# Handle user message
#-----------------------------------------------------------
    
@app.post("/message")
def add_message():
    # Get form data
    title    = request.form.get('title', '').strip()
    body     = request.form.get('body', '').strip()

    # Validate data
    if not title:
        flash("Title is required", "error")
        return redirect("/message/new")

    if len(title) > 40:
        flash("Title is too long (max 40 chars)", "error")
        return redirect("/message/new")

    # Escape text inputs
    title = html.escape(title)
    body = html.escape(body)

    # User id is in the session
    user_id = session["user"]["id"]

    # Add to the database
    with connect_db() as db:
        sql = """
            INSERT INTO messages (title, body, user_id)
            VALUES (?, ?, ?)
        """
        params = (title, body, user_id)
        db.execute(sql, params)

        flash(f"Message added")
        return redirect("/")
    
#-----------------------------------------------------------
# See all the messages
#-----------------------------------------------------------

@app.get("/messages")
def show_all_messages():
    with connect_db() as db:
        sql = """
            SELECT id, title, body
            FROM messages
        """
        params = ()
        messages = db.execute(sql, params).fetchall()

        return render_template("pages/message_list.jinja", messages=messages)
    

#-----------------------------------------------------------
# Delete a message
#-----------------------------------------------------------

@app.get("/delete/<int:id>")
def delete_a_message(id):
    with connect_db() as client:

        sql = "DELETE FROM messages WHERE id=? AND user_id=?"
        params = [id, user_id]
        client.execute(sql, params)

        # Go back to the home page
        flash("Message deleted", "success")
        return redirect("/messages")

#-----------------------------------------------------------
# login_required decorator to required routes
#-----------------------------------------------------------
    
@app.get("/admin")
@login_required
def admin_page():
    # Can only access this route if logged in
    ...

#-----------------------------------------------------------
# Handle user logout
#-----------------------------------------------------------

@app.get("/logout")
def logout_admin():
    session.clear()
    flash(f"You have been logged out", "success")
    return redirect("/")
#-----------------------------------------------------------
# Creature list page - Show all the creatures
#-----------------------------------------------------------
@app.get("/creatures")
def show_all_creatures():
    with connect_db() as db:
        sql = """
            SELECT id, species, name
            FROM creatures
        """
        params = ()
        creatures = db.execute(sql, params).fetchall()

        return render_template("pages/creature_list.jinja", creatures=creatures)


#-----------------------------------------------------------
# Help page - Show some help
#-----------------------------------------------------------
@app.get("/help")
def show_help():

    flash("Flash test message")
    flash("Flash test message with a longer bit of text")
    flash("Success test message", "success")
    flash("Error test message", "error")

    return render_template("pages/help.jinja")


#===========================================================
# Configure the app
#===========================================================
load_dotenv()
app.config.from_prefixed_env()
init_logging(app)
init_text_filters(app)
init_date_filters(app)
init_error_handlers(app)
init_database()
register_commands(app)

