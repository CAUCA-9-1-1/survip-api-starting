import uuid
import hmac
import hashlib
from causeweb import config
from causeweb.session.static import Static as Session
from causeweb.storage.db import DB
from causeweb.utilities import Utilities
from .base import Base


class Webuser(Base):
	table_name = 'tbl_webuser'
	mapping_method = {
		'GET': 'get',
		'PUT': 'modify',
		'POST': 'create',
		'DELETE': 'remove',
		'PATCH': '',
	}

	def get(self, id_webuser=None, is_active=None):
		""" Return all user information

		:param id_webuser: UUID
		"""
		with DB() as db:
			if id_webuser is None and is_active is None:
				data = db.get_all("""SELECT wu.id_webuser, attr1.attribute_value AS first_name, attr2.attribute_value AS last_name, wu.username, wu.is_active
							FROM tbl_webuser wu
							LEFT JOIN tbl_webuser_attributes attr1 ON attr1.id_webuser = wu.id_webuser AND attr1.attribute_name='first_name'
							LEFT JOIN tbl_webuser_attributes attr2 ON attr2.id_webuser = wu.id_webuser AND attr2.attribute_name='last_name'
							ORDER BY attr1.attribute_value, attr2.attribute_value;""")
			elif id_webuser is None:
				data = db.get_all("""SELECT wu.id_webuser, attr1.attribute_value AS first_name, attr2.attribute_value AS last_name, wu.username, wu.is_active
							FROM tbl_webuser wu
							LEFT JOIN tbl_webuser_attributes attr1 ON attr1.id_webuser = wu.id_webuser AND attr1.attribute_name='first_name'
							LEFT JOIN tbl_webuser_attributes attr2 ON attr2.id_webuser = wu.id_webuser AND attr2.attribute_name='last_name'
							WHERE wu.is_active=%s
							ORDER BY attr1.attribute_value, attr2.attribute_value;""", (is_active,))
			else:
				data = db.get_all("SELECT * FROM tbl_webuser WHERE id_webuser=%s;", (id_webuser,))

		for key, row in enumerate(data):
			data[key].update(self.get_webuser_attributes(row['id_webuser']))

		return {
			'data': data
		} if id_webuser is None else data[0]

	def get_webuser_attributes(self, id_webuser):
		with DB() as db:
			attributes = Utilities.list_to_dict(db.get_all(
				"SELECT attribute_name, attribute_value FROM tbl_webuser_attributes WHERE id_webuser=%s;",
				(id_webuser,)
			), 'attribute_name', 'attribute_value')

			return attributes

		return ()

	def valid_password(self, username, password):
		with DB() as db:
			return db.get("SELECT id_webuser FROM tbl_webuser WHERE username=%s AND password=%s AND is_active=%s;", (
				username, self.encrypt_password(password), True
			))

		return ''

	def change_password(self, args):
		with DB() as db:
			db.execute("UPDATE tbl_webuser SET password=%s WHERE id_webuser=%s;", (self.encrypt_password(args['password']), args['id_webuser']))
			db.execute(
			    "UPDATE tbl_webuser_attributes SET attribute_value=%s WHERE id_webuser=%s and attribute_name=%s;",
			    ('0', Session.get('userId'), 'reset_password')
			)

	def create(self, args):
		""" Create a new webuser

		:param args: {
			username: String,
			password: String,
			attribute_name: attribute_value
		}
		"""
		if self.has_permission('RightAdmin') is False:
			return self.no_access()

		id_webuser = uuid.uuid4()
		attribute_to_skip = ['username', 'password', 'confirmPassword', 'is_active']

		with DB() as db:
			db.execute("INSERT INTO tbl_webuser(id_webuser, username, password, is_active) VALUES(%s, %s, %s, True);", (
				id_webuser, args['username'], self.encrypt_password(args['password'])
			))

			for attribute_name, attribute_value in args.items():
				if attribute_name not in attribute_to_skip:
					db.execute("INSERT INTO tbl_webuser_attributes (id_webuser, attribute_name, attribute_value) VALUES (%s, %s, %s);", (
						id_webuser, attribute_name, attribute_value
					))

		return {
			'message': 'webuser successfully created'
		}

	def modify(self, args):
		if self.has_permission('RightAdmin') is False:
			return self.no_access()

		with DB() as db:
			if 'password' in args and args['password']:
				db.execute(
					"""UPDATE tbl_webuser
						SET username=%s, password=%s, is_active=%s
						WHERE id_webuser=%s;""",
					(args['username'], self.encrypt_password(args['password']), args['is_active'], args['id_webuser'])
				)
			else:
				db.execute(
					"""UPDATE tbl_webuser
						SET username=%s, is_active=%s
						WHERE id_webuser=%s;""",
					(args['username'], args['is_active'], args['id_webuser'])
				)

			for attribute, value in args.items():
				if attribute not in ['username', 'password', 'confirmPassword', 'is_active', 'id_webuser']:
					if db.get_first("SELECT attribute_value FROM tbl_webuser_attributes WHERE id_webuser=%s AND attribute_name=%s", (args['id_webuser'], attribute)):
						db.execute(
							"UPDATE tbl_webuser_attributes SET attribute_value=%s WHERE id_webuser=%s AND attribute_name=%s;",
							(value, args['id_webuser'], attribute)
						)
					else:
						db.execute(
							"INSERT INTO tbl_webuser_attributes(id_webuser, attribute_name, attribute_value) VALUES(%s, %s, %s);",
							(args['id_webuser'], attribute, value)
						)

		return {
			'message': 'webuser successfully modify'
		}

	def remove(self, args):
		if self.has_permission('RightAdmin') is False:
			return self.no_access()

		with DB() as db:
			db.execute("UPDATE tbl_webuser SET is_active=False WHERE id_webuser=%s;", (args['id_webuser'],))

	def encrypt_password(self, password):
		secretkey = bytes(config.PACKAGE_NAME, encoding='utf-8')
		hash = hmac.new(secretkey, password.encode('UTF-8'), hashlib.sha256)

		return hash.hexdigest()