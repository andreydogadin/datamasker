import sys
import argparse
import configparser 

class Setting(object):
	dbtype = ''
	host = ''
	port = ''
	user = ''
	password = ''
	dbname = ''
	tablename = ''
	fieldname = ''
	fieldidname = ''
	algorithm = ''
	extraparam = ''
	alwaysyes = ''

	def __init__(self, dbtype, host, port, user, password, dbname, tablename, fieldidname, fieldname, algorithm, extraparam, alwaysyes):
		self.dbtype = dbtype
		self.host = host
		self.port = port
		self.user = user
		self.password = password
		self.dbname = dbname
		self.tablename = tablename
		self.fieldname = fieldname
		self.fieldidname = fieldidname
		self.algorithm = algorithm
		self.extraparam = extraparam
		self.alwaysyes = alwaysyes

	def put_defauls(self):
		if not self.host:
			self.host = "localhost"
		if not self.port and self.dbtype == "mysql":
			self.port = 3306
		if not self.port and self.dbtype == "postgresql":
			self.port = 5432

def get_args():
	parser = argparse.ArgumentParser(description='Description of your program', add_help=False)
	parser.add_argument('-d','--dbtype', help='Description for foo argument', required=True)
	parser.add_argument('-h','--host', help='Description for bar argument', required=False)
	parser.add_argument('-o','--port', help='Description for bar argument', required=False)
	parser.add_argument('-u','--user', help='Description for bar argument', required=False)
	parser.add_argument('-p','--password', help='Description for bar argument', required=False)
	parser.add_argument('-f','--file', help='Description for bar argument', required=True)
	parser.add_argument('-y','--yes', help='Description for bar argument', required=False, action='store_true')
	return vars(parser.parse_args())

def get_settings():
	args = get_args()
	Config = configparser.ConfigParser()
	Config.read(args['file'])
	settings = []
	for section in Config.sections():
		dbname = Config.get(section, 'dbname')
		tablename = Config.get(section, 'tablename')
		fieldidname = Config.get(section, 'fieldidname')
		fieldname = Config.get(section, 'fieldname')
		algorithm = section
		extraparam = Config.get(section, 'extraparam')
		setting = Setting(args['dbtype'], args['host'], args['port'], args['user'], args['password'], dbname, tablename, fieldidname, fieldname, algorithm, extraparam, args['yes'])
		setting.put_defauls()
		settings.append(setting)
	return settings