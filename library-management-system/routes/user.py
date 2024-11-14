from flask import Blueprint, g, escape, session, redirect, render_template, request, jsonify, Response, flash
from app import DAO
from Misc.functions import *
import re
import logging
import bleach
from Controllers.UserManager import UserManager
from Controllers.AdminManager import AdminManager


user_view = Blueprint('user_routes', __name__, template_folder='/templates')

user_manager = UserManager(DAO)
admin_manager = AdminManager(DAO)

# Define a regex pattern for validating email format
EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

@user_view.route('/', methods=['GET'])
def home():
	g.bg = 1

	user_manager.user.set_session(session, g)
	print(g.user)

	return render_template('home.html', g=g)

# Configure logging
logging.basicConfig(
    filename='user_interactions.log',  # Log file to store the logs
    level=logging.INFO,                 # Log level
    format='%(asctime)s - %(levelname)s - %(message)s'
)


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

        # Attempt to authenticate the user
        admin_data = admin_manager.signin(email, password)
        user_data = user_manager.signin(email, password)

        if admin_data and len(admin_data) > 0:
            session['admin'] = int(admin_data["id"])
            # Log successful admin login
            logging.info(f"Admin login successful: {email}")
            return redirect("/admin")

        elif user_data and len(user_data) > 0:
            session['user'] = int(user_data["id"])
            
            # Log successful user login
            logging.info(f"User login successful: {email}")
            return redirect("/")

        # Log failed login attempt
        logging.warning(f"Failed login attempt for email: {email}")
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
		
		if not validate_password_strength(password):
			return render_template(
				'signup.html',
				error="Password must be at least 8 characters long, include an uppercase letter, a number, and a special character."
			)

		# Validate email format
		if not re.match(EMAIL_REGEX, email):
			return render_template('signup.html', error="Invalid email format")

		new_user = user_manager.signup(name, email, password)

		if new_user == "already_exists":
			return render_template('signup.html', error="User already exists with this email")

		return render_template('signup.html', msg="You've been registered!")

	return render_template('signup.html')


# Helper function to validate password strength
def validate_password_strength(password):
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):  # At least one uppercase letter
        return False
    if not re.search(r"[0-9]", password):  # At least one number
        return False
    if not re.search(r"[!@#$%^&*()_+=-]", password):  # At least one special character
        return False
    return True

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
    name = sanitize_input(str(_form.get("name", "").strip()))
    old_email = str(_form.get("old_email", "").strip())
    new_email = str(_form.get("new_email", "").strip())
    old_password = str(_form.get("old_password", "").strip())
    new_password = str(_form.get("new_password", "").strip())
    bio = sanitize_input(str(_form.get("bio", "").strip()))  # Sanitize bio

    # Get the current user data
    current_user = user_manager.get(user_manager.user.uid())
    
    # Validate old email
    if old_email != current_user['email']:
        flash('Old email does not match our records.')
        return redirect("/user/")

    # Check that the new email is different from the old
    if new_email and new_email == old_email:
        flash('New email cannot be the same as the old email.')
        return redirect("/user/")

    # Validate old password
    if not verify_password(current_user['password'], old_password):
        flash('Old password is incorrect.')
        return redirect("/user/")
    
    # Check if old password and new password are the same
    if new_password.strip() and verify_password(current_user['password'], new_password):
        flash('New password cannot be the same as the old password.')
        return redirect("/user/")

    # Only hash the new password if provided
    if new_password.strip():
        hashed_password = hash_password(new_password)
    else:
        hashed_password = current_user['password']

    # Use new email if provided and validated, otherwise keep the current email
    email_to_update = new_email if new_email else current_user['email']

    # Update the user profile
    user_manager.update(name, email_to_update, hashed_password, bio, user_manager.user.uid())

    flash('Your info has been updated successfully!')
    return redirect("/user/")
