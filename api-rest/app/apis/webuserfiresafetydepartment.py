import uuid
from causeweb.storage.db import DB
from causeweb.apis.base import Base


class WebuserFireSafetyDepartment(Base):
	table_name = 'tbl_webuser_fire_safety_department'
	mapping_method = {
		'GET': 'get',
		'PUT': 'create',
		'POST': 'modify',
		'DELETE': 'remove',
		'PATCH': '',
	}

	def get(self, id_webuser=None):
		""" Return all fire safety department of one user

		:param id_webuser: UUID
		"""
		if self.has_permission('RightAdmin') is False:
			return self.no_access()

		with DB() as db:
			if id_webuser is None:
				data = []
			else:
				data = db.get_all("""SELECT * FROM tbl_webuser_fire_safety_department
                	                WHERE id_webuser=%s;""", (id_webuser,))

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

		id_webuser_fire_safety_department = uuid.uuid4()

		with DB() as db:
			db.execute("""INSERT INTO tbl_webuser_fire_safety_department(
						id_webuser_fire_safety_department, id_webuser, id_fire_safety_department, is_active
					) VALUES (%s, %s, %s, %s);""", (
				id_webuser_fire_safety_department, args['id_webuser'], args['id_fire_safety_department'], args['is_active']
			))

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
		if 'id_webuser_fire_safety_department' not in args:
			raise Exception("You need to pass a id_webuser_fire_safety_department")

		if self.has_permission('RightAdmin') is False:
			return self.no_access()

		with DB() as db:
			db.execute("""UPDATE tbl_webuser_fire_safety_department SET
							id_webuser=%s, id_fire_safety_department=%s, is_active=%s
						  WHERE id_webuser_fire_safety_department=%s;""", (
				args['id_webuser'], args['id_fire_safety_department'], args['is_active'], args['id_webuser_fire_safety_department']
			))

		return {
			'message': 'webuser fire safety department successfully modify'
		}

	def remove(self, id_webuser_fire_safety_department):
		""" Remove a fire safety department of one user

		:param id_webuser_fire_safety_department: UUID
		"""
		if self.has_permission('RightAdmin') is False:
			return self.no_access()

		with DB() as db:
			db.execute("UPDATE tbl_webuser_fire_safety_department SET is_active=%s WHERE id_webuser_fire_safety_department=%s;", (
				False, id_webuser_fire_safety_department
			))

		return {
			'message': 'fire safety department user successfully removed'
		}