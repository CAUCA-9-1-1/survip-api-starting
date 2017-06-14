import uuid
from framework.manage.database import Database
from framework.resturls.base import Base
from ..models.webuser_fire_safety_department import WebuserFireSafetyDepartment as Table


class WebuserFireSafetyDepartment(Base):
	table_name = 'tbl_webuser_fire_safety_department'
	mapping_method = {
		'GET': 'get',
		'PUT': 'modify',
		'POST': 'create',
		'DELETE': 'remove',
		'PATCH': '',
	}

	def get(self, id_webuser=None):
		""" Return all fire safety department of one user

		:param id_webuser: UUID
		"""
		if self.has_permission('RightAdmin') is False:
			return self.no_access()

		with Database() as db:
			if id_webuser is None:
				data = []
			else:
				data = db.query(Table).filter(
					Table.id_webuser == id_webuser
				).all()

		return {
			'data': data
		}

	def create(self, args):
		""" Create a new fire safety department for one user

		:param args: {
			id_webuser: UUID,
			id_fire_safety_department: UUID,
			is_active: BOOLEAN
		}
		"""
		if self.has_permission('RightAdmin') is False:
			return self.no_access()
		if 'id_webuser' not in args or 'id_fire_safety_department' not in args:
			raise Exception("You need to pass a 'id_webuser' and 'id_fire_safety_department'")

		id_webuser_fire_safety_department = uuid.uuid4()

		with Database() as db:
			db.insert(Table(id_webuser_fire_safety_department, args['id_webuser'], args['id_fire_safety_department']))
			db.commit()

		return {
			'id_webuser_fire_safety_department': id_webuser_fire_safety_department,
			'message': 'webuser fire safety department successfully created'
		}

	def modify(self, args):
		""" Modify a fire safety department of user

		:param args: {
			id_webuser_fire_safety_department: UUID,
			id_webuser: UUID,
			id_fire_safety_department: UUID,
			is_active: BOOLEAN
		}
		"""
		if self.has_permission('RightAdmin') is False:
			return self.no_access()
		if 'id_webuser_fire_safety_department' not in args:
			raise Exception("You need to pass a 'id_webuser_fire_safety_department'")

		with Database() as db:
			data = db.query(Table).get(args['id_webuser_fire_safety_department'])

			if 'id_webuser' in args:
				data.id_webuser = args['id_webuser']
			if 'id_fire_safety_department' in args:
				data.id_fire_safety_department = args['id_fire_safety_department']
			if 'is_active' in args:
				data.is_active = args['is_active']

			db.commit()

		return {
			'message': 'webuser fire safety department successfully modified'
		}

	def remove(self, id_webuser_fire_safety_department):
		""" Remove a fire safety department of one user

		:param id_webuser_fire_safety_department: UUID
		"""
		if self.has_permission('RightAdmin') is False:
			return self.no_access()

		with Database() as db:
			data = db.query(Table).get(id_webuser_fire_safety_department)
			data.is_active = False
			db.commit()

		return {
			'message': 'webuser fire safety department successfully removed'
		}