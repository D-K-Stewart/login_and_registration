from flask import render_template,redirect,request,session,flash
from flask_app import app
from flask_app import bcrypt
from flask_app.models.user import User



@app.route('/')
def all_users():

    return render_template('index.html')



@app.route('/create', methods=['POST'])
def create():
    # validate the form here ...
    # create the hash
    print (request.form)
    if not User.validate_user(request.form):
        return redirect('/')
    password = bcrypt.generate_password_hash(request.form['password'])
    print(password)
    # put the password into the data dictionary
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email" : request.form["email"],
        "password" : password
    }
    # Call the save @classmethod on User
    User.save(data)
    # store user id into session

    return redirect("/")


@app.route('/login', methods=['POST'])
def login():
    # see if the username provided exists in the database
    data = { "email" : request.form["email"] }
    user_in_db = User.get_by_email(data)
    # user is not registered in the db
    if not user_in_db:
        flash(u"Invalid Email/Password", "login")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # if we get False after checking the password
        flash(u"Invalid Email/Password", "login")
        return redirect('/')
    # if the passwords matched, we set the user_id into session
    session['user_first_name'] = user_in_db.first_name 
    # never render on a post!!!
    return render_template("welcome.html")


@app.route('/logout')
def user():
    session.clear()
    return redirect('/')