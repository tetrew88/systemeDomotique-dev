import subprocess
import sys
import json
import os

from urllib import response


class DatabaseInstaller:
    """
        class bringing all the information and functionality of the database installer.

            Attributes:
                version
                script path (path of the main script (for files manipulation))
                database config file path

            Propertys:
                databaseConfigured: bolléan use for know if database was configured

            Methods:
                get_system_username: method used for collect the username of the system user (for sql interaction)
                get_system_user_password: method used for collect the password of the system use (for sql interaction)
                get_database_name: method used for collect the databaseName
                create_database_config_file: method used for create the database config file
                create_database: method used for create the database
                create_database_table: method used for create the database tables
                create_database_system_user: method used for create the user system in the database system
                attribute_user_system_privilege: method used for attribued all privilege on the database to the system user
                download_database_system: method used for dowload the database system
                check_database_config_file_existence: method used for checking the existence of the database config file
                check_database_existence: method used for checking the existence of an database
                check_database_user_existence: method used for checking the existence of an user in mysql system
                set_database_configuration_booleean_control: methode use for set booléen of configuration control in database config file

    """

    def __init__(self, scriptPath):
        self.version = '0.0.1'
        self.scriptPath = scriptPath
        self.databaseConfigFilePath = scriptPath + "/configs/databaseConfig.json"


    """PROPERTY"""
    @property
    def databaseConfigured(self):
        """
            bolléan use for know if database was configured 

            functioning:
                1.open config file
                2.collecte data dictionnary
                3.check if boolean was on true or false
                4.return result
                

            return:
                if database was configured return true
                else return false 
        """
        
        databaseConfigured = data = False

        #open config file
        try:
            with open(self.databaseConfigFilePath, 'r') as f:
                #collecte data dictionnary
                data = json.load(f)
        except:
            databaseConfigured = False
            data = False
            

        if data != False:
            #check if boolean was on true or false
            try:
                databaseConfigured = data['databaseConfigured']
            except:
                databaseConfigured = False
        else:
            databaseConfigured = False

        #return
        return databaseConfigured


    """METHODS"""
    """GET METHODS"""
    def get_system_username(self):
        """
            method used for collect the username of the system user

            functioning:
                1.collect the user system name
                    if user system name is empty:
                        attribute base user system name

                2.check conformity of the system username
                3.return

            return:
                if succes return system username
                else return False
        """

        systemUsername = ""
        succes = False

        #collect the user system name
        try:
            systemUsername = input("\nentrer le nom d'utilisateur: ")
        except:
            systemUsername = ""

        if systemUsername == "":
            #attribute base user system name
            systemUsername = "homeAutomationSystem"
        else:
            pass

        #check conformity of the system username
        if isinstance(systemUsername, str) and systemUsername != "":
            succes =  True
        else:
            succes = False

        #return
        if succes:
            return systemUsername
        else:
            return False


    def get_system_user_password(self):
        """
            method used for collect the password of the system user

            functioning:
                1.collect the user system password
                2.check conformity of the system password

            return:
                if succes return the system password
                else return False
        """

        succes = False
        systemPassword = ""

        #collect the user system password
        try:
            systemPassword = input("\nenter le mot de passe: ")
        except:
            systemPassword = ""

        #check conformity of the system password
        if isinstance(systemPassword, str) and systemPassword != "":
            succes = True
        else:
            succes = False

        #return
        if succes:
            return systemPassword
        else:
            return False


    def get_database_name(self):
        """
            method used for collect the databaseName

            functioning:
                1.collect the database name
                    if database name is empty:
                        attribute base database name

                2.check conformity of the database name

            return:
                if succes return databaseName
                else return False
        """

        succes = False
        databaseName = ""

        #collect the database name
        try:
            databaseName = input("\nentrer le nom de la base de donnée: ")
        except:
            databaseName = ""

        if databaseName == "":
            #attribute base database name
            databaseName = "Home"

        #check conformity of the database name
        if isinstance(databaseName, str) and databaseName != "":
            succes = True
        else:
            succes = False

        #return
        if succes:
            return databaseName
        else:
            return False



    """CREATE METHODS"""
    def create_database_config_file(self, systemUserName, systemUserPassword, databaseName, databaseConfigured):
        """
            method used for create the database config file

            functioning:
                1.check parametters conformity
                2.set the data dictionnary
                3.open/create database config file
                4.write data dictionnary in file
                5.return

            return:
                if succes return True
                else return False
        """

        succes = False
        data = {}

        #check parametters conformity
        if isinstance(systemUserName, str) and \
            isinstance(systemUserPassword, str) and \
                isinstance(databaseName, str) and \
                    isinstance(databaseConfigured, bool):

            #set the data dictionnary
            data["systemUserName"] = systemUserName
            data["systemUserPassword"] = systemUserPassword
            data["databaseName"] = databaseName
            data["databaseConfigured"] = databaseConfigured

            try:
                #open/create database config file
                with open(self.databaseConfigFilePath, 'w') as f:
                    #write data dictionnary in file
                    json.dump(data, f, indent=4)
                succes = True
            except:
                succes = False
        else:
            succes = False

        #return
        return succes


    def create_database(self, databaseName):
        """
            method used for create the database

            functioning:
                1.check parametter conformity
                2.create sql request for database creation
                3.create system request with the sql request
                4.execute system request with suprocess
                5.check subrocess return code
                    if error check if database already exist:
                        if she already exist set succes  on true
                6.check database existance
                7.return

            return:
                if succes return True
                else return False
        """

        succes = False
        sqlRequest = systemRequest = ""

        #check parametter conformity
        if isinstance(databaseName, str):
            #create sql request for database creation
            sqlRequest = "CREATE DATABASE {}".format(databaseName)
            #create system request with the sql request
            systemRequest = "sudo mysql -e '{}'".format(sqlRequest)

            #execute system request with suprocess
            try:
                proc = subprocess.Popen(systemRequest, shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, executable="/bin/bash")
                output, error = proc.communicate()
                proc.wait()

                #check subrocess return code
                if proc.returncode == 0:
                    succes = True
                else:
                    error = str(error).replace('\n', '')

                    #check if database already exist
                    if self.check_database_existence(databaseName):
                        #set succes on true
                        succes = True
                    else:
                        print("Erreur: {}".format(error.decode()))
                        succes = False
            except:
                succes = False

            #check database existance
            if self.check_database_existence(databaseName):
                succes = True
            else:
                succes = False
        else:
            succes = False

        #return
        return succes


    def create_database_table(self, databaseName):
        """
            method used for create the database tables

            functioning:
                1.check parametter conformity
                2.set the creating table file path
                3.set the system request for mysql table creation
                4.check creating table file existance
                5.check database existance
                6.execute system request with suprocess
                7.check subrocess return code
                8.return

            return:
                if succes return True
                else return False	
        """

        succes = False
        creationFileExist = databaseExist = False
        filePath = systemRequest = ""

        #check parametter conformity
        if isinstance(databaseName, str):
            #set the creating table file path
            filePath = self.scriptPath + '/configs/createHomeDatabase.sql'
            #set the system request for mysql table creation
            systemRequest = "sudo mysql {} < {}".format(databaseName, filePath)

            #check creating table file existance
            if os.path.exists(filePath):
                creationFileExist = True
            else:
                creationFileExist = False

            #check database existance
            if self.check_database_existence(databaseName):
                databaseExist = True
            else:
                databaseExist = False
            
            if creationFileExist and databaseExist:
                #execute system request with suprocess
                try:
                    proc = subprocess.Popen(systemRequest, shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, executable="/bin/bash")
                    output, error = proc.communicate()
                    proc.wait()

                    #check subrocess return code
                    if proc.returncode == 0:
                        succes = True
                    else:
                        error = str(error).replace('\n', '')
                        print("Erreur: {}".format(error))
                        succes = False
                except:
                    succes = False
            else:
                succes = False
        else:
            succes = False

        #return
        return succes


    def create_database_system_user(self, username, userPassword):
        """
            method used for create the user system in the database system

            functioning:
                1.check parametter conformity
                2.create sql user creation request
                3.create system request with user creation request
                4.execute system request with suprocess
                5.check subrocess return code
                    if error check if user already exist:
                        if he already exist set succes on true
                        else set succes on False
                6.check user existance
                7.return

            return:
                if succes return True
                else return False
        """

        succes = False
        userCreationRequest = systemRequest = ""

        #check parametter conformity
        if isinstance(username, str) and isinstance(userPassword, str):
            #create sql user creation request
            userCreationRequest = "CREATE USER '{}'@'localhost' IDENTIFIED BY '{}'".format(username, userPassword)
            #create system request with user creation request
            systemRequest = 'sudo mysql -e "{}"'.format(userCreationRequest)

            #execute system request with suprocess
            try:
                proc = subprocess.Popen(systemRequest, shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, executable="/bin/bash")
                output, error = proc.communicate()
                proc.wait()

                #check subrocess return code
                if proc.returncode == 0:
                    succes = True
                else:
                    #check if user already exist
                    if self.check_database_user_existence(username):
                        succes = True
                    else:
                        print("Erreur: {}".format(error))
                        succes = False
            except:
                succes = False

            #check user existance
            if self.check_database_user_existence(username):
                succes = True
            else:
                print("Erreur: {}".format(error))
                succes = False
        else:
            succes = False
        
        #return
        return succes



    """ATTRIBUTION METHODS"""
    def attribute_user_system_privilege(self, username, databaseName):
        """
            method used for attribued all privilege on the database to the system user

            functioning:
                1.check parametter conformity
                2.create sql attribution request
                3.create actualisation privilege request
                4.create system request with attribution request
                5.checking user existance
                6.checking database existance
                7.execute system request with subprocess
                8.check subprocess return code
                9.actualize mysql users privilege whith subprocess
                10.check subprocess return code
                11.return

            return:
                if succes return True
                else return False
        """

        succes = userExist = databaseExist = privilegAttribued = False
        attributionRequest = actualizePrivilegeRequest = systemRequest = ""

        #check parametter conformity
        if isinstance(username, str) and isinstance(databaseName, str):
            #create sql attribution request
            attributionRequest = "GRANT ALL PRIVILEGES ON {}.* TO '{}'@'localhost'".format(databaseName, username)
            #create actualisation privilege request
            actualizePrivilegeRequest = "sudo mysql -e 'FLUSH PRIVILEGES'".format(attributionRequest)

            #create system request with attribution request
            systemRequest = "sudo mysql -e '{}'".format(attributionRequest)

            #checking user existance
            if self.check_database_user_existence(username):
                userExist = True
            else:
                userExist = False

            #checking database existance
            if self.check_database_existence(databaseName):
                databaseExist = True
            else:
                databaseExist = False

            if userExist and databaseExist:
                #execute system request with subprocess
                try:
                    proc = subprocess.Popen(systemRequest, shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, executable="/bin/bash")
                    output, error = proc.communicate()
                    proc.wait()

                    #check subprocess return code
                    if proc.returncode == 0:
                        privilegAttribued = True
                    else:
                        print("Erreur: {}".format(error.decode()))
                        privilegAttribued = False
                except:
                    privilegAttribued = False

                if privilegAttribued:
                    #actualize mysql users privilege whith subprocess
                    try:
                        proc = subprocess.Popen(actualizePrivilegeRequest, shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, executable="/bin/bash")
                        output, error = proc.communicate()
                        proc.wait()

                        #check subprocess return code
                        if proc.returncode == 0:
                            succes = True
                        else:
                            print("Erreur: {}".format(error.decode()))
                            succes = False
                    except:
                        succes = False
                else:
                    succes = False
            else:
                succes = False
        else:
            succes = False

        #return
        return succes



    """DOWNLOAD METHODS"""
    def download_database_system(self):
        """
            method used for dowload the database system

            functioning:
                1.create system request
                2.execute system request with subprocess
                3.check subprocess return code
                4.return

            return:
                if succes return True
                else return False
        """

        succes = False

        #create system request
        systemRequest = 'sudo apt-get install -y mariadb-server'

        #execute system request with subprocess
        try:
            proc = subprocess.Popen(systemRequest, shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, executable="/bin/bash")
            output, error = proc.communicate()
            proc.wait()

            #check subprocess return code
            if proc.returncode == 0:
                succes = True
            else:
                print("Erreur: {}".format(error.decode()))
                succes = False
        except:
            succes = False

        #return
        return succes


    """CHECKING METHODS"""
    def check_database_config_file_existence(self):
        """
            method used for checking the existence of the database config file

            functioning:
                1.try to open the file

            return:
                if file exist return True
                else return False
        """

        succes = False

        try:
            #try openning file
            with open(self.databaseConfigFilePath, "r"):
                succes = True
        except:
            succes = False

        #return
        return succes


    #checking if database exist
    def check_database_existence(self, databaseName):
        """
            method used for checking the existence of an database

            functioning:
                1.check parametters conformity
                2.create sql checking request
                3.create system request with cheking request
                4.execute system request with subprocess
                5.check subprocess return code
                6.return

            return:
                if database exist return True
                else return False
        """
        
        succes = False
        checkingRequest = request = ""

        #check parametters conformity
        if isinstance(databaseName, str):
            #create sql checking request
            checkingRequest = 'SHOW DATABASES LIKE "{}"'.format(databaseName)
            #create system request with cheking request
            request = "sudo mysql -e '{}'".format(checkingRequest)

            #execute system request with subprocess
            try:
                proc = subprocess.Popen(request, shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, executable="/bin/bash")
                output, error = proc.communicate()
                proc.wait()

                #check subprocess return code
                if proc.returncode == 0:
                    if output != b'':
                        succes = True
                    else:
                        succes = False
                else:
                    print("Erreur: {}".format(error.decode()))
                    succes = False
            except:
                succes = False
        else:
            succes = False

        #return
        return succes


    #checking database user existence
    def check_database_user_existence(self, username):
        """
            method used for checking the existence of an user in mysql system

            functioning:
                1.check parametter conformity
                2.create sql checking request
                3.create system request with checking request
                4.execute system request with subprocess
                5.check subprocess return code
                6.check response
                7.return

            return:
                if user exist return True
                else return False
        """

        succes = False
        checkingRequest = systemRequest = ""

        #check parametter conformity
        if isinstance(username, str):
            #create sql checking request
            checkingRequest = 'SELECT * FROM mysql.user WHERE user = "{}"'.format(username)
            #create system request with checking request
            systemRequest = "sudo mysql -e '{}'".format(checkingRequest)

            try:
                #execute system request with subprocess
                proc = subprocess.Popen(systemRequest, shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, executable="/bin/bash")
                output, error = proc.communicate()
                proc.wait()

                #check subprocess return code
                if proc.returncode == 0:
                    #check response
                    if output != b'':
                        succes = True
                    else:
                        succes = False
                else:
                    print("Erreur: {}".format(error))
                    succes = False
            except:
                succes = False
        else:
            succes = False

        #return
        return succes



    """SET METHODS"""
    def set_database_configuration_booleean_control(self, value):
        """
            methode use for set booléen of configuration control in database config file

            functioning:
                1.check if value is an booleean
                2.open config file
                3.collecte data dictionnary
                4.set booléen on value
                5.return

            return:
                if succes return true
                else return false 
        """
        
        succes = data = False

        #check if value is an booleean
        if isinstance(value, bool):
            #open config file
            try:
                with open(self.databaseConfigFilePath, 'r') as f:
                    #collecte data dictionnary
                    data = json.load(f)
            except:
                succes = False

            if data != False:
                try:
                    #set booléen on value
                    data['databaseConfigured'] = value
                    #open config file
                    try:
                        with open(self.databaseConfigFilePath, 'w') as f:
                            #write data dictionnary in file
                            json.dump(data, f, indent=4)
                            succes = True
                    except:
                        succes = False
                except:
                    succes = False
            else:
                succes = False
        else:
            succes = False

        #return
        return succes
