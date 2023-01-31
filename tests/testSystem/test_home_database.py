#!/usr/bin/python3

import os
import mock
import sys
import json
import subprocess

sys.path.append("..")

from systemeDomotique.homeAutomationServer.classes.homeDatabase import *
from systemeDomotique.homeAutomationServer.classes.users.profil import *
from systemeDomotique.homeAutomationServer.classes.users.guest import *
from systemeDomotique.homeAutomationServer.classes.users.inhabitant import *
from systemeDomotique.homeAutomationServer.classes.users.user import *
from systemeDomotique.homeAutomationServer.classes.users.administrator import *

from unittest.mock import patch, mock_open, MagicMock


class FakeSuccesConnection:
    def __init__(self):
        pass

    def cursor(self, buffered):
        return True

    def close(self):
        pass

    def commit(self):
        pass

class FakeFailConnection:
    def __init__(self):
        pass

    def cursor(self, buffered):
        return False

class FakeSuccesCursor:
    def __init__(self):
        self.list = []
        self.lastrowid = 1

    def execute(self, request):
        pass

    def fetchall(self):
        return self.list

class FakeFailCursorExecute:
    def __init__(self):
        pass

class FakeFailCursorFetchall:
    def __init__(self):
        pass

    def execute(self, request):
        pass

class FakeFailCursorLastrowId:
    def __init__(self):
        self.list = []

    def execute(self, request):
        pass


