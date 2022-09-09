#!/usr/bin/python3


import os

from classes.installer import *



def install():
	scriptPath = os.path.dirname(os.path.abspath(__file__))
	installChoice = systemUserName = databaseName = systemUserPassword = rootDatabasePassword = ""
	databaseConfigured = databaseConnection = databaseCursor = False
	data = {}
	

	installer = Installer(scriptPath)
	#if user installer was lauch in sudo mode
	if os.getuid() == 0:
		print("\n\nBienvenu dans l'installateur du système domotique.\n\n")

		print("le système va télécharger les programmes et modules nécessaire\na son fonctionnement et vous demandera de remplir quelque informations\n")

		installChoice = installer.get_install_choice()
		print(installChoice)

		if installChoice != False and installChoice == "o":
			print("\ninstallation des programmes nécessaire au fonctionnement du système\n\n")

			#database installation/configuration
			installer.download_database_system()
			installer.install_database_system()

			rootDatabasePassword = installer.get_root_database_system_password()

			if rootDatabasePassword != False:
				if installer.check_database_config_file_existence():
					print("\n\nconfiguration du compte utilisateur que va utiliser le système pour intéragire avec la base de donnée\n")

					"""setting database username"""
					print("commencons par le nom d'utilisateur que le système utilisera pour interagir avec la base de donnée.\n\
						appuyer directement sur entrer pour utiliser le nom prédéfini (homeAutomationSystem)\n\n")

					systemUserName = installer.get_system_username()

					"""setting user password"""
					print("\n\nenssuite le mot de passe\n")
					systemUserPassword = installer.get_system_user_password()

					"""setting database name"""
					print("\n\nfinisson avec le nom de la base de donnée.\n\
						appuyer directement sur entrer pour utiliser le nom prédéfini (home)\n\n")

					databaseName = installer.get_database_name()

					"""creating database config file"""
					data = {}

					data["userName"] = systemUserName
					data["password"] = systemUserPassword
					data["databaseName"] = databaseName

					installer.create_database_config_file(data)
				else:
					pass

				"""mysql connexion"""
				try:
					databaseConnection = mysql.connector.connect(
						host = "localHost",
						user = "root",
						passwd = rootDatabasePassword
					)
					databaseCursor =  databaseConnection.cursor(buffered=True)
				except:
					print("\n\nerreur de connection root a la base de donnée")
					quit()

				if databaseConnection != False:
					"""user system creation"""
					print("\n\ncréation de l'utilisateur système")
					if installer.create_database_system_user(databaseCursor, systemUserName):
						"""Database création"""
						print("\n\ncréation de la base de donnée")
						if installer.create_database(databaseCursor, databaseName):
							#systeme user privilege attribution
							print("\n\nattribution des droits a l'utilisateur système")
							if installer.give_user_system_privilege(databaseCursor, systemUserName, databaseName):
								databaseConnection.close()
								databaseConfigured = True
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
			pass
	else:
		print("Lancer le programme en mode superutilisateur (sudo).")


if __name__ == '__main__':
	install()