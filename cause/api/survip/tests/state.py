import unittest
from cause.api.management.core.manage.database import Database
from ..resturls.state import State


class TestState(unittest.TestCase):
	def setUp(self):
		self.id_state = None

	def test_01_insert(self):
		result = State().create({
			'name': 'state for unittest',
			'id_country': 'fd1c0f55-1dcc-4de5-99f0-c3e8421e65a3'
		})

		self.__class__.id_state = result['id_state']
		self.assertEqual(result['message'], "state successfully created")

	def test_02_get(self):
		result = State().get(self.__class__.id_state)
		self.assertEqual(result['data'].name['fr'], 'state for unittest')

	def test_03_modify(self):
		result = State().modify({
			'id_state': self.__class__.id_state,
			'name': 'state for unittest+modify'
		})

		self.assertEqual(result['message'], "state successfully modified")

	def test_04_get(self):
		result = State().get(self.__class__.id_state)
		self.assertEqual(result['data'].name['fr'], 'state for unittest+modify')

	def test_05_remove(self):
		result = State().remove(self.__class__.id_state)
		self.assertEqual(result['message'], "state successfully removed")

	def test_06_delete(self):
		with Database() as db:
			db.execute("DELETE FROM tbl_state WHERE id_state::UUID='%s';" % self.__class__.id_state)