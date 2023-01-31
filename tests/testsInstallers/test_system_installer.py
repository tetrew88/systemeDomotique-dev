import sys
import mock

sys.path.append("..")

from systemeDomotique.classes.installers.systemInstaller import *
from unittest.mock import patch, mock_open, MagicMock


class TestDatabaseInstaller:
    """
        class used for test the database installer
        
            Attributes:
                script path (path of the main script (for files manipulation))
				database installer (class contained all function used for database installation)
                
            tests:
    """


    """constructor"""
    scriptPath = os.path.dirname(os.path.abspath(__file__))
    systemInstaller = SystemInstaller(scriptPath)


    def test_systemInstalled_property(self):
        """
            1.test if method return an bool 
            2.test if method return true if succes
            3.test if method return false if database not configured
            3.test if method return false if home automation system not configured
        """

        #test if method return an bool  
        assert isinstance(self.systemInstaller.systemInstalled, bool) == True

        with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.databaseConfigured', new_callable=mock.PropertyMock) as mockedDatabaseConfiguredProperty:
            with mock.patch('systemeDomotique.classes.installers.systemInstaller.SystemInstaller.homeAutomationSystemConfigured', new_callable=mock.PropertyMock) as mockedHomeAutomationSystemConfiguredProperty:
                mockedDatabaseConfiguredProperty.return_value = True
                mockedHomeAutomationSystemConfiguredProperty.return_value = True

                #test if method return true if succes
                assert self.systemInstaller.systemInstalled == True

                #test if method return false if database not configured
                mockedDatabaseConfiguredProperty.return_value = False
                mockedHomeAutomationSystemConfiguredProperty.return_value = True

                assert self.systemInstaller.systemInstalled == False

                #test if method return false if home automation system not configured
                mockedDatabaseConfiguredProperty.return_value = True
                mockedHomeAutomationSystemConfiguredProperty.return_value = False

                assert self.systemInstaller.systemInstalled == False


    def test_databaseConfigured_property(self):
        """
            1.test if method return an bool 
            2.test if method return good data
        """
        
        #test if method return an bool
        assert isinstance(self.systemInstaller.databaseConfigured, bool) == True

        #test if method return good data
        with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.databaseConfigured', new_callable=mock.PropertyMock) as mockedDatabaseConfiguredProperty:
            mockedDatabaseConfiguredProperty.return_value = True
            assert self.systemInstaller.databaseConfigured == True

            mockedDatabaseConfiguredProperty.return_value = False
            assert self.systemInstaller.databaseConfigured == False


    def test_homeAutomationSystemConfigured_property(self):
        """
            1.test if method return an bool 
            2.test if method return good data
        """
        
        #test if method return an bool
        assert isinstance(self.systemInstaller.homeAutomationSystemConfigured, bool) == True

        #test if method return good data
        with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.homeAutomationSystemConfigured', new_callable=mock.PropertyMock) as mockedHomeAutomationSystemConfiguredProperty:
            mockedHomeAutomationSystemConfiguredProperty.return_value = True
            assert self.systemInstaller.homeAutomationSystemConfigured == True

            mockedHomeAutomationSystemConfiguredProperty.return_value = False
            assert self.systemInstaller.homeAutomationSystemConfigured == False



    def test_getting_install_choice(self):
        """
            test if method return the good choice
        """
        
        #test if method return the choice
        with mock.patch('builtins.input', return_value="o"):
            assert self.systemInstaller.get_install_choice() == "o"

        with mock.patch('builtins.input', return_value="n"):
            assert self.systemInstaller.get_install_choice() == "n"


    def test_getting_administrator_list(self):
        with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.get_administrator_list') as mockedGettingAdministratorList:
            mockedGettingAdministratorList.return_value = []

            assert self.systemInstaller.get_administrator_list() == []

        with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.get_administrator_list') as mockedGettingAdministratorList:
            mockedGettingAdministratorList.return_value = False

            assert self.systemInstaller.get_administrator_list() == False


    def test_getting_administrator_first_name(self):
        #test if method return the choice
        with mock.patch('builtins.input', return_value="donovan"):
            assert self.systemInstaller.get_administrator_first_name() == "donovan"

        with mock.patch('builtins.input', return_value=""):
            assert self.systemInstaller.get_administrator_first_name() == False

        with mock.patch('builtins.input', return_value=False):
            assert self.systemInstaller.get_administrator_first_name() == False


    def test_getting_administrator_last_name(self):
        #test if method return the choice
        with mock.patch('builtins.input', return_value="maurice"):
            assert self.systemInstaller.get_administrator_last_name() == "maurice"

        with mock.patch('builtins.input', return_value=""):
            assert self.systemInstaller.get_administrator_last_name() == False

        with mock.patch('builtins.input', return_value=False):
            assert self.systemInstaller.get_administrator_last_name() == False


    def test_getting_administrator_date_of_birth(self):
        #test if method return the choice
        with mock.patch('builtins.input', return_value="26/09/1994"):
            assert self.systemInstaller.get_administrator_date_of_birth() == "26/09/1994"

        with mock.patch('builtins.input', return_value=""):
            assert self.systemInstaller.get_administrator_date_of_birth() == False

        with mock.patch('builtins.input', return_value=False):
            assert self.systemInstaller.get_administrator_date_of_birth() == False


    def test_getting_administrator_gender(self):
        #test if method return the choice
        with mock.patch('builtins.input', return_value="m"):
            assert self.systemInstaller.get_administrator_gender() == "m"

        with mock.patch('builtins.input', return_value="f"):
            assert self.systemInstaller.get_administrator_gender() == "f"

        with mock.patch('builtins.input', return_value=""):
            assert self.systemInstaller.get_administrator_gender() == False

        with mock.patch('builtins.input', return_value=False):
            assert self.systemInstaller.get_administrator_gender() == False

        with mock.patch('builtins.input', return_value="g"):
            assert self.systemInstaller.get_administrator_gender() == False


    def test_getting_administator_identifiant(self):
        #test if method return the choice
        with mock.patch('builtins.input', return_value="tetrew"):
            assert self.systemInstaller.get_administator_identifiant() == "tetrew"

        with mock.patch('builtins.input', return_value=""):
            assert self.systemInstaller.get_administator_identifiant() == False

        with mock.patch('builtins.input', return_value=False):
            assert self.systemInstaller.get_administator_identifiant() == False


    def test_getting_administrator_password(self):
        #test if method return the choice
        with mock.patch('builtins.input', return_value="0000"):
            assert self.systemInstaller.get_administator_identifiant() == "0000"

        with mock.patch('builtins.input', return_value=""):
            assert self.systemInstaller.get_administator_identifiant() == False

        with mock.patch('builtins.input', return_value=False):
            assert self.systemInstaller.get_administator_identifiant() == False



    def test_database_installation(self):
        """
            1.test if method return true if succes
            2.test if method return false if error
            3.test if method detect error during database dowloading
			4.test if method detect error when getting user information and databasename
			5.test if method detect creation config file error
			6.test if method detect error during database creation
			7.test if method detect error during database table creation
		    8.test if method detect error during user creation
			9.test if method detect error during the attribution of the privilege
			10.test if method detect error during setting database booleean    
        """

        #test if method return true if succes
        with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.download_database_system') as mockedDatabaseDownload:
            mockedDatabaseDownload.return_value = True

            with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.get_system_username') as mockedGettingUsername:
                mockedGettingUsername.return_value = "homeAutomationSystem"

                with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.get_system_user_password') as mockedGettingPassword:
                    mockedGettingPassword.return_value = "password"

                    with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.get_database_name') as mockedGettingDatabaseName:
                        mockedGettingDatabaseName.return_value = "Home"

                        with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.create_database_config_file') as mockedCreatingDatabaseConfigFile:
                            mockedCreatingDatabaseConfigFile.return_value = True

                            with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.create_database') as mockedCreatingDatabase:
                                mockedCreatingDatabase.return_value = True

                                with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.create_database_table') as mockedCreatingDatabaseTable:
                                    mockedCreatingDatabaseTable.return_value = True

                                    with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.create_database_system_user') as mockedCreatingDatabaseUser:
                                        mockedCreatingDatabaseUser.return_value = True

                                        with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.attribute_user_system_privilege') as mockedAttributingPrivilege:
                                            mockedAttributingPrivilege.return_value = True

                                            with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.set_database_configuration_booleean_control') as mockedSettingDatabaseConfigurationBooleean:
                                                mockedSettingDatabaseConfigurationBooleean.return_value = True

                                                assert self.systemInstaller.database_installation() == True
            
        #test if method return false if error
        with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.download_database_system') as mockedDatabaseDownload:
            mockedDatabaseDownload.return_value = False

            with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.get_system_username') as mockedGettingUsername:
                mockedGettingUsername.return_value = "homeAutomationSystem"

                with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.get_system_user_password') as mockedGettingPassword:
                    mockedGettingPassword.return_value = "password"

                    with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.get_database_name') as mockedGettingDatabaseName:
                        mockedGettingDatabaseName.return_value = "Home"

                        with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.create_database_config_file') as mockedCreatingDatabaseConfigFile:
                            mockedCreatingDatabaseConfigFile.return_value = True

                            with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.create_database') as mockedCreatingDatabase:
                                mockedCreatingDatabase.return_value = True

                                with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.create_database_table') as mockedCreatingDatabaseTable:
                                    mockedCreatingDatabaseTable.return_value = True

                                    with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.create_database_system_user') as mockedCreatingDatabaseUser:
                                        mockedCreatingDatabaseUser.return_value = True

                                        with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.attribute_user_system_privilege') as mockedAttributingPrivilege:
                                            mockedAttributingPrivilege.return_value = True

                                            with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.set_database_configuration_booleean_control') as mockedSettingDatabaseConfigurationBooleean:
                                                mockedSettingDatabaseConfigurationBooleean.return_value = True

                                                assert self.systemInstaller.database_installation() == False
            
        #test if method detect error during database dowloading
        with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.download_database_system') as mockedDatabaseDownload:
            mockedDatabaseDownload.return_value = False

            with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.get_system_username') as mockedGettingUsername:
                mockedGettingUsername.return_value = "homeAutomationSystem"

                with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.get_system_user_password') as mockedGettingPassword:
                    mockedGettingPassword.return_value = "password"

                    with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.get_database_name') as mockedGettingDatabaseName:
                        mockedGettingDatabaseName.return_value = "Home"

                        with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.create_database_config_file') as mockedCreatingDatabaseConfigFile:
                            mockedCreatingDatabaseConfigFile.return_value = True

                            with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.create_database') as mockedCreatingDatabase:
                                mockedCreatingDatabase.return_value = True

                                with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.create_database_table') as mockedCreatingDatabaseTable:
                                    mockedCreatingDatabaseTable.return_value = True

                                    with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.create_database_system_user') as mockedCreatingDatabaseUser:
                                        mockedCreatingDatabaseUser.return_value = True

                                        with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.attribute_user_system_privilege') as mockedAttributingPrivilege:
                                            mockedAttributingPrivilege.return_value = True

                                            with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.set_database_configuration_booleean_control') as mockedSettingDatabaseConfigurationBooleean:
                                                mockedSettingDatabaseConfigurationBooleean.return_value = True

                                                assert self.systemInstaller.database_installation() == False

        #test if method detect error when getting user information and databasename
        with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.download_database_system') as mockedDatabaseDownload:
            mockedDatabaseDownload.return_value = True

            with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.get_system_username') as mockedGettingUsername:
                mockedGettingUsername.return_value = False

                with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.get_system_user_password') as mockedGettingPassword:
                    mockedGettingPassword.return_value = False

                    with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.get_database_name') as mockedGettingDatabaseName:
                        mockedGettingDatabaseName.return_value = False

                        with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.create_database_config_file') as mockedCreatingDatabaseConfigFile:
                            mockedCreatingDatabaseConfigFile.return_value = True

                            with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.create_database') as mockedCreatingDatabase:
                                mockedCreatingDatabase.return_value = True

                                with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.create_database_table') as mockedCreatingDatabaseTable:
                                    mockedCreatingDatabaseTable.return_value = True

                                    with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.create_database_system_user') as mockedCreatingDatabaseUser:
                                        mockedCreatingDatabaseUser.return_value = True

                                        with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.attribute_user_system_privilege') as mockedAttributingPrivilege:
                                            mockedAttributingPrivilege.return_value = True

                                            with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.set_database_configuration_booleean_control') as mockedSettingDatabaseConfigurationBooleean:
                                                mockedSettingDatabaseConfigurationBooleean.return_value = True

                                                assert self.systemInstaller.database_installation() == False

        #test if method detect creation config file error
        with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.download_database_system') as mockedDatabaseDownload:
            mockedDatabaseDownload.return_value = True

            with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.get_system_username') as mockedGettingUsername:
                mockedGettingUsername.return_value = "systemDomotique"

                with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.get_system_user_password') as mockedGettingPassword:
                    mockedGettingPassword.return_value = "password"

                    with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.get_database_name') as mockedGettingDatabaseName:
                        mockedGettingDatabaseName.return_value = "Home"

                        with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.create_database_config_file') as mockedCreatingDatabaseConfigFile:
                            mockedCreatingDatabaseConfigFile.return_value = False

                            with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.create_database') as mockedCreatingDatabase:
                                mockedCreatingDatabase.return_value = True

                                with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.create_database_table') as mockedCreatingDatabaseTable:
                                    mockedCreatingDatabaseTable.return_value = True

                                    with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.create_database_system_user') as mockedCreatingDatabaseUser:
                                        mockedCreatingDatabaseUser.return_value = True

                                        with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.attribute_user_system_privilege') as mockedAttributingPrivilege:
                                            mockedAttributingPrivilege.return_value = True

                                            with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.set_database_configuration_booleean_control') as mockedSettingDatabaseConfigurationBooleean:
                                                mockedSettingDatabaseConfigurationBooleean.return_value = True

                                                assert self.systemInstaller.database_installation() == False

        #test if method detect error during database creation
        with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.download_database_system') as mockedDatabaseDownload:
            mockedDatabaseDownload.return_value = True

            with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.get_system_username') as mockedGettingUsername:
                mockedGettingUsername.return_value = "systemDomotique"

                with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.get_system_user_password') as mockedGettingPassword:
                    mockedGettingPassword.return_value = "password"

                    with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.get_database_name') as mockedGettingDatabaseName:
                        mockedGettingDatabaseName.return_value = "Home"

                        with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.create_database_config_file') as mockedCreatingDatabaseConfigFile:
                            mockedCreatingDatabaseConfigFile.return_value = True

                            with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.create_database') as mockedCreatingDatabase:
                                mockedCreatingDatabase.return_value = False

                                with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.create_database_table') as mockedCreatingDatabaseTable:
                                    mockedCreatingDatabaseTable.return_value = True

                                    with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.create_database_system_user') as mockedCreatingDatabaseUser:
                                        mockedCreatingDatabaseUser.return_value = True

                                        with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.attribute_user_system_privilege') as mockedAttributingPrivilege:
                                            mockedAttributingPrivilege.return_value = True

                                            with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.set_database_configuration_booleean_control') as mockedSettingDatabaseConfigurationBooleean:
                                                mockedSettingDatabaseConfigurationBooleean.return_value = True

                                                assert self.systemInstaller.database_installation() == False

        #test if method detect error during database table creation
        with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.download_database_system') as mockedDatabaseDownload:
            mockedDatabaseDownload.return_value = True

            with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.get_system_username') as mockedGettingUsername:
                mockedGettingUsername.return_value = "systemDomotique"

                with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.get_system_user_password') as mockedGettingPassword:
                    mockedGettingPassword.return_value = "password"

                    with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.get_database_name') as mockedGettingDatabaseName:
                        mockedGettingDatabaseName.return_value = "Home"

                        with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.create_database_config_file') as mockedCreatingDatabaseConfigFile:
                            mockedCreatingDatabaseConfigFile.return_value = True

                            with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.create_database') as mockedCreatingDatabase:
                                mockedCreatingDatabase.return_value = True

                                with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.create_database_table') as mockedCreatingDatabaseTable:
                                    mockedCreatingDatabaseTable.return_value = False

                                    with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.create_database_system_user') as mockedCreatingDatabaseUser:
                                        mockedCreatingDatabaseUser.return_value = True

                                        with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.attribute_user_system_privilege') as mockedAttributingPrivilege:
                                            mockedAttributingPrivilege.return_value = True

                                            with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.set_database_configuration_booleean_control') as mockedSettingDatabaseConfigurationBooleean:
                                                mockedSettingDatabaseConfigurationBooleean.return_value = True

                                                assert self.systemInstaller.database_installation() == False

        #test if method detect error during user creation
        with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.download_database_system') as mockedDatabaseDownload:
            mockedDatabaseDownload.return_value = True

            with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.get_system_username') as mockedGettingUsername:
                mockedGettingUsername.return_value = "systemDomotique"

                with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.get_system_user_password') as mockedGettingPassword:
                    mockedGettingPassword.return_value = "password"

                    with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.get_database_name') as mockedGettingDatabaseName:
                        mockedGettingDatabaseName.return_value = "Home"

                        with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.create_database_config_file') as mockedCreatingDatabaseConfigFile:
                            mockedCreatingDatabaseConfigFile.return_value = True

                            with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.create_database') as mockedCreatingDatabase:
                                mockedCreatingDatabase.return_value = True

                                with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.create_database_table') as mockedCreatingDatabaseTable:
                                    mockedCreatingDatabaseTable.return_value = True

                                    with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.create_database_system_user') as mockedCreatingDatabaseUser:
                                        mockedCreatingDatabaseUser.return_value = False

                                        with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.attribute_user_system_privilege') as mockedAttributingPrivilege:
                                            mockedAttributingPrivilege.return_value = True

                                            with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.set_database_configuration_booleean_control') as mockedSettingDatabaseConfigurationBooleean:
                                                mockedSettingDatabaseConfigurationBooleean.return_value = True

                                                assert self.systemInstaller.database_installation() == False

        #test if method detect error during the attribution of the privilege
        with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.download_database_system') as mockedDatabaseDownload:
            mockedDatabaseDownload.return_value = True

            with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.get_system_username') as mockedGettingUsername:
                mockedGettingUsername.return_value = "systemDomotique"

                with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.get_system_user_password') as mockedGettingPassword:
                    mockedGettingPassword.return_value = "password"

                    with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.get_database_name') as mockedGettingDatabaseName:
                        mockedGettingDatabaseName.return_value = "Home"

                        with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.create_database_config_file') as mockedCreatingDatabaseConfigFile:
                            mockedCreatingDatabaseConfigFile.return_value = True

                            with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.create_database') as mockedCreatingDatabase:
                                mockedCreatingDatabase.return_value = True

                                with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.create_database_table') as mockedCreatingDatabaseTable:
                                    mockedCreatingDatabaseTable.return_value = True

                                    with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.create_database_system_user') as mockedCreatingDatabaseUser:
                                        mockedCreatingDatabaseUser.return_value = True

                                        with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.attribute_user_system_privilege') as mockedAttributingPrivilege:
                                            mockedAttributingPrivilege.return_value = False

                                            with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.set_database_configuration_booleean_control') as mockedSettingDatabaseConfigurationBooleean:
                                                mockedSettingDatabaseConfigurationBooleean.return_value = True

                                                assert self.systemInstaller.database_installation() == False

        #test if method detect error during setting database booleean  
        with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.download_database_system') as mockedDatabaseDownload:
            mockedDatabaseDownload.return_value = True

            with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.get_system_username') as mockedGettingUsername:
                mockedGettingUsername.return_value = "systemDomotique"

                with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.get_system_user_password') as mockedGettingPassword:
                    mockedGettingPassword.return_value = "password"

                    with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.get_database_name') as mockedGettingDatabaseName:
                        mockedGettingDatabaseName.return_value = "Home"

                        with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.create_database_config_file') as mockedCreatingDatabaseConfigFile:
                            mockedCreatingDatabaseConfigFile.return_value = True

                            with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.create_database') as mockedCreatingDatabase:
                                mockedCreatingDatabase.return_value = True

                                with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.create_database_table') as mockedCreatingDatabaseTable:
                                    mockedCreatingDatabaseTable.return_value = True

                                    with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.create_database_system_user') as mockedCreatingDatabaseUser:
                                        mockedCreatingDatabaseUser.return_value = True

                                        with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.attribute_user_system_privilege') as mockedAttributingPrivilege:
                                            mockedAttributingPrivilege.return_value = True

                                            with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.set_database_configuration_booleean_control') as mockedSettingDatabaseConfigurationBooleean:
                                                mockedSettingDatabaseConfigurationBooleean.return_value = False

                                                assert self.systemInstaller.database_installation() == False



    def test_home_automation_system_installation(self):
        """
            1.test if method return true if succes
            2.test if method return false if error
            3.test if method detect error during supervisor downloading
		    4.test if method detect error during nginx downloading
			5.test if method detect error while getting zwave controller path
			6.test if method detect error while getting zwave config folder path
			7.test if method detect error during assignatting fixed usb port name to the controller
			8.test if method detect error during creation of the home automation config file
			9.test if method detect error while nginx config file creation
			9.test if method detect error while creation of web interface supervisor config file
			10.test if method detect error while creation of automation server supervisor config file
			10.test if method detect error while setting of home automation system configuration booléean on True   
        """

        #test if method return true if succes
        with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.dowload_supervisor') as supervisorDownload:
            supervisorDownload.return_value = True

            with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.download_nginx') as nginxDownload:
                nginxDownload.return_value = True

                with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.get_zwave_controller_path') as gettingZwaveControllerPath:
                    gettingZwaveControllerPath.return_value = "True"

                    with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.get_zwave_config_folder_path') as gettingZwaveConfigFolder:
                        gettingZwaveConfigFolder.return_value = "True"

                        with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.assign_fixed_usb_port_names_to_controller') as fixUsbName:
                            fixUsbName.return_value = True

                            with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.create_home_automation_system_config_file') as homeAutomationSystemConfigFileCreation:
                                homeAutomationSystemConfigFileCreation.return_value = True

                                with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.create_nginx_config_file') as nginxConfigFileCreation:
                                    nginxConfigFileCreation.return_value = True

                                    with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.create_web_interface_supervisor_config_file') as supervisorWebInterfaceConfigFileCreation:
                                        supervisorWebInterfaceConfigFileCreation.return_value = True

                                        with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.create_automation_server_supervisor_config_file') as supervisorAutomationServerConfigFileCreation:
                                            supervisorAutomationServerConfigFileCreation.return_value = True

                                            with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.set_home_automation_system_configuration_booleean_control') as settingHomeAutomationSystemConfigurationBooleen:
                                                settingHomeAutomationSystemConfigurationBooleen.return_value = True
                                                
                                                assert self.systemInstaller.homeAutomationSystem_installation() == True

        #test if method return false if error
        with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.dowload_supervisor') as supervisorDownload:
            supervisorDownload.return_value = False

            with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.download_nginx') as nginxDownload:
                nginxDownload.return_value = False

                with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.get_zwave_controller_path') as gettingZwaveControllerPath:
                    gettingZwaveControllerPath.return_value = False

                    with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.get_zwave_config_folder_path') as gettingZwaveConfigFolder:
                        gettingZwaveConfigFolder.return_value = False

                        with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.assign_fixed_usb_port_names_to_controller') as fixUsbName:
                            fixUsbName.return_value = False

                            with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.create_home_automation_system_config_file') as homeAutomationSystemConfigFileCreation:
                                homeAutomationSystemConfigFileCreation.return_value = False

                                with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.create_nginx_config_file') as nginxConfigFileCreation:
                                    nginxConfigFileCreation.return_value = False

                                    with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.create_web_interface_supervisor_config_file') as supervisorWebInterfaceConfigFileCreation:
                                        supervisorWebInterfaceConfigFileCreation.return_value = False

                                        with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.create_automation_server_supervisor_config_file') as supervisorAutomationServerConfigFileCreation:
                                            supervisorAutomationServerConfigFileCreation.return_value = False

                                            with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.set_home_automation_system_configuration_booleean_control') as settingHomeAutomationSystemConfigurationBooleen:
                                                settingHomeAutomationSystemConfigurationBooleen.return_value = False
                                                
                                                assert self.systemInstaller.homeAutomationSystem_installation() == False


        #test if method detect error during supervisor downloading
        with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.dowload_supervisor') as supervisorDownload:
            supervisorDownload.return_value = False

            with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.download_nginx') as nginxDownload:
                nginxDownload.return_value = True

                with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.get_zwave_controller_path') as gettingZwaveControllerPath:
                    gettingZwaveControllerPath.return_value = "True"

                    with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.get_zwave_config_folder_path') as gettingZwaveConfigFolder:
                        gettingZwaveConfigFolder.return_value = "True"

                        with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.assign_fixed_usb_port_names_to_controller') as fixUsbName:
                            fixUsbName.return_value = True

                            with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.create_home_automation_system_config_file') as homeAutomationSystemConfigFileCreation:
                                homeAutomationSystemConfigFileCreation.return_value = True

                                with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.create_nginx_config_file') as nginxConfigFileCreation:
                                    nginxConfigFileCreation.return_value = True

                                    with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.create_web_interface_supervisor_config_file') as supervisorWebInterfaceConfigFileCreation:
                                        supervisorWebInterfaceConfigFileCreation.return_value = True

                                        with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.create_automation_server_supervisor_config_file') as supervisorAutomationServerConfigFileCreation:
                                            supervisorAutomationServerConfigFileCreation.return_value = True

                                            with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.set_home_automation_system_configuration_booleean_control') as settingHomeAutomationSystemConfigurationBooleen:
                                                settingHomeAutomationSystemConfigurationBooleen.return_value = True
                                                
                                                assert self.systemInstaller.homeAutomationSystem_installation() == False

        #...
        with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.dowload_supervisor') as supervisorDownload:
            supervisorDownload.return_value = True

            with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.download_nginx') as nginxDownload:
                nginxDownload.return_value = False

                with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.get_zwave_controller_path') as gettingZwaveControllerPath:
                    gettingZwaveControllerPath.return_value = "True"

                    with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.get_zwave_config_folder_path') as gettingZwaveConfigFolder:
                        gettingZwaveConfigFolder.return_value = "True"

                        with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.assign_fixed_usb_port_names_to_controller') as fixUsbName:
                            fixUsbName.return_value = True

                            with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.create_home_automation_system_config_file') as homeAutomationSystemConfigFileCreation:
                                homeAutomationSystemConfigFileCreation.return_value = True

                                with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.create_nginx_config_file') as nginxConfigFileCreation:
                                    nginxConfigFileCreation.return_value = True

                                    with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.create_web_interface_supervisor_config_file') as supervisorWebInterfaceConfigFileCreation:
                                        supervisorWebInterfaceConfigFileCreation.return_value = True

                                        with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.create_automation_server_supervisor_config_file') as supervisorAutomationServerConfigFileCreation:
                                            supervisorAutomationServerConfigFileCreation.return_value = True

                                            with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.set_home_automation_system_configuration_booleean_control') as settingHomeAutomationSystemConfigurationBooleen:
                                                settingHomeAutomationSystemConfigurationBooleen.return_value = True
                                                
                                                assert self.systemInstaller.homeAutomationSystem_installation() == False

        #...
        with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.dowload_supervisor') as supervisorDownload:
            supervisorDownload.return_value = True

            with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.download_nginx') as nginxDownload:
                nginxDownload.return_value = True

                with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.get_zwave_controller_path') as gettingZwaveControllerPath:
                    gettingZwaveControllerPath.return_value = False

                    with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.get_zwave_config_folder_path') as gettingZwaveConfigFolder:
                        gettingZwaveConfigFolder.return_value = "True"

                        with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.assign_fixed_usb_port_names_to_controller') as fixUsbName:
                            fixUsbName.return_value = True

                            with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.create_home_automation_system_config_file') as homeAutomationSystemConfigFileCreation:
                                homeAutomationSystemConfigFileCreation.return_value = True

                                with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.create_nginx_config_file') as nginxConfigFileCreation:
                                    nginxConfigFileCreation.return_value = True

                                    with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.create_web_interface_supervisor_config_file') as supervisorWebInterfaceConfigFileCreation:
                                        supervisorWebInterfaceConfigFileCreation.return_value = True

                                        with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.create_automation_server_supervisor_config_file') as supervisorAutomationServerConfigFileCreation:
                                            supervisorAutomationServerConfigFileCreation.return_value = True

                                            with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.set_home_automation_system_configuration_booleean_control') as settingHomeAutomationSystemConfigurationBooleen:
                                                settingHomeAutomationSystemConfigurationBooleen.return_value = True
                                                
                                                assert self.systemInstaller.homeAutomationSystem_installation() == False

        #...
        with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.dowload_supervisor') as supervisorDownload:
            supervisorDownload.return_value = True

            with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.download_nginx') as nginxDownload:
                nginxDownload.return_value = True

                with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.get_zwave_controller_path') as gettingZwaveControllerPath:
                    gettingZwaveControllerPath.return_value = "True"

                    with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.get_zwave_config_folder_path') as gettingZwaveConfigFolder:
                        gettingZwaveConfigFolder.return_value = False

                        with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.assign_fixed_usb_port_names_to_controller') as fixUsbName:
                            fixUsbName.return_value = True

                            with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.create_home_automation_system_config_file') as homeAutomationSystemConfigFileCreation:
                                homeAutomationSystemConfigFileCreation.return_value = True

                                with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.create_nginx_config_file') as nginxConfigFileCreation:
                                    nginxConfigFileCreation.return_value = True

                                    with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.create_web_interface_supervisor_config_file') as supervisorWebInterfaceConfigFileCreation:
                                        supervisorWebInterfaceConfigFileCreation.return_value = True

                                        with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.create_automation_server_supervisor_config_file') as supervisorAutomationServerConfigFileCreation:
                                            supervisorAutomationServerConfigFileCreation.return_value = True

                                            with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.set_home_automation_system_configuration_booleean_control') as settingHomeAutomationSystemConfigurationBooleen:
                                                settingHomeAutomationSystemConfigurationBooleen.return_value = True
                                                
                                                assert self.systemInstaller.homeAutomationSystem_installation() == False

        #...
        with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.dowload_supervisor') as supervisorDownload:
            supervisorDownload.return_value = True

            with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.download_nginx') as nginxDownload:
                nginxDownload.return_value = True

                with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.get_zwave_controller_path') as gettingZwaveControllerPath:
                    gettingZwaveControllerPath.return_value = "True"

                    with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.get_zwave_config_folder_path') as gettingZwaveConfigFolder:
                        gettingZwaveConfigFolder.return_value = "True"

                        with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.assign_fixed_usb_port_names_to_controller') as fixUsbName:
                            fixUsbName.return_value = False

                            with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.create_home_automation_system_config_file') as homeAutomationSystemConfigFileCreation:
                                homeAutomationSystemConfigFileCreation.return_value = True

                                with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.create_nginx_config_file') as nginxConfigFileCreation:
                                    nginxConfigFileCreation.return_value = True

                                    with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.create_web_interface_supervisor_config_file') as supervisorWebInterfaceConfigFileCreation:
                                        supervisorWebInterfaceConfigFileCreation.return_value = True

                                        with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.create_automation_server_supervisor_config_file') as supervisorAutomationServerConfigFileCreation:
                                            supervisorAutomationServerConfigFileCreation.return_value = True

                                            with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.set_home_automation_system_configuration_booleean_control') as settingHomeAutomationSystemConfigurationBooleen:
                                                settingHomeAutomationSystemConfigurationBooleen.return_value = True
                                                
                                                assert self.systemInstaller.homeAutomationSystem_installation() == False

        #...
        with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.dowload_supervisor') as supervisorDownload:
            supervisorDownload.return_value = True

            with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.download_nginx') as nginxDownload:
                nginxDownload.return_value = True

                with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.get_zwave_controller_path') as gettingZwaveControllerPath:
                    gettingZwaveControllerPath.return_value = "True"

                    with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.get_zwave_config_folder_path') as gettingZwaveConfigFolder:
                        gettingZwaveConfigFolder.return_value = "True"

                        with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.assign_fixed_usb_port_names_to_controller') as fixUsbName:
                            fixUsbName.return_value = True

                            with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.create_home_automation_system_config_file') as homeAutomationSystemConfigFileCreation:
                                homeAutomationSystemConfigFileCreation.return_value = False

                                with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.create_nginx_config_file') as nginxConfigFileCreation:
                                    nginxConfigFileCreation.return_value = True

                                    with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.create_web_interface_supervisor_config_file') as supervisorWebInterfaceConfigFileCreation:
                                        supervisorWebInterfaceConfigFileCreation.return_value = True

                                        with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.create_automation_server_supervisor_config_file') as supervisorAutomationServerConfigFileCreation:
                                            supervisorAutomationServerConfigFileCreation.return_value = True

                                            with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.set_home_automation_system_configuration_booleean_control') as settingHomeAutomationSystemConfigurationBooleen:
                                                settingHomeAutomationSystemConfigurationBooleen.return_value = True
                                                
                                                assert self.systemInstaller.homeAutomationSystem_installation() == False

        #...
        with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.dowload_supervisor') as supervisorDownload:
            supervisorDownload.return_value = True

            with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.download_nginx') as nginxDownload:
                nginxDownload.return_value = True

                with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.get_zwave_controller_path') as gettingZwaveControllerPath:
                    gettingZwaveControllerPath.return_value = "True"

                    with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.get_zwave_config_folder_path') as gettingZwaveConfigFolder:
                        gettingZwaveConfigFolder.return_value = "True"

                        with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.assign_fixed_usb_port_names_to_controller') as fixUsbName:
                            fixUsbName.return_value = True

                            with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.create_home_automation_system_config_file') as homeAutomationSystemConfigFileCreation:
                                homeAutomationSystemConfigFileCreation.return_value = True

                                with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.create_nginx_config_file') as nginxConfigFileCreation:
                                    nginxConfigFileCreation.return_value = False

                                    with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.create_web_interface_supervisor_config_file') as supervisorWebInterfaceConfigFileCreation:
                                        supervisorWebInterfaceConfigFileCreation.return_value = True

                                        with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.create_automation_server_supervisor_config_file') as supervisorAutomationServerConfigFileCreation:
                                            supervisorAutomationServerConfigFileCreation.return_value = True

                                            with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.set_home_automation_system_configuration_booleean_control') as settingHomeAutomationSystemConfigurationBooleen:
                                                settingHomeAutomationSystemConfigurationBooleen.return_value = True
                                                
                                                assert self.systemInstaller.homeAutomationSystem_installation() == False


        #...
        with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.dowload_supervisor') as supervisorDownload:
            supervisorDownload.return_value = True

            with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.download_nginx') as nginxDownload:
                nginxDownload.return_value = True

                with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.get_zwave_controller_path') as gettingZwaveControllerPath:
                    gettingZwaveControllerPath.return_value = "True"

                    with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.get_zwave_config_folder_path') as gettingZwaveConfigFolder:
                        gettingZwaveConfigFolder.return_value = "True"

                        with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.assign_fixed_usb_port_names_to_controller') as fixUsbName:
                            fixUsbName.return_value = True

                            with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.create_home_automation_system_config_file') as homeAutomationSystemConfigFileCreation:
                                homeAutomationSystemConfigFileCreation.return_value = True

                                with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.create_nginx_config_file') as nginxConfigFileCreation:
                                    nginxConfigFileCreation.return_value = True

                                    with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.create_web_interface_supervisor_config_file') as supervisorWebInterfaceConfigFileCreation:
                                        supervisorWebInterfaceConfigFileCreation.return_value = False

                                        with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.create_automation_server_supervisor_config_file') as supervisorAutomationServerConfigFileCreation:
                                            supervisorAutomationServerConfigFileCreation.return_value = True

                                            with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.set_home_automation_system_configuration_booleean_control') as settingHomeAutomationSystemConfigurationBooleen:
                                                settingHomeAutomationSystemConfigurationBooleen.return_value = True
                                                
                                                assert self.systemInstaller.homeAutomationSystem_installation() == False

        #...
        with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.dowload_supervisor') as supervisorDownload:
            supervisorDownload.return_value = True

            with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.download_nginx') as nginxDownload:
                nginxDownload.return_value = True

                with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.get_zwave_controller_path') as gettingZwaveControllerPath:
                    gettingZwaveControllerPath.return_value = "True"

                    with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.get_zwave_config_folder_path') as gettingZwaveConfigFolder:
                        gettingZwaveConfigFolder.return_value = "True"

                        with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.assign_fixed_usb_port_names_to_controller') as fixUsbName:
                            fixUsbName.return_value = True

                            with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.create_home_automation_system_config_file') as homeAutomationSystemConfigFileCreation:
                                homeAutomationSystemConfigFileCreation.return_value = True

                                with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.create_nginx_config_file') as nginxConfigFileCreation:
                                    nginxConfigFileCreation.return_value = True

                                    with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.create_web_interface_supervisor_config_file') as supervisorWebInterfaceConfigFileCreation:
                                        supervisorWebInterfaceConfigFileCreation.return_value = True

                                        with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.create_automation_server_supervisor_config_file') as supervisorAutomationServerConfigFileCreation:
                                            supervisorAutomationServerConfigFileCreation.return_value = False

                                            with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.set_home_automation_system_configuration_booleean_control') as settingHomeAutomationSystemConfigurationBooleen:
                                                settingHomeAutomationSystemConfigurationBooleen.return_value = True
                                                
                                                assert self.systemInstaller.homeAutomationSystem_installation() == False

        #...
        with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.dowload_supervisor') as supervisorDownload:
            supervisorDownload.return_value = True

            with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.download_nginx') as nginxDownload:
                nginxDownload.return_value = True

                with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.get_zwave_controller_path') as gettingZwaveControllerPath:
                    gettingZwaveControllerPath.return_value = "True"

                    with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.get_zwave_config_folder_path') as gettingZwaveConfigFolder:
                        gettingZwaveConfigFolder.return_value = "True"

                        with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.assign_fixed_usb_port_names_to_controller') as fixUsbName:
                            fixUsbName.return_value = True

                            with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.create_home_automation_system_config_file') as homeAutomationSystemConfigFileCreation:
                                homeAutomationSystemConfigFileCreation.return_value = True

                                with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.create_nginx_config_file') as nginxConfigFileCreation:
                                    nginxConfigFileCreation.return_value = True

                                    with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.create_web_interface_supervisor_config_file') as supervisorWebInterfaceConfigFileCreation:
                                        supervisorWebInterfaceConfigFileCreation.return_value = True

                                        with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.create_automation_server_supervisor_config_file') as supervisorAutomationServerConfigFileCreation:
                                            supervisorAutomationServerConfigFileCreation.return_value = True

                                            with mock.patch('systemeDomotique.classes.installers.homeAutomationSystemInstaller.HomeAutomationSystemInstaller.set_home_automation_system_configuration_booleean_control') as settingHomeAutomationSystemConfigurationBooleen:
                                                settingHomeAutomationSystemConfigurationBooleen.return_value = False
                                                
                                                assert self.systemInstaller.homeAutomationSystem_installation() == False



    def test_creating_administrator_user(self):
        with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.add_user') as mockedAddingUser:
            mockedAddingUser.return_value = True

            assert self.systemInstaller.create_administrator_user("donovan", "maurice", "m", "26/09/1994", "admin", "inhabitant", "tetrew", "0000") == True

        with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.add_user') as mockedAddingUser:
            mockedAddingUser.return_value = True

            assert self.systemInstaller.create_administrator_user(1, "maurice", "m", "26/09/1994", "admin", "inhabitant", "tetrew", "0000") == False

        with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.add_user') as mockedAddingUser:
            mockedAddingUser.return_value = True

            assert self.systemInstaller.create_administrator_user("donovan", 2, "m", "26/09/1994", "admin", "inhabitant", "tetrew", "0000") == False

        with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.add_user') as mockedAddingUser:
            mockedAddingUser.return_value = True

            assert self.systemInstaller.create_administrator_user("donovan", "maurice", 3, "26/09/1994", "admin", "inhabitant", "tetrew", "0000") == False  

        with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.add_user') as mockedAddingUser:
            mockedAddingUser.return_value = True

            assert self.systemInstaller.create_administrator_user("donovan", "maurice", "h", "26/09/1994", "admin", "inhabitant", "tetrew", "0000") == False

        with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.add_user') as mockedAddingUser:
            mockedAddingUser.return_value = True

            assert self.systemInstaller.create_administrator_user("donovan", "maurice", "m", 4, "admin", "inhabitant", "tetrew", "0000") == False

        with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.add_user') as mockedAddingUser:
            mockedAddingUser.return_value = True

            assert self.systemInstaller.create_administrator_user("donovan", "maurice", "m", "26/09/1994", 5, "inhabitant", "tetrew", "0000") == False

        with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.add_user') as mockedAddingUser:
            mockedAddingUser.return_value = True

            assert self.systemInstaller.create_administrator_user("donovan", "maurice", "m", "26/09/1994", "user", "inhabitant", "tetrew", "0000") == False

        with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.add_user') as mockedAddingUser:
            mockedAddingUser.return_value = True

            assert self.systemInstaller.create_administrator_user("donovan", "maurice", "m", "26/09/1994", "admin", 6, "tetrew", "0000") == False

        with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.add_user') as mockedAddingUser:
            mockedAddingUser.return_value = True

            assert self.systemInstaller.create_administrator_user("donovan", "maurice", "m", "26/09/1994", "admin", "guest", "tetrew", "0000") == False

        with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.add_user') as mockedAddingUser:
            mockedAddingUser.return_value = True

            assert self.systemInstaller.create_administrator_user("donovan", "maurice", "m", "26/09/1994", "admin", "inhabitant", 7, "0000") == False

        with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.add_user') as mockedAddingUser:
            mockedAddingUser.return_value = True

            assert self.systemInstaller.create_administrator_user("donovan", "maurice", "m", "26/09/1994", "admin", "inhabitant", "tetrew", 8) == False