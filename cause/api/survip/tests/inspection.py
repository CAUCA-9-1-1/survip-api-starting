import unittest
from cause.api.management.core.manage.database import Database
from ..resturls.inspection import Inspection


class TestInspection(unittest.TestCase):
	def setUp(self):
		self.id_inspection = None

	def test_01_insert(self):
		result = Inspection().create({
			'id_building': '6fceb420-b76b-492f-b5f7-8d51aaad925f',
			'id_webuser': 'f14549be-296d-4a82-b593-30e08dc14fec',
			'id_survey': 'dc2aebde-82f9-40ac-b389-6c6116acc7c5'
		})

		self.__class__.id_inspection = result['id_inspection']
		self.assertEqual(result['message'], "inspection successfully created")

	def test_02_get(self):
		result = Inspection().get(self.__class__.id_inspection)
		self.assertEqual(result['data'].address, '13150, 118E RUE')

	def test_03_modify(self):
		result = Inspection().modify({
			'id_inspection': self.__class__.id_inspection,
			'is_completed': True
		})

		self.assertEqual(result['message'], "inspection successfully modified")

	def test_04_get(self):
		result = Inspection().get(self.__class__.id_inspection)
		self.assertEqual(result['data'].is_completed, True)

	def test_05_remove(self):
		result = Inspection().remove(self.__class__.id_inspection)
		self.assertEqual(result['message'], "inspection successfully removed")

	def test_06_delete(self):
		with Database() as db:
			db.execute("DELETE FROM tbl_inspection WHERE id_inspection::UUID='%s';" % self.__class__.id_inspection)