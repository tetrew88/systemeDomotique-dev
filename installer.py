#!/usr/bin/python3


import os

import mysql.connector

from classes.installer import *



def install():
	scriptPath = os.path.dirname(os.path.abspath(__file__))
	installChoice = systemUserName = databaseName = systemUserPassword = rootDatabasePassword = ""
	databaseConfigured = databaseConnection = databaseCursor = False
	data = {}
	

	installer = Installer(scriptPath)
	#if user installer was lauch in sudo mode
	print("\n\nBienvenu dans l'installateur du système domotique.\n\n")

	print("le système va télécharger les programmes et modules nécessaire\na son fonctionnement et vous demandera de remplir quelque informations\n")

	installChoice = installer.get_install_choice()
	print(installChoice)

	if installChoice != False and installChoice == "o":
		print("\ninstallation des programmes nécessaire au fonctionnement du système\n\n")

		#database installation/configuration
		print("téléchargement du système de base de donnée")
		installer.download_database_system()
		print("installation du système de base de donnée")
		installer.install_database_system()

		print("\n\n")

		print("\n\nconfiguration du compte utilisateur que va utiliser le système pour intéragire avec la base de donnée\n")

		"""setting database username"""
		print("commencons par le nom d'utilisateur que le système utilisera pour interagir avec la base de donnée.\nappuyer directement sur entrer pour utiliser le nom prédéfini (homeAutomationSystem)\n\n")

		systemUserName = installer.get_system_username()

		"""setting user password"""
		print("\n\nenssuite le mot de passe\n")
		systemUserPassword = installer.get_system_user_password()

		"""setting database name"""
		print("\n\nfinisson avec le nom de la base de donnée.\nappuyer directement sur entrer pour utiliser le nom prédéfini (home)\n\n")

		databaseName = installer.get_database_name()

		"""creating database config file"""
		data = {}

		data["userName"] = systemUserName
		data["password"] = systemUserPassword
		data["databaseName"] = databaseName

		installer.create_database_config_file(data)

		"""database création"""
		print("\n\ncréation de la base de donnée")
		if installer.create_database(databaseName):
			"""table creation"""
			if installer.create_database_table(databaseName):
				"""user system creation"""
				if installer.create_database_system_user(systemUserName):
					#systeme user privilege attribution
					if installer.give_user_system_privilege(systemUserName, databaseName)
						"""mysql test connexion"""
						databaseConnection = mysql.connector.connect(
							host = "localHost",
							user = "root",
							passwd = rootDatabasePassword,
							database = databaseName
						)
						databaseCursor =  databaseConnection.cursor(buffered=True)

						if databaseConnection != False and databaseCursor != False:
							"""user system creation"""
							print("\n\ncréation de l'utilisateur système")
							databaseConfigured = True
							databaseConnection.close()
						else:
							databaseConfigured = False
					else:
						databaseConfigured = False
				else:
					databaseConfigured = False
			else:
				databaseConfigured = False
		else:
			databaseConfigured = False

		if databaseConfigured == True:
			print("\n\nBase de donnée configurer")
		else:
			print("\n\nerreur lors de la configuration de la base de donnée")
			quit()

	else:
		pass


if __name__ == '__main__':
	install()