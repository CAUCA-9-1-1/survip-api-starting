import json
import cherrypy
from .. import config
from ..html.request import Request
from .static import Static


class WithWebService(Static):
	def logon(self, username, password):
		try:
			version = 'DEV' if config.PACKAGE_VERSION == '__package_version__' else config.PACKAGE_VERSION
			query = Request("http://%s/auth/" % config.WEBSERVICE['host'])
			data = json.loads(query.send({
				'username': username,
				'password': password
			}, None, {
				'User-Agent': '%s/%s' % (config.PACKAGE_NAME, version),
				'Authorization': 'Key %s' % config.WEBSERVICE['key']
			}))

			if 'access_token' not in data:
				return False

			self.config_session(data)

			return True
		except:
			return False

	def config_session(self, data):
		cherrypy.session['access-token'] = data['access_token']
		cherrypy.session['refresh-token'] = data['refresh_token'] if 'refresh_token' in data else ''
		cherrypy.session['user'] = data['user'] if 'user' in data else {}
		cherrypy.session['userId'] = data['user_id'] if 'user_id' in data else ''

	def change_password(self, password):
		version = 'DEV' if config.PACKAGE_VERSION == '__package_version__' else config.PACKAGE_VERSION
		user = cherrypy.session['user']
		user.update({
			'id_webuser': cherrypy.session['userId'],
			'password': password,
			'is_active': True,
			'reset_password': '0'
		})

		if 'token' in config.WEBSERVICE:
			query = Request("http://%s/user/" % config.WEBSERVICE['host'])
			data = json.loads(query.send(user, None, {
				'User-Agent': '%s/%s' % (config.PACKAGE_NAME, version),
				'Authorization': 'Token %s' % config.WEBSERVICE['token']
			}))