from App.Books import Books

class BookManager():
	def __init__(self, DAO):
		self.misc = Books(DAO.db.book)
		self.dao = self.misc.dao

	def list(self, availability=1,user_id=None):
		if user_id!= None:
			book_list = self.dao.listByUser(user_id)
		else:
			book_list = self.dao.list(availability)

		return book_list

	def getReserverdBooksByUser(self, user_id):
		books = self.dao.getReserverdBooksByUser(user_id)

		return books

	def getBook(self, id):
		books = self.dao.getBook(id)

		return books

	def search(self, keyword, availability=1):
		books = self.dao.search_book(keyword, availability)

		return books

	def reserve(self, user_id, book_id):
		books = self.dao.reserve(user_id, book_id)

		return books

	def getUserBooks(self, user_id):
		books = self.dao.getBooksByUser(user_id)

		return books

	def getUserBooksCount(self, user_id):
		books = self.dao.getBooksCountByUser(user_id)

		return books

	def delete(self, id):
		self.dao.delete(id)

	def add_book(self, title, qty, available, author, edition, desc):
		# Call the DAO method to add the book with all required fields
		return self.dao.add_book(title, qty, available, author, edition, desc)
	
	def update_book(self, book_id, title, qty, available, desc):
		# Call the DAO method to update the book with all required fields
		return self.dao.update_book(book_id, title, qty, available, desc)