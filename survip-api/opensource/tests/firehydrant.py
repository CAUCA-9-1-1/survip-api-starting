import unittest
from ..resturls.firehydrant import FireHydrant


class TestFireHydrant(unittest.TestCase):
	def setUp(self):
		pass

	def test_01_get(self):
		result = FireHydrant().get()
		isList = isinstance(result['data'], list)

		self.assertEqual(isList, True)
