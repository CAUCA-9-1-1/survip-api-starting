import unittest
from ..resturls.constructiontype import ConstructionType


class TestConstructionType(unittest.TestCase):
	def setUp(self):
		pass

	def test_01_get(self):
		result = ConstructionType().get()
		isList = isinstance(result['data'], list)

		self.assertEqual(isList, True)
