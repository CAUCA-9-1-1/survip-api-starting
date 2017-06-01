import uuid
from ..auth.encryption import Encryption
from ..manage.database import Database
from ..models.webuser import Webuser as Table
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
		""" Return all webuser information

		:param id_webuser: UUID
		:param is_active: BOOLEAN
		"""
		with Database() as db:
			if id_webuser is None and is_active is None:
				data = db.query(Table).all()
			elif id_webuser is None:
				data = db.query(Table).filter(Table.is_active == is_active).all()
			else:
				data = db.query(Table).get(id_webuser)

		return {
			'data': data
		}

	def logon(self, username, password):
		with Database() as db:
			data = db.query(Table).filter(
				Table.username == username,
				Table.password == Encryption.password(password)
			).first()

		if data is not None:
			Base.logged_id_webuser = data.id_webuser
			return True

		return False

	def create(self, args):
		id_webuser = uuid.uuid4()

		with Database() as db:
			db.insert(Table(id_webuser, args['username'], args['password']))
			db.commit()

		return {
			'id_webuser': id_webuser,
			'message': 'webuser successfully created'
		}

	def modify(self, args):
		with Database() as db:
			data = db.query(Table).get(args['id_webuser'])

			if 'username' in args:
				data.username = args['username']
			if 'password' in args:
				data.password = Encryption.password(args['password'])

			db.commit()

		return {
			'message': 'webuser successfully modified'
		}

	def remove(self, id_webuser):
		with Database() as db:
			data = db.query(Table).get(id_webuser)
			data.is_active = False
			db.commit()

		return {
			'message': 'webuser successfully removed'
		}