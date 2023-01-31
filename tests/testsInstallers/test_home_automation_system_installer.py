#!/usr/bin/python3

import os
import mock
import sys
import json
import subprocess

sys.path.append("..")

from systemeDomotique.classes.installers.homeAutomationSystemInstaller import *
from unittest.mock import patch, mock_open, MagicMock

class TestHomeAutomationSystemInstaller:
    """
        class used for test the database installer
        
            Attributes:
                script path (path of the main script (for files manipulation))
				home automation system installer (class contained all function used for home automation system installation)
                home automation system config file path

            tests:
                test_homeAutomationSystemConfigured_property
                test_getting_zwave_controller_path
                test_getting_zwave_config_folder_path
                test_downloading_nginx
                test_dowloading_supervisor
                test_creating_home_automation_system_config_file
                test_setting_home_automation_system_configuration_booleean_control

    """

    """constructor"""
    scriptPath = os.path.dirname(os.path.abspath(__file__))
    homeAutomationSystemInstaller = HomeAutomationSystemInstaller(os.path.dirname(os.path.abspath(__file__)))
    homeAutomationSystemConfigFile = os.path.dirname(os.path.abspath(__file__)) + "/configs/homeAutomationSystemConfig.json"


    """TESTS"""
    def test_homeAutomationSystemConfigured_property(self):
        """
            test if method return true or false
            test if method return false if error
            test if method return good values
        """

        assert isinstance(self.homeAutomationSystemInstaller.homeAutomationSystemConfigured, bool)

        open_mock = mock_open()
        jsonMock = MagicMock( side_effect = [ { "systemConfigured": True } ] )

        with patch("builtins.open", open_mock, create=False):
            with patch("json.load", jsonMock):
                #test if method return the good values
                assert self.homeAutomationSystemInstaller.homeAutomationSystemConfigured == True
                jsonMock = MagicMock( side_effect = [ { "systemConfigured": False } ] )
                assert self.homeAutomationSystemInstaller.homeAutomationSystemConfigured == False

            #test if method return false if error
            open_mock.return_value.write.side_effect = IOError()
            assert self.homeAutomationSystemInstaller.homeAutomationSystemConfigured == False



    def test_getting_zwave_controller_path(self):
        """
            1.test if method return the controller Path
            2.test if method detect wrong input
        """

        open_mock = mock_open()

        #test if method return the controller Path
        with mock.patch('builtins.input', return_value="/dev/ttyACM0"):
            with patch("builtins.open", open_mock, create=False):
                assert self.homeAutomationSystemInstaller.get_zwave_controller_path() == "/dev/ttyACM0"

        #test if method detect wrong input type
        with mock.patch('builtins.input', return_value=0):
            assert self.homeAutomationSystemInstaller.get_zwave_controller_path() == False


    @patch("subprocess.Popen")
    def test_getting_zwave_config_folder_path(self, mock_subproc_popen):
        """
            1.test if method return the zwave config folder
            2.test if method detect error
            3.test if method detect inexistance of folder
        """

        process_mock = mock.Mock()

        #test if method return the zwave config folder
        attrs = {"communicate.return_value": (b'/test', b"error"),
        "returncode": 0}
        process_mock.configure_mock(**attrs)
        mock_subproc_popen.return_value = process_mock
        assert self.homeAutomationSystemInstaller.get_zwave_config_folder_path() == "/test"

        #test if method detect error
        attrs = {"communicate.return_value": ("b'/test'", b"error"),
        "returncode": 1}
        process_mock.configure_mock(**attrs)
        mock_subproc_popen.return_value = process_mock

        assert self.homeAutomationSystemInstaller.get_zwave_config_folder_path() == False

        #test if method detect inexistance of folder
        attrs = {"communicate.return_value": (b"", b"error"),
        "returncode": 0}
        process_mock.configure_mock(**attrs)
        mock_subproc_popen.return_value = process_mock

        assert self.homeAutomationSystemInstaller.get_zwave_config_folder_path() == False



    @patch("subprocess.Popen")
    def test_downloading_nginx(self, mock_subproc_popen):
        """
            1.test if method return an bool 
            2.test if method return true if succes
            3.test if method return false if error
        """

        process_mock = mock.Mock()
        attrs = {"communicate.return_value": (b"output", b"error"),
        "returncode": 0}
        process_mock.configure_mock(**attrs)
        mock_subproc_popen.return_value = process_mock

        #test if method return an bool
        assert isinstance(self.homeAutomationSystemInstaller.download_nginx(), bool)

        #test if method return True if succes
        assert self.homeAutomationSystemInstaller.download_nginx() == True


        process_mock = mock.Mock()
        attrs = {"communicate.return_value": (b"output", b"error"),
        "returncode": 1}
        process_mock.configure_mock(**attrs)
        mock_subproc_popen.return_value = process_mock

        #test if method return False if error
        assert self.homeAutomationSystemInstaller.download_nginx() == False


    @patch("subprocess.Popen")
    def test_dowloading_supervisor(self, mock_subproc_popen):
        """
            1.test if method return an bool 
            2.test if method return true if succes
            3.test if method return false if error
        """

        process_mock = mock.Mock()
        attrs = {"communicate.return_value": (b"output", b"error"),
        "returncode": 0}
        process_mock.configure_mock(**attrs)
        mock_subproc_popen.return_value = process_mock

        #test if method return an bool
        assert isinstance(self.homeAutomationSystemInstaller.dowload_supervisor(), bool)

        #test if method return True if succes
        assert self.homeAutomationSystemInstaller.dowload_supervisor() == True


        process_mock = mock.Mock()
        attrs = {"communicate.return_value": (b"output", b"error"),
        "returncode": 1}
        process_mock.configure_mock(**attrs)
        mock_subproc_popen.return_value = process_mock

        #test if method return False if error
        assert self.homeAutomationSystemInstaller.dowload_supervisor() == False


    
    def test_creating_home_automation_system_config_file(self):
        """
            1.test if method write in file
                a.test if method used the good file
                b.test if good data was write
            2.test if method return true if succes
            3.test if method return false if error
            4.test if method detect bad parametters
        """

        data = {}

        data["zwaveControllerPath"] = "/test"
        data["zWaveConfigFolderPath"] = "/test/folder"
        data["systemConfigured"] = False

        #test if method write in file
        open_mock = mock_open()
        with patch("builtins.open", open_mock, create=False):
            self.homeAutomationSystemInstaller.create_home_automation_system_config_file(data["zwaveControllerPath"], data["zWaveConfigFolderPath"], data["systemConfigured"])

            #test if method used the good file
            open_mock.assert_called_with(self.homeAutomationSystemConfigFile, "w")
            #test if good data was write
            #open_mock.return_value.write.assert_called_with(data)

            #test if method return true if succes
            assert self.homeAutomationSystemInstaller.create_home_automation_system_config_file(data["zwaveControllerPath"], data["zWaveConfigFolderPath"], data["systemConfigured"]) == True

        #test if method return false if error
        open_mock.return_value.write.side_effect = IOError()
        
        with patch("builtins.open", open_mock, create=False):
            assert self.homeAutomationSystemInstaller.create_home_automation_system_config_file(data["zwaveControllerPath"], data["zWaveConfigFolderPath"], data["systemConfigured"]) == False

        #test if method detect bad parametters
        open_mock = mock_open()
        with patch("builtins.open", open_mock, create=False):
            assert self.homeAutomationSystemInstaller.create_home_automation_system_config_file(False, data["zWaveConfigFolderPath"], data["systemConfigured"]) == False
            assert self.homeAutomationSystemInstaller.create_home_automation_system_config_file(data["zwaveControllerPath"], False, data["systemConfigured"]) == False
            assert self.homeAutomationSystemInstaller.create_home_automation_system_config_file(data["zwaveControllerPath"], data["zWaveConfigFolderPath"], "False") == False


    def test_creating_nginx_config_file(self):
        pass


    def test_creating_web_interface_supervisor_config_file(self):
        pass


    def test_creating_automation_server_supervisor_config_file(self):
        pass


    def test_assignating_fixed_usb_port_names_to_controller(self):
        pass



    def test_setting_home_automation_system_configuration_booleean_control(self):
        """
            1.test if method return an bool 
            2.test if method detect wrong value type
            3.test if method return true if succes
            4.test if method return false if error
            5.test if method read file for collect the data
            6.test if method write in file
        """
        
        #test if method return an bool
        assert isinstance(self.homeAutomationSystemInstaller.set_home_automation_system_configuration_booleean_control("false"), bool) == True
        
        #test if method detect wrong value type
        assert self.homeAutomationSystemInstaller.set_home_automation_system_configuration_booleean_control("test") == False

        open_mock = mock_open()
        jsonMock = MagicMock( side_effect = [ { "test": "test" } ] )

        with patch("builtins.open", open_mock, create=False):
            with patch("json.load", jsonMock):
                #test if method return true if succes
                assert self.homeAutomationSystemInstaller.set_home_automation_system_configuration_booleean_control(True) == True

            #test if method read file for collect the data
            #open_mock.assert_called_with(self.homeAutomationSystemConfigFile, "r")

            #test if method write in file
            open_mock.assert_called_with(self.homeAutomationSystemConfigFile, "w")

        #test if method return false if error
        open_mock.return_value.write.side_effect = IOError()
        with patch("builtins.open", open_mock, create=False):
            assert self.homeAutomationSystemInstaller.set_home_automation_system_configuration_booleean_control(True) == False