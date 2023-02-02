from .user import *

class Guest(User):
    '''
        class bringing all the information and functionality of an guest

            attributes:
            	id: identifiant of the guest
				profil: profil of the guest
                grade: grade of the guest (user/admin)
                role: role of the guest (guest)
                identifiant: identifiant of the guest
                password: password of the guest

            property:
                profilId: profil id of the user
                lastname: lastname of the user
                firstname: firstname of the user
                gender: gender of the user
                date of birth: date of birth of the user

            methods:
            	serialize (allows to transform the class in dict for json use)
    '''

    def __init__(self, id, profil, identifiant, password):
        """constructor of the class"""
        User.__init__(self, id, profil, "user", 'guest', identifiant, password)