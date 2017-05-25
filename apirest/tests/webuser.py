import unittest
from ..app.resturls.webuser import Webuser


class TestWebuser(unittest.TestCase):
	def test_get(self):
		result = Webuser().get()

		self.assertEqual(result, True)