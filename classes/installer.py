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


	def get_system_username(self):
		"""
			method used for collect the username of the system user

			return:
				if succes return system username
				else return False
		"""

		systemUsername = ""

		systemUsername = input("entrer le nom d'utilisateur: ")
		
		if systemUsername == "":
			systemUsername = "homeAutomationSystem"
		else:
			pass

		if systemUsername != "":
			return systemUsername
		else:
			return False


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
				if succes return databaseName
				else return False
		"""

		databaseName = ""

		databaseName = input("entrer le nom de la base de donnée: ")
		if databaseName == "":
			databaseName = "Home"

		if databaseName != "":
			return databaseName
		else:
			return False



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



	def create_database(self, databaseName):
		"""
			method used for create the database

			return:
				if succes return True
				else return False
		"""
		succes = False

		request = "sudo mysql -e 'CREATE DATABASE {}'".format(databaseName)

		proc = subprocess.Popen(request, shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, executable="/bin/bash")
		output, error = proc.communicate()
		proc.wait()

		if proc.returncode == 0:
			succes = True
		else:
			error = str(error.replace('\n', ''))

			if 'database exists' in error:
				succes = True
			else:
				print("Erreur: {}".format(error))
				succes = False

		return succes


	def create_database_table(self, databaseName):

		succes = False

		fileName = self.scriptPath + '/configs/createHomeDatabase.sql'
		request = "sudo mysql {} < {}".format(databaseName, fileName)
		
		proc = subprocess.Popen(request, shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, executable="/bin/bash")
		output, error = proc.communicate()
		proc.wait()

		if proc.returncode == 0:
			return True
		else:
			print("Erreur: {}".format(error))
			return False


	def create_database_system_user(self, username, userPassword):
		"""
			method used for create the user of the system in the database system

			return:
				if succes return True
				else return False
		"""

		succes = False

		creationRequest = "CREATE USER '{}'@'localhost' IDENTIFIED BY '{}'".format(username, userPassword)
		request = 'sudo mysql -e "{}"'.format(creationRequest)

		proc = subprocess.Popen(request, shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, executable="/bin/bash")
		output, error = proc.communicate()
		proc.wait()

		if proc.returncode == 0:
			return True
		else:
			print("Erreur: {}".format(error))
			return False



	def give_user_system_privilege(self, username, databaseName):
		"""
			method used for give all privilege on the database to the system user
		"""

		succes = False

		attributionRequest = "GRANT ALL PRIVILEGES ON {}.* TO '{}'@'localhost'".format(databaseName, username)
		request = "sudo mysql -e '{}'".format(attributionRequest)

		proc = subprocess.Popen(request, shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, executable="/bin/bash")
		output, error = proc.communicate()
		proc.wait()

		if proc.returncode == 0:
			request = "sudo mysql -e 'FLUSH PRIVILEGES'".format(attributionRequest)

			proc = subprocess.Popen(request, shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, executable="/bin/bash")
			output, error = proc.communicate()
			proc.wait()

			if proc.returncode == 0:
				return True
			else:
				print("Erreur: {}".format(error))
				return False
		else:
			print("Erreur: {}".format(error))
			return False



	#download method
	def download_database_system(self):
		"""
			method used for dowload the database system
		"""

		succes = False

		proc = subprocess.Popen('sudo apt-get install -y mariadb-server', shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, executable="/bin/bash")
		output, error = proc.communicate()
		proc.wait()

		if proc.returncode == 0:
			return True
		else:
			print("Erreur: {}".format(error))
			return False


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