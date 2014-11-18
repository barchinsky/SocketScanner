import ConfigParser
import os

class ConfigManager():
	def __init__(self):
		self.config = ConfigParser.RawConfigParser()
		self.config.read('conf/configs.cfg')

		if not os.path.isfile('conf/configs.cfg'):
			self.createConfFile()

	def getConfFilePath(self):
		dirname = os.path.dirname(__file__)
		if dirname == "src":
			return '../conf/configs.cfg'
		else:
			return '/home/max/TF/NetworkManagmentTool/conf/configs.cfg'

	def createConfFile(self):
		#create config file
		self.config.add_section('logging')
		#self.config.set('logging', 'log_lvl', '/data/xml/device_info.xml')
		#self.config.set('logging', 'format', '')
		self.config.add_section('server')
		self.config.set('server', 'ip', 'localhost')
		self.config.set('server', 'port', '54500')
		self.config.set('server','storage','data/OpenPorts')
		self.config.add_section('client')
		self.config.set('client','ip','localhost')
		
		with open('conf/configs.cfg', 'wb') as configfile:
			self.config.write(configfile)

	def getClientIp(self):
		return self.config.get('client','ip')

	def getSaveFile(self):
		return self.config.get('server','storage')
