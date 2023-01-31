import subprocess
import re
import json
import getpass


class HomeAutomationSystemInstaller:

    def __init__(self, scriptPath):
        """constructor of the class"""
        self.scriptPath = scriptPath
        self.homeAutomationSystemConfigFilePath = scriptPath + "/configs/homeAutomationSystemConfig.json"


    @property
    def homeAutomationSystemConfigured(self):
        """
            bolléan use for know if home automation system was configured 

            functioning:
                1.open config file
                2.collecte data dictionnary
                3.check if boolean was on true or false
                4.return result
                

            return:
                if home automation system was configured return true
                else return false 
        """
        
        systemConfigured = data = False

        #open config file
        try:
            with open(self.homeAutomationSystemConfigFilePath, 'r') as f:
                #collecte data dictionnary
                data = json.load(f)
        except:
            systemConfigured = False
            

        if data != False:
            #check if boolean was on true or false
            try:
                systemConfigured = data['systemConfigured']
            except:
                systemConfigured = False
        else:
            systemConfigured = False

        #return
        return systemConfigured

    
    """METHODS"""
    """GET METHOD"""
    def get_zwave_controller_path(self):
        """
            method used for collect the path of the zwave controller

            functioning:
                1.collect the path
                2.check if path exist
                3.return

            return:
                if succes return path of the controller
                else return False
        """

        zwaveControllerPath = ""
        pathExist = False

        #collect the path
        zwaveControllerPath = input("\nentrer le chemin vers le controller zwave(ex: /dev/ttyACM0): ")

        try:
            with open(zwaveControllerPath, 'r') as f:
                pathExist = True
        except:
            print("controller introuvable")
            pathExist = False

        if pathExist:
            return zwaveControllerPath
        else:
            return False


    def get_zwave_config_folder_path(self):
        """
            method used for collect the path of the zwave config folder

            functioning:
                1.create system request
                2.execute system request with subprocess
                3.check subprocess return code
                4.return

            return:
                if succes return path of the zwave config file
                else return False
        """

        #create system request
        searchRequest = "find /home -name ozw_config"
        zwaveConfigFolderPath = ""
        succes = False

        try:
            #execute system request with subprocess
            proc = subprocess.Popen(searchRequest, shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, executable="/bin/bash")
            output, error = proc.communicate()
            proc.wait()


            #check subprocess return code
            if proc.returncode == 0:
                zwaveConfigFolderPath = output.decode()
            else:
                error = str(error.decode()).replace('\n', '')
                zwaveConfigFolderPath = ""

            if zwaveConfigFolderPath != "":
                succes = True
            else:
                succes = False
        except:
            succes = False

        if succes:
            return zwaveConfigFolderPath
        else:
            return False



    """DOWNLOAD METHODS"""
    def download_nginx(self):
        """
            method used for dowload nginx

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
        systemRequest = ""

        #create system request
        systemRequest = 'sudo apt-get install -y nginx'

        try:
            #execute system request with subprocess
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


    def dowload_supervisor(self):
        """
            method used for dowload supervisor

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
        systemRequest = 'sudo apt-get install -y supervisor'

        try:
            #execute system request with subprocess
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



    """CREATE METHODS"""
    def create_home_automation_system_config_file(self, zwaveControllerPath, zWaveConfigFolderPath, systemConfigured):
        """
            method used for create the home automation system config file

            functioning:
                1.set the data dictionnary
                2.open/create home automation system config file
                3.write data dictionnary in file
                4.return

            return:
                if succes return True
                else return False
        """

        succes = False
        data = {}

        if isinstance(zwaveControllerPath, str) and \
            isinstance(zWaveConfigFolderPath, str) and \
                isinstance(systemConfigured, bool):
            #set the data dictionnary
            data["zwaveControllerPath"] = zwaveControllerPath
            data["assignedZwaveControllerPath"] = "/dev/ttyUSB_CONTROLLER"
            data["zWaveConfigFolderPath"] = zWaveConfigFolderPath
            data["systemConfigured"] = systemConfigured

            try:
                #open/create database config file
                with open(self.homeAutomationSystemConfigFilePath, 'w') as f:
                    #write data dictionnary in file
                    json.dump(data, f, indent=4)
                succes = True
            except:
                succes = False
        else:
            succes = False

        #return
        return succes


    def create_nginx_config_file(self):
        """
            method used for create the nginx config file

            functioning:
                1.collect the ip of the rpi
                2.copy the base config file used for example
                3.modify data of the new file
                4.moved the file to the nginx site enabled folder
                5.create a link to the file in the nginx site avaiable folder
                6.return

            return:
                if succes return True
                else return False
        """

        succes = fileCopied = systemIP = baseConfigFileExist = fileMoved = False
        fileContent = nginxConfigFileCreated = linkFileCreated = False

        NginxBaseConfigFilePath = self.scriptPath + "/configs/nginxBaseConfig.txt"
        newNginxConfigFilePath = self.scriptPath + "/configs/newNginxConfig"


        interfacePath = self.scriptPath + "/webInterface/"

        copyRequest = "cp {} {}".format(NginxBaseConfigFilePath, newNginxConfigFilePath)

        try:
            #collect the ip of the rpi
            proc = subprocess.Popen("hostname -I", shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, executable="/bin/bash")
            output, error = proc.communicate()
            proc.wait()

            if proc.returncode == 0:
                systemIP = output.decode().split(" ")[0]
            else:
                error = str(error).replace('\n', '')
                systemIP = False
        except:
            systemIP = False

        try:
            with open(NginxBaseConfigFilePath, "r") as f:
                pass
            baseConfigFileExist = True

        except:
            baseConfigFileExist = False

        if systemIP and baseConfigFileExist:
            try:
                #copy the base config file used for example
                proc = subprocess.Popen(copyRequest, shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, executable="/bin/bash")
                output, error = proc.communicate()
                proc.wait()

                if proc.returncode == 0:
                    fileCopied = True
                else:
                    error = error.decode().replace('\n', '')
                    print(error)
                    fileCopied = False
            except:
                fileCopied = False

            if fileCopied:
                try:
                    with open(NginxBaseConfigFilePath, "r") as f:
                        fileContent = f.read()
                except:
                    fileContent = False

                if fileContent:
                    #modify data of the new file
                    fileContent = fileContent.replace("IP_DU_RPI", systemIP)
                    fileContent = fileContent.replace("INTERFACE_PATH", interfacePath)

                    try:
                        with open(newNginxConfigFilePath, "w") as f:
                            f.write(fileContent)

                        nginxConfigFileCreated = True
                    except:
                        nginxConfigFileCreated = False

                    if nginxConfigFileCreated:
                        try:
                            #moved the file to the nginx site enabled folder
                            proc = subprocess.Popen("sudo mv -f {} {}".format(newNginxConfigFilePath, "/etc/nginx/sites-available/homeAutomationSystem"), shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, executable="/bin/bash")
                            output, error = proc.communicate()
                            proc.wait()

                            if proc.returncode == 0:
                                fileMoved = True
                            else:
                                error = error.decode()
                                fileMoved = False
                        except:
                            fileMoved = Fale

                        if fileMoved:
                            try:
                                #create a link to the file in the nginx site avaiable folder
                                proc = subprocess.Popen("sudo ln -s /etc/nginx/sites-available/homeAutomationSystem /etc/nginx/sites-enabled", shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, executable="/bin/bash")
                                output, error = proc.communicate()
                                proc.wait()

                                if proc.returncode == 0:
                                    linkFileCreated = True
                                else:
                                    error = error.decode()
                                    if "Le fichier existe" in error:
                                        linkFileCreated = True
                                    else:
                                        linkFileCreated = False
                            except:
                                linkFileCreated = False
                        else:
                            succes = False
                    else:
                        succes = False
                else:
                    succes = False
            else:
                succes = False
        else:
            succes = False

        if linkFileCreated:
            succes = True
        else:
            succes = False

        return succes


    def create_web_interface_supervisor_config_file(self):
        """
            method used for create the nginx config file

            functioning:
                1.copy the base config file used for example
                2.modify data of the new file
                3.moved the file to the supervisor conf.d folder
                4.return

            return:
                if succes return True
                else return False
        """

        succes = fileCopied = baseConfigFileExist = fileMoved = supervisorConfigFileCreated = False
        command = "python3 manage.py runserver"
        username = getpass.getuser()
        directory = self.scriptPath + "/webInterface"

        supervisorBaseConfigFilePath = self.scriptPath + "/configs/supervisorBaseConfig.txt"
        newSupervisorConfigFilePath = self.scriptPath + "/configs/newSupervisorConfig"

        copyRequest = "cp {} {}".format(supervisorBaseConfigFilePath, newSupervisorConfigFilePath)

        try:
            with open(supervisorBaseConfigFilePath, "r") as f:
                pass
            baseConfigFileExist = True

        except:
            baseConfigFileExist = False


        if baseConfigFileExist:
            try:
                #copy the base config file used for example
                proc = subprocess.Popen(copyRequest, shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, executable="/bin/bash")
                output, error = proc.communicate()
                proc.wait()

                if proc.returncode == 0:
                    fileCopied = True
                else:
                    error = error.decode().replace('\n', '')
                    print(error)
                    fileCopied = False
            except:
                fileCopied = False

            if fileCopied:
                try:
                    with open(supervisorBaseConfigFilePath, "r") as f:
                        fileContent = f.read()
                except:
                    fileContent = False

                if fileContent:
                    #modify data of the new file
                    fileContent = fileContent.replace("COMMAND", command)
                    fileContent = fileContent.replace("USERNAME", username)
                    fileContent = fileContent.replace("PATH_TO_APPLICATION", directory)

                    try:
                        with open(newSupervisorConfigFilePath, "w") as f:
                            f.write(fileContent)

                        supervisorConfigFileCreated = True
                    except:
                        supervisorConfigFileCreated = False

                    if supervisorConfigFileCreated:
                        try:
                            #moved the file to the supervisor conf.d folder
                            proc = subprocess.Popen("sudo mv -f {} {}".format(newSupervisorConfigFilePath, "/etc/supervisor/conf.d/homeAutomationInterface.conf"), shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, executable="/bin/bash")
                            output, error = proc.communicate()
                            proc.wait()

                            if proc.returncode == 0:
                                fileMoved = True
                            else:
                                error = error.decode()
                                fileMoved = False
                        except:
                            fileMoved = False
                    else:
                        succes = False
                else:
                    succes = False
            else:
                succes = False
        else:
            succes = False

        if fileMoved:
            succes = True
        else:
            succes = False

        return succes


    def create_automation_server_supervisor_config_file(self):
        """
            method used for create the nginx config file

            functioning:
                1.copy the base config file used for example
                2.modify data of the new file
                3.moved the file to the supervisor conf.d folder
                4.return

            return:
                if succes return True
                else return False
        """

        succes = fileCopied = baseConfigFileExist = fileMoved = supervisorConfigFileCreated = False
        command = "python3 main.py"
        username = getpass.getuser()
        directory = self.scriptPath

        supervisorBaseConfigFilePath = self.scriptPath + "/configs/supervisorBaseConfig.txt"
        newSupervisorConfigFilePath = self.scriptPath + "/configs/newSupervisorConfig"

        copyRequest = "cp {} {}".format(supervisorBaseConfigFilePath, newSupervisorConfigFilePath)

        try:
            with open(supervisorBaseConfigFilePath, "r") as f:
                pass
            baseConfigFileExist = True

        except:
            baseConfigFileExist = False

        if baseConfigFileExist:
            try:
                #copy the base config file used for example
                proc = subprocess.Popen(copyRequest, shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, executable="/bin/bash")
                output, error = proc.communicate()
                proc.wait()

                if proc.returncode == 0:
                    fileCopied = True
                else:
                    error = error.decode().replace('\n', '')
                    print(error)
                    fileCopied = False
            except:
                fileCopied = False

            if fileCopied:
                try:
                    with open(supervisorBaseConfigFilePath, "r") as f:
                        fileContent = f.read()
                except:
                    fileContent = False

                if fileContent:
                    #modify data of the new file
                    fileContent = fileContent.replace("COMMAND", command)
                    fileContent = fileContent.replace("USERNAME", username)
                    fileContent = fileContent.replace("PATH_TO_APPLICATION", directory)

                    try:
                        with open(newSupervisorConfigFilePath, "w") as f:
                            f.write(fileContent)

                        supervisorConfigFileCreated = True
                    except:
                        supervisorConfigFileCreated = False

                    if supervisorConfigFileCreated:
                        try:
                            #moved the file to the supervisor conf.d folder
                            proc = subprocess.Popen("sudo mv -f {} {}".format(newSupervisorConfigFilePath, "/etc/supervisor/conf.d/automationServer.conf"), shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, executable="/bin/bash")
                            output, error = proc.communicate()
                            proc.wait()

                            if proc.returncode == 0:
                                fileMoved = True
                            else:
                                error = error.decode()
                                fileMoved = False
                        except:
                            fileMoved = False
                    else:
                        succes = False
                else:
                    succes = False
            else:
                succes = False
        else:
            succes = False

        if fileMoved:
            succes = True
        else:
            succes = False

        return succes



    """ASSIGNATION METHODS"""
    def assign_fixed_usb_port_names_to_controller(self, controllerPath): 
        """
            method used for assigned an fix name to the controller

            functioning:
                1.get controller vendor id
                2.get controller product id
                3.create assignation file with controller information
                4.move file to /etc/udev/
                5.reload udev rules
                6.return

            return:
                if succes return True
                else return False
        """

        getVendorIdRequest = "udevadm info --name={} --attribute-walk | grep -m 1 ATTRS{}".format(controllerPath, '{idVendor}')
        getProductIdRequest = "udevadm info --name={} --attribute-walk | grep -m 1 ATTRS{}".format(controllerPath, '{idProduct}')

        assignationRequest = ""
        refreshRequest = "sudo udevadm trigger"

        ruleFilePath = self.scriptPath + "/10-usb-serial.rules"

        vendorId = productId = nameAssigned = False

        if isinstance(controllerPath, str):
            #get controller vendor id
            try:
                proc = subprocess.Popen(getVendorIdRequest, shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, executable="/bin/bash")
                output, error = proc.communicate()
                proc.wait()

                if proc.returncode == 0:
                    vendorId = re.findall('"(.*?)"', output.decode().replace(" ", ""))[0]
                else:
                    error = str(error).replace('\n', '')
                    vendorId = False
            except:
                vendorId = False

            #get controller product id
            try:
                proc = subprocess.Popen(getProductIdRequest, shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, executable="/bin/bash")
                output, error = proc.communicate()
                proc.wait()

                #check subrocess return code
                if proc.returncode == 0:
                    productId = re.findall('"(.*?)"', output.decode().replace(" ", ""))[0]
                else:
                    error = str(error).replace('\n', '')
                    productId = False
            except:
                prouctId = False

            if productId and vendorId:
                #create assignation file with controller information
                assignationRequest = 'SUBSYSTEM=="tty", ATTRS{}=="{}", ATTRS{}=="{}", SYMLINK+="ttyUSB_CONTROLLER"'.format("{idProduct}", productId, "{idVendor}", vendorId)
                try:
                    with open(ruleFilePath, "w") as f:
                        f.write(assignationRequest)

                    moveRequest = "sudo mv -f " + ruleFilePath + " /etc/udev/rules.d/10-usb-serial.rules"

                    #move file to /etc/udev/
                    try:
                        proc = subprocess.Popen(moveRequest, shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, executable="/bin/bash")
                        output, error = proc.communicate()
                        proc.wait()

                        #check subrocess return code
                        if proc.returncode == 0:
                            nameAssigned = True
                        else:
                            nameAssigned = False
                    except:
                        nameAssigned = False

                except Exception as error:
                    print(error)
                    nameAssigned = False

                if nameAssigned:
                    #reload udev rules
                    try:
                        proc = subprocess.Popen(refreshRequest, shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, executable="/bin/bash")
                        output, error = proc.communicate()
                        proc.wait()

                        #check subrocess return code
                        if proc.returncode == 0:
                            succes=True
                        else:
                            succes = False
                    except:
                        succes = False
                else:
                    succes = False
            else:
                succes = False
        else:
            succes = False

        return succes



    """SET METHODS"""
    def set_home_automation_system_configuration_booleean_control(self, value):
        """
            method used for set booléen of configuration control in hoe automation system config file

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
                with open(self.homeAutomationSystemConfigFilePath, 'r') as f:
                    #collecte data dictionnary
                    data = json.load(f)
            except:
                succes = False

            if data != False:
                try:
                    #set booléen on value
                    data['systemConfigured'] = value
                    #open config file
                    try:
                        with open(self.homeAutomationSystemConfigFilePath, 'w') as f:
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
