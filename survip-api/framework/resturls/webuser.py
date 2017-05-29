import uuid
from ..auth.encryption import Encryption
from ..manage.database import Database
from ..models.webuser import Webuser as Table
from ..models.webuser_attributes import WebuserAttributes
from .base import Base


class Webuser(Base):
	id_webuser = None
	mapping_method = {
		'GET': 'get',
		'PUT': 'modify',
		'POST': 'create',
		'DELETE': 'remove',
		'PATCH': '',
	}

	def get(self, id_webuser=None, id_city=None):
		""" Return all webuser information

		:param id_webuser: UUID
		"""
		if id_city is not None and id_city is not True:
			if self.has_permission('RightTPI') is False:
				return self.no_access()

			with Database() as db:
				data = db.query(Table).join(
					WebuserAttributes.id_webuser == Table.id_webuser,
					WebuserAttributes.attribute_name == 'first_name'
				).join(
					WebuserAttributes.id_webuser == Table.id_webuser,
					WebuserAttributes.attribute_name == 'last_name'
				).join(
					WebuserAttributes.id_webuser == Table.id_webuser,
					WebuserAttributes.attribute_name == 'last_name'
				).filter().all()

				#LEFT JOIN tbl_webuser_fire_safety_department ON tbl_webuser_fire_safety_department.id_webuser = wu.id_webuser
				#LEFT JOIN tbl_fire_safety_department_city_serving ON tbl_fire_safety_department_city_serving.id_fire_safety_department = tbl_webuser_fire_safety_department.id_fire_safety_department
				#WHERE tbl_fire_safety_department_city_serving.id_city = %s
				#ORDER BY attr1.attribute_value, attr2.attribute_value;""", (id_city,))
		elif id_webuser is None:
			with Database() as db:
				data = db.query(Table).join(
					WebuserAttributes.id_webuser == Table.id_webuser,
					WebuserAttributes.attribute_name == 'first_name'
				).join(
					WebuserAttributes.id_webuser == Table.id_webuser,
					WebuserAttributes.attribute_name == 'last_name'
				).filter().all()
		else:
			with Database() as db:
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
			Webuser.id = data.id_webuser
			return True

		return False

	def create(self, args):
		id_webuser = uuid.uuid4()

		with Database() as db:
			data = db.insert(Table(id_webuser, args['username'], args['password']))
			db.commit()

		return {
			'id_webuser': id_webuser,
			'message': 'webuser successfully created'
		}

	def modify(self, args):
		with Database() as db:
			data = db.query(Table).filter(Table.id_webuser == args['id_webuser']).first()

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
			data = db.query(Table).filter(Table.id_webuser == id_webuser).first()
			data.is_active = False
			db.commit()

		return {
			'message': 'webuser successfully removed'
		}