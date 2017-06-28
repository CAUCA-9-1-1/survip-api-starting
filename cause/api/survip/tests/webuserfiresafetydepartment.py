import unittest
from cause.api.management.core.manage.database import Database
from cause.api.management.resturls.base import Base
from ..resturls.webuserfiresafetydepartment import WebuserFireSafetyDepartment


class TestWebuserFireSafetyDepartment(unittest.TestCase):
	def setUp(self):
		self.id_webuser_fire_safety_department = None

	def test_01_insert(self):
		result = WebuserFireSafetyDepartment().create({
			'id_webuser': Base.logged_id_webuser,
			'id_fire_safety_department': 'd25a7a30-22e0-4169-95b8-bd36368f12d5'
		})

		self.__class__.id_webuser_fire_safety_department = result['id_webuser_fire_safety_department']
		self.assertEqual(result['message'], "webuser fire safety department successfully created")

	def test_02_get(self):
		result = WebuserFireSafetyDepartment().get(Base.logged_id_webuser)
		last = result['data'][(len(result['data']) - 1)]
		self.assertEqual(str(last.id_fire_safety_department), 'd25a7a30-22e0-4169-95b8-bd36368f12d5')

	def test_03_modify(self):
		result = WebuserFireSafetyDepartment().modify({
			'id_webuser_fire_safety_department': self.__class__.id_webuser_fire_safety_department,
			'id_fire_safety_department': 'd25a7a30-22e0-4169-95b8-bd36368f12d4'
		})

		self.assertEqual(result['message'], "webuser fire safety department successfully modified")

	def test_04_get(self):
		result = WebuserFireSafetyDepartment().get(Base.logged_id_webuser)
		last = result['data'][(len(result['data']) - 1)]
		self.assertEqual(str(last.id_fire_safety_department), 'd25a7a30-22e0-4169-95b8-bd36368f12d4')

	def test_05_remove(self):
		result = WebuserFireSafetyDepartment().remove(self.__class__.id_webuser_fire_safety_department)
		self.assertEqual(result['message'], "webuser fire safety department successfully removed")

	def test_06_delete(self):
		with Database() as db:
			db.execute("DELETE FROM tbl_webuser_fire_safety_department WHERE id_webuser_fire_safety_department::UUID='%s';" % self.__class__.id_webuser_fire_safety_department)