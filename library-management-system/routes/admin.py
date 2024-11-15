from flask import Blueprint, g, escape, session, redirect, render_template, request, jsonify, Response, flash
from app import DAO
from Misc.functions import *
import os


from Controllers.AdminManager import AdminManager
from Controllers.BookManager import BookManager
from Controllers.UserManager import UserManager

admin_view = Blueprint('admin_routes', __name__, template_folder='../templates/admin/', url_prefix='/admin')

book_manager = BookManager(DAO)
user_manager = UserManager(DAO)
admin_manager = AdminManager(DAO)


LOG_FILE_PATH = '..\\user_interactions.log'


@admin_view.route('/', methods=['GET'])
@admin_manager.admin.login_required
def home():
    admin_manager.admin.set_session(session, g)
    
    # Read the last 10 lines from the log file
    logs = read_logs(LOG_FILE_PATH, line_count=10)
    
    return render_template('admin/home.html', g=g, logs=logs)

def read_logs(log_file, line_count=10):
    """Reads the last line_count lines from a log file and filters for login and book reservation events."""
    try:
        with open(log_file, 'r') as file:
            # Read all lines, then filter for "login successful" or "Book reserved"
            lines = file.readlines()
            filtered_logs = [
                line for line in lines if "login successful" in line 
            ]
            return filtered_logs[-line_count:]  # Return only the last 'line_count' filtered lines
    except FileNotFoundError:
        return ["No log file found."]




@admin_view.route('/signin/', methods=['GET', 'POST'])
@admin_manager.admin.redirect_if_login
def signin():
	g.bg = 1
	
	if request.method == 'POST':
		_form = request.form
		email = str(_form["email"])
		password = str(_form["password"])

		if len(email)<1 or len(password)<1:
			return render_template('admin/signin.html', error="Email and password are required")

		print(email, password)
		d = admin_manager.signin(email, password)

		if d and len(d)>0:
			session['admin'] = int(d["id"])

			return redirect("/admin")

		return render_template('admin/signin.html', error="Email or password incorrect")

	return render_template('admin/signin.html')


@admin_view.route('/signout/', methods=['GET'])
@admin_manager.admin.login_required
def signout():
	admin_manager.signout()

	return redirect("/signin", code=302)


@admin_view.route('/users/view/', methods=['GET'])
@admin_manager.admin.login_required
def users_view():
    admin_manager.admin.set_session(session, g)

    id = int(admin_manager.admin.uid())
    admin = admin_manager.get(id)
    
    # Ensure `myusers` contains `lastonline`
    myusers = admin_manager.getUsersList()  # Make sure this includes `lastonline` column

    return render_template('users.html', g=g, admin=admin, users=myusers)




@admin_view.route('/books/', methods=['GET'])
@admin_manager.admin.login_required
def books():
	admin_manager.admin.set_session(session, g)

	id = int(admin_manager.admin.uid())
	admin = admin_manager.get(id)
	mybooks = book_manager.list(availability=0)

	return render_template('books/views.html', g=g, books=mybooks, admin=admin)

@admin_view.route('/books/<int:id>')
@admin_manager.admin.login_required
def view_book(id):
	admin_manager.admin.set_session(session, g)

	if id != None:
		b = book_manager.getBook(id)
		users = user_manager.getUsersByBook(id)

		print('----------------------------')
		print(users)
		
		if b and len(b) <1:
			return render_template('books/book_view.html', error="No book found!")

		return render_template("books/book_view.html", books=b, books_owners=users, g=g)


