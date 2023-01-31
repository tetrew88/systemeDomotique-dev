#!/usr/bin/python3

import mock
import sys

sys.path.append("..")
from systemeDomotique.installer import *

from unittest.mock import patch, mock_open, MagicMock, PropertyMock

class TestInstaller:

    def test_installation(self):
        '''
            check if method return true if succes
            check if method return false if error
            check if method detect wrong install choice
            check if method detect the user choice "no"
            check if method detect error in database installation
            check if method detect error in home automation system installation
            check if method detect error during getting administrator list
            check if method detect error during getting administrator firstname
            check if method detect error during getting administrator last name
            check if method detect error during getting administrator gender
            check if method detect bad gender
            check if method detect error during getting date of birth
            check if method detect error during getting administrator identifiant
            check if method detect error during getting administrator password
            check if method detect error during administrator user creation
        '''

        #check if method return true if succes
        with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.databaseConfigured', new_callable=PropertyMock) as mockedDatabaseConfiguredProperty:
            mockedDatabaseConfiguredProperty.return_value = False

            with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.homeAutomationSystemConfigured', new_callable=PropertyMock) as mockedHomeAutomationSystemConfigured:
                mockedHomeAutomationSystemConfigured.return_value = False

                with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_install_choice') as mockedGettingInstallChoice:
                    mockedGettingInstallChoice.return_value = "o"

                    with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.database_installation') as mockedDatabaseInstallation:
                        mockedDatabaseInstallation.return_value = True

                        with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.homeAutomationSystem_installation') as mockedHomeAutomationSystemInstallation:
                            mockedHomeAutomationSystemInstallation.return_value = True

                            with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_list') as mockedGettingAdministratorList:
                                mockedGettingAdministratorList.return_value = []
                            
                                with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_first_name') as mockedGettingAdministratorFirstName:
                                    mockedGettingAdministratorFirstName.return_value = "donovan"

                                    with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_last_name') as mockedGettingAdministratorLastName:
                                        mockedGettingAdministratorLastName.return_value = "maurice"

                                        with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_gender') as mockedGettingAdministratorGender:
                                            mockedGettingAdministratorGender.return_value = "m"

                                            with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_date_of_birth') as mockedGettingAdministratorDateOfBirth:
                                                mockedGettingAdministratorDateOfBirth.return_value = "26/09/1994"
                                        
                                                with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administator_identifiant') as mockedGettingAdministratorIdentifiant:
                                                    mockedGettingAdministratorIdentifiant.return_value = "tetrew"

                                                    with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_password') as mockedGettingAdministratorPassword:
                                                        mockedGettingAdministratorPassword.return_value = "0000"

                                                        with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.create_administrator_user') as mockedCreatingAdministratorUser:
                                                            mockedCreatingAdministratorUser.return_value = True

                                                            assert install() == True


        #check if method return false if error
        with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.databaseConfigured', new_callable=PropertyMock) as mockedDatabaseConfiguredProperty:
            mockedDatabaseConfiguredProperty.return_value = False

            with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.homeAutomationSystemConfigured', new_callable=PropertyMock) as mockedHomeAutomationSystemConfigured:
                mockedHomeAutomationSystemConfigured.return_value = False

                with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_install_choice') as mockedGettingInstallChoice:
                    mockedGettingInstallChoice.return_value = False

                    with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.database_installation') as mockedDatabaseInstallation:
                        mockedDatabaseInstallation.return_value = False

                        with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.homeAutomationSystem_installation') as mockedHomeAutomationSystemInstallation:
                            mockedHomeAutomationSystemInstallation.return_value = False

                            with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_list') as mockedGettingAdministratorList:
                                mockedGettingAdministratorList.return_value = False
                            
                                with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_first_name') as mockedGettingAdministratorFirstName:
                                    mockedGettingAdministratorFirstName.return_value = False

                                    with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_last_name') as mockedGettingAdministratorLastName:
                                        mockedGettingAdministratorLastName.return_value = False

                                        with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_gender') as mockedGettingAdministratorGender:
                                            mockedGettingAdministratorGender.return_value = False

                                            with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_date_of_birth') as mockedGettingAdministratorDateOfBirth:
                                                mockedGettingAdministratorDateOfBirth.return_value = False
                                        
                                                with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administator_identifiant') as mockedGettingAdministratorIdentifiant:
                                                    mockedGettingAdministratorIdentifiant.return_value = False

                                                    with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_password') as mockedGettingAdministratorPassword:
                                                        mockedGettingAdministratorPassword.return_value = False

                                                        with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.create_administrator_user') as mockedCreatingAdministratorUser:
                                                            mockedCreatingAdministratorUser.return_value = False

                                                            assert install() == False

        #check if method detect wrong install choice
        with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.databaseConfigured', new_callable=PropertyMock) as mockedDatabaseConfiguredProperty:
            mockedDatabaseConfiguredProperty.return_value = False

            with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.homeAutomationSystemConfigured', new_callable=PropertyMock) as mockedHomeAutomationSystemConfigured:
                mockedHomeAutomationSystemConfigured.return_value = False

                with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_install_choice') as mockedGettingInstallChoice:
                    mockedGettingInstallChoice.return_value = False

                    with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.database_installation') as mockedDatabaseInstallation:
                        mockedDatabaseInstallation.return_value = True

                        with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.homeAutomationSystem_installation') as mockedHomeAutomationSystemInstallation:
                            mockedHomeAutomationSystemInstallation.return_value = True

                            with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_list') as mockedGettingAdministratorList:
                                mockedGettingAdministratorList.return_value = []
                            
                                with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_first_name') as mockedGettingAdministratorFirstName:
                                    mockedGettingAdministratorFirstName.return_value = "donovan"

                                    with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_last_name') as mockedGettingAdministratorLastName:
                                        mockedGettingAdministratorLastName.return_value = "maurice"

                                        with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_gender') as mockedGettingAdministratorGender:
                                            mockedGettingAdministratorGender.return_value = "m"

                                            with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_date_of_birth') as mockedGettingAdministratorDateOfBirth:
                                                mockedGettingAdministratorDateOfBirth.return_value = "26/09/1994"
                                        
                                                with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administator_identifiant') as mockedGettingAdministratorIdentifiant:
                                                    mockedGettingAdministratorIdentifiant.return_value = "tetrew"

                                                    with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_password') as mockedGettingAdministratorPassword:
                                                        mockedGettingAdministratorPassword.return_value = "0000"

                                                        with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.create_administrator_user') as mockedCreatingAdministratorUser:
                                                            mockedCreatingAdministratorUser.return_value = True

                                                            assert install() == False

        #check if method detect the user choice "no"
        with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.databaseConfigured', new_callable=PropertyMock) as mockedDatabaseConfiguredProperty:
            mockedDatabaseConfiguredProperty.return_value = False

            with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.homeAutomationSystemConfigured', new_callable=PropertyMock) as mockedHomeAutomationSystemConfigured:
                mockedHomeAutomationSystemConfigured.return_value = False

                with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_install_choice') as mockedGettingInstallChoice:
                    mockedGettingInstallChoice.return_value = "n"

                    with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.database_installation') as mockedDatabaseInstallation:
                        mockedDatabaseInstallation.return_value = True

                        with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.homeAutomationSystem_installation') as mockedHomeAutomationSystemInstallation:
                            mockedHomeAutomationSystemInstallation.return_value = True

                            with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_list') as mockedGettingAdministratorList:
                                mockedGettingAdministratorList.return_value = []
                            
                                with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_first_name') as mockedGettingAdministratorFirstName:
                                    mockedGettingAdministratorFirstName.return_value = "donovan"

                                    with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_last_name') as mockedGettingAdministratorLastName:
                                        mockedGettingAdministratorLastName.return_value = "maurice"

                                        with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_gender') as mockedGettingAdministratorGender:
                                            mockedGettingAdministratorGender.return_value = "m"

                                            with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_date_of_birth') as mockedGettingAdministratorDateOfBirth:
                                                mockedGettingAdministratorDateOfBirth.return_value = "26/09/1994"
                                        
                                                with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administator_identifiant') as mockedGettingAdministratorIdentifiant:
                                                    mockedGettingAdministratorIdentifiant.return_value = "tetrew"

                                                    with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_password') as mockedGettingAdministratorPassword:
                                                        mockedGettingAdministratorPassword.return_value = "0000"

                                                        with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.create_administrator_user') as mockedCreatingAdministratorUser:
                                                            mockedCreatingAdministratorUser.return_value = True

                                                            assert install() == True

        #check if method detect error in database installation
        with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.databaseConfigured', new_callable=PropertyMock) as mockedDatabaseConfiguredProperty:
            mockedDatabaseConfiguredProperty.return_value = False

            with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.homeAutomationSystemConfigured', new_callable=PropertyMock) as mockedHomeAutomationSystemConfigured:
                mockedHomeAutomationSystemConfigured.return_value = False

                with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_install_choice') as mockedGettingInstallChoice:
                    mockedGettingInstallChoice.return_value = "o"

                    with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.database_installation') as mockedDatabaseInstallation:
                        mockedDatabaseInstallation.return_value = False

                        with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.homeAutomationSystem_installation') as mockedHomeAutomationSystemInstallation:
                            mockedHomeAutomationSystemInstallation.return_value = True

                            with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_list') as mockedGettingAdministratorList:
                                mockedGettingAdministratorList.return_value = []
                            
                                with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_first_name') as mockedGettingAdministratorFirstName:
                                    mockedGettingAdministratorFirstName.return_value = "donovan"

                                    with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_last_name') as mockedGettingAdministratorLastName:
                                        mockedGettingAdministratorLastName.return_value = "maurice"

                                        with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_gender') as mockedGettingAdministratorGender:
                                            mockedGettingAdministratorGender.return_value = "m"

                                            with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_date_of_birth') as mockedGettingAdministratorDateOfBirth:
                                                mockedGettingAdministratorDateOfBirth.return_value = "26/09/1994"
                                        
                                                with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administator_identifiant') as mockedGettingAdministratorIdentifiant:
                                                    mockedGettingAdministratorIdentifiant.return_value = "tetrew"

                                                    with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_password') as mockedGettingAdministratorPassword:
                                                        mockedGettingAdministratorPassword.return_value = "0000"

                                                        with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.create_administrator_user') as mockedCreatingAdministratorUser:
                                                            mockedCreatingAdministratorUser.return_value = True

                                                            assert install() == False

        #check if method detect error in home automation system installation
        with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.databaseConfigured', new_callable=PropertyMock) as mockedDatabaseConfiguredProperty:
            mockedDatabaseConfiguredProperty.return_value = False

            with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.homeAutomationSystemConfigured', new_callable=PropertyMock) as mockedHomeAutomationSystemConfigured:
                mockedHomeAutomationSystemConfigured.return_value = False

                with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_install_choice') as mockedGettingInstallChoice:
                    mockedGettingInstallChoice.return_value = "o"

                    with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.database_installation') as mockedDatabaseInstallation:
                        mockedDatabaseInstallation.return_value = True

                        with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.homeAutomationSystem_installation') as mockedHomeAutomationSystemInstallation:
                            mockedHomeAutomationSystemInstallation.return_value = False

                            with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_list') as mockedGettingAdministratorList:
                                mockedGettingAdministratorList.return_value = []
                            
                                with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_first_name') as mockedGettingAdministratorFirstName:
                                    mockedGettingAdministratorFirstName.return_value = "donovan"

                                    with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_last_name') as mockedGettingAdministratorLastName:
                                        mockedGettingAdministratorLastName.return_value = "maurice"

                                        with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_gender') as mockedGettingAdministratorGender:
                                            mockedGettingAdministratorGender.return_value = "m"

                                            with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_date_of_birth') as mockedGettingAdministratorDateOfBirth:
                                                mockedGettingAdministratorDateOfBirth.return_value = "26/09/1994"
                                        
                                                with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administator_identifiant') as mockedGettingAdministratorIdentifiant:
                                                    mockedGettingAdministratorIdentifiant.return_value = "tetrew"

                                                    with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_password') as mockedGettingAdministratorPassword:
                                                        mockedGettingAdministratorPassword.return_value = "0000"

                                                        with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.create_administrator_user') as mockedCreatingAdministratorUser:
                                                            mockedCreatingAdministratorUser.return_value = True

                                                            assert install() == False

        #check if method detect error during getting administrator list
        with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.databaseConfigured', new_callable=PropertyMock) as mockedDatabaseConfiguredProperty:
            mockedDatabaseConfiguredProperty.return_value = False

            with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.homeAutomationSystemConfigured', new_callable=PropertyMock) as mockedHomeAutomationSystemConfigured:
                mockedHomeAutomationSystemConfigured.return_value = False

                with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_install_choice') as mockedGettingInstallChoice:
                    mockedGettingInstallChoice.return_value = "o"

                    with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.database_installation') as mockedDatabaseInstallation:
                        mockedDatabaseInstallation.return_value = True

                        with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.homeAutomationSystem_installation') as mockedHomeAutomationSystemInstallation:
                            mockedHomeAutomationSystemInstallation.return_value = True

                            with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_list') as mockedGettingAdministratorList:
                                mockedGettingAdministratorList.return_value = False
                            
                                with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_first_name') as mockedGettingAdministratorFirstName:
                                    mockedGettingAdministratorFirstName.return_value = "donovan"

                                    with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_last_name') as mockedGettingAdministratorLastName:
                                        mockedGettingAdministratorLastName.return_value = "maurice"

                                        with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_gender') as mockedGettingAdministratorGender:
                                            mockedGettingAdministratorGender.return_value = "m"

                                            with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_date_of_birth') as mockedGettingAdministratorDateOfBirth:
                                                mockedGettingAdministratorDateOfBirth.return_value = "26/09/1994"
                                        
                                                with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administator_identifiant') as mockedGettingAdministratorIdentifiant:
                                                    mockedGettingAdministratorIdentifiant.return_value = "tetrew"

                                                    with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_password') as mockedGettingAdministratorPassword:
                                                        mockedGettingAdministratorPassword.return_value = "0000"

                                                        with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.create_administrator_user') as mockedCreatingAdministratorUser:
                                                            mockedCreatingAdministratorUser.return_value = True

                                                            assert install() == False

        #check if method detect error during getting administrator firstname
        with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.databaseConfigured', new_callable=PropertyMock) as mockedDatabaseConfiguredProperty:
            mockedDatabaseConfiguredProperty.return_value = False

            with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.homeAutomationSystemConfigured', new_callable=PropertyMock) as mockedHomeAutomationSystemConfigured:
                mockedHomeAutomationSystemConfigured.return_value = False

                with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_install_choice') as mockedGettingInstallChoice:
                    mockedGettingInstallChoice.return_value = "o"

                    with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.database_installation') as mockedDatabaseInstallation:
                        mockedDatabaseInstallation.return_value = True

                        with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.homeAutomationSystem_installation') as mockedHomeAutomationSystemInstallation:
                            mockedHomeAutomationSystemInstallation.return_value = True

                            with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_list') as mockedGettingAdministratorList:
                                mockedGettingAdministratorList.return_value = []
                            
                                with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_first_name') as mockedGettingAdministratorFirstName:
                                    mockedGettingAdministratorFirstName.return_value = False

                                    with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_last_name') as mockedGettingAdministratorLastName:
                                        mockedGettingAdministratorLastName.return_value = "maurice"

                                        with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_gender') as mockedGettingAdministratorGender:
                                            mockedGettingAdministratorGender.return_value = "m"

                                            with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_date_of_birth') as mockedGettingAdministratorDateOfBirth:
                                                mockedGettingAdministratorDateOfBirth.return_value = "26/09/1994"
                                        
                                                with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administator_identifiant') as mockedGettingAdministratorIdentifiant:
                                                    mockedGettingAdministratorIdentifiant.return_value = "tetrew"

                                                    with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_password') as mockedGettingAdministratorPassword:
                                                        mockedGettingAdministratorPassword.return_value = "0000"

                                                        with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.create_administrator_user') as mockedCreatingAdministratorUser:
                                                            mockedCreatingAdministratorUser.return_value = True

                                                            assert install() == False

        #check if method detect error during getting administrator last name
        with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.databaseConfigured', new_callable=PropertyMock) as mockedDatabaseConfiguredProperty:
            mockedDatabaseConfiguredProperty.return_value = False

            with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.homeAutomationSystemConfigured', new_callable=PropertyMock) as mockedHomeAutomationSystemConfigured:
                mockedHomeAutomationSystemConfigured.return_value = False

                with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_install_choice') as mockedGettingInstallChoice:
                    mockedGettingInstallChoice.return_value = "o"

                    with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.database_installation') as mockedDatabaseInstallation:
                        mockedDatabaseInstallation.return_value = True

                        with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.homeAutomationSystem_installation') as mockedHomeAutomationSystemInstallation:
                            mockedHomeAutomationSystemInstallation.return_value = True

                            with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_list') as mockedGettingAdministratorList:
                                mockedGettingAdministratorList.return_value = []
                            
                                with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_first_name') as mockedGettingAdministratorFirstName:
                                    mockedGettingAdministratorFirstName.return_value = True

                                    with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_last_name') as mockedGettingAdministratorLastName:
                                        mockedGettingAdministratorLastName.return_value = False

                                        with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_gender') as mockedGettingAdministratorGender:
                                            mockedGettingAdministratorGender.return_value = "m"

                                            with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_date_of_birth') as mockedGettingAdministratorDateOfBirth:
                                                mockedGettingAdministratorDateOfBirth.return_value = "26/09/1994"
                                        
                                                with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administator_identifiant') as mockedGettingAdministratorIdentifiant:
                                                    mockedGettingAdministratorIdentifiant.return_value = "tetrew"

                                                    with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_password') as mockedGettingAdministratorPassword:
                                                        mockedGettingAdministratorPassword.return_value = "0000"

                                                        with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.create_administrator_user') as mockedCreatingAdministratorUser:
                                                            mockedCreatingAdministratorUser.return_value = True

                                                            assert install() == False

        #check if method detect error during getting administrator gender
        with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.databaseConfigured', new_callable=PropertyMock) as mockedDatabaseConfiguredProperty:
            mockedDatabaseConfiguredProperty.return_value = False

            with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.homeAutomationSystemConfigured', new_callable=PropertyMock) as mockedHomeAutomationSystemConfigured:
                mockedHomeAutomationSystemConfigured.return_value = False

                with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_install_choice') as mockedGettingInstallChoice:
                    mockedGettingInstallChoice.return_value = "o"

                    with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.database_installation') as mockedDatabaseInstallation:
                        mockedDatabaseInstallation.return_value = True

                        with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.homeAutomationSystem_installation') as mockedHomeAutomationSystemInstallation:
                            mockedHomeAutomationSystemInstallation.return_value = True

                            with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_list') as mockedGettingAdministratorList:
                                mockedGettingAdministratorList.return_value = []
                            
                                with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_first_name') as mockedGettingAdministratorFirstName:
                                    mockedGettingAdministratorFirstName.return_value = "donovan"

                                    with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_last_name') as mockedGettingAdministratorLastName:
                                        mockedGettingAdministratorLastName.return_value = "maurice"

                                        with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_gender') as mockedGettingAdministratorGender:
                                            mockedGettingAdministratorGender.return_value = False

                                            with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_date_of_birth') as mockedGettingAdministratorDateOfBirth:
                                                mockedGettingAdministratorDateOfBirth.return_value = "26/09/1994"
                                        
                                                with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administator_identifiant') as mockedGettingAdministratorIdentifiant:
                                                    mockedGettingAdministratorIdentifiant.return_value = "tetrew"

                                                    with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_password') as mockedGettingAdministratorPassword:
                                                        mockedGettingAdministratorPassword.return_value = "0000"

                                                        with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.create_administrator_user') as mockedCreatingAdministratorUser:
                                                            mockedCreatingAdministratorUser.return_value = True

                                                            assert install() == False

        #check if method detect bad gender
        with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.databaseConfigured', new_callable=PropertyMock) as mockedDatabaseConfiguredProperty:
            mockedDatabaseConfiguredProperty.return_value = False

            with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.homeAutomationSystemConfigured', new_callable=PropertyMock) as mockedHomeAutomationSystemConfigured:
                mockedHomeAutomationSystemConfigured.return_value = False

                with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_install_choice') as mockedGettingInstallChoice:
                    mockedGettingInstallChoice.return_value = "o"

                    with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.database_installation') as mockedDatabaseInstallation:
                        mockedDatabaseInstallation.return_value = True

                        with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.homeAutomationSystem_installation') as mockedHomeAutomationSystemInstallation:
                            mockedHomeAutomationSystemInstallation.return_value = True

                            with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_list') as mockedGettingAdministratorList:
                                mockedGettingAdministratorList.return_value = []
                            
                                with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_first_name') as mockedGettingAdministratorFirstName:
                                    mockedGettingAdministratorFirstName.return_value = "donovan"

                                    with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_last_name') as mockedGettingAdministratorLastName:
                                        mockedGettingAdministratorLastName.return_value = "maurice"

                                        with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_gender') as mockedGettingAdministratorGender:
                                            mockedGettingAdministratorGender.return_value = "i"

                                            with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_date_of_birth') as mockedGettingAdministratorDateOfBirth:
                                                mockedGettingAdministratorDateOfBirth.return_value = "26/09/1994"
                                        
                                                with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administator_identifiant') as mockedGettingAdministratorIdentifiant:
                                                    mockedGettingAdministratorIdentifiant.return_value = "tetrew"

                                                    with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_password') as mockedGettingAdministratorPassword:
                                                        mockedGettingAdministratorPassword.return_value = "0000"

                                                        with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.create_administrator_user') as mockedCreatingAdministratorUser:
                                                            mockedCreatingAdministratorUser.return_value = True

                                                            assert install() == False

        #check if method detect error during getting date of birth
        with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.databaseConfigured', new_callable=PropertyMock) as mockedDatabaseConfiguredProperty:
            mockedDatabaseConfiguredProperty.return_value = False

            with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.homeAutomationSystemConfigured', new_callable=PropertyMock) as mockedHomeAutomationSystemConfigured:
                mockedHomeAutomationSystemConfigured.return_value = False

                with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_install_choice') as mockedGettingInstallChoice:
                    mockedGettingInstallChoice.return_value = "o"

                    with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.database_installation') as mockedDatabaseInstallation:
                        mockedDatabaseInstallation.return_value = True

                        with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.homeAutomationSystem_installation') as mockedHomeAutomationSystemInstallation:
                            mockedHomeAutomationSystemInstallation.return_value = True

                            with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_list') as mockedGettingAdministratorList:
                                mockedGettingAdministratorList.return_value = []
                            
                                with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_first_name') as mockedGettingAdministratorFirstName:
                                    mockedGettingAdministratorFirstName.return_value = "donovan"

                                    with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_last_name') as mockedGettingAdministratorLastName:
                                        mockedGettingAdministratorLastName.return_value = "maurice"

                                        with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_gender') as mockedGettingAdministratorGender:
                                            mockedGettingAdministratorGender.return_value = "m"

                                            with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_date_of_birth') as mockedGettingAdministratorDateOfBirth:
                                                mockedGettingAdministratorDateOfBirth.return_value = False
                                        
                                                with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administator_identifiant') as mockedGettingAdministratorIdentifiant:
                                                    mockedGettingAdministratorIdentifiant.return_value = "tetrew"

                                                    with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_password') as mockedGettingAdministratorPassword:
                                                        mockedGettingAdministratorPassword.return_value = "0000"

                                                        with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.create_administrator_user') as mockedCreatingAdministratorUser:
                                                            mockedCreatingAdministratorUser.return_value = True

                                                            assert install() == False

        #check if method detect error during getting administrator identifiant
        with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.databaseConfigured', new_callable=PropertyMock) as mockedDatabaseConfiguredProperty:
            mockedDatabaseConfiguredProperty.return_value = False

            with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.homeAutomationSystemConfigured', new_callable=PropertyMock) as mockedHomeAutomationSystemConfigured:
                mockedHomeAutomationSystemConfigured.return_value = False

                with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_install_choice') as mockedGettingInstallChoice:
                    mockedGettingInstallChoice.return_value = "o"

                    with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.database_installation') as mockedDatabaseInstallation:
                        mockedDatabaseInstallation.return_value = True

                        with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.homeAutomationSystem_installation') as mockedHomeAutomationSystemInstallation:
                            mockedHomeAutomationSystemInstallation.return_value = True

                            with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_list') as mockedGettingAdministratorList:
                                mockedGettingAdministratorList.return_value = []
                            
                                with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_first_name') as mockedGettingAdministratorFirstName:
                                    mockedGettingAdministratorFirstName.return_value = "donovan"

                                    with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_last_name') as mockedGettingAdministratorLastName:
                                        mockedGettingAdministratorLastName.return_value = "maurice"

                                        with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_gender') as mockedGettingAdministratorGender:
                                            mockedGettingAdministratorGender.return_value = "m"

                                            with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_date_of_birth') as mockedGettingAdministratorDateOfBirth:
                                                mockedGettingAdministratorDateOfBirth.return_value = "26/09/1994"
                                        
                                                with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administator_identifiant') as mockedGettingAdministratorIdentifiant:
                                                    mockedGettingAdministratorIdentifiant.return_value = False

                                                    with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_password') as mockedGettingAdministratorPassword:
                                                        mockedGettingAdministratorPassword.return_value = "0000"

                                                        with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.create_administrator_user') as mockedCreatingAdministratorUser:
                                                            mockedCreatingAdministratorUser.return_value = True

                                                            assert install() == False

        #check if method detect error during getting administrator password
        with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.databaseConfigured', new_callable=PropertyMock) as mockedDatabaseConfiguredProperty:
            mockedDatabaseConfiguredProperty.return_value = False

            with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.homeAutomationSystemConfigured', new_callable=PropertyMock) as mockedHomeAutomationSystemConfigured:
                mockedHomeAutomationSystemConfigured.return_value = False

                with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_install_choice') as mockedGettingInstallChoice:
                    mockedGettingInstallChoice.return_value = "o"

                    with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.database_installation') as mockedDatabaseInstallation:
                        mockedDatabaseInstallation.return_value = True

                        with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.homeAutomationSystem_installation') as mockedHomeAutomationSystemInstallation:
                            mockedHomeAutomationSystemInstallation.return_value = True

                            with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_list') as mockedGettingAdministratorList:
                                mockedGettingAdministratorList.return_value = []
                            
                                with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_first_name') as mockedGettingAdministratorFirstName:
                                    mockedGettingAdministratorFirstName.return_value = "donovan"

                                    with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_last_name') as mockedGettingAdministratorLastName:
                                        mockedGettingAdministratorLastName.return_value = "maurice"

                                        with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_gender') as mockedGettingAdministratorGender:
                                            mockedGettingAdministratorGender.return_value = "m"

                                            with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_date_of_birth') as mockedGettingAdministratorDateOfBirth:
                                                mockedGettingAdministratorDateOfBirth.return_value = "26/09/1994"
                                        
                                                with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administator_identifiant') as mockedGettingAdministratorIdentifiant:
                                                    mockedGettingAdministratorIdentifiant.return_value = "tetrew"

                                                    with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_password') as mockedGettingAdministratorPassword:
                                                        mockedGettingAdministratorPassword.return_value = False

                                                        with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.create_administrator_user') as mockedCreatingAdministratorUser:
                                                            mockedCreatingAdministratorUser.return_value = True

                                                            assert install() == False

        #check if method detect error during administrator user creation
        with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.databaseConfigured', new_callable=PropertyMock) as mockedDatabaseConfiguredProperty:
            mockedDatabaseConfiguredProperty.return_value = False

            with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.homeAutomationSystemConfigured', new_callable=PropertyMock) as mockedHomeAutomationSystemConfigured:
                mockedHomeAutomationSystemConfigured.return_value = False

                with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_install_choice') as mockedGettingInstallChoice:
                    mockedGettingInstallChoice.return_value = "o"

                    with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.database_installation') as mockedDatabaseInstallation:
                        mockedDatabaseInstallation.return_value = True

                        with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.homeAutomationSystem_installation') as mockedHomeAutomationSystemInstallation:
                            mockedHomeAutomationSystemInstallation.return_value = True

                            with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_list') as mockedGettingAdministratorList:
                                mockedGettingAdministratorList.return_value = []
                            
                                with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_first_name') as mockedGettingAdministratorFirstName:
                                    mockedGettingAdministratorFirstName.return_value = "donovan"

                                    with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_last_name') as mockedGettingAdministratorLastName:
                                        mockedGettingAdministratorLastName.return_value = "maurice"

                                        with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_gender') as mockedGettingAdministratorGender:
                                            mockedGettingAdministratorGender.return_value = "m"

                                            with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_date_of_birth') as mockedGettingAdministratorDateOfBirth:
                                                mockedGettingAdministratorDateOfBirth.return_value = "26/09/1994"
                                        
                                                with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administator_identifiant') as mockedGettingAdministratorIdentifiant:
                                                    mockedGettingAdministratorIdentifiant.return_value = "tetrew"

                                                    with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.get_administrator_password') as mockedGettingAdministratorPassword:
                                                        mockedGettingAdministratorPassword.return_value = "0000"

                                                        with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.create_administrator_user') as mockedCreatingAdministratorUser:
                                                            mockedCreatingAdministratorUser.return_value = False

                                                            assert install() == False