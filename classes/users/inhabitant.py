from .user import *

class Inhabitant(User):
    '''
        class bringing all the information and functionality of an inhabitant

            attributes:
            	id: identifiant of the inhabitant
				profil: profil of the inhabitant
                grade: grade of the inhabitant (user/admin)
                role: role of the inhabitant (inhabitant)
                identifiant: identifiant of the inhabitant
                password: password of the inhabitant

            property:
                profilId: profil id of the user
                lastname: lastname of the user
                firstname: firstname of the user
                gender: gender of the user
                date of birth: date of birth of the user

            methods:
            	serialize (allows to transform the class in dict for json use)
    '''

    def __init__(self, id, profil, grade, identifiant, password):
        """constructor of the class"""
        User.__init__(self, id, profil, grade, 'inhabitant', identifiant, password)