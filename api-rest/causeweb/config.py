import os
import cherrypy

# Database config
DATABASE = None
"""
DATABASE = {
	'general': {
		'type': 'mysql',
		'host': 'bd-dev-maitre',
		'dbname': 'geobase',
		'username': 'usrFireQPhp',
		'password': 'feuQ!123',
	},
	'mysql_winc': {
		'type': 'mysql',
		'host': 'casrvwincdev',
		'dbname': 'geobase',
		'username': 'admin2',
		'password': 'a9d8m7i6n5qwe',
	}
}
"""

# Logs
LOGS_NAME = 'causeweb'
LOGS = {
	'level': 'info',
	'format': '%(asctime)s:%(name)s/%(funcName)s()@%(lineno)d:%(levelname)s:%(message)s',
}

# LDAP config
LDAP = None
"""
LDAP = {
	'server': 'cadevldap3.ad.cauca.ca',
	'baseDN': 'dc=ad,dc=cauca,dc=ca',
    'baseCN': 'Web-Incendie-ACL',
    'bindUser': 'uid=lookup,ou=people',
    'bindPassword': 'eePh5quo'
}
"""

# Rabbit MQ config
RABBIT_MQ = None

# Permission in tbl_permission on DB "general"
PERMISSION = None
"""
PERMISSION = {
	'systemID': ''
}
"""

# Host for development
IS_DEV = False
USE_UWSGI = True
DEV_HOST = []
SESSION_TIMEOUT = 30

# Folder
ROOT = os.path.abspath(os.getcwd())
WEBROOT = '/'

# Web
PACKAGE_NAME = "causeweb"
PACKAGE_VERSION = "__package_version__"
WEBSERVICE = None
"""
WEBSERVICE = {
	'host': '',
	'key': ''
}
"""
WINC_GROUP = "" # IS DECRECIATED
WINC_ACCESS = "" # IS DECRECIATED
IS_SSL = False
MINIMIZE_JS = True
RECAPTCHA_SECRET_KEY = None
CONTENT_SECURITY_POLICY_CONNECT = None
CAUSEJS = "st.cauca.ca"
VERSIONJS = {
	'devExtreme': '16.2.5',
	'jQuery': '3.1.0'
}

""" Override all default config with the user config
"""
if os.path.isfile("config.py"):
	with open("config.py") as file:
		exec(file.read())

if cherrypy.request.base in DEV_HOST:
	IS_DEV = True