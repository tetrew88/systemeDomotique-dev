class Home:
	"""
		class bringing all the information and functionality of the system.

			Attributes:
				home database (class used for interact with the home database)
				home automation network (class used for interact with the zwave network and zwave module)

			Propertys:

			Methods:
	"""


	def __init__(self):
		self.homeDatabase = False
		self.homeAutomationNetwork = False