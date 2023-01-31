import sys

sys.path.append("..")

from systemeDomotique.homeAutomationServer.classes.users.user import *
from systemeDomotique.homeAutomationServer.classes.users.profil import *

class Test_user:

    user = User(1, Profil( 1, "donovan","maurice", "m", "26/09/1994"), "admin", "inhabitant", "tetrew", "0000")


    def test_profilId_property(self):
        assert self.user.profilId == 1


    def test_lastName_property(self):
        assert self.user.lastName == "maurice"


    def test_firstName_property(self):
        assert self.user.firstName == "donovan"


    def test_gender_property(self):
        assert self.user.gender == "m"


    def test_dateOfBirth_property(self):
        assert self.user.dateOfBirth == "26/09/1994"