@admin_view.route('/books/add', methods=['GET', 'POST'])
@admin_manager.admin.login_required
def book_add():
    admin_manager.admin.set_session(session, g)

    if request.method == 'POST':
        # Get form data
        title = request.form.get('title')
        qty = request.form.get('qty')
        available = 1 if request.form.get('available') == 'on' else 0  # Checkbox returns 'on' if checked
        author = request.form.get('author')
        edition = request.form.get('edition')
        desc = request.form.get('desc')

        # Validation checks
        error = None
        try:
            qty = int(qty)
            if qty < 0:
                error = "Quantity should be a positive integer."
        except ValueError:
            error = "Quantity must be an integer."

        if not title:
            error = "Title is required."
        elif not author:
            error = "Author is required."
        elif not edition:
            error = "Edition is required."
        elif not desc:
            error = "Description is required."

        if error:
            flash(error)
            return render_template('books/add.html', g=g, error=error)
        
        # Call the book manager to add the book
        success = book_manager.add_book(title, qty, available, author, edition, desc)

        if success:
            return redirect('/admin/books/')  # Redirect to the books list after adding
        else:
            error = "Failed to add book."
            flash(error)
            return render_template('books/add.html', g=g, error=error)

    return render_template('books/add.html', g=g)

@admin_view.route('/books/edit/<int:id>', methods=['GET', 'POST'])
@admin_manager.admin.login_required
def book_edit(id):
    admin_manager.admin.set_session(session, g)

    # Fetch the existing book details
    b = book_manager.getBook(id)

    if not b:
        return render_template('edit.html', error="No book found!")

    if request.method == 'POST':
        # Get form data
        title = request.form.get('title')
        qty = request.form.get('qty')
        available = 1 if request.form.get('available') == 'on' else 0  # Checkbox returns 'on' if checked
        desc = request.form.get('desc')

        # Validation
        error = None
        try:
            qty = int(qty)
            if qty < 0:
                error = "Quantity should be a positive integer."
        except ValueError:
            error = "Quantity must be an integer."

        if not title:
            error = "Title is required."
        elif not desc:
            error = "Description is required."

        if error:
            flash(error)
            return render_template('books/edit.html', book=b, g=g, error=error)

        # Call the book manager to update the book
        success = book_manager.update_book(id, title, qty, available, desc)

        if success:
            return redirect('/admin/books/')  # Redirect to the books list after updating
        else:
            flash("Failed to update book.")
            return render_template('books/edit.html', book=b, g=g, error="Failed to update book.")

    # If GET request, display the form with existing book data
    return render_template("books/edit.html", book=b, g=g)

@admin_view.route('/books/delete/<int:id>', methods=['GET'])
@admin_manager.admin.login_required
def book_delete(id):
	id = int(id)

	if id is not None:
		book_manager.delete(id)
	
	return redirect('/admin/books/')


@admin_view.route('/books/search', methods=['GET'])
def search():
	admin_manager.admin.set_session(session, g)

	if "keyword" not in request.args:
		return render_template("books/view.html")

	keyword = request.args["keyword"]

	if len(keyword)<1:
		return redirect('/admin/books')

	id = int(admin_manager.admin.uid())
	admin = admin_manager.get(id)

	d=book_manager.search(keyword, 0)

	if len(d) >0:
		return render_template("books/views.html", search=True, books=d, count=len(d), keyword=escape(keyword), g=g, admin=admin)

	return render_template('books/views.html', error="No books found!", keyword=escape(keyword))


@admin_view.route('/users/delete/<int:id>', methods=['POST'])
@admin_manager.admin.login_required
def delete_user(id):
	admin_manager.admin.set_session(session, g)
	
	if id is not None:
		admin_manager.delete_user(id)
	
	return redirect('/admin/users/view/')


@admin_view.route('/users/promote/<int:id>', methods=['POST'])
@admin_manager.admin.login_required
def promote_user(id):
    # Retrieve the user data from the users table
    user = user_manager.get(id)

    # Check if the user exists
    if not user:
        print("Error: User data could not be retrieved.")
        return jsonify({"success": False, "message": "User data not found"})

    # Promote the user to admin
    print(f"Promoting user with ID {id} to admin...")
    success = user_manager.promote_to_admin(user)
    if not success:
        print("Error: Failed to promote user to admin.")
        return jsonify({"success": False, "message": "User promotion failed"})

    # Delete the user from users table using UserManager
    print(f"Deleting user with ID {id} from users table...")
    delete_success = user_manager.delete_user(id)
    if delete_success:
        return jsonify({"success": True})
    else:
        print("Error: Failed to delete user from users table.")
        return jsonify({"success": False, "message": "User promotion succeeded, but user deletion failed"})