#!/usr/bin/python3


import os

import mysql.connector

from classes.installer import *



def install():
	scriptPath = os.path.dirname(os.path.abspath(__file__))
	installChoice = systemUserName = databaseName = systemUserPassword = ""
	succes = databaseConfigured = databaseConnection = databaseCursor = False
	data = {}
	

	installer = Installer(scriptPath)
	#if user installer was lauch in sudo mode
	print("\n\nBienvenu dans l'installateur du système domotique.\n\n")

	print("le système va télécharger les programmes et modules nécessaire\na son fonctionnement et vous demandera de remplir quelque informations")

	installChoice = installer.get_install_choice()

	if installChoice != False and installChoice == "o":

		print("\n\ninstallation des programmes nécessaire au fonctionnement du système")
		#database installation/configuration

		"""download database system"""
		print("\n\ntéléchargement du système de base de donnée")
		installer.download_database_system()

		print("\n\nconfiguration de la base de donnée")


		"""setting database username"""
		print("\n\nEntrer le nom d'uilisateur qui sera utiliser par le system.\nappuyer sur entrer pour utiliser le nom prédéfini (homeAutomationSystem)\n\n")

		systemUserName = installer.get_system_username()

		"""setting user password"""
		print("\n\nenssuite le mot de passe du compte utilisateur system\n")
		systemUserPassword = installer.get_system_user_password()

		"""setting database name"""
		print("\n\nfinisson avec le nom de la base de donnée.\nappuyer sur entrer pour utiliser le nom prédéfini (Home)\n\n")

		databaseName = installer.get_database_name()


		"""creating database config file"""
		data = {}

		data["userName"] = systemUserName
		data["password"] = systemUserPassword
		data["databaseName"] = databaseName

		if installer.create_database_config_file(data):


			"""database création"""
			print("\n\ncréation de la base de donnée")
			if installer.create_database(databaseName):
				"""table creation"""

				print("créations des tables")
				if installer.create_database_table(databaseName):
					"""user system creation"""

					print("création de l'utilisateur system")
					if installer.create_database_system_user(systemUserName, systemUserPassword):
						#systeme user privilege attribution

						print("attribution des droits a l'utilisateur system")
						if installer.give_user_system_privilege(systemUserName, databaseName):
							"""mysql test connexion"""

							print("test de connexion a la base de donnee")
							try:
								databaseConnection = mysql.connector.connect(
									host = "localHost",
									user = systemUserName,
									passwd = systemUserPassword,
									database = databaseName
								)
								databaseCursor =  databaseConnection.cursor(buffered=True)
							except:
								databaseConnection = databaseCursor = False
								print("erreur lord de la connexion a la base de donnée")

							if databaseConnection != False and databaseCursor != False:
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

		else:
			databaseConfigured = False


		if databaseConfigured == True:
			print("\n\nBase de donnée configurer")
		else:
			print("\n\nerreur lors de la configuration de la base de donnée")

		if databaseConfigured == True and if installer.check_database_config_file_existence():
			succes = True
		else:
			succes = False


		if succes:
			print("\n\nsysteme installer")
		else:
			print("\n\nerreur lors de l'installation")
			if databaseConfigured == False:
				print('i:erreur lors de la configuration de la base de donnée')
			if installer.check_database_config_file_existence():
				print("i:erreur lors de la création du fichier de configuration de la base de donnée")

	else:
		pass


if __name__ == '__main__':
	install()