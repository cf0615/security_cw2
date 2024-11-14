class UserDAO():
	def __init__(self, DAO):
		self.db = DAO
		self.db.table = "users"


	def list(self):
		users = self.db.query("""
			SELECT 
				@table.*,
				COUNT(reserve.book_id) as books_owned 
			FROM @table 
			LEFT JOIN reserve ON reserve.user_id=@table.id 
			GROUP BY 
				@table.id,
				@table.name,
				@table.email,
				@table.bio,
				@table.mob,
				@table.lock,
				@table.created_at
		""").fetchall()

		return users

	def getById(self, id):
		q = self.db.query("select * from @table where id='{}'".format(id))

		user = q.fetchone()

		return user

	def getUsersByBook(self, book_id):
		q = self.db.query("select * from @table LEFT JOIN reserve ON reserve.user_id = @table.id WHERE reserve.book_id={}".format(book_id))

		user = q.fetchall()

		return user

	def getByEmail(self, email):
		q = self.db.query("select * from @table where email='{}'".format(email))

		user = q.fetchone()

		return user

	def add(self, user):
		name = user['name']
		email = user['email']
		password = user['password']
		bio = user.get('bio', '')
		mob = user.get('mob', '')
		lock = user.get('lock', 0)
		print(name, email, password, bio, mob, lock)

		q = self.db.query("INSERT INTO @table (name, email, password, bio, mob, `lock`) VALUES('{}', '{}', '{}', '{}', '{}', {});".format(name, email, password, bio, mob, lock))
		self.db.commit()
		
		return q


	def update(self, user, _id):
		name = user['name']
		email = user['email']
		password = user['password']
		bio = user['bio']

		q = self.db.query("UPDATE @table SET name = '{}', email='{}', password='{}', bio='{}' WHERE id={}".format(name, email, password, bio, _id))
		self.db.commit()
		
		return q

	def delete(self, id):
		try:
			# First delete any book reservations by this user
			self.db.query("DELETE FROM reserve WHERE user_id = {}".format(id))
			
			# Then delete the user
			self.db.query("DELETE FROM @table WHERE id = {}".format(id))
			self.db.commit()
			return True
		except Exception as e:
			print(f"Error deleting user: {str(e)}")
			return False
		
	def promote_to_admin(self, user):
		try:
			# Format the SQL string manually with email and password
			query = "INSERT INTO admin (email, password) VALUES ('{}', '{}')".format(
				user['email'], user['password']
			)

			# Execute the query
			self.db.query(query)
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
		"""Update lastonline column to current timestamp."""
		query = "UPDATE users SET lastonline = CURRENT_TIMESTAMP WHERE id = {}".format(user_id)
		self.db.query(query)  # Call query without parameters
		self.db.commit()
