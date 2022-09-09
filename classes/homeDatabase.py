import json

class HomeDatabase:
	"""
		class bringing all the information and functionality of the home database.

			Attributes:
                host: host of the database

                db_connection
                db_cursor

			Property:
				username: username used for database connection
				database name: name of the database
                database password: password for the database

			Methods:
				check config file existence
	"""


	def __init__(self, configFilePath):
		self.configFilePath = configFilePath
		self.host = "localHost"

		self.db_connection = False
		self.db_cursor = False



	@property
	def databaseName(self):
		"""
			property allowing to retrieve the database name from config file

			return:
				if succes:
					databaseName(str)
				else:
					False
		"""

		succes = data = databaseName = False

		if self.checkConfigFileExistence() is True:
			try:
				with open(self.configFilePath) as configFile:
				    data = json.load(configFile)
			except:
				succes = False
		else:
			succes = False

		if data is not False:
			try:
				databaseName = data['databaseName']
			except KeyError:
				databaseName = False
				succes = False

		if databaseName is not False:
			succes = True
		else:
			succes = False

		if succes:
			return databaseName
		else:
			return False


	@property
	def username(self):
		"""
			property allowing to retrieve the username from config file

			return:
				if succes:
					username(str)
				else:
					False
		"""

		succes = data = username = False

		if self.checkConfigFileExistence() is True:
			try:
				with open(self.configFilePath) as configFile:
				    data = json.load(configFile)
			except:
				succes = False
		else:
			succes = False

		if data is not False:
			try:
				username = data['username']
			except KeyError:
				username = False
				succes = False

		if username is not False:
			succes = True
		else:
			succes = False

		if succes:
			return username
		else:
			return False


	@property
	def password(self):
		"""
			property allowing to retrieve the user password from config file

			return:
				if succes:
					password(str)
				else:
					False
		"""

		succes = data = password = False

		if self.checkConfigFileExistence() is True:
			try:
				with open(self.configFilePath) as configFile:
				    data = json.load(configFile)
			except:
				succes = False
		else:
			succes = False

		if data is not False:
			try:
				password = data['password']
			except KeyError:
				password = False
				succes = False

		if password is not False:
			succes = True
		else:
			succes = False

		if succes:
			return password
		else:
			return False



	#base method
	def connect(self):
		"""
			method called for establish connection with the home database

			return:
				succes (True/False)
		"""
		succes = False

		try:
			self.db_connection = mysql.connector.connect(
				host=self.host,
				user=self.username,
				passwd=self.password,
				database=self.databaseName
			)
			self.db_cursor = self.db_connection.cursor(buffered=True)

			if self.db_connection == False or self.db_cursor == False:
				succes = False
			else:
				succes = True
		except:
			succes = False

		return succes
		

	def disconnect(self):
			"""
				method called for cut the connection with the home database

				return:
					succes (True/False)
			"""

			succes = False

			if self.db_connection is not False:
				try:
					self.db_connection.close()
					self.db_cursor = False
					self.db_connection = False

					succes = True
				except:
					succes = False

			return succes


	def commit_change(self):
		"""
			method called for commit change to the database

			return:
				succes (True/False)
		"""

		succes = False

		if self.db_connection != False:
			self.db_connection.commit()

			succes = True
		else:
			succes = False

		return False



	#checking methods
	def checkConfigFileExistence(self):
		"""
			Method used for checking the existence of the config file.

			functioning:
				1) the method try to open the databaseConfigFile
				2) if opening succes the method return True else the method return False

			return:
				succes (True/False)
		"""

		succes = False

		try:
			with open(self.configFilePath):
				pass
			succes = True
		except IOError:
			succes = False

		return succes


	def checkDatabaseConnection(self):
		"""
			Method used for checking the connection with the database.

			functioning:
				1) the method try to connect to the database
				2) if connection succes the method return True else the method return False

			return:
				succes (True/False)
		"""

		succes = False

		if self.connect() is True:
			self.disconnect()

			succes = True
		else:
			succes = False

		return succes