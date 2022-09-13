import subprocess
import sys
import json


class Installer:
	"""
		class bringing all the information and functionality of the installer.

			Attributes:
				version
				script path (path of the main script (for file manipulation))
				database configFilePath

			Propertys:

			Methods:
	"""

	def __init__(self, scriptPath):
		self.version = '0.0.1'
		self.scriptPath = scriptPath
		self.databaseConfigFilePath = scriptPath + "/configs/databaseConfig.json"



	#get method
	def get_install_choice(self):
		"""
			method used for collect the install choice of the use

			return:
				if succes return the install choice
				else return False
		"""

		succes = False
		installChoice = ""

		while installChoice != 'o' or installChoice != 'n':
			installChoice = input("\nvoulez-vous installer le système domotique ?(o/n): ").lower()
			
			if installChoice == 'o' or installChoice == 'n':
				break

		if installChoice != "":
			succes = True
		else:
			succes = False

		if succes:
			return installChoice
		else:
			return False


	def get_root_database_system_password(self):
		"""
			method used for collect the root database system password

			return:
				if succes return the root database system password
				else return False
		"""

		succes = False
		rootDatabaseSystemPassword = ""

		while rootDatabaseSystemPassword == "":
			rootDatabaseSystemPassword = input("veuillez entrer a nouveau le mot de passe root de la base de donnée: ")

		if rootDatabaseSystemPassword != "":
			succes = True
		else:
			succes = False

		if succes:
			return rootDatabaseSystemPassword
		else:
			return False


	def get_system_username(self):
		"""
			method used for collect the username of the system user

			return:
				system username
		"""

		systemUsername = input("entrer le nom d'utilisateur: ")
		
		if systemUsername == "":
			systemUsername = "homeAutomationSystem"
		else:
			pass

		return systemUsername


	def get_system_user_password(self):
		"""
			method used for collect the password of the system user

			return:
				if succes return the system password
				else return False
		"""

		systemPassword = input("enter le mot de passe: ")

		if systemPassword != "":
			succes = True
		else:
			succes = False

		if succes:
			return systemPassword
		else:
			return False


	def get_database_name(self):
		"""
			method used for collect the databaseName

			return:
				databaseName
		"""
		databaseName = input("entrer le nom de la base de donnée: ")
		if databaseName == "":
			databaseName = "Home"

		return databaseName



	#create method
	def create_database_config_file(self, data):
		"""
			method used for create the database config file

			return:
				if succes return True
				else return False
		"""

		succes = False

		try:
			with open(databaseConfigFilePath, 'w') as f:
				json.dump(data, f, indent=4)

			succes = True
		except:
			succes = False

		return succes


	def create_database_system_user(self, databaseCursor, username):
		"""
			method used for create the user of the system in the database system

			return:
				if succes return True
				else return False
		"""

		succes = False

		if self.check_user_presence_in_database_system(databaseCursor, username):
			succes = True
		else:
			request = "CREATE USER '{}'@'localhost' IDENTIFIED BY '{}'".format(username, databasePassword)
			databaseCursor.execute(request)

			if self.check_user_presence_in_database_system(databaseCursor, username):
				succes = True
			else:
				succes = False

		return succes


	def create_database(self, databaseName):
		"""
			method used for create the database

			return:
				if succes return True
				else return False
		"""

		request = "sudo mysql -e 'CREATE DATABASE {}'".format(databaseName)

		proc = subprocess.Popen(request, shell=True, stdin=None, stdout=open("/dev/null", "w"), stderr=None, executable="/bin/bash")
		proc.wait()

		if proc.returncode == 0:
			return True
		else:
			return False


	def create_database_table(self, databaseName):

		fileName = self.scriptPath + '/configs/createHomeDatabase.sql'
		request = "sudo mysql {} < {}".format(databaseName, fileName)
		databaseCursor.execute(request)



	def give_user_system_privilege(self, databaseCursor, username, databaseName):
		"""
			method used for give all privilege on the database to the system user
		"""

		request = "GRANT ALL PRIVILEGES ON {}.* TO '{'@'localhost'".format(databaseName, username)
		databaseCursor.execute(request)

		request = "FLUSH PRIVILEGES"
		databaseCursor.execute(request)



	#download method
	def download_database_system(self):
		"""
			method used for dowload the database system
		"""

		proc = subprocess.Popen('sudo apt-get install -y mariadb-server', shell=True, stdin=None, stdout=open("/dev/null", "w"), stderr=None, executable="/bin/bash")
		proc.wait()



	#install method
	def install_database_system(self):
		"""
			method used for install the database system
		"""

		proc = subprocess.run("sudo mysql_secure_installation", shell=True, check=True)



	#checking method
	def check_database_config_file_existence(self):
		"""
			method used for checking the existence of the database config file

			return:
				if file exist return True
				else return False
		"""

		succes = False

		try:
			with open(self.databaseConfigFilePath):
				pass
			succes = True
		except IOError:
			succes = False

		return succes


	def check_user_presence_in_database_system(self, databaseCursor, username):
		"""
			method used for check the presence of the system user in the database system

			return:
				if the user was present return True
				else return False
		"""

		request = "SELECT * FROM users WHERE username='{}'".format(username)
			
		databaseCursor.execute(request)
		response = databaseCursor.fetchall()

		if len(response) > 0:
			succes = True
		else:
			succes = False


	def check_database_existence(self, databaseCursor, username):
		"""
			method used for check the existence of the database

			return:
				if database exist return True
				else return False
		"""

		succes = False

		request = "SHOW DATABASES LIKE '{}'".format(databaseName)
		databaseCursor.execute(request)
		response = databaseCursor.fetchall()

		if len(response) > 0:
			succes = True
		else:
			succes = False

		return succes