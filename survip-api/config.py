# Database
DATABASE = {
	'general': {
		'engine': 'postgresql',
		'host': 'localhost',
		'dbname': 'survi_prevention',
		'username': 'postgres',
		'password': 'postgres',
	}
}

PERMISSION = {
	'systemID': '2d9f85c6-c41b-4b53-b391-9caa31bb3494',
}

LOGS_NAME = 'survip-api'
FORCE_CAMELCASE = True
IS_DEV = True
IS_UWSGI = False
PACKAGE_NAME = "SURVI-Prevention-API"
PACKAGE_VERSION = "0.0.1"
SESSION_TIMEOUT = 5

WEBROOT = '/'
SEARCH_FOLDERS = ['app', 'cause.api.survip', 'cause.api.management']
