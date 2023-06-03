from flask import Flask, render_template, send_file, url_for, redirect, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, current_user, login_required, logout_user

from forms import LoginForm, NewUserForm, ChangePasswordForm
from config import db_url, root_domain, secret_key
from models import User, db, login

import sass
import flask

app = Flask(__name__) # Create the app

# Flask app configuation
app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SECRET_KEY"] = secret_key

db.init_app(app) # Initialise the app with the extension
login.init_app(app) # Inisialise the app

@app.before_first_request
def initialize_server():
    # Ensure our database is present.
    db.create_all()

db.configure_mappers()

@app.login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for("login"))


@app.route('/')
def landing():
    return render_template("landing.html")


@app.route("/user/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
        else:
            login_user(user, remember=False)
            return redirect(url_for("home"))

    return render_template("login.html", form=form)
        
@app.route("/user/register", methods=["GET", "POST"])
def register():
    form = NewUserForm()
    if form.validate_on_submit():
        u = User(username=form.username.data)
        if form.password1.data != form.password2.data:
            flash("Invalid password")
        else:
            u.set_password(form.password1.data)
            db.session.add(u)
            db.session.commit()

            return redirect(url_for("home"))
    
    return render_template("register.html", form=form)
    
@app.route("/user/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        print(type(current_user))
        u = User.query.filter_by(username=current_user.username).first()
        u.set_password(form.new_password1.data)
        db.session.add(u)
        db.session.commit()
        return redirect(url_for("home"))

    return render_template(
        "pwchange.html", form=form, username=current_user.username
    )

@app.route("/user/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("landing"))

@app.route('/home')
@login_required
def home():
    return f"Welcome, {current_user.username}!"



@app.route('/assets/<asset>')
def asset(asset):
    return send_file(f"./static/site/{asset}")


if __name__ == '__main__':
    sass.compile(dirname=('./static/site/scss', './static/site'), output_style='compressed')
    app.run(root_domain, 80, debug=True)