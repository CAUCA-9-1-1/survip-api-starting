import uuid
from causeweb.storage.db import DB
from causeweb.apis.base import Base


class FireSafetyDepartmentCityServing(Base):
	table_name = 'tbl_fire_safety_department_city_serving'
	mapping_method = {
		'GET': 'get',
		'PUT': 'modify',
		'POST': 'create',
		'DELETE': 'remove',
		'PATCH': '',
	}

	def get(self, id_fire_safety_department=None):
		""" Return all information for one fire safety department of city serving

		:param id_fire_safety_department: UUID
		"""
		with DB() as db:
			if id_fire_safety_department is None:
				data = []
			else:
				data = db.get_all("""SELECT * FROM tbl_fire_safety_department_city_serving
                	                WHERE id_fire_safety_department=%s;""", (id_fire_safety_department,))

		return {
			'data': data
		}

	def create(self, args):
		""" Create a new fire safety department if of city serving

		:param args: {
			id_fire_safety_department: UUID,
			id_city: UUID,
			is_active: BOOLEAN
		}
		"""
		id_fire_safety_department_city_serving = uuid.uuid4()

		with DB() as db:
			db.execute("""INSERT INTO tbl_fire_safety_department_city_serving(
						id_fire_safety_department_city_serving, id_fire_safety_department, id_city, is_active
					) VALUES (%s, %s, %s, %s);""", (
				id_fire_safety_department_city_serving, args['id_fire_safety_department'], args['id_city'], args['is_active']
			))

		return {
			'id_fire_safety_department_city_serving': id_fire_safety_department_city_serving,
			'message': 'fire safety department city serving successfully created'
		}

	def modify(self, args):
		""" Modify a fire safety department of city serving

		:param args: {
			id_fire_safety_department_city_serving: UUID,
			id_fire_safety_department: UUID,
			id_city: UUID,
			is_active: BOOLEAN
		}
		"""
		if 'id_fire_safety_department_city' not in args:
			raise Exception("You need to pass a id_fire_safety_department_city")

		with DB() as db:
			db.execute("""UPDATE tbl_fire_safety_department_city_serving SET
							id_fire_safety_department=%s, id_city=%s, is_active=%s
						  WHERE id_fire_safety_department_city_serving=%s;""", (
				args['id_fire_safety_department'], args['id_city'], args['is_active'], args['id_fire_safety_department_city_serving']
			))

		return {
			'message': 'fire safety department city serving successfully modify'
		}

	def remove(self, id_fire_safety_department_city):
		""" Remove a fire safety department of city serving

		:param id_fire_safety_department_city_serving: UUID
		"""
		with DB() as db:
			db.execute("UPDATE tbl_fire_safety_department_city_serving SET is_active=%s WHERE id_fire_safety_department_city_serving=%s;", (
				False, id_fire_safety_department_city
			))

		return {
			'message': 'fire safety department city serving successfully removed'
		}