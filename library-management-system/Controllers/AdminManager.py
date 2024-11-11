from App.Admin import Admin
from Misc.functions import verify_password

class AdminManager():
	def __init__(self, DAO):
		self.admin = Admin(DAO.db.admin)
		self.user = DAO.db.user
		self.dao = self.admin.dao

	def signin(self, email, password):
		admin = self.dao.getByEmail(email)

		if admin is None:
			return False

		if not verify_password(admin['password'], password):
			return False

		return admin
		
	def get(self, id):
		admin = self.dao.getById(id)

		return admin
		
	def getUsersList(self):
		admin = self.user.list()
		print(admin)

		return admin

	def signout(self):
		self.admin.signout()

	def user_list(self):
		return self.user.list()

	def delete_user(self, id):
		return self.user.delete(id)