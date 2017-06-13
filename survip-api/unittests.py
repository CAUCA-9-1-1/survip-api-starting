import unittest
from framework.tests.__main__ import get_test_framework
from opensource.tests.__main__ import get_test_opensource
from app.tests.__main__ import get_test_app


if __name__ == '__main__':
	suite = unittest.TestSuite()
	suite = get_test_framework(suite)
	suite = get_test_opensource(suite)
	suite = get_test_app(suite)

	runner = unittest.TextTestRunner()
	runner.run(suite)
