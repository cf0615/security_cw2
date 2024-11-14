class AdminDAO():
    db = {}

    def __init__(self, DAO):
        self.db = DAO
        self.db.table = "admin"

    def getById(self, id):
        # Parameterized query to prevent SQL injection
        query = "SELECT * FROM @table WHERE id=%s".replace("@table", self.db.table)
        q = self.db.query(query, (id,))
        user = q.fetchone()
        return user

    def getByEmail(self, email):
        # Parameterized query to prevent SQL injection
        query = "SELECT * FROM @table WHERE email=%s".replace("@table", self.db.table)
        q = self.db.query(query, (email,))
        user = q.fetchone()
        return user
