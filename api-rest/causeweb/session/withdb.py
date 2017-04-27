import json
import cherrypy
from .. import config
from ..apis.webuser import Webuser
from .static import Static


class WithDB(Static):
	def logon(self, username, password):
		if username == '' or password == '':
			return False

		user_id = Webuser().valid_password(username, password)

		if user_id is None or user_id == '':
			return False

		self.config_session(user_id, username)

		return True

	def config_session(self, user_id, username):
		user = Webuser().get_webuser_attributes(user_id)
		user.update({
			'username': username
		})

		cherrypy.session['user'] = user
		cherrypy.session['userID'] = user_id

	def change_password(self, password):
		if 'general' in config.DATABASE:
			Webuser().change_password({
				'id_webuser': Static.get('userID'),
				'password': password,
			})