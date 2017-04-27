import logging
import cherrypy
from .. import config
from ..storage.ldap import LDAP
from .static import Static


class WithLDAP(Static):
	def logon(self, user, password):
		ldap = LDAP()

		if ldap.connect(user, password):
			if ldap.user_is_member_of_group():
				self.config_session(ldap.get_user_info())

				return True
			else:
				logging.info("The user doesn't have access the the filtered group")
		else:
			logging.info("The username and password doesn't match LDAP information")

		return False

	def config_session(self, user):
		cherrypy.session['user'] = user;
		cherrypy.session['userId'] = 'ldap:%s' % cherrypy.session['user']['username']

	def change_password(self, password):
		pass