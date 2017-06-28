import unittest

from api.management.core.database import Database
from ..resturls.firesafetydepartment import FireSafetyDepartment


class TestFireSafetyDepartment(unittest.TestCase):
	def setUp(self):
		self.id_fire_safety_department = None

	def test_01_insert(self):
		result = FireSafetyDepartment().create({
			'name': 'fire safety department for unittest',
			'language': 'fr'
		})

		self.__class__.id_fire_safety_department = result['id_fire_safety_department']
		self.assertEqual(result['message'], "fire safety department successfully created")

	def test_02_get(self):
		result = FireSafetyDepartment().get(self.__class__.id_fire_safety_department)
		self.assertEqual(result['data'].language, 'fr')

	def test_03_modify(self):
		result = FireSafetyDepartment().modify({
			'id_fire_safety_department': self.__class__.id_fire_safety_department,
			'language': 'en'
		})

		self.assertEqual(result['message'], "fire safety department successfully modified")

	def test_04_get(self):
		result = FireSafetyDepartment().get(self.__class__.id_fire_safety_department)
		self.assertEqual(result['data'].language, 'en')

	def test_05_remove(self):
		result = FireSafetyDepartment().remove(self.__class__.id_fire_safety_department)
		self.assertEqual(result['message'], "fire safety department successfully removed")

	def test_06_delete(self):
		with Database() as db:
			db.execute("DELETE FROM tbl_fire_safety_department WHERE id_fire_safety_department::UUID='%s';" % self.__class__.id_fire_safety_department)