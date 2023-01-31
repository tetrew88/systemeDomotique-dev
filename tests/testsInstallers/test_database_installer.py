#!/usr/bin/python3

import os
import mock
import sys
import json
import subprocess

sys.path.append("..")

from systemeDomotique.classes.installers.databaseInstaller import *
from unittest.mock import patch, mock_open, MagicMock

class TestDatabaseInstaller:
    """
        class used for test the database installer
        
            Attributes:
                script path (path of the main script (for files manipulation))
				database installer (class contained all function used for database installation)
                database config file path

            tests:
                test_databaseConfigured_property
                test_getting_system_username
                test_getting_system_user_password
                test_getting_database_name
                test_creating_database_config_file
                test_creating_database
                test_creating_database_table
                test_creating_database_system_user
                test_user_system_privilege_attribution
                test_database_system_download
                test_checking_database_config_file_existance
                test_checking_database_existence
                test_checking_database_user_existence
                test_setting_database_configuration_booleean_control

    """

    """constructor"""
    scriptPath = os.path.dirname(os.path.abspath(__file__))
    databaseInstaller = DatabaseInstaller(scriptPath)
    databaseConfigFilePath = scriptPath + "/configs/databaseConfig.json"


    """TESTS"""
    def test_databaseConfigured_property(self):
        """
            test if method return true or false
            test if method return false if error
            test if method return good values
        """

        assert isinstance(self.databaseInstaller.databaseConfigured, bool)

        open_mock = mock_open()
        jsonMock = MagicMock( side_effect = [ { "databaseConfigured": True } ] )

        with patch("builtins.open", open_mock, create=False):
            with patch("json.load", jsonMock):
                #test if method return the good values
                assert self.databaseInstaller.databaseConfigured == True
                jsonMock = MagicMock( side_effect = [ { "databaseConfigured": False } ] )
                assert self.databaseInstaller.databaseConfigured == False

            #test if methid detect error in dictionnary reading
            jsonMock = MagicMock( side_effect = [ { "NULL": False } ] )
            assert self.databaseInstaller.databaseConfigured == False

            #test if method return false if error
            open_mock.return_value.write.side_effect = IOError()
            assert self.databaseInstaller.databaseConfigured == False


    def test_getting_system_username(self):
        """
            1.test if method return the username
            2.test if method detect empty input and auto fill username value to 'homeAutomationSystem'
            3.test if method detect wrong input
        """

        #test if method return the username
        with mock.patch('builtins.input', return_value="hestia"):
            assert self.databaseInstaller.get_system_username() == "hestia"
        #test if method detect empty input and auto fill username value to 'homeAutomationSystem'
        with mock.patch('builtins.input', return_value=""):
            assert self.databaseInstaller.get_system_username() == "homeAutomationSystem"

        #test if method detect wrong input type
        with mock.patch('builtins.input', return_value=0):
            assert self.databaseInstaller.get_system_username() == False


    def test_getting_system_user_password(self):
        """
            1.test if method return the password
            2.test if method detect empty input
            3.test if method detect wrong input
        """
        
        #test if method return the password
        with mock.patch('builtins.input', return_value="hestia"):
            assert self.databaseInstaller.get_system_user_password() == "hestia"

        #test if method detect empty input
        with mock.patch('builtins.input', return_value=""):
            assert self.databaseInstaller.get_system_user_password() == False

        #test if method detect wrong input
        with mock.patch('builtins.input', return_value=0):
            assert self.databaseInstaller.get_system_user_password() == False


    def test_getting_database_name(self):
        """
            1.test if method return the database name
            2.test if method detect empty input and auto fill username value to 'Home'
            3.test if method detect wrong input
        """

        #test if method return the database name
        with mock.patch('builtins.input', return_value="hestia"):
            assert self.databaseInstaller.get_database_name() == "hestia"

        #test if method detect empty input and auto fill username value to 'Home'
        with mock.patch('builtins.input', return_value=""):
            assert self.databaseInstaller.get_database_name() == "Home"

        #test if method detect wrong input
        with mock.patch('builtins.input', return_value=0):
            assert self.databaseInstaller.get_database_name() == False


    def test_creating_database_config_file(self):
        """
            1.test if method write in file
                a.test if method used the good file
                b.test if good data was write
            2.test if method return true if succes
            3.test if method return false if error
            4.test if method detect wrong parametters
        """

        data = {}

        data["systemUserName"] = "testUserName"
        data["systemUserPassword"] = "TestUserPassword"
        data["databaseName"] = "testDatabaseName"
        data["databaseConfigured"] = False

        #test if method write in file
        open_mock = mock_open()
        with patch("builtins.open", open_mock, create=False):
            self.databaseInstaller.create_database_config_file(data["systemUserName"], data["systemUserPassword"], data["databaseName"], data["databaseConfigured"])

            #test if method used the good file
            open_mock.assert_called_with(self.databaseConfigFilePath, "w")
            #test if good data was write
            #open_mock.return_value.write.assert_called_with(data)

            #test if method return true if succes
            open_mock = mock_open()
            with patch("builtins.open", open_mock, create=False):
                assert self.databaseInstaller.create_database_config_file(data["systemUserName"], data["systemUserPassword"], data["databaseName"], data["databaseConfigured"]) == True

        #test if method return false if error
        open_mock.return_value.write.side_effect = IOError()
        
        with patch("builtins.open", open_mock, create=False):
            assert self.databaseInstaller.create_database_config_file(data["systemUserName"], data["systemUserPassword"], data["databaseName"], data["databaseConfigured"]) == False

        open_mock = mock_open()
        with patch("builtins.open", open_mock, create=False):
            data["systemUserName"] = False
            data["systemUserPassword"] = "TestUserPassword"
            data["databaseName"] = "testDatabaseName"
            data["databaseConfigured"] = False
            assert self.databaseInstaller.create_database_config_file(data["systemUserName"], data["systemUserPassword"], data["databaseName"], data["databaseConfigured"]) == False

            data["systemUserName"] = "testUserName"
            data["systemUserPassword"] = False
            data["databaseName"] = "testDatabaseName"
            data["databaseConfigured"] = False
            assert self.databaseInstaller.create_database_config_file(data["systemUserName"], data["systemUserPassword"], data["databaseName"], data["databaseConfigured"]) == False

            data["systemUserName"] = "testUserName"
            data["systemUserPassword"] = "TestUserPassword"
            data["databaseName"] = False
            data["databaseConfigured"] = False
            assert self.databaseInstaller.create_database_config_file(data["systemUserName"], data["systemUserPassword"], data["databaseName"], data["databaseConfigured"]) == False

            data["systemUserName"] = "testUserName"
            data["systemUserPassword"] = "TestUserPassword"
            data["databaseName"] = "testDatabaseName"
            data["databaseConfigured"] = ""
            assert self.databaseInstaller.create_database_config_file(data["systemUserName"], data["systemUserPassword"], data["databaseName"], data["databaseConfigured"]) == False


    @patch("subprocess.Popen")
    def test_creating_database(self, mock_subproc_popen):
        """
            1.test if method return an bool 
            2.test if method return true if succes
            3.test if method return false if error
            4.test if method detect already exist database
            5.test if method detect wrong parametters
        """

        process_mock = mock.Mock()
        attrs = {"communicate.return_value": ("output", "error"),
        "returncode": 0}
        process_mock.configure_mock(**attrs)
        mock_subproc_popen.return_value = process_mock

        #test if method return an bool
        assert isinstance(self.databaseInstaller.create_database("test"), bool)

        #test if method return true if succes
        assert self.databaseInstaller.create_database("test") == True


        attrs = {"communicate.return_value": ("output", "error"),
        "returncode": 1}
        process_mock.configure_mock(**attrs)
        mock_subproc_popen.return_value = process_mock

        #test if method return FALSE if error
        assert self.databaseInstaller.create_database("test") == False

        #test if method detect already exist database
        with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.check_database_existence') as mockedMethod:
            mockedMethod.return_value = False
            assert self.databaseInstaller.create_database("test") == False
            mockedMethod.return_value = True
            assert self.databaseInstaller.create_database("test") == True

        #test if method detect wrong parametters
        attrs = {"communicate.return_value": ("output", "error"),
        "returncode": 0}
        process_mock.configure_mock(**attrs)
        mock_subproc_popen.return_value = process_mock
        assert self.databaseInstaller.create_database(False) == False


    @patch("subprocess.Popen")
    def test_creating_database_table(self, mock_subproc_popen):
        """
            1.test if method return an bool 
            2.test if method return true if succes
            3.test if method detect creation file error
            4.test if method detect database existance error
            5.check if method detect wrong parametters
        """
        
        process_mock = mock.Mock()
        attrs = {"communicate.return_value": ("output", "error"),
        "returncode": 0}
        process_mock.configure_mock(**attrs)
        mock_subproc_popen.return_value = process_mock

        #test if method return an bool
        assert isinstance(self.databaseInstaller.create_database_table("test"), bool)

        #test if method return true if succes
        with mock.patch('os.path.exists') as mockedPath:
            mockedPath.return_value = True # 1
            
            with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.check_database_existence') as mockedMethod:
                mockedMethod.return_value = True
                assert self.databaseInstaller.create_database_table("test") == True

        #test if method detect creation file error
        with mock.patch('os.path.exists') as mockedPath:
            mockedPath.return_value = False
            
            with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.check_database_existence') as mockedMethod:
                mockedMethod.return_value = True
                assert self.databaseInstaller.create_database_table("test") == False

        #test if method detect database existance error
        with mock.patch('os.path.exists') as mockedPath:
            mockedPath.return_value = True # 1
            
            with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.check_database_existence') as mockedMethod:
                mockedMethod.return_value = False
                assert self.databaseInstaller.create_database_table("test") == False

        #test if method detect wrong parametters 
        attrs = {"communicate.return_value": ("output", "error"),
        "returncode": 0}
        process_mock.configure_mock(**attrs)
        mock_subproc_popen.return_value = process_mock

        with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.check_database_existence') as mockedMethod:
                mockedMethod.return_value = True
                assert self.databaseInstaller.create_database_table(False) == False


    @patch("subprocess.Popen")
    def test_creating_database_system_user(self, mock_subproc_popen):
        """
            1.test if method return an bool 
            2.test if method return true if succes
            3.test if method return false if error
            4.test if method detect database user already existance
            5.check if method detect wrong parametters
        """

        process_mock = mock.Mock()
        attrs = {"communicate.return_value": ("output", "error"),
        "returncode": 0}
        process_mock.configure_mock(**attrs)
        mock_subproc_popen.return_value = process_mock

        #test if method return an bool
        assert isinstance(self.databaseInstaller.create_database_system_user("testUser", "testDatabase"), bool)

        #test if method return True if succes
        assert self.databaseInstaller.create_database_system_user("testUser", "testDatabase") == True


        attrs = {"communicate.return_value": ("output", "error"),
        "returncode": 1}
        process_mock.configure_mock(**attrs)
        mock_subproc_popen.return_value = process_mock

        #test if method return FALSE if error
        assert self.databaseInstaller.create_database_system_user("testUser", "testDatabase") == False

        #test if method detect database user already existance
        with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.check_database_user_existence') as mockedMethod:
            mockedMethod.return_value = True
            assert self.databaseInstaller.create_database_system_user("testUser", "testDatabase") == True

        #check if method detect wrong parametters
        attrs = {"communicate.return_value": ("output", "error"),
        "returncode": 0}
        process_mock.configure_mock(**attrs)
        mock_subproc_popen.return_value = process_mock

        assert self.databaseInstaller.create_database_system_user(False, "testDatabase") == False
        assert self.databaseInstaller.create_database_system_user("testUser", False) == False
        assert self.databaseInstaller.create_database_system_user(False, False) == False




    @patch("subprocess.Popen")
    def test_user_system_privilege_attribution(self, mock_subproc_popen):
        """
            1.test if method return an bool 
            2.test if method return true if succes
            3.test if method detect database user existance
            4.test if method detect database existance
            5.test if method return false if error
            6.test if method detect bad parramatters
        """

        process_mock = mock.Mock()
        attrs = {"communicate.return_value": ("output", "error"),
        "returncode": 0}
        process_mock.configure_mock(**attrs)
        mock_subproc_popen.return_value = process_mock

        with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.check_database_user_existence') as mockedUserControl:
            mockedUserControl.return_value = True
            with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.check_database_existence') as mockedDatabaseControl:
                mockedDatabaseControl.return_value = True
        
                #test if method return an bool
                assert isinstance(self.databaseInstaller.attribute_user_system_privilege("testUser", "testDatabase"), bool)

                #test if method return True if succes
                assert self.databaseInstaller.attribute_user_system_privilege("testUser", "testDatabase") == True

        with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.check_database_user_existence') as mockedUserControl:
            mockedUserControl.return_value = False
            with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.check_database_existence') as mockedDatabaseControl:
                mockedDatabaseControl.return_value = True
                assert self.databaseInstaller.attribute_user_system_privilege("testUser", "testDatabase") == False

        with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.check_database_user_existence') as mockedUserControl:
            mockedUserControl.return_value = True
            with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.check_database_existence') as mockedDatabaseControl:
                mockedDatabaseControl.return_value = False
                assert self.databaseInstaller.attribute_user_system_privilege("testUser", "testDatabase") == False


        attrs = {"communicate.return_value": ("output", "error"),
        "returncode": 1}
        process_mock.configure_mock(**attrs)
        mock_subproc_popen.return_value = process_mock

        with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.check_database_user_existence') as mockedUserControl:
            mockedUserControl.return_value = True
            with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.check_database_existence') as mockedDatabaseControl:
                mockedDatabaseControl.return_value = True

                #test if method return FALSE if error
                assert self.databaseInstaller.attribute_user_system_privilege("testUser", "testDatabase") == False

        attrs = {"communicate.return_value": ("output", "error"),
        "returncode": 0}
        process_mock.configure_mock(**attrs)
        mock_subproc_popen.return_value = process_mock

        #test if method detect bad parramatters
        with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.check_database_user_existence') as mockedUserControl:
            mockedUserControl.return_value = True
            with mock.patch('systemeDomotique.classes.installers.databaseInstaller.DatabaseInstaller.check_database_existence') as mockedDatabaseControl:
                mockedDatabaseControl.return_value = True

                assert self.databaseInstaller.attribute_user_system_privilege(False, "testDatabase") == False
                assert self.databaseInstaller.attribute_user_system_privilege("testUser", False) == False



    @patch("subprocess.Popen")
    def test_database_system_download(self, mock_subproc_popen):
        """
            1.test if method return an bool 
            2.test if method return true if succes
            3.test if method return false if error
        """

        process_mock = mock.Mock()
        attrs = {"communicate.return_value": ("output", "error"),
        "returncode": 0}
        process_mock.configure_mock(**attrs)
        mock_subproc_popen.return_value = process_mock

        #test if method return an bool
        assert isinstance(self.databaseInstaller.download_database_system(), bool)

        #test if method return True if succes
        assert self.databaseInstaller.download_database_system() == True


        process_mock = mock.Mock()
        attrs = {"communicate.return_value": ("output", "error"),
        "returncode": 1}
        process_mock.configure_mock(**attrs)
        mock_subproc_popen.return_value = process_mock

        #test if method return False if error
        assert self.databaseInstaller.download_database_system() == False


    def test_checking_database_config_file_existance(self):
        """
            1.test if method return an bool 
            2.test if method return true if succes
            3.test if method used the good file
            4.test if method return false if error
        """
        
        open_mock = mock_open()
        with patch("builtins.open", open_mock, create=False):
            #test if method return an bool 
            assert isinstance(self.databaseInstaller.check_database_config_file_existence(), bool) == True

            #test if method return true if succes
            assert self.databaseInstaller.check_database_config_file_existence() == True

            #test if method used the good file
            open_mock.assert_called_with(self.databaseConfigFilePath, "r")

        #test if method return false if error
        open_mock.return_value = IOError()
        with patch("builtins.open", open_mock, create=False):
            assert self.databaseInstaller.check_database_config_file_existence() == False


    @patch("subprocess.Popen")
    def test_checking_database_existence(self, mock_subproc_popen):
        """
            1.test if method return an bool 
            2.test if method return true if succes
            3.test if method return false if error
            4.test if method detect bad parametters
        """

        process_mock = mock.Mock()
        attrs = {"communicate.return_value": ("output", "error"),
        "returncode": 0}
        process_mock.configure_mock(**attrs)
        mock_subproc_popen.return_value = process_mock

        #test if method return an bool
        assert isinstance(self.databaseInstaller.check_database_existence("testDatabase"), bool)

        #test if method return True if succes
        assert self.databaseInstaller.check_database_existence("testDatabase") == True


        process_mock = mock.Mock()
        attrs = {"communicate.return_value": ("output", "error"),
        "returncode": 1}
        process_mock.configure_mock(**attrs)
        mock_subproc_popen.return_value = process_mock

        #test if method return False if error
        assert self.databaseInstaller.check_database_existence("testDatabase") == False

        attrs = {"communicate.return_value": ("output", "error"),
        "returncode": 0}
        process_mock.configure_mock(**attrs)
        mock_subproc_popen.return_value = process_mock

        #test if method detect bad parametters
        assert self.databaseInstaller.check_database_existence(False) == False


    @patch("subprocess.Popen")
    def test_checking_database_user_existence(self, mock_subproc_popen):
        """
            1.test if method return an bool 
            2.test if method return true if succes
            3.test if method return false if error
            4.test if method detect bad parametters
        """

        process_mock = mock.Mock()
        attrs = {"communicate.return_value": ("output", "error"),
        "returncode": 0}
        process_mock.configure_mock(**attrs)
        mock_subproc_popen.return_value = process_mock

        #test if method return an bool
        assert isinstance(self.databaseInstaller.check_database_user_existence("testUser"), bool)

        #test if method return True if succes
        assert self.databaseInstaller.check_database_user_existence("testUser") == True


        process_mock = mock.Mock()
        attrs = {"communicate.return_value": ("output", "error"),
        "returncode": 1}
        process_mock.configure_mock(**attrs)
        mock_subproc_popen.return_value = process_mock

        #test if method return False if error
        assert self.databaseInstaller.check_database_user_existence("testUser") == False

        attrs = {"communicate.return_value": ("output", "error"),
        "returncode": 0}
        process_mock.configure_mock(**attrs)
        mock_subproc_popen.return_value = process_mock

        #test if method detect bad parametters
        assert self.databaseInstaller.check_database_user_existence(False) == False


    def test_setting_database_configuration_booleean_control(self):
        """
            1.test if method return an bool 
            2.test if method detect wrong value type
            3.test if method return true if succes
            4.test if method return false if error
            5.test if method read file for collect the data
            6.test if method write in file
        """

        #test if method return an bool 
        assert isinstance(self.databaseInstaller.set_database_configuration_booleean_control("false"), bool) == True

        #test if method detect wrong value type
        assert self.databaseInstaller.set_database_configuration_booleean_control("test") == False

        open_mock = mock_open()
        jsonMock = MagicMock( side_effect = [ { "test": "test" } ] )

        with patch("builtins.open", open_mock, create=False):
            with patch("json.load", jsonMock):
                #test if method return true if succes
                assert self.databaseInstaller.set_database_configuration_booleean_control(True) == True

            #test if method read file for collect the data
            #open_mock.assert_called_with(self.databaseConfigFilePath, "r")

            #test if method write in file
            open_mock.assert_called_with(self.databaseConfigFilePath, "w")

        #test if method return false if error
        open_mock.return_value.write.side_effect = IOError()
        with patch("builtins.open", open_mock, create=False):
            assert self.databaseInstaller.set_database_configuration_booleean_control(True) == False