class BookDAO():
    def __init__(self, DAO):
        self.db = DAO
        self.db.table = "books"

    def delete(self, id):
        # Parameterized query to prevent SQL injection
        query = "DELETE FROM @table WHERE id=%s"
        q = self.db.query(query, (id,))
        self.db.commit()
        return q

    def reserve(self, user_id, book_id):
        # Check availability first
        if not self.available(book_id):
            return "err_out"

        # Use parameterized queries to prevent SQL injection
        reserve_query = "INSERT INTO reserve (user_id, book_id) VALUES (%s, %s)"
        self.db.query(reserve_query, (user_id, book_id))

        update_query = "UPDATE @table SET count = count - 1 WHERE id = %s"
        self.db.query(update_query, (book_id,))
        self.db.commit()

        return "Reserved"

    def getBooksByUser(self, user_id):
        # Parameterized query to prevent SQL injection
        query = """
            SELECT * FROM @table
            LEFT JOIN reserve ON reserve.book_id = @table.id
            WHERE reserve.user_id = %s
        """
        q = self.db.query(query, (user_id,))
        books = q.fetchall()
        return books

    def getBooksCountByUser(self, user_id):
        # Parameterized query to prevent SQL injection
        query = """
            SELECT COUNT(reserve.book_id) AS books_count
            FROM @table
            LEFT JOIN reserve ON reserve.book_id = @table.id
            WHERE reserve.user_id = %s
        """
        q = self.db.query(query, (user_id,))
        books = q.fetchall()
        return books

    def getBook(self, id):
        # Parameterized query to prevent SQL injection
        query = "SELECT * FROM @table WHERE id = %s"
        q = self.db.query(query, (id,))
        book = q.fetchone()
        return book

    def available(self, id):
        book = self.getById(id)
        count = book['count'] if book else 0
        return count > 0

    def getById(self, id):
        # Parameterized query to prevent SQL injection
        query = "SELECT * FROM @table WHERE id = %s"
        q = self.db.query(query, (id,))
        book = q.fetchone()
        return book

    def list(self, availability=1):
        # Dynamic query with parameter to prevent SQL injection
        if availability == 1:
            query = "SELECT * FROM @table WHERE availability = %s"
            q = self.db.query(query, (availability,))
        else:
            query = "SELECT * FROM @table"
            q = self.db.query(query)
        books = q.fetchall()
        return books

    def getReserverdBooksByUser(self, user_id):
        # Parameterized query to prevent SQL injection
        query = "SELECT GROUP_CONCAT(book_id) AS user_books FROM reserve WHERE user_id = %s"
        q = self.db.query(query, (user_id,))
        books = q.fetchone()
        return books

    def search_book(self, name, availability=1):
        # Parameterized query to prevent SQL injection
        query = "SELECT * FROM @table WHERE name LIKE %s"
        if availability == 1:
            query += " AND availability = %s"
            q = self.db.query(query, (f"%{name}%", availability))
        else:
            q = self.db.query(query, (f"%{name}%",))
        books = q.fetchall()
        return books
