import datetime
import hashlib
import random
import uuid
import cherrypy
from ..config import setup as config


class Token:
	def logon(self, args):
		"""if WithDB().logon(args['username'], args['password']):
			id_access_token = uuid.uuid4()
			access_token = self.generate_token()
			refresh_token = self.generate_token()

			with DB() as db:
				db.execute(""INSERT INTO tbl_access_token(id_access_token, id_webuser, access_token, refresh_token, created_on, expires_in)
							VALUES(%s, %s, %s, %s, NOW(), %s);"", (
					id_access_token, WithDB.get('userId'), access_token, refresh_token, (self.expires_in_minutes * 60)
				))

			return {
				'authorizationType': 'Token',
				'expiresIn': (self.expires_in_minutes * 60),
				'accessToken': access_token,
				'refreshToken': refresh_token,
				'userId': WithDB.get('userId'),
				'user': WithDB.get('user')
			}
		else:"""
		raise Exception("authentification failed")

	def generate_secretkey(self, name):
		randomkey = str(random.getrandbits(256))
		secretkey = "%s-%s" % (name, randomkey)

		return {
			'randomkey': randomkey,
			'secretkey': hashlib.sha224(secretkey.encode('utf-8')).hexdigest()
		}

	def generate_token(self):
		randomkey = str(random.getrandbits(256))
		secretkey = "%s-%s" % (config.PACKAGE_NAME, randomkey)

		return hashlib.sha224(secretkey.encode('utf-8')).hexdigest()

	def valid_access_from_header(self):
		authorization = cherrypy.request.headers.get('Authorization')
		authorization = authorization if authorization is not None else ''
		secretkey = authorization.replace('Key ', '') if 'Key' in authorization else None
		token = authorization.replace('Token ', '') if 'Token' in authorization else None

		if secretkey is not None:
			return self.valid_secretkey(secretkey)
		elif token is not None:
			return self.valid_token(token)

		#return False
		return True

	def valid_secretkey(self, key):
		"""with DB() as db:
			is_active = db.get("SELECT is_active FROM tbl_access_secretkey WHERE secretkey=%s", (key,))

		return True if is_active is True else False"""
		return True

	def valid_token(self, token):
		"""with DB() as db:
			row = db.get_row("SELECT created_on, expires_in FROM tbl_access_token WHERE access_token=%s", (token,))

		if row is None or 'created_on' not in row:
			return False

		expires = row['created_on'] + datetime.timedelta(0, row['expires_in'])

		if expires > datetime.datetime.now():
			self.active_session(token)

			return True

		return False"""
		return True

	def active_session(self, token):
		"""with DB() as db:
			user = db.get_row(""SELECT tbl_access_token.id_webuser, tbl_webuser.username
								FROM tbl_access_token
								LEFT JOIN tbl_webuser ON tbl_webuser.id_webuser = tbl_access_token.id_webuser
								WHERE tbl_access_token.access_token=%s"", (token,))

			WithDB().config_session(user['id_webuser'], user['username'])"""