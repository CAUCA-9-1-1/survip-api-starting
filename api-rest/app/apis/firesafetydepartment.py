import uuid
from causeweb.storage.db import DB
from causeweb.site.multilang import MultiLang
from causeweb.apis.base import Base


class FireSafetyDepartment(Base):
	table_name = 'tbl_fire_safety_department'
	mapping_method = {
		'GET': 'get',
		'PUT': 'create',
		'POST': 'modify',
		'DELETE': 'remove',
		'PATCH': '',
	}

	def get(self, id_fire_safety_department=None):
		""" Return all information for one fire safety department

		:param id_fire_safety_department: UUID
		"""
		with DB() as db:
			if id_fire_safety_department is None:
				data = db.get_all("SELECT * FROM tbl_fire_safety_department;")
			else:
				data = db.get_row("""SELECT * FROM tbl_fire_safety_department
                	                WHERE id_fire_safety_department=%s;""", (id_fire_safety_department,))

		for key, row in enumerate(data):
			data[key]['name'] = MultiLang.get(row['id_language_content_name'])

		return {
			'data': data
		} if id_fire_safety_department is None else data[0]

	def create(self, args):
		""" Create a new fire safety department

		:param args: {
			name: JSON,
			is_active: BOOLEAN
		}
		"""
		id_fire_safety_department = uuid.uuid4()
		id_language_content = MultiLang.set(args['name'], True)

		with DB() as db:
			db.execute("""INSERT INTO tbl_fire_safety_department(
							id_fire_safety_department, id_language_content_name, is_active
						  ) VALUES(%s, %s, %s);""", (
				id_fire_safety_department, id_language_content, args['is_active']
			))

		return {
			'id_fire_safety_department': id_fire_safety_department,
			'message': 'fire safety department successfully created'
		}

	def modify(self, args):
		""" Modify a fire safety department

		:param args: {
			id_fire_safety_department: UUID,
			name: JSON,
			is_active: BOOLEAN
		}
		"""
		if 'id_fire_safety_department' not in args:
			raise Exception("You need to pass a id_fire_safety_department")

		id_language_content = MultiLang.set(args['name'])

		with DB() as db:
			db.execute("""UPDATE tbl_fire_safety_department
							SET id_language_content_name=%s, is_active=%s
							WHERE id_fire_safety_department=%s;""", (
				id_language_content, args['is_active'], args['id_fire_safety_department']
			))

		return {
			'message': 'fire safety department successfully modify'
		}

	def remove(self, id_fire_safety_department):
		""" Remove a fire safety department

		:param id_fire_safety_department: UUID
		"""
		with DB() as db:
			db.execute("UPDATE tbl_fire_safety_department SET is_active=%s WHERE id_fire_safety_department=%s;", (
				False, id_fire_safety_department
			))

		return {
			'message': 'fire safety department successfully removed'
		}
