class UserDAO():
    def __init__(self, DAO):
        self.db = DAO
        self.db.table = "users"

    def list(self):
        # Parameterized query
        query = """
            SELECT 
                @table.*,
                COUNT(reserve.book_id) as books_owned 
            FROM @table 
            LEFT JOIN reserve ON reserve.user_id = @table.id 
            GROUP BY 
                @table.id,
                @table.name,
                @table.email,
                @table.bio,
                @table.mob,
                @table.lock,
                @table.created_at
        """.replace("@table", self.db.table)
        
        users = self.db.query(query).fetchall()
        return users

    def getById(self, id):
        # Parameterized query
        query = "SELECT * FROM {} WHERE id = %s".format(self.db.table)
        q = self.db.query(query, (id,))
        user = q.fetchone()
        return user

    def getUsersByBook(self, book_id):
        # Parameterized query
        query = """
            SELECT * FROM @table 
            LEFT JOIN reserve ON reserve.user_id = @table.id 
            WHERE reserve.book_id = %s
        """.replace("@table", self.db.table)
        
        q = self.db.query(query, (book_id,))
        user = q.fetchall()
        return user

    def getByEmail(self, email):
        # Parameterized query
        query = "SELECT * FROM {} WHERE email = %s".format(self.db.table)
        q = self.db.query(query, (email,))
        user = q.fetchone()
        return user

    def add(self, user):
        # Parameterized query
        name = user['name']
        email = user['email']
        password = user['password']
        bio = user.get('bio', '')
        mob = user.get('mob', '')
        lock = user.get('lock', 0)

        query = "INSERT INTO {} (name, email, password, bio, mob, `lock`) VALUES (%s, %s, %s, %s, %s, %s)".format(self.db.table)
        q = self.db.query(query, (name, email, password, bio, mob, lock))
        self.db.commit()
        
        return q

    def update(self, user, _id):
        # Parameterized query
        name = user['name']
        email = user['email']
        password = user['password']
        bio = user['bio']

        query = "UPDATE {} SET name = %s, email = %s, password = %s, bio = %s WHERE id = %s".format(self.db.table)
        q = self.db.query(query, (name, email, password, bio, _id))
        self.db.commit()
        
        return q

    def delete(self, id):
        try:
            # Parameterized query for deleting reservations
            self.db.query("DELETE FROM reserve WHERE user_id = %s", (id,))
            
            # Parameterized query for deleting user
            self.db.query("DELETE FROM {} WHERE id = %s".format(self.db.table), (id,))
            self.db.commit()
            return True
        except Exception as e:
            print(f"Error deleting user: {str(e)}")
            return False
          
    def promote_to_admin(self, user):
        try:
            # Use a parameterized query to safely insert email and password
            query = "INSERT INTO admin (email, password) VALUES (%s, %s)"
            
            # Execute the query with user parameters
            self.db.query(query, (user['email'], user['password']))
            self.db.commit()
            
            print("User promoted to admin successfully.")
            return True
        except Exception as e:
            print(f"Error promoting user to admin: {str(e)}")  # Log the error message
            return False

    def delete_user(self, user_id):
      query = "DELETE FROM users WHERE id = %s"
      cursor = self.db.cursor()
      cursor.execute(query, (user_id,))
      self.db.commit()
      cursor.close()
      return True

    def update_last_online(self, user_id):
        #Update lastonline column to current timestamp using parameterized query.
        query = "UPDATE users SET lastonline = CURRENT_TIMESTAMP WHERE id = %s"
        self.db.query(query, (user_id,))  # Pass `user_id` as a parameter in a tuple
        self.db.commit()
