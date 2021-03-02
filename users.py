
class Users:
	def __init__(self, user_name, user_password, permissions):
		self.user_name = user_name
		self.user_password = user_password
		self.permissions = permissions

	def permissions(self,npermissions):	
		self.permissions = npermissions
