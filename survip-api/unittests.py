import unittest

from app.tests.__main__ import get_test_app
from cause.api.management.tests.__main__ import get_test_api_management
from cause.api.survip.tests.__main__ import get_test_api_survip

if __name__ == '__main__':
	suite = unittest.TestSuite()
	suite = get_test_api_management(suite)
	suite = get_test_api_survip(suite)
	suite = get_test_app(suite)

	runner = unittest.TextTestRunner()
	runner.run(suite)