class TestDatabaseInstaller:
    """
        class used for test the home database
        
            Attributes:

            tests:

    """

    """constructor"""
    scriptPath = os.path.dirname(os.path.abspath(__file__))
    homeDatabase = HomeDatabase(scriptPath)


    def test_databaseName_property(self):
        """
            1.test if method return the good values
            2.test if methid detect error in dictionnary reading
            3.test if method return false if error
        """
        open_mock = mock_open()
        jsonMock = MagicMock( side_effect = [ { "systemUserName": "test" } ] )

        with patch("builtins.open", open_mock, create=False):
            with patch("json.load", jsonMock):
                #test if method return the good values
                assert self.homeDatabase.username == "test"

            #test if methid detect error in dictionnary reading
            jsonMock = MagicMock( side_effect = [ { "NULL": False } ] )
            assert self.homeDatabase.username == False

            #test if method return false if error
            open_mock.return_value.write.side_effect = IOError()
            assert self.homeDatabase.username == False

    
    def test_password_property(self):
        """
            1.test if method return the good values
            2.test if methid detect error in dictionnary reading
            3.test if method return false if error
        """
        
        open_mock = mock_open()
        jsonMock = MagicMock( side_effect = [ { "systemUserPassword": "test" } ] )

        with patch("builtins.open", open_mock, create=False):
            with patch("json.load", jsonMock):
                #test if method return the good values
                assert self.homeDatabase.password == "test"

                #test if methid detect error in dictionnary reading
                jsonMock = MagicMock( side_effect = [ { "NULL": False } ] )
                assert self.homeDatabase.password == False

                #test if method return false if error
                open_mock.return_value.write.side_effect = IOError()
                assert self.homeDatabase.password == False


    
    def test_connection(self):
        """
            1.test if method return True if succes
            2.test if method return succes if connection was already established
            3.test if methid detect error during connection
            4.test if method detect bas cursor
        """
        
        self.homeDatabase.db_connection = False
        self.homeDatabase.db_cursor = False
        #test if method return True if succes
        with mock.patch("mysql.connector.connect") as mockDatabaseConnection:
            mockDatabaseConnection.return_value = FakeSuccesConnection()

            assert self.homeDatabase.connect() == True

        #test if method return succes if connection was already established
        self.homeDatabase.db_connection = FakeSuccesConnection()
        self.homeDatabase.db_cursor = self.homeDatabase.db_connection.cursor(buffered=True)
        assert self.homeDatabase.connect() == True


        self.homeDatabase.db_connection = False
        self.homeDatabase.db_cursor = False
        #test if methid detect error during connection
        with mock.patch("mysql.connector.connect") as mockDatabaseConnection:
            mockDatabaseConnection.return_value = FakeFailConnection()

            assert self.homeDatabase.connect() == False

        self.homeDatabase.db_connection = False
        self.homeDatabase.db_cursor = False
        #test if method detect bas cursor
        with mock.patch("mysql.connector.connect") as mockDatabaseConnection:
            mockDatabaseConnection.return_value = False

            assert self.homeDatabase.connect() == False


    def test_disconnection(self):
        """
            1.test if method return true if succes
            2.test if method return true if connection was already disconnected
            3.test if method detect error during disconnection
        """
        
        #test if method return true if succes
        self.homeDatabase.db_connection = FakeSuccesConnection()
        assert self.homeDatabase.disconnect() == True

        #test if method return true if connection was already disconnected
        self.homeDatabase.db_connection = False
        assert self.homeDatabase.disconnect() == True

        #test if method detect error during disconnection
        self.homeDatabase.db_connection = FakeFailConnection()
        assert self.homeDatabase.disconnect() == False


    def test_commiting_change(self):
        """
            1.test if method return True if succes
            2.test if method detect error durring connection
            3.test if method detect error durring committing
        """

        #test if method return True if succes
        self.homeDatabase.db_connection = FakeSuccesConnection()
        assert self.homeDatabase.commit_change() == True

        #test if method detect error durring connection
        self.homeDatabase.db_connection = False
        assert self.homeDatabase.commit_change() == False

        #test if method detect error durring committing
        self.homeDatabase.db_connection = FakeFailConnection()
        assert self.homeDatabase.commit_change() == False



    def test_getting_users_list(self):
        """
            1.test if method return good type of data
            2.test if method detect error during database connection
            3.test if method detect error during request execution
            4.test if method during getting request answer
            5.test if method detect error during getting profil
        """
        
        #test if method return good type of data
        with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.connect') as mockedDatabaseConnection:
            mockedDatabaseConnection.return_value = True
            self.homeDatabase.db_cursor = FakeSuccesCursor()
            self.homeDatabase.db_cursor.list = [
                (1, 1, "admin", "inhabitant", "tetrew", "0000"),
                (1, 1, "user", "inhabitant", "tetrew", "0000"),
                (1, 1, "user", "guest", "tetrew", "0000")
            ]

            with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.get_profil_by_id') as mockeGettingProfilById:
                mockeGettingProfilById.return_value = Profil(1, "donovan", "maurice", "m", "26/09/1994")

                assert isinstance(self.homeDatabase.get_users_list(), list) == True

                usersList = self.homeDatabase.get_users_list()
                assert isinstance(usersList[0], Administrator)
                assert isinstance(usersList[0], Inhabitant)
                assert isinstance(usersList[1], Inhabitant)
                assert isinstance(usersList[2], Guest)

                for user in usersList:
                    assert isinstance(user, User)

        with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.connect') as mockedDatabaseConnection:
            mockedDatabaseConnection.return_value = True
            self.homeDatabase.db_cursor = FakeSuccesCursor()
            self.homeDatabase.db_cursor.list = []

            assert self.homeDatabase.get_users_list() == []


        #test if method detect error during database connection
        with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.connect') as mockedDatabaseConnection:
            mockedDatabaseConnection.return_value = False
            self.homeDatabase.db_cursor = FakeSuccesCursor()
            self.homeDatabase.db_cursor.list = [
                (1, 1, "admin", "inhabitant", "tetrew", "0000"),
                (1, 1, "user", "inhabitant", "tetrew", "0000"),
                (1, 1, "user", "guest", "tetrew", "0000")
            ]


            with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.get_profil_by_id') as mockeGettingProfilById:
                mockeGettingProfilById.return_value = Profil(1, "donovan", "maurice", "m", "26/09/1994")

                assert self.homeDatabase.get_users_list() == False

        
        #test if method detect error during request execution
        with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.connect') as mockedDatabaseConnection:
            mockedDatabaseConnection.return_value = True
            self.homeDatabase.db_cursor = FakeFailCursorExecute()

            with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.get_profil_by_id') as mockeGettingProfilById:
                mockeGettingProfilById.return_value = Profil(1, "donovan", "maurice", "m", "26/09/1994")

                assert self.homeDatabase.get_users_list() == False

        #test if method during request answer captation
        with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.connect') as mockedDatabaseConnection:
            mockedDatabaseConnection.return_value = True
            self.homeDatabase.db_cursor = FakeFailCursorFetchall()

            with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.get_profil_by_id') as mockeGettingProfilById:
                mockeGettingProfilById.return_value = Profil(1, "donovan", "maurice", "m", "26/09/1994")

                assert self.homeDatabase.get_users_list() == False


        #test if method detect error during getting profil
        with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.connect') as mockedDatabaseConnection:
            mockedDatabaseConnection.return_value = True
            self.homeDatabase.db_cursor = FakeSuccesCursor()
            self.homeDatabase.db_cursor.list = [
                (1, 1, "admin", "inhabitant", "tetrew", "0000"),
                (1, 1, "user", "inhabitant", "tetrew", "0000"),
                (1, 1, "user", "guest", "tetrew", "0000")
            ]


            with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.get_profil_by_id') as mockeGettingProfilById:
                mockeGettingProfilById.return_value = False

                assert self.homeDatabase.get_users_list() == False


    def test_getting_profils_list(self):
        """
            1.test if method return good type of data
            2.test if method detect database error connection
            3.test if method detect error during request execution
            4.test if method during getting request answer
        """
        
        #test if method return good type of data
        with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.connect') as mockedDatabaseConnection:
            mockedDatabaseConnection.return_value = True
            self.homeDatabase.db_cursor = FakeSuccesCursor()
            self.homeDatabase.db_cursor.list = [
                (1, "donovan", "maurice", "m", "26/09/1994")
            ]

            assert isinstance(self.homeDatabase.get_profils_list(), list) == True

            profilsList = self.homeDatabase.get_profils_list()

            for profil in profilsList:
                    assert isinstance(profil, Profil)
        
        with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.connect') as mockedDatabaseConnection:
            mockedDatabaseConnection.return_value = True
            self.homeDatabase.db_cursor = FakeSuccesCursor()
            self.homeDatabase.db_cursor.list = []

            assert self.homeDatabase.get_profils_list() == []


        #test if method detect database error connection
        with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.connect') as mockedDatabaseConnection:
            mockedDatabaseConnection.return_value = False
            self.homeDatabase.db_cursor = FakeSuccesCursor()

            assert self.homeDatabase.get_profils_list() == False


        #test if method detect error during request execution
        with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.connect') as mockedDatabaseConnection:
            mockedDatabaseConnection.return_value = True
            self.homeDatabase.db_cursor = FakeFailCursorExecute()

            assert self.homeDatabase.get_profils_list() == False


        #test if method during getting request answer
        with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.connect') as mockedDatabaseConnection:
            mockedDatabaseConnection.return_value = True
            self.homeDatabase.db_cursor = FakeFailCursorFetchall()

            assert self.homeDatabase.get_profils_list() == False


    def test_getting_inhabitant_List(self):
        """
            1.test if method return good type of data
            2.test if method detect error during database connection
            3.test if method detect error during request execution
            4.test if method during getting request answer
            5.test if method detect error during getting profil
        """
        
        #test if method return good type of data
        with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.connect') as mockedDatabaseConnection:
            mockedDatabaseConnection.return_value = True
            self.homeDatabase.db_cursor = FakeSuccesCursor()
            self.homeDatabase.db_cursor.list = [
                (1, 1, "admin", "inhabitant", "tetrew", "0000"),
                (1, 1, "user", "inhabitant", "tetrew", "0000")
            ]

            with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.get_profil_by_id') as mockeGettingProfilById:
                mockeGettingProfilById.return_value = Profil(1, "donovan", "maurice", "m", "26/09/1994")

                assert isinstance(self.homeDatabase.get_inhabitant_List(), list) == True

                inhabitantList = self.homeDatabase.get_users_list()
                assert isinstance(inhabitantList[0], Administrator)
                assert isinstance(inhabitantList[0], Inhabitant)
                assert isinstance(inhabitantList[1], Inhabitant)

                for inhabitant in inhabitantList:
                    assert isinstance(inhabitant, Inhabitant)

        with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.connect') as mockedDatabaseConnection:
            mockedDatabaseConnection.return_value = True
            self.homeDatabase.db_cursor = FakeSuccesCursor()
            self.homeDatabase.db_cursor.list = []

            assert self.homeDatabase.get_inhabitant_List() == []


        #test if method detect error during database connection
        with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.connect') as mockedDatabaseConnection:
            mockedDatabaseConnection.return_value = False
            self.homeDatabase.db_cursor = FakeSuccesCursor()
            self.homeDatabase.db_cursor.list = [
                (1, 1, "admin", "inhabitant", "tetrew", "0000"),
                (1, 1, "user", "inhabitant", "tetrew", "0000")
            ]


            with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.get_profil_by_id') as mockeGettingProfilById:
                mockeGettingProfilById.return_value = Profil(1, "donovan", "maurice", "m", "26/09/1994")

                assert self.homeDatabase.get_inhabitant_List() == False

        
        #test if method detect error during request execution
        with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.connect') as mockedDatabaseConnection:
            mockedDatabaseConnection.return_value = True
            self.homeDatabase.db_cursor = FakeFailCursorExecute()

            with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.get_profil_by_id') as mockeGettingProfilById:
                mockeGettingProfilById.return_value = Profil(1, "donovan", "maurice", "m", "26/09/1994")

                assert self.homeDatabase.get_inhabitant_List() == False

        
        #test if method during getting request answer
        with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.connect') as mockedDatabaseConnection:
            mockedDatabaseConnection.return_value = True
            self.homeDatabase.db_cursor = FakeFailCursorFetchall()

            with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.get_profil_by_id') as mockeGettingProfilById:
                mockeGettingProfilById.return_value = Profil(1, "donovan", "maurice", "m", "26/09/1994")

                assert self.homeDatabase.get_inhabitant_List() == False

        
        #test if method detect error during getting profil
        with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.connect') as mockedDatabaseConnection:
            mockedDatabaseConnection.return_value = True
            self.homeDatabase.db_cursor = FakeSuccesCursor()
            self.homeDatabase.db_cursor.list = [
                (1, 1, "admin", "inhabitant", "tetrew", "0000"),
                (1, 1, "user", "inhabitant", "tetrew", "0000")
            ]

            with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.get_profil_by_id') as mockeGettingProfilById:
                mockeGettingProfilById.return_value = False

                assert self.homeDatabase.get_inhabitant_List() == False

            
    def test_getting_guest_list(self):
        """
            1.test if method return good type of data
            2.test if method detect error during database connection
            3.test if method detect error during request execution
            4.test if method during getting request answer
            5.test if method detect error during getting profil
        """

        #test if method return good type of data
        with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.connect') as mockedDatabaseConnection:
            mockedDatabaseConnection.return_value = True
            self.homeDatabase.db_cursor = FakeSuccesCursor()
            self.homeDatabase.db_cursor.list = [
                (1, 1, "user", "guest", "tetrew", "0000")
            ]

            with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.get_profil_by_id') as mockeGettingProfilById:
                mockeGettingProfilById.return_value = Profil(1, "donovan", "maurice", "m", "26/09/1994")

                assert isinstance(self.homeDatabase.get_guest_list(), list) == True

                guestList = self.homeDatabase.get_guest_list()
                assert isinstance(guestList[0], Guest)

        with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.connect') as mockedDatabaseConnection:
            mockedDatabaseConnection.return_value = True
            self.homeDatabase.db_cursor = FakeSuccesCursor()
            self.homeDatabase.db_cursor.list = []

            assert self.homeDatabase.get_guest_list() == []


        #test if method detect error during database connection
        with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.connect') as mockedDatabaseConnection:
            mockedDatabaseConnection.return_value = False
            self.homeDatabase.db_cursor = FakeSuccesCursor()
            self.homeDatabase.db_cursor.list = [
                (1, 1, "user", "guest", "tetrew", "0000")
            ]


            with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.get_profil_by_id') as mockeGettingProfilById:
                mockeGettingProfilById.return_value = Profil(1, "donovan", "maurice", "m", "26/09/1994")

                assert self.homeDatabase.get_guest_list() == False

        
        #test if method detect error during request execution
        with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.connect') as mockedDatabaseConnection:
            mockedDatabaseConnection.return_value = True
            self.homeDatabase.db_cursor = FakeFailCursorExecute()

            with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.get_profil_by_id') as mockeGettingProfilById:
                mockeGettingProfilById.return_value = Profil(1, "donovan", "maurice", "m", "26/09/1994")

                assert self.homeDatabase.get_guest_list() == False

        
        #test if method during getting request answer
        with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.connect') as mockedDatabaseConnection:
            mockedDatabaseConnection.return_value = True
            self.homeDatabase.db_cursor = FakeFailCursorFetchall()

            with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.get_profil_by_id') as mockeGettingProfilById:
                mockeGettingProfilById.return_value = Profil(1, "donovan", "maurice", "m", "26/09/1994")

                assert self.homeDatabase.get_guest_list() == False

        
        #test if method detect error during getting profil
        with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.connect') as mockedDatabaseConnection:
            mockedDatabaseConnection.return_value = True
            self.homeDatabase.db_cursor = FakeSuccesCursor()
            self.homeDatabase.db_cursor.list = [
                (1, 1, "user", "guest", "tetrew", "0000")]

            with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.get_profil_by_id') as mockeGettingProfilById:
                mockeGettingProfilById.return_value = False

                assert self.homeDatabase.get_guest_list() == False


    def test_getting_administrator_list(self):
        """
            1.test if method return good type of data
            2.test if method detect error during database connection
            3.test if method detect error during request execution
            4.test if method during getting request answer
            5.test if method detect error during getting profil
        """

        #test if method return good type of data
        with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.connect') as mockedDatabaseConnection:
            mockedDatabaseConnection.return_value = True
            self.homeDatabase.db_cursor = FakeSuccesCursor()
            self.homeDatabase.db_cursor.list = [
                (1, 1, "admin", "inhabitant", "tetrew", "0000")
            ]

            with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.get_profil_by_id') as mockeGettingProfilById:
                mockeGettingProfilById.return_value = Profil(1, "donovan", "maurice", "m", "26/09/1994")

                assert isinstance(self.homeDatabase.get_administrator_list(), list) == True

                adminList = self.homeDatabase.get_administrator_list()
                assert isinstance(adminList[0], Administrator)

        with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.connect') as mockedDatabaseConnection:
            mockedDatabaseConnection.return_value = True
            self.homeDatabase.db_cursor = FakeSuccesCursor()
            self.homeDatabase.db_cursor.list = []

            assert self.homeDatabase.get_administrator_list() == []


        #test if method detect error during database connection
        with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.connect') as mockedDatabaseConnection:
            mockedDatabaseConnection.return_value = False
            self.homeDatabase.db_cursor = FakeSuccesCursor()
            self.homeDatabase.db_cursor.list = [
                (1, 1, "admin", "inhabitant", "tetrew", "0000")
            ]


            with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.get_profil_by_id') as mockeGettingProfilById:
                mockeGettingProfilById.return_value = Profil(1, "donovan", "maurice", "m", "26/09/1994")

                assert self.homeDatabase.get_administrator_list() == False

        
        #test if method detect error during request execution
        with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.connect') as mockedDatabaseConnection:
            mockedDatabaseConnection.return_value = True
            self.homeDatabase.db_cursor = FakeFailCursorExecute()

            with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.get_profil_by_id') as mockeGettingProfilById:
                mockeGettingProfilById.return_value = Profil(1, "donovan", "maurice", "m", "26/09/1994")

                assert self.homeDatabase.get_administrator_list() == False

        
        #test if method during getting request answer
        with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.connect') as mockedDatabaseConnection:
            mockedDatabaseConnection.return_value = True
            self.homeDatabase.db_cursor = FakeFailCursorFetchall()

            with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.get_profil_by_id') as mockeGettingProfilById:
                mockeGettingProfilById.return_value = Profil(1, "donovan", "maurice", "m", "26/09/1994")

                assert self.homeDatabase.get_administrator_list() == False

        
        #test if method detect error during getting profil
        with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.connect') as mockedDatabaseConnection:
            mockedDatabaseConnection.return_value = True
            self.homeDatabase.db_cursor = FakeSuccesCursor()
            self.homeDatabase.db_cursor.list = [
                (1, 1, "admin", "inhabitant", "tetrew", "0000")]

            with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.get_profil_by_id') as mockeGettingProfilById:
                mockeGettingProfilById.return_value = False

                assert self.homeDatabase.get_administrator_list() == False


    def test_getting_profil_by_id(self):
        """
            1.test if method return good type of data
            2.test if method detect parametters error
            3.test if method detect database connection error
            4.test if method detect error during request execution
            5.test if method during getting request answer
        """

        #test if method return good type of data
        with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.connect') as mockedDatabaseConnection:
            mockedDatabaseConnection.return_value = True
            self.homeDatabase.db_cursor = FakeSuccesCursor()
            self.homeDatabase.db_cursor.list = [
                (1, "donovan", "maurice", "m", "26/09/1994")
            ]

            assert isinstance(self.homeDatabase.get_profil_by_id(1), Profil) == True


        #test if method detect parametters error
        with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.connect') as mockedDatabaseConnection:     
            mockedDatabaseConnection.return_value = True
            self.homeDatabase.db_cursor = FakeSuccesCursor()
            self.homeDatabase.db_cursor.list = [(1, "donovan", "maurice", "m", "26/09/1994")]

            assert self.homeDatabase.get_profil_by_id("1") == False


        #test if method detect database connection error
        with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.connect') as mockedDatabaseConnection:
            mockedDatabaseConnection.return_value = False
            self.homeDatabase.db_cursor = FakeSuccesCursor()
            self.homeDatabase.db_cursor.list = [(1, "donovan", "maurice", "m", "26/09/1994")]

            assert self.homeDatabase.get_profil_by_id(1) == False

        
        #test if method detect error during request execution
        with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.connect') as mockedDatabaseConnection:
            mockedDatabaseConnection.return_value = True
            self.homeDatabase.db_cursor = FakeFailCursorExecute()

            assert self.homeDatabase.get_profil_by_id(1) == False

        
        #test if method during getting request answer
        with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.connect') as mockedDatabaseConnection:
            mockedDatabaseConnection.return_value = True
            self.homeDatabase.db_cursor = FakeFailCursorFetchall()

            assert self.homeDatabase.get_profil_by_id(1) == False



    def test_adding_user(self):
        """
            1.test if method return True if succes
            2.test if method detect parametters error
            3.test if method detect error during adding profil
            4.test if method detect error during database connection
            5.test if method detect error during request execution
            6.test if method detect error durring getting lastrowId
            7.test if method detect error during committing change
            8.test if method detect new user not found in user list
        """

        #test if method return True if succes
        with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.add_profil') as mockedAddingProfil:
            mockedAddingProfil.return_value = 1
            
            with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.connect') as mockedDatabaseConnection:
                mockedDatabaseConnection.return_value = True

                self.homeDatabase.db_cursor = FakeSuccesCursor()

                with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.commit_change') as mockedCommitingChange:
                    mockedCommitingChange.return_value = True

                    with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.get_users_list') as mockedGettingUsersList:
                        mockedGettingUsersList.return_value = [Administrator(1, Profil(1, "donovan", "maurice", "m", "26/09/1994"), "tetrew" , "0000")]

                        assert self.homeDatabase.add_user("donovan", "maurice", "m", "26/09/1994", "admin", "inhabitant", "tetrew", "0000") == True


        #test if method detect parametters error
        assert self.homeDatabase.add_user(1, "maurice", "m", "26/09/1994", "admin", "inhabitant", "tetrew", "0000") == False
        assert self.homeDatabase.add_user("donovan", 1, "m", "26/09/1994", "admin", "inhabitant", "tetrew", "0000") == False
        assert self.homeDatabase.add_user("donovan", "maurice", 1, "26/09/1994", "admin", "inhabitant", "tetrew", "0000") == False
        assert self.homeDatabase.add_user("donovan", "maurice", "g", "26/09/1994", "admin", "inhabitant", "tetrew", "0000") == False
        assert self.homeDatabase.add_user("donovan", "maurice", "m", 1, "admin", "inhabitant", "tetrew", "0000") == False
        assert self.homeDatabase.add_user("donovan", "maurice", "m", "26/09/1994", 1, "inhabitant", "tetrew", "0000") == False
        assert self.homeDatabase.add_user("donovan", "maurice", "m", "26/09/1994", "random", "inhabitant", "tetrew", "0000") == False
        assert self.homeDatabase.add_user("donovan", "maurice", "m", "26/09/1994", "admin", 1, "tetrew", "0000") == False
        assert self.homeDatabase.add_user("donovan", "maurice", "m", "26/09/1994", "admin", "random", "tetrew", "0000") == False
        assert self.homeDatabase.add_user("donovan", "maurice", "m", "26/09/1994", "admin", "inhabitant", 1, "0000") == False
        assert self.homeDatabase.add_user("donovan", "maurice", "m", "26/09/1994", "admin", "inhabitant", "tetrew", 1) == False


        #test if method detect error during adding profil
        with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.add_profil') as mockedAddingProfil:
            mockedAddingProfil.return_value = False
            
            with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.connect') as mockedDatabaseConnection:
                mockedDatabaseConnection.return_value = True

                self.homeDatabase.db_cursor = FakeSuccesCursor()

                with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.commit_change') as mockedCommitingChange:
                    mockedCommitingChange.return_value = True

                    with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.get_users_list') as mockedGettingUsersList:
                        mockedGettingUsersList.return_value = [Administrator(1, Profil(1, "donovan", "maurice", "m", "26/09/1994"), "tetrew" , "0000")]

                        assert self.homeDatabase.add_user("donovan", "maurice", "m", "26/09/1994", "admin", "inhabitant", "tetrew", "0000") == False


        #test if method detect error during database connection
        with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.add_profil') as mockedAddingProfil:
            mockedAddingProfil.return_value = True
            
            with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.connect') as mockedDatabaseConnection:
                mockedDatabaseConnection.return_value = False

                self.homeDatabase.db_cursor = FakeSuccesCursor()

                with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.commit_change') as mockedCommitingChange:
                    mockedCommitingChange.return_value = True

                    with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.get_users_list') as mockedGettingUsersList:
                        mockedGettingUsersList.return_value = [Administrator(1, Profil(1, "donovan", "maurice", "m", "26/09/1994"), "tetrew" , "0000")]

                        assert self.homeDatabase.add_user("donovan", "maurice", "m", "26/09/1994", "admin", "inhabitant", "tetrew", "0000") == False


        #test if method detect error during request execution
        with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.add_profil') as mockedAddingProfil:
            mockedAddingProfil.return_value = True
            
            with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.connect') as mockedDatabaseConnection:
                mockedDatabaseConnection.return_value = True

                self.homeDatabase.db_cursor = FakeFailCursorExecute()

                with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.commit_change') as mockedCommitingChange:
                    mockedCommitingChange.return_value = True

                    with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.get_users_list') as mockedGettingUsersList:
                        mockedGettingUsersList.return_value = [Administrator(1, Profil(1, "donovan", "maurice", "m", "26/09/1994"), "tetrew" , "0000")]

                        assert self.homeDatabase.add_user("donovan", "maurice", "m", "26/09/1994", "admin", "inhabitant", "tetrew", "0000") == False


        #test if method detect error durring getting lastrowId
        with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.add_profil') as mockedAddingProfil:
            mockedAddingProfil.return_value = True
            
            with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.connect') as mockedDatabaseConnection:
                mockedDatabaseConnection.return_value = True

                self.homeDatabase.db_cursor = FakeFailCursorLastrowId()

                with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.commit_change') as mockedCommitingChange:
                    mockedCommitingChange.return_value = True

                    with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.get_users_list') as mockedGettingUsersList:
                        mockedGettingUsersList.return_value = [Administrator(1, Profil(1, "donovan", "maurice", "m", "26/09/1994"), "tetrew" , "0000")]

                        assert self.homeDatabase.add_user("donovan", "maurice", "m", "26/09/1994", "admin", "inhabitant", "tetrew", "0000") == False


        #test if method detect error during committing change
        with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.add_profil') as mockedAddingProfil:
            mockedAddingProfil.return_value = True
            
            with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.connect') as mockedDatabaseConnection:
                mockedDatabaseConnection.return_value = True

                self.homeDatabase.db_cursor = FakeSuccesCursor()

                with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.commit_change') as mockedCommitingChange:
                    mockedCommitingChange.return_value = False

                    with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.get_users_list') as mockedGettingUsersList:
                        mockedGettingUsersList.return_value = [Administrator(1, Profil(1, "donovan", "maurice", "m", "26/09/1994"), "tetrew" , "0000")]

                        assert self.homeDatabase.add_user("donovan", "maurice", "m", "26/09/1994", "admin", "inhabitant", "tetrew", "0000") == False


        #test if method detect new user not found in user list
        with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.add_profil') as mockedAddingProfil:
            mockedAddingProfil.return_value = True
            
            with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.connect') as mockedDatabaseConnection:
                mockedDatabaseConnection.return_value = True

                self.homeDatabase.db_cursor = FakeSuccesCursor()

                with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.commit_change') as mockedCommitingChange:
                    mockedCommitingChange.return_value = True

                    with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.get_users_list') as mockedGettingUsersList:
                        mockedGettingUsersList.return_value = []

                        assert self.homeDatabase.add_user("donovan", "maurice", "m", "26/09/1994", "admin", "inhabitant", "tetrew", "0000") == False


    def test_adding_profil(self):
        """
            1.test if method return True if succes
            2.test if method detect parametters error
            3.test if method detect error during database connection
            4.test if method detect error during request execution
            5.test if method detect error durring getting lastrowId
            6.test if method detect error during committing change
            7.test if method detect new profil not found in profil list
        """

        #test if method return True if succes
        with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.connect') as mockedDatabaseConnection:
            mockedDatabaseConnection.return_value = True

            self.homeDatabase.db_cursor = FakeSuccesCursor()

            with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.commit_change') as mockedCommitingChange:
                mockedCommitingChange.return_value = True

                with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.get_profils_list') as mockedGettingProfilsList:
                    mockedGettingProfilsList.return_value = [Profil(1, "donovan", "maurice", "m", "26/09/1994")]

                    assert self.homeDatabase.add_profil("donovan", "maurice", "m", "26/09/1994") == True

        #test if method detect parametters error
        assert self.homeDatabase.add_profil(1, "maurice", "m", "26/09/1994") == False
        assert self.homeDatabase.add_profil("donovan", 1, "m", "26/09/1994") == False
        assert self.homeDatabase.add_profil("donovan", "maurice", 1, "26/09/1994") == False
        assert self.homeDatabase.add_profil("donovan", "maurice", "g", "26/09/1994") == False
        assert self.homeDatabase.add_profil("donovan", "maurice", "m", 1) == False

        #test if method detect error during database connection
        with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.connect') as mockedDatabaseConnection:
            mockedDatabaseConnection.return_value = False

            self.homeDatabase.db_cursor = FakeSuccesCursor()

            with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.commit_change') as mockedCommitingChange:
                mockedCommitingChange.return_value = True

                with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.get_profils_list') as mockedGettingProfilsList:
                    mockedGettingProfilsList.return_value = [Profil(1, "donovan", "maurice", "m", "26/09/1994")]

                    assert self.homeDatabase.add_profil("donovan", "maurice", "m", "26/09/1994") == False


        #test if method detect error during request execution
        with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.connect') as mockedDatabaseConnection:
            mockedDatabaseConnection.return_value = True

            self.homeDatabase.db_cursor = FakeFailCursorExecute()

            with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.commit_change') as mockedCommitingChange:
                mockedCommitingChange.return_value = True

                with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.get_profils_list') as mockedGettingProfilsList:
                    mockedGettingProfilsList.return_value = [Profil(1, "donovan", "maurice", "m", "26/09/1994")]

                    assert self.homeDatabase.add_profil("donovan", "maurice", "m", "26/09/1994") == False


        #test if method detect error durring getting lastrowId
        with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.connect') as mockedDatabaseConnection:
            mockedDatabaseConnection.return_value = True

            self.homeDatabase.db_cursor = FakeFailCursorLastrowId()

            with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.commit_change') as mockedCommitingChange:
                mockedCommitingChange.return_value = True

                with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.get_profils_list') as mockedGettingProfilsList:
                    mockedGettingProfilsList.return_value = [Profil(1, "donovan", "maurice", "m", "26/09/1994")]

                    assert self.homeDatabase.add_profil("donovan", "maurice", "m", "26/09/1994") == False


        #test if method detect error during committing change
        with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.connect') as mockedDatabaseConnection:
            mockedDatabaseConnection.return_value = True

            self.homeDatabase.db_cursor = FakeSuccesCursor()

            with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.commit_change') as mockedCommitingChange:
                mockedCommitingChange.return_value = False

                with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.get_profils_list') as mockedGettingProfilsList:
                    mockedGettingProfilsList.return_value = [Profil(1, "donovan", "maurice", "m", "26/09/1994")]

                    assert self.homeDatabase.add_profil("donovan", "maurice", "m", "26/09/1994") == False


        #test if method detect new profil not found in profil list
        with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.connect') as mockedDatabaseConnection:
            mockedDatabaseConnection.return_value = True

            self.homeDatabase.db_cursor = FakeSuccesCursor()

            with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.commit_change') as mockedCommitingChange:
                mockedCommitingChange.return_value = True

                with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.get_profils_list') as mockedGettingProfilsList:
                    mockedGettingProfilsList.return_value = []

                    assert self.homeDatabase.add_profil("donovan", "maurice", "m", "26/09/1994") == False



    def test_checking_config_file_existence(self):
        """
            1.test if method return an bool
            2.test if method return true if succes
            3.test if method return false if error
        """
        
        open_mock = mock_open()
        with patch("builtins.open", open_mock, create=False):
            #test if method return an bool 
            assert isinstance(self.homeDatabase.check_config_file_existence(), bool) == True

            #test if method return true if succes
            assert self.homeDatabase.check_config_file_existence() == True

        #test if method return false if error
        open_mock.return_value = IOError()
        with patch("builtins.open", open_mock, create=False):
            assert self.homeDatabase.check_config_file_existence() == False


    def test_checking_database_connection(self):
        """
            1.test if method return true if succes
            2.test if method detect database error connection
            3.test if method detect error during execution
        """

        #test if method return true if succes
        with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.connect') as mockedDatabaseConnection:
            mockedDatabaseConnection.return_value = True

            with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.disconnect') as mockedDatabaseDisconnection:
                mockedDatabaseDisconnection.return_value = True

                assert self.homeDatabase.check_database_connection() == True


        #test if method detect database error connection
        with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.connect') as mockedDatabaseConnection:
            mockedDatabaseConnection.return_value = False

            with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.disconnect') as mockedDatabaseDisconnection:
                mockedDatabaseDisconnection.return_value = True

                assert self.homeDatabase.check_database_connection() == False

        with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.connect') as mockedDatabaseConnection:
            mockedDatabaseConnection.return_value = True

            with mock.patch('systemeDomotique.homeAutomationServer.classes.homeDatabase.HomeDatabase.disconnect') as mockedDatabaseDisconnection:
                mockedDatabaseDisconnection.return_value = False

                assert self.homeDatabase.check_database_connection() == False