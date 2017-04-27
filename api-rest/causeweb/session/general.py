import logging
import os
import json
import cherrypy
from datetime import datetime
from .. import config
from .static import Static
from .withdb import WithDB
from .withldap import WithLDAP
from .withwebservice import WithWebService

if config.DATABASE is not None:
	from ..storage.db import DB


class Session(Static):
	nb_try_by_ip = {}

	def __init__(self):
		if not os.path.exists("%s/data/" % config.ROOT):
			os.makedirs("%s/data/" % config.ROOT)
		if not os.path.exists("%s/data/sessions/" % config.ROOT):
			os.makedirs("%s/data/sessions/" % config.ROOT)

	def change_password(self, password):
		if config.WEBSERVICE is not None:
			WithWebService().change_password(password)
		elif config.LDAP is not None:
			WithLDAP().change_password(password)
		elif config.DATABASE is not None:
			WithDB().change_password(password)

		if 'user' in cherrypy.session:
			if 'reset_password' in cherrypy.session['user']:
				cherrypy.session['user']['reset_password'] = '0'

	def logout(self):
		cherrypy.session['user'] = None
		cherrypy.session['userID'] = None
		cherrypy.session['userIP'] = None
		cherrypy.session['ldap-user'] = None
		cherrypy.session['ldap-password'] = None
		cherrypy.session['access-token'] = None
		cherrypy.session['refresh-token'] = None

		Session.log('causeweb.session.general', 'logout', {
			'application': config.PACKAGE_NAME,
			'sessionID': cherrypy.session.id,
			'userIP': cherrypy.session['userIP'] if 'userIP' in cherrypy.session else '',
		})

	def logon(self, user, password=''):
		""" Generate a session on server

		:param user: Username of user to open the session
		:param password: Password of user to open the session
		:return: True if the session is valid
		"""
		self.logout()

		cherrypy.session['userIP'] = cherrypy.request.headers["Remote-Addr"]
		arguments = {
			'application': config.PACKAGE_NAME,
			'platform': cherrypy.request.headers.get('User-Agent', 'Unknown'),
			'sessionID': cherrypy.session.id,
			'userIP': cherrypy.session['userIP'],
		}

		if config.WEBSERVICE is not None:
			self.log('causeweb.session.withwebservice', 'logon', arguments)

			return WithWebService().logon(user, password)
		elif 'mysql_winc' in config.DATABASE:
			from ..cauca.geobase_sessionusers import GeobaseSessionUsers

			return GeobaseSessionUsers().logon(user, password)
		elif config.LDAP is not None:
			self.log('causeweb.session.withldap', 'logon', arguments)

			return WithLDAP().logon(user, password)
		elif config.DATABASE is not None:
			self.log('causeweb.session.withdb', 'logon', arguments)

			return WithDB().logon(user, password)

		return False

	def is_logged(self, post=None):
		if self.get('user') is not None:
			return True

		""" Check if the parameter 'phone' is passed and valid. This is use when page is call by SURVI-Mobile."""
		if post is not None and config.DATABASE is not None:
			if 'general' in config.DATABASE and 'phone' in post:
				with DB() as db:
					ssi = db.get("SELECT gf.IDSSI FROM vwFireQ_GetFireFighter gf WHERE Cellulaire=%s;", (post['phone'],))

				if ssi == '':
					logging.exception("We can't find the SSI for this number : %s" % post['phone'])
					return False
				else:
					cherrypy.session['user'] = 'codePHP'
					cherrypy.session['fire_safety_department'] = [ssi]

					return True

		return False

	def is_limited(self, maximum_try=5, every="hour", unique_id=None):
		if every == "minute":
			period = datetime.now().strftime("%Y-%m-%d:%H:%M")
		else:
			period = datetime.now().strftime("%Y-%m-%d:%H")

		if unique_id is None:
			idtime = "%s-%s" % (period, cherrypy.request.headers["Remote-Addr"])
		else:
			idtime = "%s-%s" % (period, unique_id)

		if idtime in self.nb_try_by_ip:
			self.nb_try_by_ip[idtime] += 1
		else:
			self.nb_try_by_ip[idtime] = 1

		if self.nb_try_by_ip[idtime] >= maximum_try:
			return True

		return False

	def reset_limited(self, every="hour", unique_id=None):
		if every == "minute":
			period = datetime.now().strftime("%Y-%m-%d:%H:%M")
		else:
			period = datetime.now().strftime("%Y-%m-%d:%H")

		if unique_id is None:
			idtime = "%s-%s" % (period, cherrypy.request.headers["Remote-Addr"])
		else:
			idtime = "%s-%s" % (period, unique_id)

		if idtime in self.nb_try_by_ip:
			self.nb_try_by_ip[idtime] = 0