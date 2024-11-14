from flask import Blueprint, g, escape, session, redirect, render_template, request, jsonify, Response, flash
from app import DAO
from Misc.functions import *
import re
import bleach
from Controllers.UserManager import UserManager

user_view = Blueprint('user_routes', __name__, template_folder='/templates')

user_manager = UserManager(DAO)

# Define a regex pattern for validating email format
EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

@user_view.route('/', methods=['GET'])
def home():
	g.bg = 1

	user_manager.user.set_session(session, g)
	print(g.user)

	return render_template('home.html', g=g)


@user_view.route('/signin', methods=['GET', 'POST'])
@user_manager.user.redirect_if_login
def signin():
	if request.method == 'POST':
		_form = request.form
		email = str(_form["email"])
		password = str(_form["password"])

		if len(email)<1 or len(password)<1:
			return render_template('signin.html', error="Email and password are required")
		
		# Validate email format
		if not re.match(EMAIL_REGEX, email):
			return render_template('signin.html', error="Invalid email format")

		d = user_manager.signin(email, password)

		if d and len(d)>0:
			session['user'] = int(d['id'])

			return redirect("/")

		return render_template('signin.html', error="Email or password incorrect")


	return render_template('signin.html')


@user_view.route('/signup', methods=['GET', 'POST'])
@user_manager.user.redirect_if_login
def signup():
	if request.method == 'POST':
		name = request.form.get('name')
		email = request.form.get('email')
		password = request.form.get('password')

		# Check if fields are empty
		if len(name) < 1 or len(email) < 1 or len(password) < 1:
			return render_template('signup.html', error="All fields are required")

		# Validate email format
		if not re.match(EMAIL_REGEX, email):
			return render_template('signup.html', error="Invalid email format")

		new_user = user_manager.signup(name, email, password)

		if new_user == "already_exists":
			return render_template('signup.html', error="User already exists with this email")

		return render_template('signup.html', msg="You've been registered!")

	return render_template('signup.html')

@user_view.route('/signout/', methods=['GET'])
@user_manager.user.login_required
def signout():
	user_manager.signout()

	return redirect("/", code=302)

@user_view.route('/user/', methods=['GET'])
@user_manager.user.login_required
def show_user(id=None):
	user_manager.user.set_session(session, g)
	
	if id is None:
		id = int(user_manager.user.uid())

	d = user_manager.get(id)
	mybooks = user_manager.getBooksList(id)

	return render_template("profile.html", user=d, books=mybooks, g=g)

def sanitize_input(user_input):
    allowed_tags = ['b', 'i', 'u', 'strong', 'em']  # Allowed safe tags
    allowed_attrs = {}
    return bleach.clean(user_input, tags=allowed_tags, attributes=allowed_attrs)

@user_view.route('/user', methods=['POST'])
@user_manager.user.login_required
def update():
	user_manager.user.set_session(session, g)
	
	_form = request.form
	name = sanitize_input(str(_form.get("name", "").strip()))  # Sanitize and strip whitespace
	email = str(_form.get("email", "").strip())
	password = str(_form.get("password", "").strip())
	bio = sanitize_input(str(_form.get("bio", "").strip()))  # Sanitize bio

	# Check if name or email is empty and show an error if true
	if not name:
		flash('Name cannot be empty', 'error')
		return redirect("/user/")
	if not email:
		flash('Email cannot be empty', 'error')
		return redirect("/user/")

	# Validate email format
	if not re.match(EMAIL_REGEX, email):
		return render_template('signup.html', error="Invalid email format")
	

	# Only hash password if a new one is provided
	if password.strip():
		password = hash_password(password)
	else:
		# Get current user to keep existing password
		current_user = user_manager.get(user_manager.user.uid())
		password = current_user['password']

	user_manager.update(name, email, password, bio, user_manager.user.uid())

	flash('Your info has been updated!')
	return redirect("/user/")