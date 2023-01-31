#!/usr/bin/python3

import os

import mysql.connector

import sys

sys.path.append("..")

from systemeDomotique.classes.installers.systemInstaller import *


def install():
	"""
		function used for install/configure the component of the automation system

		functioning:
			1.get user choice
			2.install and configure database
			3.install and configure home automation system
			4.check installations succes
			5.create administrator user
			6.return succes

		return:
			if succes return true
			else return false	
	"""

	scriptPath = os.path.dirname(os.path.abspath(__file__))
	installChoice = ""
	succes = databaseInstalled = homeAutomationSystemInstalled = False
	administratorList = administratorUserCreated = False
	administratorFirstName = administratorLastName = administratorGender = ""
	administratorDateOfBirth = administratorIdentifiant = administratorPassword = ""
	administratorGrade = "admin"
	administratorRole = "inhabitant"
	systemInstaller = SystemInstaller(scriptPath)

	print("\n\nBienvenu dans l'installateur du système domotique.\n\n")

	print("le système va télécharger les programmes et modules nécessaire\n"\
		"a son fonctionnement et vous demandera de remplir quelque informations")

	#get user choice
	installChoice = systemInstaller.get_install_choice()


	if installChoice == "o":
		#database installation/configuration
		if systemInstaller.databaseConfigured == False:
			print("\ninstallation/configuration de la base de donnée")
			if systemInstaller.database_installation():
				print("\nbase de donne configurer")
				databaseInstalled = True
			else:
				print("\nerreur lors de la configuration de la base de donnée")
				databaseInstalled = False
		else:
				databaseInstalled = True
			
		if databaseInstalled:
			if systemInstaller.homeAutomationSystemConfigured == False:
				#home automation system installation/configuration
				print("\ninstallation/configuration du système domotique")
				if systemInstaller.homeAutomationSystem_installation():
					print("\nsystème domotique configurer")
					homeAutomationSystemInstalled = True
				else:
					print("\nerreur lors de la configuration du système domotique")
					homeAutomationSystemInstalled = False
			else:
				homeAutomationSystemInstalled = True
		else:
			homeAutomationSystemInstalled = False

		#checking succes of installation
		if databaseInstalled == True and homeAutomationSystemInstalled == True:
			administratorList = systemInstaller.get_administrator_list()

			if administratorList != False:
				if len(administratorList) < 1:
					#create administrator user
					administratorFirstName = systemInstaller.get_administrator_first_name()
					administratorLastName = systemInstaller.get_administrator_last_name()
					administratorGender = systemInstaller.get_administrator_gender()
					administratorDateOfBirth = systemInstaller.get_administrator_date_of_birth()
					administratorIdentifiant = systemInstaller.get_administator_identifiant()
					administratorPassword = systemInstaller.get_administrator_password()

					if isinstance(administratorFirstName, str) == True\
						and isinstance(administratorLastName, str)\
						and isinstance(administratorDateOfBirth, str)\
						and (administratorGender == "f" or administratorGender == "m")\
						and administratorGrade == "admin"\
						and administratorRole == "inhabitant"\
						and isinstance(administratorIdentifiant, str)\
						and isinstance(administratorPassword, str):

						if systemInstaller.create_administrator_user(administratorFirstName, administratorLastName, administratorGender, administratorDateOfBirth, administratorGrade, administratorRole, administratorIdentifiant, administratorPassword):
							administratorUserCreated = True
						else:
							administratorUserCreated = False
					else:
						administratorUserCreated = False
				else:
					administratorUserCreated = True
			else:
				administratorUserCreated = False
		else:
			administratorUserCreated = False

		#checking if all is succesfull
		if administratorUserCreated == True and databaseInstalled  == True and homeAutomationSystemInstalled == True:
			succes = True
		else:
			succes = False

		if succes:
			print("\nl'installation s'est dérouler avec succes")
		else:
			print("\nune erreur s'est produite durrant l'installation")
	
	else:
		if installChoice == 'n':
			print('\naurevoir')
			succes = True
		else:
			succes = False

	#return
	return succes


if __name__ == '__main__':
	install()