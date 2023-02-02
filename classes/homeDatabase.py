import json
import mysql.connector

from .users.administrator import *
from .users.guest import *
from .users.user import *
from .users.profil import *

class HomeDatabase:
	"""
		class bringing all the information and functionality of the home database.

			Attributes:
				config file path: path to the config file
                host: host of the database

                db_connection
                db_cursor

			Property:
				username: username used for database connection
				database name: name of the database
                database password: password for the database

			Methods:
				connect
				disconnect
				commit_change
				get_users_list
				get_profils_list
				get_inhabitant_List
				get_guest_list
				get_administrator_list
				get_profil_by_id
				add_user
				add_profil
				check_config_file_existence
				check_database_connection
	"""


	def __init__(self, scriptPath):
		self.configFilePath = scriptPath + "/configs/databaseConfig.json"
		self.host = "localHost"

		self.db_connection = False
		self.db_cursor = False



	@property
	def databaseName(self):
		"""
			property allowing to retrieve the database name from config file

			functionning:
				1.check config file existance
				2.collecte data
				3.select database name data
				4.return

			return:
				if succes:
					databaseName(str)
				else:
					False
		"""

		succes = data = databaseName = False

		if self.check_config_file_existence() is True:
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

			functionning:
				1.check config file existance
				2.collecte data
				3.select system user name data
				4.return


			return:
				if succes:
					username(str)
				else:
					False
		"""

		succes = data = username = False

		if self.check_config_file_existence() is True:
			try:
				with open(self.configFilePath) as configFile:
				    data = json.load(configFile)
			except:
				succes = False
		else:
			succes = False

		if data is not False:
			try:
				username = data['systemUserName']
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

			functionning:
				1.check config file existance
				2.collecte data
				3.select system user password data
				4.return

			return:
				if succes:
					password(str)
				else:
					False
		"""

		succes = data = password = False

		if self.check_config_file_existence() is True:
			try:
				with open(self.configFilePath) as configFile:
				    data = json.load(configFile)
			except:
				succes = False
		else:
			succes = False

		if data is not False:
			try:
				password = data['systemUserPassword']
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

			functionning:
				1.check if connection wasn't aleady established
				2.establish the connection
				3.check if connection succes
				4.return

			return:
				succes (True/False)
		"""

		succes = False

		if self.db_connection == False or self.db_cursor == False:
			try:
				self.db_connection = mysql.connector.connect(
					host=self.host,
					user=self.username,
					passwd=self.password,
					database=self.databaseName
				)
				self.db_cursor = self.db_connection.cursor(buffered=True)
			except Exception as e:
				self.db_connection = False
				self.db_cursor = False

			if self.db_connection == False or self.db_cursor == False:
				succes = False
			else:
				succes = True
		else:
			succes = True

		print(self.db_cursor)

		return succes
		

	def disconnect(self):
			"""
				method called for cut the connection with the home database

				functioning:
					1.test if connection wasn't already disconnected
					2.disconnection of the database
					3.return


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
			else:
				succes = True

			return succes


	def commit_change(self):
		"""
			method called for commit change to the database

			functionnement:
				1.test if connection was established
				2.commit change in datatabase
				3.return

			return:
				succes (True/False)
		"""

		succes = False

		if self.db_connection != False:
			try:
				self.db_connection.commit()
				succes = True
			except:
				succes = False
		else:
			succes = False

		return succes



	#get method
	def get_users_list(self):
		"""
    		method called for get an list of user

			functioning:
				1.connect to the database
				2.get all user in database
				3.database disconnection
				4.transform all user in database on user instance classe
				5.check user list conformity
				6.return
    		
			return:
    			list of user class
    	"""

		succes = requestExecuted = tmpUsersList = usersList = False

		request = """SELECT * FROM Users"""

		#connect to the database
		if self.connect():
			try:
				#get all user in database
				self.db_cursor.execute(request)
				tmpUsersList = self.db_cursor.fetchall()
				requestExecuted = True
			except:
				self.disconnect()
				requestExecuted = False

			if requestExecuted:
				#database disconnection
				self.disconnect()
			else:
				tmpUsersList = False
		else:
			tmpUsersList = False

		#transform all user in database on user instance classe
		if tmpUsersList != False:
			usersList = []

			if len(tmpUsersList) > 0:
				for user in tmpUsersList:
					userProfil = False
					userProfil = self.get_profil_by_id(int(user[1]))

					if userProfil != False:
						try:
							if user[3] == "inhabitant":
								if user[2] == "admin":
									usersList.append(Administrator(user[0], userProfil, user[4], user[5]))
								else:
									usersList.append(Inhabitant(user[0], userProfil, user[2], user[4], user[5]))
							else:	
								usersList.append(Guest(user[0], userProfil, user[4], user[5]))
						except Exception as e:
							print(e)
							pass
					else:
						usersList = False
						break
			else:
				usersList = []
		else:
			succes = False

		#check user list conformity
		if usersList != False:
			if len(usersList) > 0:
				for user in usersList:
					if isinstance(user, User):
						succes = True
					else:
						succes = False
						break
			else:
				succes = True
		else:
			succes = False

		print(usersList)

		#return
		if succes:
			return usersList
		else:
			return False

	
	def get_profils_list(self):
		"""
    		method called for get an list of profil

			functioning:
				1.connect to the database
				2.get all profil in database
				3.database disconnection
				4.transform all profil in database on profils instance classe
				5.check profil list conformity
				6.return
    		
			return:
    			list of profil class
    	"""

		succes = requestExecuted = tmpProfilsList = profilsList = False

		request = """SELECT * FROM Profils"""

		#connect to the database
		if self.connect():
			try:
				#get all profil in database
				self.db_cursor.execute(request)
				tmpProfilsList = self.db_cursor.fetchall()
				requestExecuted = True
			except:
				self.disconnect()
				requestExecuted = False

			if requestExecuted:
				#database disconnection
				self.disconnect()
			else:
				succes = False
		else:
			succes = False

		#transform all profil in database on profils instance classe
		if tmpProfilsList != False:
			profilsList = []

			if len(tmpProfilsList) > 0:
				for profil in tmpProfilsList:
					try:
						profilsList.append(Profil(profil[0], profil[1], profil[2], profil[3], profil[4]))
					except:
						profilsList = False
						break
			else:
				profilsList = []
		else:
			profilsList = False

		if profilsList != False:
			if len(profilsList) > 0:
				for profil in profilsList:
					if isinstance(profil, Profil):
						succes = True
					else:
						profilsList = False
						break
			else:
				succes = True
		else:
			succes = False

		if succes:
			return profilsList
		else:
			return False


	def get_inhabitant_List(self):
		"""
    		method called for get an list of inhabitant

			functioning:
				1.connect to the database
				2.get all inhabitant in database
				3.database disconnection
				4.transform all inhabitant in database on inhabitant instance classe
				5.check inhabitant list conformity
				6.return
    		
			return:
    			list of inhabitant class
    	"""

		succes = requestExecuted = tmpInhabitantList = inhabitantList = False

		request = """SELECT * FROM Users WHERE role = 'inhabitant'"""

		#connect to the database
		if self.connect():
			try:
				#get all inhabitant in database
				self.db_cursor.execute(request)
				tmpInhabitantList = self.db_cursor.fetchall()
				requestExecuted = True
			except:
				self.disconnect()
				requestExecuted = False

			if requestExecuted:
				#database disconnection
				self.disconnect()
			else:
				succes = False
		else:
			succes = False

		#transform all inhabitant in database on inhabitant instance classe
		if tmpInhabitantList != False:
			inhabitantList = []

			if len(tmpInhabitantList) > 0:
				for inhabitant in tmpInhabitantList:
					inhabitantProfil = False
					inhabitantProfil = self.get_profil_by_id(int(inhabitant[1]))

					if inhabitantProfil != False:
						try:
							if inhabitant[2] == "admin":
								inhabitantList.append(Administrator(inhabitant[0], inhabitantProfil, inhabitant[4], inhabitant[5]))
							else:
								inhabitantList.append(Inhabitant(inhabitant[0], inhabitantProfil, inhabitant[2], inhabitant[4], inhabitant[5]))
						except:
							pass
					else:
						inhabitantList = False
						break
			else:
				inhabitantList = []
		else:
			succes = False

		#check inhabitant list conformity
		if inhabitantList != False:
			if len(inhabitantList) > 0:
				for inhabitant in inhabitantList:
					if isinstance(inhabitant, Inhabitant):
						succes = True
					else:
						succes = False
						break
			else:
				succes = True
		else:
			succes = False

		#return
		if succes:
			return inhabitantList
		else:
			return False


	def get_guest_list(self):
		"""
    		method called for get an list of guest

			functioning:
				1.connect to the database
				2.get all guest in database
				3.database disconnection
				4.transform all guest in database on guest instance classe
				5.check guest list conformity
				6.return
    		
			return:
    			list of guest class
    	"""

		succes = requestExecuted = tmpGuestList = guestList = False

		request = """SELECT * FROM Users WHERE role = 'guest'"""

		#connect to the database
		if self.connect():
			try:
				#get all guest in database
				self.db_cursor.execute(request)
				tmpGuestList = self.db_cursor.fetchall()
				requestExecuted = True
			except:
				self.disconnect()
				requestExecuted = False

			if requestExecuted:
				#database disconnection
				self.disconnect()
			else:
				succes = False
		else:
			succes = False

		#transform all guest in database on guest instance classe
		if tmpGuestList != False:
			guestList = []

			if len(tmpGuestList) > 0:
				for guest in tmpGuestList:
					guestProfil = False
					guestProfil = self.get_profil_by_id(int(guest[1]))

					if guestProfil != False:
						try:
							guestList.append(Guest(guest[0], guestProfil, guest[4], guest[5]))
						except:
							pass
					else:
						guestList = False
						break
			else:
				guestList = []
		else:
			succes = False

		#check guest list conformity
		if guestList != False:
			if len(guestList) > 0:
				for guest in guestList:
					if isinstance(guest, Guest):
						succes = True
					else:
						succes = False
						break
			else:
				succes = True
		else:
			succes = False

		#return
		if succes:
			return guestList
		else:
			return False


	def get_administrator_list(self):
		"""
    		method called for get an list of administator

			functioning:
				1.connect to the database
				2.get all administator in database
				3.database disconnection
				4.transform all inhabitant in administator on inhabitant instance classe
				5.check administator list conformity
				6.return
    		
			return:
    			list of administator class
    	"""

		succes = requestExecuted = tmpAdministatorList = administatorList = False

		request = """SELECT * FROM Users WHERE grade = 'admin'"""

		#connect to the database
		if self.connect():
			try:
				#get all administator in database
				self.db_cursor.execute(request)
				tmpAdministatorList = self.db_cursor.fetchall()
				requestExecuted = True
			except:
				self.disconnect()
				requestExecuted = False

			if requestExecuted:
				#database disconnection
				self.disconnect()
			else:
				succes = False
		else:
			succes = False

		#transform all inhabitant in administator on inhabitant instance classe
		if tmpAdministatorList != False:
			administatorList = []

			if len(tmpAdministatorList) > 0:
				for administator in tmpAdministatorList:
					administatorProfil = False
					administatorProfil = self.get_profil_by_id(int(administator[1]))

					if administatorProfil != False:
						try:
							administatorList.append(Administrator(administator[0], administatorProfil, administator[4], administator[5]))
						except:
							pass
					else:
						administatorList = False
						break
			else:
				administatorList = []
		else:
			succes = False

		#check administator list conformity
		if administatorList != False:
			if len(administatorList) > 0:
				for administator in administatorList:
					if isinstance(administator, Administrator):
						succes = True
					else:
						succes = False
						break
			else:
				succes = True
		else:
			succes = False

		#return
		if succes:
			return administatorList
		else:
			return False


	def get_profil_by_id(self, profilId):
		"""
    		method called for get an specific profil
				functionning:
					1.connect to database
					2.ask to database to select the profil with an predefined id
					3.database disconnection
					4.transform alprofil in profil instance classe
					5.check profil conformity
					6.return
    			return:
    				profil class/False
    	"""

		profil = requestExecuted = False

		#connect to database
		if isinstance(profilId, int):
			if self.connect():
				request = "SELECT * FROM Profils WHERE id = {}".format(profilId)
				
				try:
					#ask to database to select the profil with an predefined id
					self.db_cursor.execute(request)
					profil = self.db_cursor.fetchall()
					requestExecuted = True
				except:
					self.disconnect()
					requestExecuted = False

				if requestExecuted != False:
					#database disconnection
					self.disconnect()
				else:
					profil = False

				if profil != False:
					#transform profil in profil instance classe
					if len(profil) > 0:
						profil = profil[0]
						profil = Profil(profil[0], profil[1], profil[2], profil[3], profil[4])
					else:
						profil = False
				else:
					profil = False
			else:
				profil = False
		else:
			profil = False

		#check profil conformity
		if profil != False:
			if isinstance(profil, Profil):
				succes = True
			else:
				succes = False
		else:
			succes = False

		#return
		if succes:
			return profil
		else:
			return False



	#add method
	def add_user(self, firstName, lastName, gender, dateOfBirth, grade, role, identifiant, password):
		"""
            method used for create an user in database 

            functioning:
                1.check parametters conformity
				2.connect to the database
				3.add the profil of the user
				4.add the user
				5.commit change
				6.database disconnection
				7.check if the user is present in the users list
				8.return
                
            return:
				if succes return the user id
				else return false
                
        """

		succes = profilId = userId = requestExecuted = False

		#check parametters conformity
		if isinstance(firstName, str) \
			and isinstance(lastName, str) \
			and (gender == "f" or gender == "m")\
			and isinstance(dateOfBirth, str)\
			and isinstance(grade, str)\
			and (grade == "user" or grade == "admin")\
			and isinstance(role, str)\
			and (role == "guest" or role == "inhabitant")\
			and isinstance(identifiant, str)\
			and isinstance(password, str):

			#add the profil of the user
			profilId = self.add_profil(firstName, lastName, gender, dateOfBirth)

			if profilId != False:
				#connect to the database
				if self.connect():
					request = "INSERT INTO Users(fk_profil_id, grade, role, identifiant, password) VALUES\
						({}, '{}', '{}', '{}', '{}')".format(profilId, grade, role, identifiant, password)

					try:
						##add the user
						self.db_cursor.execute(request)
						requestExecuted = True
					except Exception as e:
						self.disconnect()
						requestExecuted = False

					if requestExecuted:
						#commit change
						if self.commit_change():
							try:
								userId = self.db_cursor.lastrowid
								#database disconnection
								self.disconnect()
							except:
								userId = False
								self.disconnect()
						else:
							userId = False
							self.disconnect()

						#check if the user is present in the users list
						if profilId != False and userId != False:
							for user in self.get_users_list():
								if user.id == userId and user.profil.id == profilId:
									succes = True
								else:
									succes = False

								if succes:
									break
					else:
						succes = False
						self.disconnect()
				else:
					succes = False
			else:
				succes = False
		else:
			succes = False

		#return
		if succes:
			return userId
		else:
			return False


	def add_profil(self, firstName, lastName, gender, dateOfBirth):
		"""
    		method called for adding an profil
    		functionning:
				1.check parametters conformity
				2.connect to the database
				3.add profil in database
				4.commit change
				5.get id of the new profil
				6.diconnection of the database
				7.check if profil is in profils list
				8.return

    		return:
    			if succes return profil id
				else return false
    	"""

		succes = profilId = requestExecuted = False

		#check parametters conformity
		if isinstance(firstName, str) \
				and isinstance(lastName, str) \
				and (gender == "f" or gender == "m")\
				and isinstance(dateOfBirth, str):

			#connect to the database
			if self.connect():
				request = "INSERT INTO Profils(first_name, last_name, gender, date_of_birth) VALUES\
				('{}', '{}', '{}', '{}')".format(firstName, lastName, gender, dateOfBirth)

				try:
					#add profil in database
					self.db_cursor.execute(request)
					requestExecuted = True
				except Exception as e:
					print(e)
					self.disconnect()
					requestExecuted = False

				if requestExecuted:
					#commit change
					if self.commit_change():
						try:
							#get id of the new profil
							profilId = self.db_cursor.lastrowid
							#diconnection of the database
							self.disconnect()
						except:
							profilId = False
							self.disconnect()
					else:
						profilId = False
						self.disconnect()

					if profilId != False:
						#check if profil is in profils list
						for profil in self.get_profils_list():
							if profil.id == profilId \
								and profil.firstName == firstName \
								and profil.lastName == lastName \
								and profil.gender == gender \
								and profil.dateOfBirth == dateOfBirth:

								succes = True
							else:
								succes = False

							if succes:
								break
					else:
						succes = False
				else:
					succes = False
					self.disconnect()
			else:
				succes = False
		else:
			succes = False

		#return
		if succes:
			return profilId
		else:
			return False



	#checking methods
	def check_config_file_existence(self):
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
		except:
			succes = False

		return succes


	def check_database_connection(self):
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
			if self.disconnect():
				succes = True
			else:
				succes = False
		else:
			succes = False

		return succes