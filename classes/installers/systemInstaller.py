import sys
sys.path.append("..")

from systemeDomotique.homeAutomationServer.classes.homeDatabase import *

from .databaseInstaller import *
from .homeAutomationSystemInstaller import *


class SystemInstaller:
	"""
		class bringing all the information and functionality of the installer.

			Attributes:
				version: version of the installer
				script path (path of the main script (for files manipulation))

				database installer (class contained all function used for database installation)
				home automation system installer (class contained all function used for home automation system installation)

			Propertys:
				systemInstalled: boolean allowing to know if the system is installed
				databaseConfigured: boolean allowing to know if the databse is configured
				homeAutomationSystemConfigured: boolean allowing to know if the home automation system is configured

			Methods:
				get_install_choice: method allowing to get the user install choice
				database_installation: method used for database installation
				homeAutomationSystem_installation: method used for home automation system installation

	"""

	def __init__(self, scriptPath):
		self.version = '0.0.1'
		self.scriptPath = scriptPath
		self.databaseInstaller = DatabaseInstaller(scriptPath)
		self.homeAutomationSystemInstaller = HomeAutomationSystemInstaller(scriptPath)


	"""PROPERTY"""
	@property
	def systemInstalled(self):
		if self.databaseConfigured == True and self.homeAutomationSystemConfigured == True:
			return True
		else:
			return False


	@property
	def databaseConfigured(self):
		return self.databaseInstaller.databaseConfigured


	@property
	def homeAutomationSystemConfigured(self):
		return self.homeAutomationSystemInstaller.homeAutomationSystemConfigured



	"""GET METHODS"""
	def get_install_choice(self):
		"""
			method used for collect the install choice of the user

			functioning:
				1.collecte user choice
				2.check conformity of the choice
				3.return

			return:
				if succes return the install choice
				else return False
		"""

		succes = False
		installChoice = ""

		#collect user choice
		try:
			installChoice = input("\nvoulez-vous installer le système domotique ?(o/n): ").lower()
		except:
			installChoice = "" 

		#check conformity of the choice
		if installChoice == 'o' or installChoice == 'n':
			succes = True
		else:
			succes = False

		#return
		if succes:
			return installChoice
		else:
			return False


	def get_administrator_list(self):
		homeDatabase = HomeDatabase(self.scriptPath)

		return homeDatabase.get_administrator_list()


	def get_administrator_first_name(self):
		"""
            method used for collect the administrator first name

            functioning:
                1.collect the first name
                2.check conformity of the first name

            return:
                if succes return the first name
                else return False
        """
		
		succes = False
		firstName = ""
		
		#collect the first name
		try:
			firstName = input("\nentrer votre prenom: ")
		except:
			firstName = ""

        #check conformity of the first name
		if isinstance(firstName, str) and firstName != "":
			succes = True
		else:
			succes = False

        #return
		if succes:
			return firstName
		else:
			return False


	def get_administrator_last_name(self):
		"""
            method used for collect the administrator last name

            functioning:
                1.collect the last name
                2.check conformity of the last name

            return:
                if succes return the last name
                else return False
        """
		
		succes = False
		lastName = ""
		
		#collect the last name
		try:
			lastName = input("\nentrer votre nom: ")
		except:
			lastName = ""

        #check conformity of the last name
		if isinstance(lastName, str) and lastName != "":
			succes = True
		else:
			succes = False

        #return
		if succes:
			return lastName
		else:
			return False


	def get_administrator_date_of_birth(self):
		"""
            method used for collect the administrator date of birth

            functioning:
                1.collect the date of birth
                2.check conformity of the date of birth

            return:
                if succes return the date of birth
                else return False
        """
		
		succes = False
		dateOfBirth = ""
		
		#collect the dateOfBirth
		try:
			dateOfBirth = input("\nentrer votre date de naissance(ex: 26/09/1994): ")
		except:
			dateOfBirth = ""

        #check conformity of the dateOfBirth
		if isinstance(dateOfBirth, str) and len(dateOfBirth) == 10:
			succes = True
		else:
			succes = False

        #return
		if succes:
			return dateOfBirth
		else:
			return False


	def get_administrator_gender(self):
		"""
            method used for collect the administrator gender

            functioning:
                1.collect the gender
                2.check conformity of the gender

            return:
                if succes return the gender
                else return False
        """
		
		succes = False
		gender = ""
		
		#collect the gender
		try:
			gender = input("\nentrer votre sexe (m/f): ").lower()
		except:
			gender = ""

        #check conformity of the gender
		if isinstance(gender, str) and gender == "m" or gender =="f":
			succes = True
		else:
			succes = False

        #return
		if succes:
			return gender
		else:
			return False


	def get_administator_identifiant(self):
		"""
            method used for collect the administrator identifiant

            functioning:
                1.collect the identifiant
                2.check conformity of the identifiant

            return:
                if succes return the identifiant
                else return False
        """
		
		succes = False
		identifiant = ""
		
		#collect the identifiant
		try:
			identifiant = input("\nentrer votre identifiant: ").lower()
		except:
			identifiant = ""

        #check conformity of the identifiant
		if isinstance(identifiant, str) and identifiant != "":
			succes = True
		else:
			succes = False

        #return
		if succes:
			return identifiant
		else:
			return False


	def get_administrator_password(self):
		"""
            method used for collect the administrator password

            functioning:
                1.collect the password
                2.check conformity of the password

            return:
                if succes return the password
                else return False
        """
		
		succes = False
		password = ""
		
		#collect the password
		try:
			password = input("\nentrer votre mot de passe: ").lower()
		except:
			password = ""

        #check conformity of the password
		if isinstance(password, str) and password != "":
			succes = True
		else:
			succes = False

        #return
		if succes:
			return password
		else:
			return False


	"""INSTALLATION METHODS"""
	def database_installation(self):
		"""
			method used for database installation

			functioning:
				1.download database system (maria db)
				2.get system user information and database name
				3.create the config file of the database
				4.create the database
				5.create table of the database
				6.create system user in database system
				7.attribute privilege on database at the system user
				8.set database configuration control booleen on true
				9.return

			return:
				if succes return True
				else return False
		"""

		succes = databaseInstalled = False
		configFileCreated = databaseCreated = databaseTablesCreated = False
		systemUserCreated = privilegeAttribued = False
		systemUserName = systemUserPassword = databaseName = ""
			
		#download database system (maria db)
		if self.databaseInstaller.download_database_system():
			databaseInstalled = True
		else:
			databaseInstalled = False


		if databaseInstalled:
			#get system user information and database name
			systemUserName = self.databaseInstaller.get_system_username()
			systemUserPassword = self.databaseInstaller.get_system_user_password()
			databaseName = self.databaseInstaller.get_database_name()

			if systemUserName and systemUserPassword and databaseName:
				#create the config file of the database
				if self.databaseInstaller.create_database_config_file(systemUserName, systemUserPassword, databaseName, False):
					configFileCreated = True
				else:
					configFileCreated = False
			else:
				succes = False

			if configFileCreated:
				#create the database
				if self.databaseInstaller.create_database(databaseName):
					databaseCreated = True
				else:
					databaseCreated = False
			else:
				succes = False

			if databaseCreated:
				#create table of the database
				if self.databaseInstaller.create_database_table(databaseName):
					databaseTablesCreated = True
				else:
					databaseTablesCreated = False
			else:
				succes = False

			if databaseCreated and databaseTablesCreated:
				#create system user in database system
				if self.databaseInstaller.create_database_system_user(systemUserName, systemUserPassword):
					systemUserCreated = True
				else:
					systemUserCreated = False
			else:
				succes = False

			if systemUserCreated:
				#attribute privilege on database at the system user
				if self.databaseInstaller.attribute_user_system_privilege(systemUserName, databaseName):
					privilegeAttribued = True
				else:
					privilegeAttribued = False
			else:
				succes = False
		else:
			succes = False

		if databaseInstalled and configFileCreated and \
			databaseCreated and databaseTablesCreated and \
				systemUserCreated and privilegeAttribued:
			#set database configuration control booleen on true
			if self.databaseInstaller.set_database_configuration_booleean_control(True):
				succes = True
			else:
				succes = False
		else:
			succes = False

		return succes


	def homeAutomationSystem_installation(self):
		"""
			method used for home automation system installation

			functioning:
				1.download supervisor
				2.download nginx
				3.get zwave controller path
				4.get zwave config folder path
				5.assigned an fixed usb port name to the controller
				6.create home automation config file
				7.create nginx config file
				8.create web interface supervisor config file
				9.create automation server supervisor config file
				10.set home automation system configuration booléean on True
				11. ...

			return:
				if succes return True
				else return False
		"""

		succes = nginxInstalled = supervisorInstalled = usbPortNameAssigned  = False
		configFileCreated = nginxConfigFileCreated = False
		webIntefaceSuperviorConfigFileCreated = automationServerSuperviorConfigFileCreated = False
		zwaveControllerPath = zWaveConfigFolderPath = ""


		if self.homeAutomationSystemInstaller.dowload_supervisor() :
			supervisorInstalled = True
		else:
			supervisorInstalled = False

		if self.homeAutomationSystemInstaller.download_nginx():
			nginxInstalled = True
		else:
			nginxInstalled = False

		if nginxInstalled and supervisorInstalled:
			#get zwave controller path
			zwaveControllerPath = self.homeAutomationSystemInstaller.get_zwave_controller_path()
			
			zWaveConfigFolderPath = self.homeAutomationSystemInstaller.get_zwave_config_folder_path()


			if zwaveControllerPath and zWaveConfigFolderPath:
				if self.homeAutomationSystemInstaller.assign_fixed_usb_port_names_to_controller(zwaveControllerPath):
					usbPortNameAssigned = True
				else:
					usbPortNameAssigned = False

				if usbPortNameAssigned:
					if self.homeAutomationSystemInstaller.create_home_automation_system_config_file(zwaveControllerPath, zWaveConfigFolderPath, False):
						configFileCreated = True
					else:
						configFileCreated = False

					if configFileCreated:
						if self.homeAutomationSystemInstaller.create_nginx_config_file():
							nginxConfigFileCreated = True
						else:
							nginxConfigFileCreated = False

						if nginxConfigFileCreated:
							if self.homeAutomationSystemInstaller.create_web_interface_supervisor_config_file():
								webIntefaceSuperviorConfigFileCreated = True
							else:
								webIntefaceSuperviorConfigFileCreated = False

							if self.homeAutomationSystemInstaller.create_automation_server_supervisor_config_file():
								automationServerSuperviorConfigFileCreated = True
							else:
								automationServerSuperviorConfigFileCreated = False
						else:
							succes = False
					else:
						succes = False
				else:
					succes = False
			else:
				succes = False
		else:
			succes = False

		if usbPortNameAssigned and configFileCreated and nginxConfigFileCreated and webIntefaceSuperviorConfigFileCreated and automationServerSuperviorConfigFileCreated:
			if self.homeAutomationSystemInstaller.set_home_automation_system_configuration_booleean_control(True):
				succes = True
			else:
				succes = False
		else:
			succes = False

		return succes



	#create method
	def create_administrator_user(self, firstName, lastName, gender, dateOfBirth, grade, role, identifiant, password):
		"""
			method used for create an administrator user

			functionning:
				1.check parametters conformity
				2.add the user to the database
				3.return

			return:
				if succes return true
				else return false
		"""
		
		homeDatabase = HomeDatabase(self.scriptPath)
		succes = False

		#check parametters conformity
		if isinstance(firstName, str) \
			and isinstance(lastName, str) \
			and (gender == "f" or gender == "m")\
			and isinstance(dateOfBirth, str)\
			and isinstance(grade, str)\
			and grade == "admin"\
			and isinstance(role, str)\
			and role == "inhabitant"\
			and isinstance(identifiant, str)\
			and isinstance(password, str):

			#add the user to the database
			if homeDatabase.add_user(firstName, lastName, gender, dateOfBirth, grade, role, identifiant, password):
				succes = True
			else:
				succes = False
		else:
			succes = False

		#return
		return succes