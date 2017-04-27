import cherrypy
import logging
from .. import config

try:
	import ldap3
except Exception as e:
	logging.exception("We need to install the pyldap library")


class LDAP:
	server = None
	link = None

	def __init__(self, server=None):
		try:
			if server is None:
				uri = 'ldap://%s:389' % config.LDAP['server']

			user = config.LDAP['bindUser']
			password = config.LDAP['bindPassword']

			if 'ldap-user' in cherrypy.session and cherrypy.session['ldap-user']:
				user = cherrypy.session['ldap-user']
				password = cherrypy.session['ldap-password']

			self.server = ldap3.Server(uri, use_ssl=True)
			self.link = ldap3.Connection(
		        self.server,
		        user='%s,%s' % (user, config.LDAP['baseDN']),
		        password=password)
		except Exception as e:
			logging.exception("Error when using pyldap library")

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		if self.link is not None:
			self.link.unbind()

	def is_connect(self):
		return True if self.link.bind() else False

	def connect(self, username, password):
		dn_user = self.get_user_dn(username)

		if self.link:
			self.link = ldap3.Connection(
				self.server,
				user=dn_user,
				password=password
			)

			if self.link.bind():
				cherrypy.session['ldap-username'] = username

				if 'adminCN' in config.LDAP:
					cherrypy.session['ldap-user'] = 'uid=%s,cn=%s' % (username, config.LDAP['adminCN'])
					cherrypy.session['ldap-password'] = password

				return True

		return False

	def get_user_dn(self, user):
		entry = self.get_user_entry(user)

		return entry['dn'] if entry else ''

	def get_user_entry(self, user):
		if self.link.bind() is False:
			return ''

		self.link.search(config.LDAP['baseDN'], '(uid=%s)' % user, ldap3.SUBTREE)

		for entry in self.link.response:
			return entry

		return None

	def user_is_member_of_group(self, filters=None):
		if self.link.bind() is False:
			return False

		if filters is None:
			filters = [config.LDAP['baseCN']]

			if 'adminCN' in config.LDAP:
				filters.append(config.LDAP['adminCN'])
		elif isinstance(filters, str):
			filters = [filters]

		for filter in filters:
			dn_user = self.get_user_dn(cherrypy.session['ldap-username'])
			self.link.search(config.LDAP['baseDN'], '(cn=%s)' % filter, ldap3.SUBTREE, attributes=['*'])

			for entry in self.link.response:
				if 'attributes' in entry and 'member' in entry['attributes']:
					for user in entry['attributes']['member']:
						if user == dn_user:
							return True

		return False

	def get_user_info(self):
		self.link.search(config.LDAP['baseDN'], '(uid=%s)' % cherrypy.session['ldap-username'], ldap3.SUBTREE, attributes=['*'])

		for entry in self.link.response:
			return {
				'username': entry['attributes']['uid'][0],
				'first_name': entry['attributes']['givenName'][0],
				'last_name': entry['attributes']['sn'][0],
				'full_name': entry['attributes']['cn'][0],
				'language': entry['attributes']['preferredLanguage'][0][0:2],
				'department_number': entry['attributes']['departmentNumber'][0] if 'departmentNumber' in entry['attributes'] else '',
			}

		return None
