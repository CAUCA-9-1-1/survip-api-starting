import unittest
from apirest.tests.building import TestBuilding


if __name__ == '__main__':
	suite = unittest.TestSuite()
	suite.addTest(unittest.makeSuite(TestBuilding))
	runner = unittest.TextTestRunner()

	print(runner.run(suite))
