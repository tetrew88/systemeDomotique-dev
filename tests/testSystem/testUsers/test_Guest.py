import sys

sys.path.append("..")

from systemeDomotique.homeAutomationServer.classes.users.guest import *
from systemeDomotique.homeAutomationServer.classes.users.profil import *

class Test_guest:

    guest = Guest(1, Profil( 1, "donovan","maurice", "m", "26/09/1994"), "tetrew", "0000")


    def test_profilId_property(self):
        assert self.guest.profilId == 1


    def test_lastName_property(self):
        assert self.guest.lastName == "maurice"


    def test_firstName_property(self):
        assert self.guest.firstName == "donovan"


    def test_gender_property(self):
        assert self.guest.gender == "m"


    def test_dateOfBirth_property(self):
        assert self.guest.dateOfBirth == "26/09/1994"