#!/usr/bin/python3

import json

#socket io import/initialisation (for network interaction)
import eventlet
import socketio

socketIoServer = socketio.Server(cors_allowed_origins="*")
app = socketio.WSGIApp(socketIoServer, object)



class HomeAutomationSystem(socketio.Namespace):
	"""
		class bringing all the information and functionality of the system.

			Attributes:
				version
				running (control boolean to know if the system is in working order)

				home database (class used for interact with the home database)

			Propertys:

			Methods:
				start (allows to start the system)
				stop (allows to stop the system)

				listen request (listen and respond to (interface, assistant, ...) requests)
				run (basic functionement of the system (check temperature, check presence, ...)
	"""


    def __init__(self):
    	socketio.Namespace.__init__(self, '/HomeAutomationSystem')

    	self.version = 0.0.1
		self.running = False
		self.home = False