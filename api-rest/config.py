# Database
DATABASE = {
	'general': {
		'type': 'postgresql',
		'host': 'localhost',
		'dbname': 'survi_prevention',
		'username': 'postgres',
		'password': 'postgres',
	}
}

PERMISSION = {
	'systemID': '2d9f85c6-c41b-4b53-b391-9caa31bb3494',
}

LOGS_NAME = 'webservice'

IS_DEV = True
USE_UWSGI = False
MINIMIZE_JS = False

# Folder
WEBROOT = '/'
SEND_EMAIL_FROM = 'michael.jolin@cauca.ca'

# Web
PACKAGE_NAME = "API-SURVI-Prevention"
CAUSEJS = "stdev.cauca.ca"
VERSIONJS = {
	'devExtreme': '16.2.6',
	'jQuery': '3.1.0'
}
