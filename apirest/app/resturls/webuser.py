from causeweb.storage.db import DB
from causeweb.apis.webuser import Webuser as CausewebWebuser
from causeweb.apis.base import Base
from .building import Building


class Webuser(Base):
	mapping_method = {
		'GET': 'get',
		'PUT': 'modify',
		'POST': 'create',
		'DELETE': 'remove',
		'PATCH': '',
	}

	def get(self, id_webuser=None, id_city=None):
		""" Return all user information

		:param id_webuser: UUID
		"""
		if id_city is not None and id_city is not True:
			if self.has_permission('RightTPI') is False:
				return self.no_access()

			with DB() as db:
				data = db.get_all("""SELECT wu.id_webuser, attr1.attribute_value AS first_name, attr2.attribute_value AS last_name, wu.username, wu.is_active
							FROM tbl_webuser wu
							LEFT JOIN tbl_webuser_attributes attr1 ON attr1.id_webuser = wu.id_webuser AND attr1.attribute_name='first_name'
							LEFT JOIN tbl_webuser_attributes attr2 ON attr2.id_webuser = wu.id_webuser AND attr2.attribute_name='last_name'
							LEFT JOIN tbl_webuser_fire_safety_department ON tbl_webuser_fire_safety_department.id_webuser = wu.id_webuser
							LEFT JOIN tbl_fire_safety_department_city_serving ON tbl_fire_safety_department_city_serving.id_fire_safety_department = tbl_webuser_fire_safety_department.id_fire_safety_department
							WHERE tbl_fire_safety_department_city_serving.id_city = %s
							ORDER BY attr1.attribute_value, attr2.attribute_value;""", (id_city,))

			for key, user in enumerate(data):
				data[key].update(CausewebWebuser().get_webuser_attributes(user['id_webuser']))

			return {
				'data': data
			}
		else:
			return CausewebWebuser().get(id_webuser)

	def create(self, args):
		return CausewebWebuser().create(args)

	def modify(self, args):
		return CausewebWebuser().modify(args)

	def remove(self, args):
		return CausewebWebuser().remove(args)