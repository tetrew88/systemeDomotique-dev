from .inhabitant import *

class Administrator(Inhabitant):
    '''
        class bringing all the information and functionality of an administator

            attributes:
            	id: identifiant of the administrator
				profil: profil of the administrator
                grade: grade of the administrator (admin)
                role: role of the administrator (inhabitant)
                identifiant: identifiant of the administrator
                password: password of the administrator

            property:
                profilId: profil id of the user
                lastname: lastname of the user
                firstname: firstname of the user
                gender: gender of the user
                date of birth: date of birth of the userssssss

            methods:
            	serialize (allows to transform the class in dict for json use)
    '''

    def __init__(self, id, profil, identifiant, password):
        """constructor of the class"""
        Inhabitant.__init__(self, id, profil, "admin", identifiant, password)