from ..auth.encryption import Encryption
from ..manage.database import Database
from ..models.webuser import Webuser as Table
from ..models.webuserattributes import WebuserAttributes
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

			return {
				'data': data
			}
		else:
			return CausewebWebuser().get(id_webuser)

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
		return CausewebWebuser().create(args)

	def modify(self, args):
		return CausewebWebuser().modify(args)

	def remove(self, args):
		return CausewebWebuser().remove(args)